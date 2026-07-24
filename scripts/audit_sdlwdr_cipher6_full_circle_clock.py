#!/usr/bin/env python3
"""Run the frozen full-Circle rotating-clock audit for Cipher #6."""

from __future__ import annotations

from pathlib import Path

from eye_mystery.practice_cipher6 import (
    full_circle_clock_audit,
    read_ciphertext,
    render_line,
)


ROOT = Path(__file__).resolve().parents[1]
CIPHERTEXT = ROOT / "artifacts/practice-sdlwdr/cipher6-revised.txt"


def main() -> None:
    results = full_circle_clock_audit(read_ciphertext(CIPHERTEXT))

    print(f"candidates={len(results)}")
    print("prefix low/total fraction distinct max initial schedule dir align base")
    for result in results[:30]:
        base = "one" if result.plus_one else "zero"
        print(
            f"{result.prefix_matches:>6} "
            f"{result.low_rank_count:>3}/{result.total:<3} "
            f"{result.low_rank_fraction:.6f} "
            f"{result.distinct:>8} {result.maximum:>3} "
            f"{result.initial_deck:<10} {result.schedule:<22} "
            f"{result.physical_direction:<3} {result.alignment_mode:<10} {base}"
        )
        print("  natural:", render_line(result.decoded[0])[:100])
        print("  altar:  ", render_line(result.decoded[0], altar=True)[:100])


if __name__ == "__main__":
    main()
