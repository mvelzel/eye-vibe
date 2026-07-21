#!/usr/bin/env python3
"""Known-plaintext analysis of sdlwdr practice ciphers #1 and #2."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CIPHER1 = json.loads(
    (ROOT / "artifacts/practice-sdlwdr/cipher1.json").read_text()
)
CIPHER2 = json.loads(
    (ROOT / "artifacts/practice-sdlwdr/cipher2.json").read_text()
)

# This is the recovered interleaving of the two 41-cycles.  Tilde denotes raw
# symbol 0 (the literal space) so the leading/trailing space stays visible.
COMBINED82 = r'''p>9iEZ81q-',D[].6f$0;<jl2Q7_kdP&`BLFng"5R^X:?V@OmG/+re~oUa=3)c\h!4YSKT*N(#HMbCW%IA'''
CYCLE1 = r'''pX9?E@8mq/'rD~]U6=$);\j!2Y7Kk*P(`HLbnW"IR'''
CYCLE2 = r'''#BMFCg%5A^>:iVZO1G-+,e[o.af30c<hl4QS_TdN&'''
EXCEPTIONAL_RAW = ord("J") - 32


def normalized_crawford_rune42(path: Path) -> str:
    source = path.read_text()
    heading = source.index("RUNE XLII.", source.index("RUNE XLII.") + 1)
    start = source.index("Wainamoinen, old and truthful,", heading)
    end = source.index("RUNE XLIII.", start)
    # The puzzle deletes punctuation rather than replacing it, then collapses
    # source whitespace.  This keeps SEAS and OER rather than SEA S and O ER.
    letters_and_whitespace = re.sub(r"[^A-Za-z\s]", "", source[start:end])
    return " ".join(letters_and_whitespace.upper().split())


def raw_to_coordinate(raw: int) -> int:
    symbol = "~" if raw == 0 else chr(raw + 32)
    return COMBINED82.index(symbol)


def align_first_message(source: str) -> tuple[tuple[int, ...], str]:
    ciphertext = tuple(raw for raw in CIPHER1[0] if raw != EXCEPTIONAL_RAW)
    plaintext = source[: len(ciphertext)]
    return tuple(map(raw_to_coordinate, ciphertext)), plaintext


def report_group_counts(label: str, values: list[int], plaintext: str) -> None:
    grouped: dict[str, set[int]] = defaultdict(set)
    for character, value in zip(plaintext, values, strict=True):
        grouped[character].add(value)
    counts = sorted((len(items), character, sorted(items)) for character, items in grouped.items())
    print(label, "max", max(count for count, _, _ in counts))
    for count, character, items in counts:
        print(f"  {character!r}: {count:2} {items[:16]}")


def main() -> None:
    if len(COMBINED82) != 82 or len(set(COMBINED82)) != 82:
        raise RuntimeError(
            f"bad recovered alphabet: length={len(COMBINED82)}, unique={len(set(COMBINED82))}"
        )
    source_path = Path("/private/tmp/kalevala-crawford.txt")
    if not source_path.exists():
        raise SystemExit("download Gutenberg 5186-0.txt to /private/tmp first")
    source = normalized_crawford_rune42(source_path)
    coordinates, plaintext = align_first_message(source)
    print("aligned plaintext length", len(plaintext))
    print("plaintext prefix", plaintext[:80])
    print("ciphertext-coordinate prefix", coordinates[:20])
    print(
        "combined cycle memberships",
        "".join("1" if symbol in CYCLE1 else "2" for symbol in COMBINED82),
    )
    print(
        "combined internal positions",
        tuple(
            CYCLE1.index(symbol) if symbol in CYCLE1 else CYCLE2.index(symbol)
            for symbol in COMBINED82
        ),
    )

    differences82 = [coordinates[0]] + [
        (right - left) % 82
        for left, right in zip(coordinates, coordinates[1:], strict=False)
    ]
    report_group_counts("absolute coordinate", list(coordinates), plaintext)
    report_group_counts("adjacent delta mod82", differences82, plaintext)
    report_group_counts(
        "adjacent delta mod41", [value % 41 for value in differences82], plaintext
    )


if __name__ == "__main__":
    main()
