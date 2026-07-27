"""Ordinary-GAK recovery with pinned and unknown plaintext actions.

Each trace begins in an independent arbitrary deck state. ``None`` schedule
entries are solver-selected, while integer entries pin a shared action label.
Only cards still needed by a later observation are tracked. Partial action
bijections are completed to full permutations before every exact replay.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from eye_mystery.arbitrary_gak_sat import encrypt_messages
from eye_mystery.arbitrary_state_sparse_gak import (
    _complete_deck,
    _complete_permutation,
)


@dataclass(frozen=True)
class PartiallyKnownGAKWitness:
    """One constructive key, start deck, and completed schedule per trace."""

    initial_decks: tuple[tuple[int, ...], ...]
    operations: tuple[tuple[int, ...], ...]
    plaintexts: tuple[tuple[int, ...], ...]


def _select(z3: Any, selector: Any, values: Sequence[Any]) -> Any:
    selected = values[-1]
    for index in range(len(values) - 2, -1, -1):
        selected = z3.If(selector == index, values[index], selected)
    return selected


def recover_partially_known_arbitrary_state_gak(
    schedules: Sequence[Sequence[int | None]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    timeout_ms: int = 30_000,
) -> tuple[str, PartiallyKnownGAKWitness | None]:
    """Recover shared actions with arbitrary starts and partially known text."""

    try:
        import z3  # type: ignore[import-not-found]
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("partially known GAK recovery requires z3-solver") from error

    patterns = tuple(tuple(schedule) for schedule in schedules)
    ciphers = tuple(tuple(ciphertext) for ciphertext in ciphertexts)
    if len(patterns) != len(ciphers):
        raise ValueError("schedule and ciphertext trace counts differ")
    if any(
        len(schedule) != len(ciphertext)
        for schedule, ciphertext in zip(patterns, ciphers, strict=True)
    ):
        raise ValueError("schedule and ciphertext lengths differ")
    if deck_size < 2 or plaintext_alphabet_size < 1:
        raise ValueError("alphabet sizes must be positive")
    if any(
        symbol is not None
        and not 0 <= symbol < plaintext_alphabet_size
        for schedule in patterns
        for symbol in schedule
    ):
        raise ValueError("pinned symbol is outside the operation alphabet")
    if any(
        not 0 <= card < deck_size
        for ciphertext in ciphers
        for card in ciphertext
    ):
        raise ValueError("ciphertext card is outside the deck")

    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    operations = [
        z3.Function(f"op_{symbol}", z3.IntSort(), z3.IntSort())
        for symbol in range(plaintext_alphabet_size)
    ]
    inverses = [
        z3.Function(f"inv_{symbol}", z3.IntSort(), z3.IntSort())
        for symbol in range(plaintext_alphabet_size)
    ]
    transition_records: list[tuple[Any, Any, Any]] = []
    initial_positions_by_trace: list[dict[int, Any]] = []
    selectors_by_trace: list[tuple[Any, ...]] = []

    for trace_index, (schedule, ciphertext) in enumerate(
        zip(patterns, ciphers, strict=True)
    ):
        cards = tuple(sorted(set(ciphertext)))
        initial_positions = {
            card: z3.Int(f"initial_{trace_index}_{card}") for card in cards
        }
        solver.add(
            *(
                z3.And(position >= 0, position < deck_size)
                for position in initial_positions.values()
            )
        )
        if len(initial_positions) > 1:
            solver.add(z3.Distinct(*initial_positions.values()))
        initial_positions_by_trace.append(initial_positions)
        last_offset = {
            card: max(
                offset for offset, value in enumerate(ciphertext) if value == card
            )
            for card in cards
        }
        previous = initial_positions
        selectors: list[Any] = []

        for offset, (pinned, emitted) in enumerate(
            zip(schedule, ciphertext, strict=True)
        ):
            if pinned is None:
                selector = z3.Int(f"plain_{trace_index}_{offset}")
                solver.add(
                    selector >= 0, selector < plaintext_alphabet_size
                )
            else:
                selector = z3.IntVal(pinned)
            selectors.append(selector)
            current: dict[int, Any] = {}
            active_cards = tuple(
                card for card in cards if last_offset[card] >= offset
            )
            for card in active_cards:
                old_position = previous[card]
                new_position = z3.Int(
                    f"position_{trace_index}_{offset}_{card}"
                )
                images = tuple(
                    operation(old_position) for operation in operations
                )
                solver.add(new_position == _select(z3, selector, images))
                solver.add(new_position >= 0, new_position < deck_size)
                for symbol, inverse in enumerate(inverses):
                    solver.add(
                        z3.Implies(
                            selector == symbol,
                            inverse(new_position) == old_position,
                        )
                    )
                transition_records.append(
                    (selector, old_position, new_position)
                )
                current[card] = new_position
            solver.add(current[emitted] == 0)
            previous = current
        selectors_by_trace.append(tuple(selectors))

    result = solver.check()
    if result == z3.unsat:
        return "unsat", None
    if result != z3.sat:
        return "unknown", None

    model = solver.model()
    plaintexts = tuple(
        tuple(model.eval(selector, model_completion=True).as_long() for selector in row)
        for row in selectors_by_trace
    )
    transitions: list[list[tuple[Any, Any]]] = [
        [] for _ in range(plaintext_alphabet_size)
    ]
    for selector, old_position, new_position in transition_records:
        symbol = model.eval(selector, model_completion=True).as_long()
        transitions[symbol].append((old_position, new_position))
    completed_operations_tuple = tuple(
        _complete_permutation(model, records, deck_size=deck_size)
        for records in transitions
    )
    initial_decks = tuple(
        _complete_deck(model, positions, deck_size=deck_size)
        for positions in initial_positions_by_trace
    )
    witness = PartiallyKnownGAKWitness(
        initial_decks,
        completed_operations_tuple,
        plaintexts,
    )
    replay = tuple(
        encrypt_messages((plaintext,), deck, completed_operations_tuple)[0]
        for plaintext, deck in zip(plaintexts, initial_decks, strict=True)
    )
    if replay != ciphers:
        raise AssertionError("partially known GAK witness failed exact replay")
    return "sat", witness
