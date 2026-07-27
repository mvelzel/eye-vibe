#!/usr/bin/env python3
"""Reproduce the Wall Messages steganography practice solution."""

from __future__ import annotations

from pathlib import Path

from eye_mystery.wall_steganography import (
    carrier_groups,
    decode_cover,
    mismatches_against_plaintext,
)


ROOT = Path(__file__).resolve().parents[1]
COVER_PATH = ROOT / "artifacts" / "practice-wall-steganography.txt"
BIT_REPAIRS = {37: "-", 64: "."}
SOLUTION = (
    "VISIONS OF ETERNITY LIE AHEAD FULL OF HOPELESSNESS "
    "RUBEDO JUST OUT OF REACH"
)


def main() -> None:
    text = COVER_PATH.read_text(encoding="utf-8").strip()
    raw_groups = carrier_groups(text)
    raw = decode_cover(text)
    repaired = decode_cover(text, bit_overrides=BIT_REPAIRS)

    print("carrier words:", sum(len(group.words) for group in raw_groups))
    print("Morse groups:", len(raw_groups))
    print("raw decode:", raw)
    print("bit repairs:", BIT_REPAIRS)
    print("repaired decode:", repaired)
    print("minimal mismatch certificate:")
    for mismatch in mismatches_against_plaintext(text, SOLUTION):
        print(
            f"  group={mismatch.group_index} "
            f"plaintext={mismatch.plaintext} "
            f"word={mismatch.word.index}:{mismatch.word.text} "
            f"observed={mismatch.word.bit} expected={mismatch.expected_bit}"
        )
    print()
    for index, group in enumerate(
        carrier_groups(text, bit_overrides=BIT_REPAIRS),
        1,
    ):
        print(
            f"{index:2d} {group.decoded:1s} {group.code:4s} "
            f"{group.text}"
        )


if __name__ == "__main__":
    main()
