#!/usr/bin/env python3
"""Measure the exact shared-operation GAK feasibility frontier on Eye prefixes."""

from __future__ import annotations

import argparse

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.unknown_gak_smt import solve_unknown_gak_messages_with_z3


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prefixes",
        nargs="+",
        type=int,
        default=(1, 2, 3, 4, 5),
    )
    parser.add_argument(
        "--operation-counts",
        nargs="+",
        type=int,
        default=(9, 26),
    )
    parser.add_argument("--timeout-ms", type=int, default=30_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    streams = tuple(
        trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    )
    for operation_count in args.operation_counts:
        for prefix_length in args.prefixes:
            result = solve_unknown_gak_messages_with_z3(
                tuple(stream[:prefix_length] for stream in streams),
                deck_size=83,
                operation_alphabet_size=operation_count,
                timeout_ms=args.timeout_ms,
            )
            print(
                f"k={operation_count:>2}",
                f"prefix={prefix_length:>3}",
                f"{result.status:>7}",
                f"{result.elapsed_seconds:>9.3f}s",
                f"{result.formula_bytes:>9} bytes",
                flush=True,
            )


if __name__ == "__main__":
    main()
