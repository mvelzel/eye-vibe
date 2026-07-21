#!/usr/bin/env python3
"""Exact bounded-alphabet test for sdlwdr #3's progression hypothesis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import z3


SIZE = 83
ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-symbols", type=int, default=42)
    parser.add_argument("--skip-marker", action="store_true")
    parser.add_argument("--timeout-ms", type=int, default=300_000)
    args = parser.parse_args()
    if not 1 <= args.max_symbols < SIZE:
        raise SystemExit("max-symbols must be in 1..82")

    data = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher3.json").read_text()
    )
    skip = int(args.skip_marker)
    streams = {
        f"{group}{index}": tuple(message[skip:])
        for group, messages in data.items()
        for index, message in enumerate(messages)
    }

    value_sort = z3.BitVecSort(7)
    solver = z3.SolverFor("QF_AUFBV")
    solver.set(timeout=args.timeout_ms)

    def constant(value: int):
        return z3.BitVecVal(value, 7)

    def bounded(value):
        return z3.ULT(value, SIZE)

    inverse = z3.Array("cipher3_inverse", value_sort, value_sort)
    inverse_values = [z3.Select(inverse, constant(i)) for i in range(SIZE)]
    solver.add(*(bounded(value) for value in inverse_values))
    solver.add(z3.Distinct(*inverse_values))

    maximum_position = max(map(len, streams.values())) - 1
    identity = z3.Array("cipher3_inverse_power_0", value_sort, value_sort)
    solver.add(
        *(z3.Select(identity, constant(i)) == constant(i) for i in range(SIZE))
    )
    inverse_powers = [identity]
    for position in range(1, maximum_position + 1):
        power = z3.Array(
            f"cipher3_inverse_power_{position}", value_sort, value_sort
        )
        solver.add(
            *(
                z3.Select(power, constant(symbol))
                == z3.Select(
                    inverse,
                    z3.Select(inverse_powers[position - 1], constant(symbol)),
                )
                for symbol in range(SIZE)
            )
        )
        inverse_powers.append(power)

    decoded = {
        (name, position): z3.Select(
            inverse_powers[position], constant(symbol)
        )
        for name, stream in streams.items()
        for position, symbol in enumerate(stream)
    }
    alphabet = [
        z3.BitVec(f"cipher3_plain_symbol_{index}", 7)
        for index in range(args.max_symbols)
    ]
    solver.add(*(bounded(value) for value in alphabet))
    solver.add(
        *(
            z3.ULT(alphabet[index], alphabet[index + 1])
            for index in range(len(alphabet) - 1)
        )
    )
    for value in decoded.values():
        solver.add(z3.Or(*(value == symbol for symbol in alphabet)))

    print(
        f"mode={'body' if args.skip_marker else 'full'} "
        f"events={len(decoded)} powers={maximum_position + 1} "
        f"max_symbols={args.max_symbols}",
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
    resolved_inverse = tuple(
        model.eval(z3.Select(inverse, constant(i))).as_long()
        for i in range(SIZE)
    )
    resolved_alphabet = tuple(model.eval(value).as_long() for value in alphabet)
    print("alphabet:", " ".join(map(str, resolved_alphabet)))
    print("inverse:", " ".join(map(str, resolved_inverse)))
    for name, stream in streams.items():
        values = tuple(
            model.eval(decoded[name, position]).as_long()
            for position in range(len(stream))
        )
        print(f"{name}: {' '.join(map(str, values))}")


if __name__ == "__main__":
    main()
