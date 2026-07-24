#!/usr/bin/env python3
"""Run the frozen custom-Alberti ciphertext-autokey audit for Cipher #6."""

from __future__ import annotations

from pathlib import Path

from eye_mystery.practice_cipher6 import (
    ciphertext_autokey_audit,
    read_ciphertext,
    render_line,
)


ROOT = Path(__file__).resolve().parents[1]
CIPHERTEXT = ROOT / "artifacts/practice-sdlwdr/cipher6-revised.txt"


def main() -> None:
    results = ciphertext_autokey_audit(read_ciphertext(CIPHERTEXT))

    print(f"candidates={len(results)}")
    print("prefix low/total fraction distinct max initial source align base cut details")
    for result in results[:30]:
        base = "one" if result.one_based else "zero"
        details = ""
        if result.key_source == "asset-tape":
            symbols = "append" if result.appended_nonletters else "literal"
            details = (
                f"{result.binary_direction}/{result.value_alphabet}/{symbols}"
            )
        print(
            f"{result.prefix_matches:>6} "
            f"{result.low_rank_count:>3}/{result.total:<3} "
            f"{result.low_rank_fraction:.6f} "
            f"{result.distinct:>8} {result.maximum:>3} "
            f"{result.initial_deck:<10} {result.key_source:<10} "
            f"{result.alignment_mode:<10} {base:<4} "
            f"{result.cut_direction:<5} {details}"
        )
        print("  natural:", render_line(result.decoded[0])[:100])
        print("  altar:  ", render_line(result.decoded[0], altar=True)[:100])


if __name__ == "__main__":
    main()
