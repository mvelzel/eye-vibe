#!/usr/bin/env python3
"""Exact bounded-alphabet test for AGL(1,83) group autokey using Z3."""

from __future__ import annotations

import argparse

import z3

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values


def discrete_log_table(generator: int = 2) -> dict[int, int]:
    table = {}
    value = 1
    for exponent in range(82):
        table[value] = exponent
        value = value * generator % 83
    if len(table) != 82:
        raise ValueError(f"{generator} is not a primitive root modulo 83")
    return table


def mode_parts(message, mode):
    if mode == "full":
        return 0, 1, message
    if mode == "primer":
        return message[0], 1, message[1:]
    if mode == "skip":
        return 0, 1, message[1:]
    if mode == "indicator-hidden":
        return 0, message[0], message[1:]
    if mode == "indicator-both":
        return message[0], message[0], message[1:]
    raise ValueError(mode)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="skip")
    parser.add_argument("--max-symbols", type=int, default=27)
    parser.add_argument("--timeout-ms", type=int, default=300_000)
    args = parser.parse_args()
    log = discrete_log_table()
    messages = tuple(trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER)

    solver = z3.Solver()
    solver.set(timeout=args.timeout_ms)
    multipliers = z3.Array("multipliers", z3.IntSort(), z3.IntSort())
    representatives = [
        z3.Int(f"representative_{index}") for index in range(args.max_symbols)
    ]
    for representative in representatives:
        solver.add(representative >= 0, representative < 82)
        solver.add(z3.Select(multipliers, representative) >= 0)
        solver.add(z3.Select(multipliers, representative) < 82)
    for left, right in zip(representatives, representatives[1:]):
        solver.add(left < right)
    state_streams = []
    all_states = []

    for message_index, message in enumerate(messages):
        previous, initial_hidden, body = mode_parts(message, args.mode)
        differences = []
        for current in body:
            difference = (current - previous) % 83
            if difference == 0:
                raise ValueError("affine logarithm model cannot encode a double")
            differences.append(log[difference])
            previous = current
        states = [
            z3.Int(f"t_{message_index}_{position}")
            for position in range(len(body))
        ]
        state_streams.append(states)
        all_states.extend(states)
        for state in states:
            solver.add(state >= 0, state < 82)
            solver.add(z3.Or([state == value for value in representatives]))

        initial_exponent = log[initial_hidden]
        solver.add(states[0] == (differences[0] + initial_exponent) % 82)
        for position in range(len(states) - 1):
            delta = (differences[position + 1] - differences[position]) % 82
            outgoing = z3.Select(multipliers, states[position])
            solver.add(states[position + 1] == (states[position] + delta + outgoing) % 82)
    print(
        f"checking mode={args.mode}, alphabet<={args.max_symbols}, "
        f"constraints={len(all_states)} states"
    )
    outcome = solver.check()
    print(outcome)
    if outcome != z3.sat:
        if outcome == z3.unknown:
            print("reason:", solver.reason_unknown())
        return

    model = solver.model()
    realized = sorted(
        {
            model.eval(state).as_long()
            for state in all_states
        }
    )
    print(f"realized alphabet: {len(realized)} states {realized}")
    print("multiplier exponents:")
    for state in realized:
        print(f"  {state:>2}: {model.eval(z3.Select(multipliers, state)).as_long():>2}")
    print("state streams:")
    for name, stream in zip(MESSAGE_ORDER, state_streams):
        values = [model.eval(state).as_long() for state in stream]
        print(f"{name:>5}: {' '.join(map(str, values))}")


if __name__ == "__main__":
    main()
