"""Finite-domain ordinary-GAK recovery using OR-Tools CP-SAT."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from eye_mystery.arbitrary_gak_sat import encrypt_messages


@dataclass(frozen=True)
class CPSATGAKWitness:
    """One complete CP-SAT key, start deck set, and plaintext schedule."""

    initial_decks: tuple[tuple[int, ...], ...]
    operations: tuple[tuple[int, ...], ...]
    plaintexts: tuple[tuple[int, ...], ...]


def _canonical_trace_zero_assignments(
    card_count: int,
    *,
    deck_size: int,
) -> tuple[tuple[int, ...], ...]:
    assignments: list[tuple[int, ...]] = []
    if card_count < deck_size:
        assignments.append(tuple(range(1, card_count + 1)))
    for top_index in range(card_count):
        row: list[int] = []
        next_position = 1
        for index in range(card_count):
            if index == top_index:
                row.append(0)
            else:
                row.append(next_position)
                next_position += 1
        assignments.append(tuple(row))
    return tuple(assignments)


def _complete_deck(
    solver: Any,
    positions: dict[int, Any],
    *,
    deck_size: int,
) -> tuple[int, ...]:
    deck: list[int | None] = [None] * deck_size
    used_cards = set(positions)
    for card, variable in positions.items():
        position = solver.value(variable)
        if deck[position] is not None:
            raise AssertionError("CP-SAT gives two cards one initial position")
        deck[position] = card
    remaining = iter(card for card in range(deck_size) if card not in used_cards)
    for position, card in enumerate(deck):
        if card is None:
            deck[position] = next(remaining)
    return tuple(card for card in deck if card is not None)


def recover_cp_sat_gak(
    schedules: Sequence[Sequence[int | None]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    timeout_seconds: float = 30.0,
    num_workers: int = 8,
    break_position_symmetry: bool = True,
) -> tuple[str, CPSATGAKWitness | None]:
    """Recover shared full permutations and symbolic gap action labels."""

    try:
        from ortools.sat.python import cp_model
    except ImportError as error:  # pragma: no cover - optional dependency
        raise RuntimeError("CP-SAT GAK recovery requires OR-Tools") from error

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

    model = cp_model.CpModel()
    inverse_operations = tuple(
        tuple(
            model.new_int_var(
                0,
                deck_size - 1,
                f"inverse_operation_{symbol}_{position}",
            )
            for position in range(deck_size)
        )
        for symbol in range(plaintext_alphabet_size)
    )
    for operation in inverse_operations:
        model.add_all_different(operation)
    flat_operations = tuple(
        value for operation in inverse_operations for value in operation
    )

    initial_positions_by_trace: list[dict[int, Any]] = []
    selectors_by_trace: list[tuple[int | Any, ...]] = []
    unknown_selectors: list[Any] = []

    for trace_index, (schedule, ciphertext) in enumerate(
        zip(patterns, ciphers, strict=True)
    ):
        cards = tuple(sorted(set(ciphertext)))
        initial_positions = {
            card: model.new_int_var(
                0,
                deck_size - 1,
                f"initial_{trace_index}_{card}",
            )
            for card in cards
        }
        if len(initial_positions) > 1:
            model.add_all_different(tuple(initial_positions.values()))
        if trace_index == 0 and break_position_symmetry:
            model.add_allowed_assignments(
                tuple(initial_positions.values()),
                _canonical_trace_zero_assignments(
                    len(cards),
                    deck_size=deck_size,
                ),
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
        selectors: list[int | Any] = []

        for offset, (pinned, emitted) in enumerate(
            zip(schedule, ciphertext, strict=True)
        ):
            if pinned is None:
                selector: int | Any = model.new_int_var(
                    0,
                    plaintext_alphabet_size - 1,
                    f"plaintext_{trace_index}_{offset}",
                )
                unknown_selectors.append(selector)
            else:
                selector = pinned
            selectors.append(selector)
            current: dict[int, Any] = {}
            for card in cards:
                if last_offset[card] < offset:
                    continue
                old_position = previous[card]
                new_position = model.new_int_var(
                    0,
                    deck_size - 1,
                    f"position_{trace_index}_{offset}_{card}",
                )
                if isinstance(selector, int):
                    model.add_element(
                        old_position,
                        inverse_operations[selector],
                        new_position,
                    )
                else:
                    flat_index = model.new_int_var(
                        0,
                        plaintext_alphabet_size * deck_size - 1,
                        f"flat_index_{trace_index}_{offset}_{card}",
                    )
                    model.add(
                        flat_index == selector * deck_size + old_position
                    )
                    model.add_element(
                        flat_index,
                        flat_operations,
                        new_position,
                    )
                current[card] = new_position
            model.add(current[emitted] == 0)
            previous = current
        selectors_by_trace.append(tuple(selectors))

    if unknown_selectors:
        model.add_decision_strategy(
            unknown_selectors,
            cp_model.CHOOSE_FIRST,
            cp_model.SELECT_MIN_VALUE,
        )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = timeout_seconds
    solver.parameters.num_search_workers = num_workers
    solver.parameters.random_seed = 31072026
    result = solver.solve(model)
    if result == cp_model.INFEASIBLE:
        return "unsat", None
    if result not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return "unknown", None

    plaintexts = tuple(
        tuple(
            selector
            if isinstance(selector, int)
            else solver.value(selector)
            for selector in selectors
        )
        for selectors in selectors_by_trace
    )
    inverse_rows = tuple(
        tuple(solver.value(value) for value in operation)
        for operation in inverse_operations
    )
    operations: list[tuple[int, ...]] = []
    for inverse in inverse_rows:
        forward = [0] * deck_size
        for old_position, new_position in enumerate(inverse):
            forward[new_position] = old_position
        operations.append(tuple(forward))
    initial_decks = tuple(
        _complete_deck(solver, positions, deck_size=deck_size)
        for positions in initial_positions_by_trace
    )
    witness = CPSATGAKWitness(
        initial_decks=initial_decks,
        operations=tuple(operations),
        plaintexts=plaintexts,
    )
    replay = tuple(
        encrypt_messages((plaintext,), deck, witness.operations)[0]
        for plaintext, deck in zip(
            plaintexts, initial_decks, strict=True
        )
    )
    if replay != ciphers:
        raise AssertionError("CP-SAT GAK witness failed exact replay")
    return "sat", witness
