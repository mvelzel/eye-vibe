#!/usr/bin/env python3
"""Run the frozen exact signed-path test for practice Cipher 3."""

from __future__ import annotations

import argparse

from eye_mystery.practice_cipher3_signed_path import (
    flatten_groups,
    make_signed_path_plant,
    solve_signed_path,
)
from eye_mystery.practice_cipher3_wide import load_cipher3


def summarize(name: str, result: object) -> None:
    status = result.status
    print(f"{name}: {status}")
    if status == "sat":
        print(
            f"  first map: orientation={result.orientation:+d} "
            f"offset={result.offset}; survivors={result.valid_candidates}"
        )
        supports = tuple(len(set(message)) for message in result.plaintexts)
        print(f"  plaintext supports: {supports}")
        for index, message in enumerate(result.plaintexts[:3]):
            print(f"  message {index}: {' '.join(map(str, message[:60]))}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase",
        choices=("control", "real", "both"),
        default="both",
    )
    args = parser.parse_args()

    real = flatten_groups(load_cipher3())
    lengths = tuple(len(message) for message in real)

    if args.phase in ("control", "both"):
        for mode in ("full", "primer"):
            plant, _, _ = make_signed_path_plant(lengths, mode)
            summarize(
                f"control {mode}",
                solve_signed_path(plant, mode),
            )

    if args.phase in ("real", "both"):
        for mode in ("full", "primer"):
            summarize(
                f"real {mode}",
                solve_signed_path(real, mode),
            )


if __name__ == "__main__":
    main()
