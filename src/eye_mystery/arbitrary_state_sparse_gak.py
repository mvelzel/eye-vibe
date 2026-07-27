"""Exact sparse ordinary-GAK recovery from independent starting states.

Each trace may start from an arbitrary deck, while all traces share one fixed
position permutation per plaintext symbol. Only ciphertext cards observed in
that trace are tracked. Partial bijections are sufficient because every
partial injection on a finite set extends to a full permutation.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from eye_mystery.arbitrary_gak_sat import encrypt_messages


@dataclass(frozen=True)
class ArbitraryStateGAKWitness:
    initial_decks: tuple[tuple[int, ...], ...]
    operations: tuple[tuple[int, ...], ...]


def _constrain_partial_permutation_step(
    z3: Any,
    solver: Any,
    transitions: list[tuple[Any, Any]],
    old_position: Any,
    new_position: Any,
    *,
    deck_size: int,
) -> None:
    solver.add(new_position >= 0, new_position < deck_size)
    for prior_old, prior_new in transitions:
        solver.add((old_position == prior_old) == (new_position == prior_new))
    transitions.append((old_position, new_position))


def _complete_permutation(
    model: Any,
    transitions: Sequence[tuple[Any, Any]],
    *,
    deck_size: int,
) -> tuple[int, ...]:
    inverse: dict[int, int] = {}
    used_outputs: set[int] = set()
    for old_expression, new_expression in transitions:
        old_position = model.eval(old_expression, model_completion=True).as_long()
        new_position = model.eval(new_expression, model_completion=True).as_long()
        if old_position in inverse and inverse[old_position] != new_position:
            raise AssertionError("model violates operation functionality")
        if new_position in used_outputs and inverse.get(old_position) != new_position:
            raise AssertionError("model violates operation injectivity")
        inverse[old_position] = new_position
        used_outputs.add(new_position)
    for old_position, new_position in zip(
        (value for value in range(deck_size) if value not in inverse),
        (value for value in range(deck_size) if value not in used_outputs),
        strict=True,
    ):
        inverse[old_position] = new_position
    forward = [0] * deck_size
    for old_position, new_position in inverse.items():
        forward[new_position] = old_position
    return tuple(forward)


def _complete_deck(
    model: Any,
    initial_positions: dict[int, Any],
    *,
    deck_size: int,
) -> tuple[int, ...]:
    deck: list[int | None] = [None] * deck_size
    used_cards = set(initial_positions)
    for card, expression in initial_positions.items():
        position = model.eval(expression, model_completion=True).as_long()
        if deck[position] is not None:
            raise AssertionError("model gives two cards one initial position")
        deck[position] = card
    remaining_cards = (
        card for card in range(deck_size) if card not in used_cards
    )
    for position, card in zip(
        (index for index, value in enumerate(deck) if value is None),
        remaining_cards,
        strict=True,
    ):
        deck[position] = card
    return tuple(value for value in deck if value is not None)


def recover_arbitrary_state_gak_witness(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    timeout_ms: int = 30_000,
) -> tuple[str, ArbitraryStateGAKWitness | None]:
    """Recover shared operations and one arbitrary start deck per trace."""

    try:
        import z3  # type: ignore[import-not-found]
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("arbitrary-state GAK recovery requires z3-solver") from error

    plains = tuple(tuple(message) for message in plaintexts)
    ciphers = tuple(tuple(message) for message in ciphertexts)
    if len(plains) != len(ciphers):
        raise ValueError("plaintext and ciphertext trace counts differ")
    if any(
        len(plaintext) != len(ciphertext)
        for plaintext, ciphertext in zip(plains, ciphers, strict=True)
    ):
        raise ValueError("plaintext and ciphertext lengths differ")
    if any(
        not 0 <= symbol < plaintext_alphabet_size
        for plaintext in plains
        for symbol in plaintext
    ):
        raise ValueError("plaintext symbol is outside the operation alphabet")
    if any(
        not 0 <= card < deck_size
        for ciphertext in ciphers
        for card in ciphertext
    ):
        raise ValueError("ciphertext card is outside the deck")

    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    transitions: list[list[tuple[Any, Any]]] = [
        [] for _ in range(plaintext_alphabet_size)
    ]
    trace_initial_positions: list[dict[int, Any]] = []

    for trace_index, (plaintext, ciphertext) in enumerate(
        zip(plains, ciphers, strict=True)
    ):
        cards = tuple(sorted(set(ciphertext)))
        initial_positions = {
            card: z3.Int(f"initial_{trace_index}_{card}")
            for card in cards
        }
        solver.add(
            *(
                z3.And(position >= 0, position < deck_size)
                for position in initial_positions.values()
            )
        )
        solver.add(z3.Distinct(*initial_positions.values()))
        trace_initial_positions.append(initial_positions)
        previous = initial_positions

        for offset, (symbol, emitted) in enumerate(
            zip(plaintext, ciphertext, strict=True)
        ):
            current: dict[int, Any] = {}
            for card in cards:
                position = z3.Int(f"position_{trace_index}_{offset}_{card}")
                _constrain_partial_permutation_step(
                    z3,
                    solver,
                    transitions[symbol],
                    previous[card],
                    position,
                    deck_size=deck_size,
                )
                current[card] = position
            solver.add(current[emitted] == 0)
            previous = current

    result = solver.check()
    if result == z3.unsat:
        return "unsat", None
    if result != z3.sat:
        return "unknown", None
    model = solver.model()
    operations = tuple(
        _complete_permutation(model, operation, deck_size=deck_size)
        for operation in transitions
    )
    initial_decks = tuple(
        _complete_deck(model, positions, deck_size=deck_size)
        for positions in trace_initial_positions
    )
    witness = ArbitraryStateGAKWitness(initial_decks, operations)
    replay = tuple(
        encrypt_messages((plaintext,), deck, operations)[0]
        for plaintext, deck in zip(plains, initial_decks, strict=True)
    )
    if replay != ciphers:
        raise AssertionError("arbitrary-state sparse witness failed exact replay")
    return "sat", witness
