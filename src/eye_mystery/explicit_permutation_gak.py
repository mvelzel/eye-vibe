"""Exact ordinary-GAK recovery with explicit finite permutation tables.

This is the finite-domain counterpart to
``partially_known_arbitrary_state_gak``.  It models the inverse of every deck
operation as a complete permutation of positions, so a card position advances
with one array lookup per plaintext character.  Unknown plaintext characters
select one of the shared operation tables.

The representation is deliberately constructive: every SAT model is inverted
back to the forward GAK convention and independently replayed.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from eye_mystery.arbitrary_gak_sat import encrypt_messages


@dataclass(frozen=True)
class ExplicitPermutationGAKWitness:
    """One exact key, independent start deck, and completed plaintext."""

    initial_decks: tuple[tuple[int, ...], ...]
    operations: tuple[tuple[int, ...], ...]
    plaintexts: tuple[tuple[int, ...], ...]


def _complete_deck_from_positions(
    model: Any,
    positions: dict[int, Any],
    *,
    deck_size: int,
) -> tuple[int, ...]:
    deck: list[int | None] = [None] * deck_size
    used_cards = set(positions)
    for card, expression in positions.items():
        position = model.eval(expression, model_completion=True).as_long()
        if deck[position] is not None:
            raise AssertionError("model gives two cards one initial position")
        deck[position] = card
    remaining = iter(card for card in range(deck_size) if card not in used_cards)
    for index, card in enumerate(deck):
        if card is None:
            deck[index] = next(remaining)
    return tuple(card for card in deck if card is not None)


def _selected_transition(
    z3: Any,
    selector: Any,
    old_position: Any,
    inverse_operations: Sequence[Any],
    *,
    selector_width: int,
) -> Any:
    selected = z3.Select(inverse_operations[-1], old_position)
    for symbol in range(len(inverse_operations) - 2, -1, -1):
        selected = z3.If(
            selector == z3.BitVecVal(symbol, selector_width),
            z3.Select(inverse_operations[symbol], old_position),
            selected,
        )
    return selected


def _add_trace_zero_position_symmetry(
    z3: Any,
    solver: Any,
    positions: dict[int, Any],
    *,
    deck_size: int,
    position_width: int,
) -> None:
    """Choose one representative under conjugation fixing top position zero.

    A global relabelling of nonzero positions changes neither the emitted top
    cards nor feasibility.  For the first trace, enumerate whether an observed
    card initially occupies zero and place every other observed card in
    card-label order at consecutive positive positions.  The "none at zero"
    case is available when the trace does not observe every deck card.
    """

    cards = tuple(sorted(positions))
    cases: list[Any] = []
    if len(cards) < deck_size:
        cases.append(
            z3.And(
                *(
                    positions[card] == z3.BitVecVal(index + 1, position_width)
                    for index, card in enumerate(cards)
                )
            )
        )
    for top_index, top_card in enumerate(cards):
        constraints = [
            positions[top_card] == z3.BitVecVal(0, position_width)
        ]
        next_position = 1
        for index, card in enumerate(cards):
            if index == top_index:
                continue
            constraints.append(
                positions[card]
                == z3.BitVecVal(next_position, position_width)
            )
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
    selector_width: int,
) -> None:
    """Canonicalize interchangeable action labels not used by pinned text."""

    for index, selector in enumerate(unknown_selectors):
        for symbol in range(pinned_action_count + 1, action_count):
            prior = [
                earlier == z3.BitVecVal(symbol - 1, selector_width)
                for earlier in unknown_selectors[:index]
            ]
            solver.add(
                z3.Implies(
                    selector == z3.BitVecVal(symbol, selector_width),
                    z3.Or(*prior) if prior else z3.BoolVal(False),
                )
            )


def recover_explicit_permutation_gak(
    schedules: Sequence[Sequence[int | None]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    pinned_action_count: int = 0,
    timeout_ms: int = 30_000,
    break_position_symmetry: bool = True,
    break_extra_action_symmetry: bool = True,
) -> tuple[str, ExplicitPermutationGAKWitness | None]:
    """Recover a shared ordinary-GAK key and unknown schedule positions.

    The return status is ``sat``, ``unsat``, or ``unknown``.  Independent
    arbitrary initial decks are allowed for the supplied traces.
    """

    try:
        import z3  # type: ignore[import-not-found]
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("explicit permutation GAK recovery requires z3") from error

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
    position_width = max(1, deck_size.bit_length())
    selector_width = max(1, plaintext_alphabet_size.bit_length())
    position_sort = z3.BitVecSort(position_width)
    inverse_operations = [
        z3.Array(
            f"inverse_operation_{symbol}",
            position_sort,
            position_sort,
        )
        for symbol in range(plaintext_alphabet_size)
    ]
    for operation in inverse_operations:
        row = [
            z3.Select(operation, z3.BitVecVal(position, position_width))
            for position in range(deck_size)
        ]
        solver.add(z3.Distinct(*row))
        solver.add(
            *(
                z3.ULT(value, z3.BitVecVal(deck_size, position_width))
                for value in row
            )
        )

    initial_positions_by_trace: list[dict[int, Any]] = []
    selectors_by_trace: list[tuple[Any, ...]] = []
    unknown_selectors: list[Any] = []

    for trace_index, (schedule, ciphertext) in enumerate(
        zip(patterns, ciphers, strict=True)
    ):
        cards = tuple(sorted(set(ciphertext)))
        initial_positions = {
            card: z3.BitVec(
                f"initial_{trace_index}_{card}", position_width
            )
            for card in cards
        }
        solver.add(
            *(
                z3.ULT(
                    position,
                    z3.BitVecVal(deck_size, position_width),
                )
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
                position_width=position_width,
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
                selector = z3.BitVec(
                    f"plaintext_{trace_index}_{offset}",
                    selector_width,
                )
                solver.add(
                    z3.ULT(
                        selector,
                        z3.BitVecVal(
                            plaintext_alphabet_size, selector_width
                        ),
                    )
                )
                unknown_selectors.append(selector)
            else:
                selector = z3.BitVecVal(pinned, selector_width)
            selectors.append(selector)
            current: dict[int, Any] = {}
            for card in cards:
                if last_offset[card] < offset:
                    continue
                new_position = z3.BitVec(
                    f"position_{trace_index}_{offset}_{card}",
                    position_width,
                )
                solver.add(
                    new_position
                    == _selected_transition(
                        z3,
                        selector,
                        previous[card],
                        inverse_operations,
                        selector_width=selector_width,
                    )
                )
                current[card] = new_position
            solver.add(
                current[emitted] == z3.BitVecVal(0, position_width)
            )
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
            selector_width=selector_width,
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
    inverse_rows = tuple(
        tuple(
            model.eval(
                z3.Select(
                    operation,
                    z3.BitVecVal(position, position_width),
                ),
                model_completion=True,
            ).as_long()
            for position in range(deck_size)
        )
        for operation in inverse_operations
    )
    operations: list[tuple[int, ...]] = []
    for inverse in inverse_rows:
        forward = [0] * deck_size
        for old_position, new_position in enumerate(inverse):
            forward[new_position] = old_position
        operations.append(tuple(forward))
    initial_decks = tuple(
        _complete_deck_from_positions(
            model,
            positions,
            deck_size=deck_size,
        )
        for positions in initial_positions_by_trace
    )
    witness = ExplicitPermutationGAKWitness(
        initial_decks=initial_decks,
        operations=tuple(operations),
        plaintexts=plaintexts,
    )
    replay = tuple(
        encrypt_messages((plaintext,), deck, witness.operations)[0]
        for plaintext, deck in zip(
            witness.plaintexts, witness.initial_decks, strict=True
        )
    )
    if replay != ciphers:
        raise AssertionError("explicit permutation witness failed exact replay")
    return "sat", witness
