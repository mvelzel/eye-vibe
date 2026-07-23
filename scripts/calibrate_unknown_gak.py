#!/usr/bin/env python3
"""Reproduce the tiny ciphertext-only GAK orphan and scaling calibration."""

from __future__ import annotations

from eye_mystery.unknown_gak import (
    arbitrary_length_no_double_witness,
    minimum_operation_alphabet,
    recover_unknown_plaintext_bruteforce,
    replay_unknown_gak,
    top_changing_operation_count,
)
from math import comb


def cards(text: str) -> tuple[int, ...]:
    return tuple(ord(symbol) - ord("A") for symbol in text)


def main() -> None:
    for text in ("BCBDBCDA", "BCBDBCDAC"):
        result = recover_unknown_plaintext_bruteforce(
            cards(text),
            deck_size=4,
            operation_alphabet_size=2,
        )
        print(
            text,
            result.status,
            f"{result.operation_sets_checked}/{result.total_operation_sets}",
        )
        if result.witness is not None:
            print("  plaintext:", "".join("ab"[value] for value in result.witness.plaintext))
            print("  operations:", result.witness.operations)
            print(
                "  replay:",
                replay_unknown_gak(
                    result.witness.plaintext,
                    result.witness.operations,
                    deck_size=4,
                ),
            )

    for length in range(1, 10):
        prefix = cards("BCBDBCDAC"[:length])
        minimum, results = minimum_operation_alphabet(
            prefix,
            deck_size=4,
            maximum=3,
        )
        print(
            "prefix",
            length,
            "minimum",
            minimum,
            "statuses",
            tuple(result.status for result in results),
        )

    print("two-operation search-space growth")
    for deck_size in range(4, 9):
        operations = top_changing_operation_count(deck_size)
        print(deck_size, operations, comb(operations, 2))

    ciphertext, _ = arbitrary_length_no_double_witness(1_028, deck_size=83)
    print(
        "83-card one-operation no-double witness:",
        len(ciphertext),
        "symbols; doubles",
        sum(left == right for left, right in zip(ciphertext, ciphertext[1:])),
    )


if __name__ == "__main__":
    main()
