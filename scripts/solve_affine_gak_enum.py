#!/usr/bin/env python3
"""Finite-enumeration SMT test for bounded-alphabet affine group autokey."""

from __future__ import annotations

import argparse

import z3

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values


def discrete_log_table(generator: int = 2) -> dict[int, int]:
    result = {}
    value = 1
    for exponent in range(82):
        result[value] = exponent
        value = value * generator % 83
    return result


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

    StateSort, values = z3.EnumSort("AffinePlainState", [f"s{i}" for i in range(82)])
    transition = z3.Array("transition", StateSort, StateSort)
    used = z3.Array("used", StateSort, z3.BoolSort())
    solver = z3.Solver()
    solver.set(timeout=args.timeout_ms)
    state_streams = []
    deltas_used = set()
    constraints = []

    for message_index, message in enumerate(messages):
        previous, initial_hidden, body = mode_parts(message, args.mode)
        differences = []
        for current in body:
            difference = (current - previous) % 83
            if difference == 0:
                raise ValueError("model cannot encode adjacent doubles")
            differences.append(log[difference])
            previous = current
        states = [
            z3.Const(f"t_{message_index}_{position}", StateSort)
            for position in range(len(body))
        ]
        state_streams.append(states)
        constraints.extend(z3.Select(used, state) for state in states)
        initial = (differences[0] + log[initial_hidden]) % 82
        constraints.append(states[0] == values[initial])
        for position in range(len(states) - 1):
            delta = (differences[position + 1] - differences[position]) % 82
            deltas_used.add(delta)
            # shift arrays are filled below after we know which deltas occur.
            constraints.append((states[position + 1], transition, states[position], delta))

    shifts = {}
    for delta in deltas_used:
        array = z3.Array(f"shift_{delta}", StateSort, StateSort)
        shifts[delta] = array
        for index, value in enumerate(values):
            solver.add(z3.Select(array, value) == values[(index + delta) % 82])

    for constraint in constraints:
        if isinstance(constraint, tuple):
            target, array, source, delta = constraint
            solver.add(target == z3.Select(shifts[delta], z3.Select(array, source)))
        else:
            solver.add(constraint)
    solver.add(
        z3.PbLe(
            [(z3.Select(used, value), 1) for value in values],
            args.max_symbols,
        )
    )

    print(
        f"checking enum mode={args.mode}, alphabet<={args.max_symbols}, "
        f"states={sum(map(len, state_streams))}, deltas={len(deltas_used)}",
        flush=True,
    )
    outcome = solver.check()
    print(outcome)
    if outcome != z3.sat:
        if outcome == z3.unknown:
            print("reason:", solver.reason_unknown())
        return
    model = solver.model()
    realized_names = {
        str(model.eval(state)) for stream in state_streams for state in stream
    }
    realized = sorted(int(name[1:]) for name in realized_names)
    print(f"realized alphabet: {len(realized)} states {realized}")
    print("transition base:")
    for state in realized:
        target = model.eval(z3.Select(transition, values[state]))
        print(f"  {state:>2}: {target}")
    print("state streams:")
    for name, stream in zip(MESSAGE_ORDER, state_streams):
        decoded = [int(str(model.eval(state))[1:]) for state in stream]
        print(f"{name:>5}: {' '.join(map(str, decoded))}")


if __name__ == "__main__":
    main()
