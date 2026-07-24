#!/usr/bin/env python3
"""Calibrate the symbolic unknown-plaintext GAK encoding before Eye use."""

from __future__ import annotations

from eye_mystery.unknown_gak import replay_unknown_gak
from eye_mystery.unknown_gak_smt import solve_unknown_gak_with_z3


def cards(text: str) -> tuple[int, ...]:
    return tuple(ord(symbol) - ord("A") for symbol in text)


def rotations(deck_size: int, count: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((position + shift) % deck_size for position in range(deck_size))
        for shift in range(1, count + 1)
    )


def report(label: str, ciphertext: tuple[int, ...], deck_size: int, operations: int) -> None:
    result = solve_unknown_gak_with_z3(
        ciphertext,
        deck_size=deck_size,
        operation_alphabet_size=operations,
        timeout_ms=30_000,
    )
    print(
        label,
        result.status,
        f"{result.elapsed_seconds:.6f}s",
        f"{result.formula_bytes} bytes",
    )
    if result.witness is not None:
        print("  plaintext:", result.witness.plaintext)
        print("  operation tops:", tuple(row[0] for row in result.witness.operations))


def main() -> None:
    report("four-card parent", cards("BCBDBCDA"), 4, 2)
    report("four-card orphan", cards("BCBDBCDAC"), 4, 2)
    report(
        "five-card constructed orphan",
        tuple(map(int, "13010212020")),
        5,
        2,
    )
    report(
        "six-card constructed orphan",
        tuple(map(int, "13023101020")),
        6,
        2,
    )

    for deck_size in (6, 8, 10, 12):
        operation_count = min(4, deck_size - 1)
        operations = rotations(deck_size, operation_count)
        plaintext = tuple(
            (position * position + 3 * position + 1) % operation_count
            for position in range(32)
        )
        ciphertext = replay_unknown_gak(
            plaintext,
            operations,
            deck_size=deck_size,
        )
        report(
            f"planted deck {deck_size}",
            ciphertext,
            deck_size,
            operation_count,
        )


if __name__ == "__main__":
    main()
