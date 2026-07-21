#!/usr/bin/env python3
"""Exact bounded-alphabet test for ``cipher_i = P**i(S[plain_i])``."""

from __future__ import annotations

import argparse

import z3

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values


SIZE = 83


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-symbols", type=int, default=26)
    parser.add_argument("--full-marker", action="store_true")
    parser.add_argument("--timeout-ms", type=int, default=300_000)
    parser.add_argument("--integer", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.max_symbols < SIZE:
        raise SystemExit("max-symbols must be in 1..82")

    if args.integer:
        value_sort = z3.IntSort()
        solver = z3.SolverFor("QF_AUFLIA")
        constant = z3.IntVal

        def bounded(value):
            return z3.And(0 <= value, value < SIZE)

        def increasing(left, right):
            return left < right

    else:
        value_sort = z3.BitVecSort(7)
        solver = z3.SolverFor("QF_AUFBV")

        def constant(value):
            return z3.BitVecVal(value, 7)

        def bounded(value):
            return z3.ULT(value, SIZE)

        def increasing(left, right):
            return z3.ULT(left, right)

    solver.set(timeout=args.timeout_ms)
    inverse = z3.Array("inverse", value_sort, value_sort)
    inverse_values = [z3.Select(inverse, index) for index in range(SIZE)]
    solver.add(*(bounded(value) for value in inverse_values))
    solver.add(z3.Distinct(*inverse_values))

    skip = 0 if args.full_marker else 1
    streams = {
        name: trigram_values(MESSAGES[name])[skip:] for name in MESSAGE_ORDER
    }
    maximum_position = max(len(stream) for stream in streams.values()) - 1

    identity = z3.Array("inverse_power_0", value_sort, value_sort)
    solver.add(*(z3.Select(identity, index) == index for index in range(SIZE)))
    inverse_powers = [identity]
    for position in range(1, maximum_position + 1):
        power = z3.Array(
            f"inverse_power_{position}", value_sort, value_sort
        )
        solver.add(
            *(
                z3.Select(power, symbol)
                == z3.Select(
                    inverse,
                    z3.Select(inverse_powers[position - 1], symbol),
                )
                for symbol in range(SIZE)
            )
        )
        inverse_powers.append(power)

    decoded = {
        (name, position): z3.Select(inverse_powers[position], symbol)
        for name, stream in streams.items()
        for position, symbol in enumerate(stream)
    }
    alphabet = [
        z3.Const(f"plain_symbol_{index}", value_sort)
        for index in range(args.max_symbols)
    ]
    solver.add(*(bounded(value) for value in alphabet))
    solver.add(
        *(
            increasing(alphabet[index], alphabet[index + 1])
            for index in range(len(alphabet) - 1)
        )
    )
    for value in decoded.values():
        solver.add(z3.Or(*(value == symbol for symbol in alphabet)))

    print(
        f"marker_mode={'full' if args.full_marker else 'reset'} "
        f"events={len(decoded)} powers={maximum_position + 1} "
        f"max_symbols={args.max_symbols} "
        f"logic={'QF_AUFLIA' if args.integer else 'QF_AUFBV'}",
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
        model.eval(z3.Select(inverse, index)).as_long()
        for index in range(SIZE)
    )
    resolved_alphabet = tuple(
        model.eval(value).as_long() for value in alphabet
    )
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
