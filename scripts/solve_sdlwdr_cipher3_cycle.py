#!/usr/bin/env python3
"""Exact SAT test of fixed-cycle progressions for sdlwdr cipher #3.

Assigning ciphertext symbol ``s`` to offset ``c`` in a cycle makes an
occurrence at position ``i`` decode to offset ``(c-i) mod cycle_length`` in
that same cycle.  A permutation matrix assigns one slot to every symbol, while
83 Boolean variables mark the allowed decoded alphabet.  This avoids
materializing 215 symbolic permutation powers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import z3

from eye_mystery.permutation_progression import CycleLayout


SIZE = 83
ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-symbols", type=int, default=42)
    parser.add_argument("--cycle-lengths", default="83")
    parser.add_argument("--group", choices=("ALL", "A", "B", "C"), default="ALL")
    parser.add_argument("--skip-marker", action="store_true")
    parser.add_argument("--timeout-ms", type=int, default=120_000)
    args = parser.parse_args()
    cycle_lengths = tuple(map(int, args.cycle_lengths.split(",")))
    if any(length < 1 for length in cycle_lengths) or sum(cycle_lengths) != SIZE:
        raise SystemExit("cycle lengths must be positive and sum to 83")
    layout = CycleLayout(cycle_lengths)
    cycle_slots = []
    start = 0
    for length in cycle_lengths:
        slots = tuple(range(start, start + length))
        cycle_slots.append(slots)
        start += length

    data = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher3.json").read_text()
    )
    skip = int(args.skip_marker)
    streams = {
        f"{group}{index}": tuple(message[skip:])
        for group, messages in data.items()
        if args.group == "ALL" or group == args.group
        for index, message in enumerate(messages)
    }
    positions = [set() for _ in range(SIZE)]
    for stream in streams.values():
        for position, symbol in enumerate(stream):
            # Keep the true stream position.  Reducing modulo the complete
            # 83-slot alphabet is only valid for C83, not C82 or C41.
            positions[symbol].add(position)

    solver = z3.Solver()
    solver.set(timeout=args.timeout_ms)
    assignment = [
        [z3.Bool(f"cipher3_coordinate_{symbol}_{coordinate}") for coordinate in range(SIZE)]
        for symbol in range(SIZE)
    ]
    used = [z3.Bool(f"cipher3_plain_{value}") for value in range(SIZE)]

    for symbol in range(SIZE):
        solver.add(z3.PbEq([(item, 1) for item in assignment[symbol]], 1))
    for coordinate in range(SIZE):
        solver.add(
            z3.PbEq(
                [(assignment[symbol][coordinate], 1) for symbol in range(SIZE)],
                1,
            )
        )
    # Whichever cycle contains symbol 0 may be rotated to put it at offset 0.
    solver.add(z3.Or(*(assignment[0][slots[0]] for slots in cycle_slots)))
    solver.add(z3.PbLe([(item, 1) for item in used], args.max_symbols))

    for symbol in range(SIZE):
        for coordinate in range(SIZE):
            required = {
                layout.decode_slot(coordinate, position)
                for position in positions[symbol]
            }
            solver.add(
                z3.Implies(
                    assignment[symbol][coordinate],
                    z3.And(*(used[value] for value in required)),
                )
            )

    print(
        f"mode={'body' if args.skip_marker else 'full'} "
        f"events={sum(map(len, streams.values()))} "
        f"distinct-position constraints={sum(map(len, positions))} "
        f"max_symbols={args.max_symbols} cycles={cycle_lengths} group={args.group}",
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
    coordinates = tuple(
        next(
            coordinate
            for coordinate in range(SIZE)
            if z3.is_true(model.eval(assignment[symbol][coordinate]))
        )
        for symbol in range(SIZE)
    )
    alphabet = tuple(
        value for value in range(SIZE) if z3.is_true(model.eval(used[value]))
    )
    print("alphabet:", " ".join(map(str, alphabet)))
    print("coordinates:", " ".join(map(str, coordinates)))
    for name, stream in streams.items():
        values = []
        for position, symbol in enumerate(stream):
            values.append(layout.decode_slot(coordinates[symbol], position))
        print(f"{name}: {' '.join(map(str, values))}")


if __name__ == "__main__":
    main()
