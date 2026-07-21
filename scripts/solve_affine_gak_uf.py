#!/usr/bin/env python3
"""Exact bounded-alphabet AGL(1,83) test using an integer unary function.

This is equivalent to the array encodings in the other solver scripts, but it
shares literal ciphertext prefixes and lets Z3 reason about the unknown state
transition as an uninterpreted function.  It is intended as a faster decision
procedure for the question "can the decoded stream use at most K symbols?".
"""

from __future__ import annotations

import argparse

import z3

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values


MODULUS = 83
EXPONENTS = 82


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
    """Return each initial plaintext exponent and subsequent delta sequence."""
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
    solver = z3.SolverFor("QF_UFLIA")
    solver.set(timeout=args.timeout_ms)
    transition = z3.Function("transition", z3.IntSort(), z3.IntSort())
    representatives = [
        z3.Int(f"representative_{index}") for index in range(args.max_symbols)
    ]
    for representative in representatives:
        solver.add(0 <= representative, representative < EXPONENTS)
    solver.add(*(
        left < right for left, right in zip(representatives, representatives[1:])
    ))

    # A trie merges the long ciphertext prefixes shared by each message family.
    nodes: dict[tuple[int, tuple[int, ...]], z3.ArithRef] = {}
    streams = []
    edges: dict[tuple[z3.ArithRef, int, z3.ArithRef], None] = {}
    for initial, deltas in paths:
        prefix: tuple[int, ...] = ()
        root_key = (initial, prefix)
        nodes.setdefault(root_key, z3.IntVal(initial))
        stream = [nodes[root_key]]
        for delta in deltas:
            source = nodes[(initial, prefix)]
            prefix += (delta,)
            key = (initial, prefix)
            if key not in nodes:
                nodes[key] = z3.Int(f"state_{len(nodes)}")
            target = nodes[key]
            edges[(source, delta, target)] = None
            stream.append(target)
        streams.append(tuple(stream))

    unique_states = tuple(dict.fromkeys(nodes.values()))
    symbolic_states = tuple(state for state in unique_states if not z3.is_int_value(state))
    for state in symbolic_states:
        solver.add(0 <= state, state < EXPONENTS)
    for state in unique_states:
        solver.add(z3.Or(*(state == value for value in representatives)))
        solver.add(0 <= transition(state), transition(state) < EXPONENTS)
    for source, delta, target in edges:
        solver.add(target == (transition(source) + delta) % EXPONENTS)
        if args.hidden_order == 41:
            # Multipliers in C_41 have even discrete-log exponents, so the
            # transition base F(s)=s+log(u(s)) preserves exponent parity.
            solver.add(transition(source) % 2 == source % 2)

    print(
        f"checking UF mode={args.mode}, H={args.hidden_order}, "
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
        target = model.eval(transition(state), model_completion=True).as_long()
        print(f"  {state:>2}: {target:>2}")
    print("state streams:")
    for name, stream in zip(MESSAGE_ORDER, streams):
        decoded = [model.eval(state).as_long() for state in stream]
        print(f"{name:>5}: {' '.join(map(str, decoded))}")


if __name__ == "__main__":
    main()
