#!/usr/bin/env python3
"""Exact bounded-alphabet AGL(1,83) test using bit-vector SAT.

The hidden transition is represented by 82 seven-bit table entries.  Shared
ciphertext prefixes are merged into a trie, and each table lookup is compiled
to a bit-vector multiplexer.  This avoids integer modular arithmetic and SMT
arrays while preserving the same unrestricted affine-GAK model.
"""

from __future__ import annotations

import argparse

import z3

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values


MODULUS = 83
EXPONENTS = 82
WIDTH = 7


def discrete_log_table(generator: int = 2) -> dict[int, int]:
    table: dict[int, int] = {}
    value = 1
    for exponent in range(EXPONENTS):
        table[value] = exponent
        value = value * generator % MODULUS
    if len(table) != EXPONENTS:
        raise ValueError(f"{generator} is not primitive modulo {MODULUS}")
    return table


def mode_parts(message: tuple[int, ...], mode: str):
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


def exponent_paths(mode: str) -> tuple[tuple[int, tuple[int, ...]], ...]:
    log = discrete_log_table()
    paths = []
    for name in MESSAGE_ORDER:
        message = trigram_values(MESSAGES[name])
        previous, initial_hidden, body = mode_parts(message, mode)
        differences = []
        for current in body:
            difference = (current - previous) % MODULUS
            if difference == 0:
                raise ValueError("affine GAK cannot encode adjacent doubles")
            differences.append(log[difference])
            previous = current
        initial = (differences[0] + log[initial_hidden]) % EXPONENTS
        deltas = tuple(
            (right - left) % EXPONENTS
            for left, right in zip(differences, differences[1:])
        )
        paths.append((initial, deltas))
    return tuple(paths)


def lookup(state: z3.BitVecRef, table: tuple[z3.BitVecRef, ...]) -> z3.BitVecRef:
    """Select a table entry; callers constrain ``state`` to 0..81."""
    result = table[-1]
    for index in range(EXPONENTS - 2, -1, -1):
        result = z3.If(state == index, table[index], result)
    return result


def add_mod_82(value: z3.BitVecRef, delta: int) -> z3.BitVecRef:
    wide = z3.ZeroExt(1, value) + z3.BitVecVal(delta, WIDTH + 1)
    reduced = z3.If(
        z3.UGE(wide, z3.BitVecVal(EXPONENTS, WIDTH + 1)),
        wide - EXPONENTS,
        wide,
    )
    return z3.Extract(WIDTH - 1, 0, reduced)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="skip")
    parser.add_argument("--max-symbols", type=int, default=27)
    parser.add_argument("--timeout-ms", type=int, default=300_000)
    parser.add_argument("--hidden-order", type=int, choices=(41, 82), default=82)
    args = parser.parse_args()
    if not 1 <= args.max_symbols <= EXPONENTS:
        parser.error("--max-symbols must be between 1 and 82")

    paths = exponent_paths(args.mode)
    solver = z3.SolverFor("QF_BV")
    solver.set(timeout=args.timeout_ms)
    upper = z3.BitVecVal(EXPONENTS, WIDTH)
    transition = tuple(z3.BitVec(f"transition_{index}", WIDTH) for index in range(EXPONENTS))
    solver.add(*(z3.ULT(value, upper) for value in transition))

    representatives = tuple(
        z3.BitVec(f"representative_{index}", WIDTH)
        for index in range(args.max_symbols)
    )
    solver.add(*(z3.ULT(value, upper) for value in representatives))
    solver.add(*(
        z3.ULT(left, right)
        for left, right in zip(representatives, representatives[1:])
    ))

    nodes: dict[tuple[int, tuple[int, ...]], z3.BitVecRef] = {}
    streams = []
    edges: dict[tuple[z3.BitVecRef, int, z3.BitVecRef], None] = {}
    for initial, deltas in paths:
        prefix: tuple[int, ...] = ()
        root_key = (initial, prefix)
        nodes.setdefault(root_key, z3.BitVecVal(initial, WIDTH))
        stream = [nodes[root_key]]
        for delta in deltas:
            source = nodes[(initial, prefix)]
            prefix += (delta,)
            key = (initial, prefix)
            if key not in nodes:
                nodes[key] = z3.BitVec(f"state_{len(nodes)}", WIDTH)
            target = nodes[key]
            edges[(source, delta, target)] = None
            stream.append(target)
        streams.append(tuple(stream))

    unique_states = tuple(dict.fromkeys(nodes.values()))
    symbolic_states = tuple(state for state in unique_states if not z3.is_bv_value(state))
    solver.add(*(z3.ULT(state, upper) for state in symbolic_states))
    for state in unique_states:
        solver.add(z3.Or(*(state == value for value in representatives)))

    selected: dict[z3.BitVecRef, z3.BitVecRef] = {}
    for source, delta, target in edges:
        if source not in selected:
            selected[source] = lookup(source, transition)
            if args.hidden_order == 41:
                solver.add(
                    z3.Extract(0, 0, selected[source])
                    == z3.Extract(0, 0, source)
                )
        solver.add(target == add_mod_82(selected[source], delta))

    print(
        f"checking BV mode={args.mode}, H={args.hidden_order}, "
        f"alphabet<={args.max_symbols}, "
        f"nodes={len(unique_states)}, edges={len(edges)}",
        flush=True,
    )
    outcome = solver.check()
    print(outcome)
    if outcome != z3.sat:
        if outcome == z3.unknown:
            print("reason:", solver.reason_unknown())
        return

    model = solver.model()
    realized = sorted({model.eval(state).as_long() for state in unique_states})
    print(f"realized alphabet: {len(realized)} states {realized}")
    print("transition base:")
    for state in realized:
        target = model.eval(transition[state]).as_long()
        print(f"  {state:>2}: {target:>2}")
    print("state streams:")
    for name, stream in zip(MESSAGE_ORDER, streams):
        decoded = [model.eval(state).as_long() for state in stream]
        print(f"{name:>5}: {' '.join(map(str, decoded))}")


if __name__ == "__main__":
    main()
