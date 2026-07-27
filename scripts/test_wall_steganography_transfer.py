#!/usr/bin/env python3
"""Run the frozen practice-steganography rule on Noita's Wall Messages."""

from __future__ import annotations

from itertools import groupby
from pathlib import Path

from eye_mystery.noita_wall_messages import load_wall_messages
from eye_mystery.wall_steganography import carrier_groups, decode_cover


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "artifacts" / "noita-wall-messages-en.txt"


def longest_alpha_run(text: str) -> int:
    return max(
        (len(tuple(run)) for is_alpha, run in groupby(text, str.isalpha) if is_alpha),
        default=0,
    )


def main() -> None:
    total_groups = 0
    total_valid = 0
    for map_id, text in load_wall_messages(CORPUS):
        groups = carrier_groups(text)
        decoded = decode_cover(text)
        valid = sum(group.decoded != "?" for group in groups)
        total_groups += len(groups)
        total_valid += valid
        print(
            f"{map_id:3s} words={sum(len(group.words) for group in groups):3d} "
            f"groups={len(groups):2d} valid={valid:2d} "
            f"longest={longest_alpha_run(decoded):2d} decode={decoded}"
        )
    print(
        f"TOTAL groups={total_groups} valid={total_valid} "
        f"invalid={total_groups - total_valid}"
    )


if __name__ == "__main__":
    main()
