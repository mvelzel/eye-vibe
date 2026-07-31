"""Sparse exact ordinary-GAK recovery with symbolic plaintext actions.

For each observed card transition this model records

``new_position = move(action, old_position)``

and

``old_position = unmove(action, new_position)``.

The two shared uninterpreted functions enforce functionality and injectivity
without materializing unobserved permutation entries.  Every resulting finite
partial injection extends to a full permutation of the deck positions.
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
class SymbolicSparseGAKWitness:
    """One completed key, independent start deck, and plaintext schedule."""

    initial_decks: tuple[tuple[int, ...], ...]
    operations: tuple[tuple[int, ...], ...]
    plaintexts: tuple[tuple[int, ...], ...]


def _add_trace_zero_position_symmetry(
    z3: Any,
    solver: Any,
    positions: dict[int, Any],
    *,
    deck_size: int,
) -> None:
    cards = tuple(sorted(positions))
    cases: list[Any] = []
    if len(cards) < deck_size:
        cases.append(
            z3.And(
                *(
                    positions[card] == index + 1
                    for index, card in enumerate(cards)
                )
            )
        )
    for top_index, top_card in enumerate(cards):
        constraints = [positions[top_card] == 0]
        next_position = 1
        for index, card in enumerate(cards):
            if index == top_index:
                continue
            constraints.append(positions[card] == next_position)
            next_position += 1
        cases.append(z3.And(*constraints))
    solver.add(z3.Or(*cases))


def _add_extra_action_first_use_symmetry(
    z3: Any,
    solver: Any,
    unknown_selectors: Sequence[Any],
    *,
    pinned_action_count: int,
    action_count: int,
) -> None:
    for index, selector in enumerate(unknown_selectors):
        for symbol in range(pinned_action_count + 1, action_count):
            prior = [
                earlier == symbol - 1
                for earlier in unknown_selectors[:index]
            ]
            solver.add(
                z3.Implies(
                    selector == symbol,
                    z3.Or(*prior) if prior else z3.BoolVal(False),
                )
            )


def recover_symbolic_sparse_gak(
    schedules: Sequence[Sequence[int | None]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    pinned_action_count: int = 0,
    timeout_ms: int = 30_000,
    break_position_symmetry: bool = True,
    break_extra_action_symmetry: bool = True,
) -> tuple[str, SymbolicSparseGAKWitness | None]:
    """Recover shared partial actions, then complete and replay them exactly."""

    try:
        import z3  # type: ignore[import-not-found]
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("symbolic sparse GAK recovery requires z3") from error

    patterns = tuple(tuple(schedule) for schedule in schedules)
    ciphers = tuple(tuple(ciphertext) for ciphertext in ciphertexts)
    if len(patterns) != len(ciphers):
        raise ValueError("schedule and ciphertext trace counts differ")
    if not patterns:
        raise ValueError("at least one trace is required")
    if any(
        len(schedule) != len(ciphertext)
        for schedule, ciphertext in zip(patterns, ciphers, strict=True)
    ):
        raise ValueError("schedule and ciphertext lengths differ")
    if deck_size < 2 or plaintext_alphabet_size < 1:
        raise ValueError("alphabet sizes must be positive")
    if not 0 <= pinned_action_count <= plaintext_alphabet_size:
        raise ValueError("pinned action count is outside the action alphabet")
    if any(
        symbol is not None
        and not 0 <= symbol < plaintext_alphabet_size
        for schedule in patterns
        for symbol in schedule
    ):
        raise ValueError("pinned symbol is outside the action alphabet")
    if any(
        not 0 <= card < deck_size
        for ciphertext in ciphers
        for card in ciphertext
    ):
        raise ValueError("ciphertext card is outside the deck")

    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    move = z3.Function(
        "move",
        z3.IntSort(),
        z3.IntSort(),
        z3.IntSort(),
    )
    unmove = z3.Function(
        "unmove",
        z3.IntSort(),
        z3.IntSort(),
        z3.IntSort(),
    )
    initial_positions_by_trace: list[dict[int, Any]] = []
    selectors_by_trace: list[tuple[Any, ...]] = []
    unknown_selectors: list[Any] = []
    transition_records: list[tuple[Any, Any, Any]] = []

    for trace_index, (schedule, ciphertext) in enumerate(
        zip(patterns, ciphers, strict=True)
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
        if len(initial_positions) > 1:
            solver.add(z3.Distinct(*initial_positions.values()))
        if trace_index == 0 and break_position_symmetry:
            _add_trace_zero_position_symmetry(
                z3,
                solver,
                initial_positions,
                deck_size=deck_size,
            )
        initial_positions_by_trace.append(initial_positions)
        last_offset = {
            card: max(
                offset
                for offset, value in enumerate(ciphertext)
                if value == card
            )
            for card in cards
        }
        previous = initial_positions
        selectors: list[Any] = []

        for offset, (pinned, emitted) in enumerate(
            zip(schedule, ciphertext, strict=True)
        ):
            if pinned is None:
                selector = z3.Int(f"plaintext_{trace_index}_{offset}")
                solver.add(
                    selector >= 0,
                    selector < plaintext_alphabet_size,
                )
                unknown_selectors.append(selector)
            else:
                selector = z3.IntVal(pinned)
            selectors.append(selector)
            current: dict[int, Any] = {}
            for card in cards:
                if last_offset[card] < offset:
                    continue
                old_position = previous[card]
                new_position = z3.Int(
                    f"position_{trace_index}_{offset}_{card}"
                )
                solver.add(
                    new_position == move(selector, old_position),
                    new_position >= 0,
                    new_position < deck_size,
                    unmove(selector, new_position) == old_position,
                )
                transition_records.append(
                    (selector, old_position, new_position)
                )
                current[card] = new_position
            solver.add(current[emitted] == 0)
            previous = current
        selectors_by_trace.append(tuple(selectors))

    if (
        break_extra_action_symmetry
        and pinned_action_count < plaintext_alphabet_size
    ):
        _add_extra_action_first_use_symmetry(
            z3,
            solver,
            unknown_selectors,
            pinned_action_count=pinned_action_count,
            action_count=plaintext_alphabet_size,
        )

    result = solver.check()
    if result == z3.unsat:
        return "unsat", None
    if result != z3.sat:
        return "unknown", None

    model = solver.model()
    plaintexts = tuple(
        tuple(
            model.eval(selector, model_completion=True).as_long()
            for selector in selectors
        )
        for selectors in selectors_by_trace
    )
    transitions: list[list[tuple[Any, Any]]] = [
        [] for _ in range(plaintext_alphabet_size)
    ]
    for selector, old_position, new_position in transition_records:
        symbol = model.eval(selector, model_completion=True).as_long()
        transitions[symbol].append((old_position, new_position))
    operations = tuple(
        _complete_permutation(model, records, deck_size=deck_size)
        for records in transitions
    )
    initial_decks = tuple(
        _complete_deck(model, positions, deck_size=deck_size)
        for positions in initial_positions_by_trace
    )
    witness = SymbolicSparseGAKWitness(
        initial_decks=initial_decks,
        operations=operations,
        plaintexts=plaintexts,
    )
    replay = tuple(
        encrypt_messages((plaintext,), deck, operations)[0]
        for plaintext, deck in zip(
            plaintexts, initial_decks, strict=True
        )
    )
    if replay != ciphers:
        raise AssertionError("symbolic sparse witness failed exact replay")
    return "sat", witness
