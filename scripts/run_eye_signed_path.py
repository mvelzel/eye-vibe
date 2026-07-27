#!/usr/bin/env python3
"""Run the frozen signed-path transfer on the Eye trigrams."""

from __future__ import annotations

import argparse

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.practice_cipher3_signed_path import (
    make_signed_path_plant,
    solve_signed_path,
)


def eye_streams() -> tuple[tuple[int, ...], ...]:
    return tuple(
        trigram_values(MESSAGES[name])
        for name in MESSAGE_ORDER
    )


def summarize(name: str, result: object) -> None:
    print(f"{name}: {result.status}")
    if result.status == "sat":
        print(
            f"  first map: orientation={result.orientation:+d} "
            f"offset={result.offset}; survivors={result.valid_candidates}"
        )
        for message_name, message in zip(
            MESSAGE_ORDER,
            result.plaintexts,
            strict=True,
        ):
            print(f"  {message_name}: {' '.join(map(str, message[:80]))}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase",
        choices=("control", "real", "both"),
        default="both",
    )
    args = parser.parse_args()
    streams = eye_streams()
    lengths = tuple(len(message) for message in streams)

    if args.phase in ("control", "both"):
        for mode in ("full", "primer"):
            plant, _, _ = make_signed_path_plant(lengths, mode)
            summarize(f"control {mode}", solve_signed_path(plant, mode))

    if args.phase in ("real", "both"):
        for mode in ("full", "primer"):
            summarize(f"real {mode}", solve_signed_path(streams, mode))


if __name__ == "__main__":
    main()
