#!/usr/bin/env python3
"""Calibrate Waite's three-gap phrase fingerprint on control books.

The reference and control texts receive the same OCR/whitespace normalization.
For each corpus, the script finds the longest literal string occurring twice
at every one of the fixed gaps 28, 30, and 35.  It reports individual controls
and non-overlapping control blocks matched to the reference's total size.

This measures source-text rarity only.  It does not estimate the probability
that the Eye ciphertext positions, reading order, or source were selected.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

try:
    from scripts.search_waite_that_which import (
        TARGET_GAPS,
        maximal_common_gap_strings,
        normalize_ocr,
    )
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from search_waite_that_which import (
        TARGET_GAPS,
        maximal_common_gap_strings,
        normalize_ocr,
    )


@dataclass(frozen=True)
class Fingerprint:
    name: str
    characters: int
    length: int
    strings: tuple[str, ...]


def fingerprint(name: str, texts: tuple[str, ...], limit: int) -> Fingerprint:
    length, strings = maximal_common_gap_strings(
        texts, TARGET_GAPS, limit=limit
    )
    return Fingerprint(
        name,
        sum(map(len, texts)),
        length,
        tuple(sorted(strings)),
    )


def matched_blocks(
    texts: tuple[str, ...],
    size: int,
) -> tuple[str, ...]:
    if size < 1:
        raise ValueError("block size must be positive")
    joined_parts: list[str] = []
    for index, text in enumerate(texts):
        joined_parts.extend((text, chr(0xE000 + index)))
    joined = "".join(joined_parts)
    return tuple(
        joined[start : start + size]
        for start in range(0, len(joined) - size + 1, size)
    )


def render(item: Fingerprint) -> str:
    preview = item.strings[:5]
    return (
        f"{item.name}: characters={item.characters} "
        f"length={item.length} strings={preview!r}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reference",
        action="append",
        required=True,
        type=Path,
        help="reference text; repeat for multiple volumes",
    )
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("controls", nargs="+", type=Path)
    args = parser.parse_args()

    references = tuple(
        normalize_ocr(path.read_text(errors="replace"))
        for path in args.reference
    )
    controls = tuple(
        normalize_ocr(path.read_text(errors="replace"))
        for path in args.controls
    )
    reference = fingerprint("reference", references, args.limit)
    print(render(reference))

    individual: list[Fingerprint] = []
    for path, text in zip(args.controls, controls, strict=True):
        item = fingerprint(path.name, (text,), args.limit)
        individual.append(item)
        print(render(item))

    blocks = matched_blocks(controls, reference.characters)
    matched = tuple(
        fingerprint(f"matched-{index:02d}", (block,), args.limit)
        for index, block in enumerate(blocks, start=1)
    )
    for item in matched:
        print(render(item))
    print(
        f"individual-at-least-reference="
        f"{sum(item.length >= reference.length for item in individual)}"
        f"/{len(individual)}"
    )
    print(
        f"matched-at-least-reference="
        f"{sum(item.length >= reference.length for item in matched)}"
        f"/{len(matched)}"
    )


if __name__ == "__main__":
    main()
