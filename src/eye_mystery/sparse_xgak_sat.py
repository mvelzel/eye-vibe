"""Sparse known-plaintext recovery for arbitrary-permutation XGAK.

For plaintext symbol ``s`` the forward convention is::

    new_deck[i] = old_deck[operation_s[i]]
    output = new_deck[output_position_s]

The output position is fixed per plaintext symbol.  As in the sparse ordinary
GAK encoding, the solver tracks only positions of cards that are observed.
With unknown output positions, an arbitrary common reset deck is position-
conjugate to the identity deck, so the identity reset used here loses no
generality.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from eye_mystery.sparse_gak_sat import (
    _constrain_partial_permutation_step,
    _validate,
)
from eye_mystery.xgak_identifiability import run_xgak


@dataclass(frozen=True)
class XGAKWitness:
    """One exact identity-reset XGAK key."""

    operations: tuple[tuple[int, ...], ...]
    output_positions: tuple[int, ...]


@dataclass(frozen=True)
class XGAKSpecificAlternative:
    """Feasibility of an actual and one preselected alternative next card."""

    actual_card: int
    actual_status: str
    alternative_card: int
    alternative_status: str
    actual_witness: XGAKWitness | None
    alternative_witness: XGAKWitness | None

    @property
    def non_forcing(self) -> bool:
        return self.actual_status == self.alternative_status == "sat"


@dataclass
class _SparseXGAKProblem:
    z3: Any
    solver: Any
    transitions: list[list[tuple[Any, Any]]]
    output_positions: list[Any]
    width: int


def encrypt_xgak_messages(
    plaintexts: Sequence[Sequence[int]],
    witness: XGAKWitness,
) -> tuple[tuple[int, ...], ...]:
    """Replay reset messages under one XGAK witness."""

    return tuple(
        run_xgak(
            plaintext,
            witness.operations,
            witness.output_positions,
        ).ciphertext
        for plaintext in plaintexts
    )


def _build_problem(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    tracked_cards: Sequence[int],
    distinct_output_positions: bool,
    timeout_ms: int,
) -> _SparseXGAKProblem:
    try:
        import z3  # type: ignore[import-not-found]
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("sparse XGAK recovery requires z3-solver") from error

    plains, ciphers = _validate(
        plaintexts,
        ciphertexts,
        deck_size=deck_size,
        plaintext_alphabet_size=plaintext_alphabet_size,
    )
    cards = tuple(sorted(set(tracked_cards)))
    if any(not 0 <= card < deck_size for card in cards):
        raise ValueError("tracked card is outside the deck")
    if distinct_output_positions and plaintext_alphabet_size > deck_size:
        raise ValueError("distinct output positions exceed the deck size")

    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    width = max(1, deck_size.bit_length())
    output_positions = [
        z3.BitVec(f"xgak_output_{symbol}", width)
        for symbol in range(plaintext_alphabet_size)
    ]
    solver.add(
        *(
            z3.ULT(position, z3.BitVecVal(deck_size, width))
            for position in output_positions
        )
    )
    if distinct_output_positions:
        solver.add(z3.Distinct(output_positions))

    transitions: list[list[tuple[Any, Any]]] = [
        [] for _ in range(plaintext_alphabet_size)
    ]
    for message_index, (plaintext, ciphertext) in enumerate(
        zip(plains, ciphers, strict=True)
    ):
        last_needed = {
            card: max(
                offset
                for offset, emitted in enumerate(ciphertext)
                if emitted == card
            )
            for card in cards
            if card in ciphertext
        }
        previous = {
            card: z3.BitVecVal(card, width)
            for card in last_needed
        }
        for offset, (symbol, emitted) in enumerate(
            zip(plaintext, ciphertext, strict=True)
        ):
            current: dict[int, Any] = {}
            for card, last_offset in last_needed.items():
                if last_offset < offset:
                    continue
                position = z3.BitVec(
                    f"xgak_pos_{message_index}_{offset}_{card}",
                    width,
                )
                _constrain_partial_permutation_step(
                    z3,
                    solver,
                    transitions[symbol],
                    previous[card],
                    position,
                    deck_size=deck_size,
                    width=width,
                )
                current[card] = position
            if emitted not in current:
                raise ValueError("every observed ciphertext card must be tracked")
            solver.add(current[emitted] == output_positions[symbol])
            previous = current

    return _SparseXGAKProblem(
        z3=z3,
        solver=solver,
        transitions=transitions,
        output_positions=output_positions,
        width=width,
    )


def _extract_witness(
    problem: _SparseXGAKProblem,
    *,
    deck_size: int,
) -> XGAKWitness:
    model = problem.solver.model()
    forward_operations: list[tuple[int, ...]] = []
    for transitions in problem.transitions:
        partial: dict[int, int] = {}
        used_outputs: set[int] = set()
        for old_expression, new_expression in transitions:
            old_position = model.eval(
                old_expression,
                model_completion=True,
            ).as_long()
            new_position = model.eval(
                new_expression,
                model_completion=True,
            ).as_long()
            if old_position in partial and partial[old_position] != new_position:
                raise AssertionError("model violates operation functionality")
            if (
                new_position in used_outputs
                and partial.get(old_position) != new_position
            ):
                raise AssertionError("model violates operation injectivity")
            partial[old_position] = new_position
            used_outputs.add(new_position)

        missing_inputs = [
            position for position in range(deck_size) if position not in partial
        ]
        missing_outputs = [
            position for position in range(deck_size) if position not in used_outputs
        ]
        inverse_values = [0] * deck_size
        for old_position, new_position in partial.items():
            inverse_values[old_position] = new_position
        for old_position, new_position in zip(
            missing_inputs,
            missing_outputs,
            strict=True,
        ):
            inverse_values[old_position] = new_position
        forward = [0] * deck_size
        for old_position, new_position in enumerate(inverse_values):
            forward[new_position] = old_position
        forward_operations.append(tuple(forward))

    return XGAKWitness(
        operations=tuple(forward_operations),
        output_positions=tuple(
            model.eval(position, model_completion=True).as_long()
            for position in problem.output_positions
        ),
    )


def recover_sparse_xgak_witness(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    distinct_output_positions: bool = False,
    timeout_ms: int = 30_000,
) -> tuple[str, XGAKWitness | None]:
    """Recover one exact arbitrary-operation XGAK witness, if decidable."""

    tracked_cards = sorted(
        {card for ciphertext in ciphertexts for card in ciphertext}
    )
    problem = _build_problem(
        plaintexts,
        ciphertexts,
        deck_size=deck_size,
        plaintext_alphabet_size=plaintext_alphabet_size,
        tracked_cards=tracked_cards,
        distinct_output_positions=distinct_output_positions,
        timeout_ms=timeout_ms,
    )
    result = problem.solver.check()
    if result == problem.z3.unsat:
        return "unsat", None
    if result != problem.z3.sat:
        return "unknown", None

    witness = _extract_witness(problem, deck_size=deck_size)
    expected = tuple(tuple(message) for message in ciphertexts)
    if encrypt_xgak_messages(plaintexts, witness) != expected:
        raise AssertionError("sparse XGAK witness failed exact forward replay")
    return "sat", witness


def check_specific_xgak_next_card(
    plaintext_prefix: Sequence[int],
    ciphertext_prefix: Sequence[int],
    next_symbol: int,
    actual_next_card: int,
    alternative_next_card: int,
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    distinct_output_positions: bool = False,
    timeout_ms: int = 30_000,
) -> XGAKSpecificAlternative:
    """Test one frozen alternative completion of a known-plaintext prefix."""

    if len(plaintext_prefix) != len(ciphertext_prefix):
        raise ValueError("plaintext and ciphertext prefix lengths differ")
    if actual_next_card == alternative_next_card:
        raise ValueError("actual and alternative next cards must differ")
    if not 0 <= next_symbol < plaintext_alphabet_size:
        raise ValueError("next plaintext symbol is outside the operation alphabet")
    if any(
        not 0 <= card < deck_size
        for card in (actual_next_card, alternative_next_card)
    ):
        raise ValueError("next card is outside the deck")

    plaintext = (tuple(plaintext_prefix) + (next_symbol,),)

    def solve(next_card: int) -> tuple[str, XGAKWitness | None]:
        return recover_sparse_xgak_witness(
            plaintext,
            (tuple(ciphertext_prefix) + (next_card,),),
            deck_size=deck_size,
            plaintext_alphabet_size=plaintext_alphabet_size,
            distinct_output_positions=distinct_output_positions,
            timeout_ms=timeout_ms,
        )

    actual_status, actual_witness = solve(actual_next_card)
    alternative_status, alternative_witness = solve(alternative_next_card)
    return XGAKSpecificAlternative(
        actual_card=actual_next_card,
        actual_status=actual_status,
        alternative_card=alternative_next_card,
        alternative_status=alternative_status,
        actual_witness=actual_witness,
        alternative_witness=alternative_witness,
    )
