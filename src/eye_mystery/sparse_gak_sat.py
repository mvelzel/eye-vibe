"""Sparse inverse-position SMT encoding for arbitrary-permutation GAK.

The ordinary forward convention is::

    new_deck[i] = old_deck[p_symbol[i]]
    output = new_deck[0]

If ``q_symbol`` is the inverse of ``p_symbol``, a card's position instead
evolves as ``new_position = q_symbol[old_position]``.  Tracking only card
positions needed by the observations avoids materializing an entire deck at
every step.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from eye_mystery.arbitrary_gak_sat import GAKWitness, encrypt_messages


@dataclass(frozen=True)
class NextCardForcing:
    """Feasibility of the observed and an alternative next output."""

    actual_status: str
    alternative_status: str
    alternative_card: int | None
    actual_witness: GAKWitness | None
    alternative_witness: GAKWitness | None

    @property
    def forced(self) -> bool:
        return self.actual_status == "sat" and self.alternative_status == "unsat"


@dataclass(frozen=True)
class SparseUnsatCore:
    """Observed output positions sufficient for an exact rejection."""

    status: str
    observations: tuple[tuple[int, int], ...]


@dataclass
class _SparseProblem:
    z3: Any
    solver: Any
    top_card: Any
    transitions: list[list[tuple[Any, Any]]]
    observation_guards: list[tuple[tuple[int, int], Any]]
    final_positions: dict[int, Any]
    width: int


def canonical_initial_deck(size: int, top_card: int) -> tuple[int, ...]:
    """Return the position-conjugacy representative for one top card."""

    if size < 2:
        raise ValueError("deck size must be at least two")
    if not 0 <= top_card < size:
        raise ValueError("initial top card is outside the deck")
    return (top_card, *(card for card in range(size) if card != top_card))


def encode_text(text: str) -> tuple[tuple[int, ...], tuple[str, ...]]:
    """Map literal characters to integers in first-occurrence order."""

    alphabet = tuple(dict.fromkeys(text))
    lookup = {character: index for index, character in enumerate(alphabet)}
    return tuple(lookup[character] for character in text), alphabet


def _validate(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    plains = tuple(tuple(message) for message in plaintexts)
    ciphers = tuple(tuple(message) for message in ciphertexts)
    if len(plains) != len(ciphers):
        raise ValueError("plaintext and ciphertext message counts differ")
    if any(
        len(plaintext) != len(ciphertext)
        for plaintext, ciphertext in zip(plains, ciphers, strict=True)
    ):
        raise ValueError("plaintext and ciphertext lengths differ")
    if deck_size < 2 or plaintext_alphabet_size < 1:
        raise ValueError("alphabet sizes must be positive")
    if any(
        not 0 <= symbol < plaintext_alphabet_size
        for plaintext in plains
        for symbol in plaintext
    ):
        raise ValueError("plaintext symbol is outside the operation alphabet")
    if any(
        not 0 <= card < deck_size for ciphertext in ciphers for card in ciphertext
    ):
        raise ValueError("ciphertext card is outside the deck")
    return plains, ciphers


def _initial_position(
    z3: Any,
    card: int,
    top_card: Any,
    width: int,
) -> Any:
    """Position of ``card`` in the canonical deck with symbolic top."""

    return z3.If(
        top_card == z3.BitVecVal(card, width),
        z3.BitVecVal(0, width),
        z3.If(
            z3.ULT(z3.BitVecVal(card, width), top_card),
            z3.BitVecVal(card + 1, width),
            z3.BitVecVal(card, width),
        ),
    )


def _constrain_partial_permutation_step(
    z3: Any,
    solver: Any,
    transitions: list[tuple[Any, Any]],
    old_position: Any,
    new_position: Any,
    *,
    deck_size: int,
    width: int,
) -> None:
    """Add one edge to a partial bijection on the finite position set."""

    solver.add(z3.ULT(new_position, z3.BitVecVal(deck_size, width)))
    for prior_old, prior_new in transitions:
        solver.add(
            (old_position == prior_old) == (new_position == prior_new)
        )
    transitions.append((old_position, new_position))


def _build_problem(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    tracked_cards: Sequence[int],
    timeout_ms: int,
    track_through_end: bool = False,
    guard_observations: bool = False,
) -> _SparseProblem:
    try:
        import z3  # type: ignore[import-not-found]
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("sparse GAK recovery requires z3-solver") from error

    plains, ciphers = _validate(
        plaintexts,
        ciphertexts,
        deck_size=deck_size,
        plaintext_alphabet_size=plaintext_alphabet_size,
    )
    cards = tuple(sorted(set(tracked_cards)))
    if any(not 0 <= card < deck_size for card in cards):
        raise ValueError("tracked card is outside the deck")

    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    width = max(1, deck_size.bit_length())
    top_card = z3.BitVec("initial_top_card", width)
    solver.add(z3.ULT(top_card, z3.BitVecVal(deck_size, width)))

    transitions: list[list[tuple[Any, Any]]] = [
        [] for _ in range(plaintext_alphabet_size)
    ]
    observation_guards: list[tuple[tuple[int, int], Any]] = []

    last_positions: dict[int, Any] = {}
    for message_index, (plaintext, ciphertext) in enumerate(
        zip(plains, ciphers, strict=True)
    ):
        if track_through_end:
            last_needed = {card: len(plaintext) - 1 for card in cards}
        else:
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
            card: _initial_position(z3, card, top_card, width)
            for card in last_needed
        }
        for offset, (symbol, emitted) in enumerate(
            zip(plaintext, ciphertext, strict=True)
        ):
            current: dict[int, Any] = {}
            for card in last_needed:
                if last_needed[card] < offset:
                    continue
                position = z3.BitVec(
                    f"pos_{message_index}_{offset}_{card}",
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
            output_constraint = (
                current[emitted] == z3.BitVecVal(0, width)
            )
            if guard_observations:
                guard = z3.Bool(f"observe_{message_index}_{offset}")
                solver.add(z3.Implies(guard, output_constraint))
                observation_guards.append(((message_index, offset), guard))
            else:
                solver.add(output_constraint)
            previous = current
        if len(plains) == 1:
            last_positions = previous

    return _SparseProblem(
        z3=z3,
        solver=solver,
        top_card=top_card,
        transitions=transitions,
        observation_guards=observation_guards,
        final_positions=last_positions,
        width=width,
    )


def _extract_witness(
    problem: _SparseProblem,
    *,
    deck_size: int,
) -> GAKWitness:
    model = problem.solver.model()
    top_card = model.eval(problem.top_card, model_completion=True).as_long()
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
    return GAKWitness(
        initial_deck=canonical_initial_deck(deck_size, top_card),
        operations=tuple(forward_operations),
    )


def recover_sparse_known_plaintext_witness(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    timeout_ms: int = 30_000,
) -> tuple[str, GAKWitness | None]:
    """Recover one exact arbitrary-operation witness, if decidable."""

    tracked_cards = sorted(
        {card for ciphertext in ciphertexts for card in ciphertext}
    )
    problem = _build_problem(
        plaintexts,
        ciphertexts,
        deck_size=deck_size,
        plaintext_alphabet_size=plaintext_alphabet_size,
        tracked_cards=tracked_cards,
        timeout_ms=timeout_ms,
    )
    result = problem.solver.check()
    if result == problem.z3.unsat:
        return "unsat", None
    if result != problem.z3.sat:
        return "unknown", None

    witness = _extract_witness(problem, deck_size=deck_size)
    expected = tuple(tuple(message) for message in ciphertexts)
    if encrypt_messages(plaintexts, witness.initial_deck, witness.operations) != expected:
        raise AssertionError("sparse solver witness failed exact forward replay")
    return "sat", witness


def find_sparse_unsat_core(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    timeout_ms: int = 30_000,
) -> SparseUnsatCore:
    """Return a solver core of output observations when the instance is UNSAT."""

    tracked_cards = sorted(
        {card for ciphertext in ciphertexts for card in ciphertext}
    )
    problem = _build_problem(
        plaintexts,
        ciphertexts,
        deck_size=deck_size,
        plaintext_alphabet_size=plaintext_alphabet_size,
        tracked_cards=tracked_cards,
        timeout_ms=timeout_ms,
        guard_observations=True,
    )
    assumptions = [guard for _, guard in problem.observation_guards]
    result = problem.solver.check(*assumptions)
    if result == problem.z3.unsat:
        core_names = {str(guard) for guard in problem.solver.unsat_core()}
        observations = tuple(
            location
            for location, guard in problem.observation_guards
            if str(guard) in core_names
        )
        return SparseUnsatCore("unsat", observations)
    if result == problem.z3.sat:
        return SparseUnsatCore("sat", ())
    return SparseUnsatCore("unknown", ())


def check_next_card_forcing(
    plaintext_prefix: Sequence[int],
    ciphertext_prefix: Sequence[int],
    next_symbol: int,
    actual_next_card: int,
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    timeout_ms: int = 30_000,
) -> NextCardForcing:
    """Test the actual next card, then any alternative, from a frozen prefix."""

    if len(plaintext_prefix) != len(ciphertext_prefix):
        raise ValueError("plaintext and ciphertext prefix lengths differ")
    if not 0 <= next_symbol < plaintext_alphabet_size:
        raise ValueError("next plaintext symbol is outside the operation alphabet")
    if not 0 <= actual_next_card < deck_size:
        raise ValueError("actual next card is outside the deck")
    plaintext = (tuple(plaintext_prefix) + (next_symbol,),)
    prefix_cipher = tuple(ciphertext_prefix)
    if not prefix_cipher:
        raise ValueError("at least one observed prefix card is required")

    # Build the observed prefix with all cards tracked.
    problem = _build_problem(
        (tuple(plaintext_prefix),),
        (prefix_cipher,),
        deck_size=deck_size,
        plaintext_alphabet_size=plaintext_alphabet_size,
        tracked_cards=tuple(range(deck_size)),
        timeout_ms=timeout_ms,
        track_through_end=True,
    )
    next_positions: dict[int, Any] = {}
    for card in range(deck_size):
        position = problem.z3.BitVec(f"heldout_pos_{card}", problem.width)
        _constrain_partial_permutation_step(
            problem.z3,
            problem.solver,
            problem.transitions[next_symbol],
            problem.final_positions[card],
            position,
            deck_size=deck_size,
            width=problem.width,
        )
        next_positions[card] = position

    def solve_with(constraint: Any) -> tuple[str, GAKWitness | None]:
        problem.solver.push()
        problem.solver.add(constraint)
        result = problem.solver.check()
        if result == problem.z3.unsat:
            status, witness = "unsat", None
        elif result == problem.z3.sat:
            status = "sat"
            witness = _extract_witness(problem, deck_size=deck_size)
        else:
            status, witness = "unknown", None
        problem.solver.pop()
        return status, witness

    zero = problem.z3.BitVecVal(0, problem.width)
    actual_status, actual_witness = solve_with(
        next_positions[actual_next_card] == zero
    )
    alternative_status, alternative_witness = solve_with(
        next_positions[actual_next_card] != zero
    )
    alternative_card = None
    if alternative_status == "sat":
        assert alternative_witness is not None
        replay = encrypt_messages(
            plaintext,
            alternative_witness.initial_deck,
            alternative_witness.operations,
        )[0]
        alternative_card = replay[-1]
        if alternative_card == actual_next_card:
            raise AssertionError("alternative constraint returned the actual card")

    if actual_status == "sat":
        assert actual_witness is not None
        actual_replay = encrypt_messages(
            plaintext,
            actual_witness.initial_deck,
            actual_witness.operations,
        )[0]
        if actual_replay[:-1] != prefix_cipher or actual_replay[-1] != actual_next_card:
            raise AssertionError("actual held-out witness failed forward replay")
    if alternative_status == "sat":
        assert alternative_witness is not None
        alternative_replay = encrypt_messages(
            plaintext,
            alternative_witness.initial_deck,
            alternative_witness.operations,
        )[0]
        if alternative_replay[:-1] != prefix_cipher:
            raise AssertionError("alternative held-out witness failed prefix replay")

    return NextCardForcing(
        actual_status=actual_status,
        alternative_status=alternative_status,
        alternative_card=alternative_card,
        actual_witness=actual_witness,
        alternative_witness=alternative_witness,
    )
