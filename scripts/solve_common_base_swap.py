#!/usr/bin/env python3
"""Exact bounded-alphabet solver for an arbitrary common base plus top swap.

The model is ``apply B; swap(top, plaintext_position); emit top``.  ``B`` is
an unrestricted permutation of 83 positions.  An arbitrary initial deck order
is normalized, up to conjugacy, by choosing which observed card is initially
on top; the other coordinates can then be named canonically.
"""

from __future__ import annotations

import argparse

import z3

from eye_mystery.corpus import MESSAGES, trigram_values


SIZE = 83
FIRST_CONTEXT_SPECS = (
    ("west1", 34, "west1", 64, 18),
)
PREFIX_CONTEXT_SPECS = (
    ("east1", 1, "west1", 1, 24),
    ("east1", 1, "east2", 1, 24),
    ("west2", 1, "east3", 1, 5),
    ("west2", 1, "west3", 1, 5),
    ("east4", 1, "west4", 1, 20),
    ("east4", 1, "east5", 1, 20),
)
LAST_CONTEXT_SPECS = (
    ("east4", 68, "west4", 71, 30),
    ("east4", 68, "east5", 69, 30),
)


def relabel(card: int, top_label: int) -> int:
    if card == top_label:
        return 0
    if card == 0:
        return top_label
    return card


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-symbols", type=int, default=26)
    parser.add_argument("--top-label", type=int, default=0)
    parser.add_argument("--skip-marker", action="store_true")
    parser.add_argument("--timeout-ms", type=int, default=300_000)
    parser.add_argument("--logic")
    parser.add_argument("--integer", action="store_true")
    parser.add_argument(
        "--contexts",
        choices=("prefix", "first", "last", "combined", "all"),
        default="all",
    )
    parser.add_argument(
        "--restrict-anchor",
        action="store_true",
        help=(
            "require B(0) to avoid all markers and shared-prefix labels, "
            "as forced when markers are ordinary top-swap actions"
        ),
    )
    args = parser.parse_args()
    if not 1 <= args.max_symbols < SIZE:
        raise SystemExit("max-symbols must be in 1..82")
    if not 0 <= args.top_label < SIZE:
        raise SystemExit("top-label must be in 0..82")

    if args.integer:
        value_sort = z3.IntSort()
        logic = args.logic or "QF_AUFLIA"
        constant = z3.IntVal

        def bounded(value):
            return z3.And(0 <= value, value < SIZE)

        def increasing(left, right):
            return left < right

    else:
        value_sort = z3.BitVecSort(7)
        logic = args.logic or "QF_AUFBV"

        def constant(value):
            return z3.BitVecVal(value, 7)

        def bounded(value):
            return z3.ULT(value, SIZE)

        def increasing(left, right):
            return z3.ULT(left, right)

    solver = z3.SolverFor(logic)
    solver.set(timeout=args.timeout_ms)
    base_inverse = z3.Array("base_inverse", value_sort, value_sort)
    base = z3.Array("base", value_sort, value_sort)
    inverse_values = [z3.Select(base_inverse, index) for index in range(SIZE)]
    base_values = [z3.Select(base, index) for index in range(SIZE)]
    for values in (inverse_values, base_values):
        solver.add(*(bounded(value) for value in values))
        solver.add(z3.Distinct(*values))
    for index in range(SIZE):
        solver.add(
            z3.Select(base_inverse, z3.Select(base, index)) == index,
            z3.Select(base, z3.Select(base_inverse, index)) == index,
        )

    if args.contexts == "prefix":
        context_specs = PREFIX_CONTEXT_SPECS
    elif args.contexts == "first":
        context_specs = FIRST_CONTEXT_SPECS
    elif args.contexts == "last":
        context_specs = LAST_CONTEXT_SPECS
    elif args.contexts == "combined":
        context_specs = FIRST_CONTEXT_SPECS + LAST_CONTEXT_SPECS
    else:
        context_specs = (
            PREFIX_CONTEXT_SPECS
            + FIRST_CONTEXT_SPECS
            + LAST_CONTEXT_SPECS
        )
    required_ends: dict[str, int] = {}
    for left_name, left_start, right_name, right_start, length in context_specs:
        required_ends[left_name] = max(
            required_ends.get(left_name, 0), left_start + length
        )
        required_ends[right_name] = max(
            required_ends.get(right_name, 0), right_start + length
        )

    start = 1 if args.skip_marker else 0
    maximum_steps = max(end - start for end in required_ends.values())
    identity = z3.Array("identity", value_sort, value_sort)
    solver.add(*(z3.Select(identity, index) == index for index in range(SIZE)))
    inverse_powers = [identity]
    top_coordinates = [constant(0)]
    for step in range(1, maximum_steps + 1):
        power = z3.Array(
            f"base_inverse_power_{step}", value_sort, value_sort
        )
        solver.add(
            *(
                z3.Select(power, coordinate)
                == z3.Select(
                    base_inverse,
                    z3.Select(inverse_powers[step - 1], coordinate),
                )
                for coordinate in range(SIZE)
            )
        )
        inverse_powers.append(power)
        top_coordinates.append(
            z3.Select(base, top_coordinates[step - 1])
        )

    instructions: dict[tuple[str, int], z3.ArithRef] = {}
    final_states = {}
    for name, end in required_ends.items():
        raw = trigram_values(MESSAGES[name])
        cards = tuple(relabel(card, args.top_label) for card in raw[start:end])
        coordinate_of = identity
        card_at_coordinate = identity
        for step, card in enumerate(cards, start=1):
            original_index = start + step - 1
            card_coordinate = z3.Select(coordinate_of, card)
            position = z3.Select(inverse_powers[step], card_coordinate)
            instructions[name, original_index] = position
            top_coordinate = top_coordinates[step]
            top_card = z3.Select(card_at_coordinate, top_coordinate)
            coordinate_of = z3.Store(
                z3.Store(coordinate_of, top_card, card_coordinate),
                card,
                top_coordinate,
            )
            card_at_coordinate = z3.Store(
                z3.Store(card_at_coordinate, top_coordinate, card),
                card_coordinate,
                top_card,
            )
        final_states[name] = coordinate_of

    for left_name, left_start, right_name, right_start, length in context_specs:
        for offset in range(length):
            solver.add(
                instructions[left_name, left_start + offset]
                == instructions[right_name, right_start + offset]
            )

    if args.integer:
        alphabet = [
            z3.Int(f"plaintext_position_{i}") for i in range(args.max_symbols)
        ]
    else:
        alphabet = [
            z3.BitVec(f"plaintext_position_{i}", 7)
            for i in range(args.max_symbols)
        ]
    for value in alphabet:
        solver.add(bounded(value))
    solver.add(
        *(
            increasing(alphabet[index], alphabet[index + 1])
            for index in range(len(alphabet) - 1)
        )
    )
    forbidden = z3.Select(base_inverse, 0)
    if args.restrict_anchor:
        if args.skip_marker:
            raise SystemExit("anchor restriction requires markers in the model")
        blocked_labels = {
            trigram_values(MESSAGES[name])[0] for name in MESSAGES
        }
        for left_name, left_start, _, _, length in PREFIX_CONTEXT_SPECS[::2]:
            blocked_labels.update(
                trigram_values(MESSAGES[left_name])[
                    left_start : left_start + length
                ]
            )
        allowed_anchors = tuple(
            relabel(label, args.top_label)
            for label in range(SIZE)
            if label not in blocked_labels
        )
        solver.add(
            z3.Or(
                *(
                    z3.Select(base, 0) == constant(label)
                    for label in allowed_anchors
                )
            )
        )
        print(
            f"anchor candidates={len(allowed_anchors)}",
            flush=True,
        )
    for instruction in instructions.values():
        solver.add(z3.Or(*(instruction == value for value in alphabet)))
        solver.add(instruction != forbidden)

    print(
        f"top_label={args.top_label} skip_marker={args.skip_marker} "
        f"contexts={args.contexts} events={len(instructions)} "
        f"equalities={sum(s[-1] for s in context_specs)} "
        f"max_symbols={args.max_symbols} logic={logic}",
        flush=True,
    )
    outcome = solver.check()
    print(outcome)
    if outcome == z3.unknown:
        print("reason:", solver.reason_unknown())
        return
    if outcome == z3.unsat:
        return

    model = solver.model()
    resolved_alphabet = tuple(model.eval(value).as_long() for value in alphabet)
    resolved_base = tuple(
        model.eval(z3.Select(base, index)).as_long() for index in range(SIZE)
    )
    print("alphabet:", " ".join(map(str, resolved_alphabet)))
    print("base:", " ".join(map(str, resolved_base)))
    for name, end in required_ends.items():
        stream = tuple(
            model.eval(instructions[name, index]).as_long()
            for index in range(start, end)
        )
        print(f"{name}: {' '.join(map(str, stream))}")


if __name__ == "__main__":
    main()
