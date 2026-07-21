#!/usr/bin/env python3
"""Search text files for the Eye messages' exact repeat geometry."""

from __future__ import annotations

import argparse
import glob
from pathlib import Path

from eye_mystery.source_fingerprints import (
    extract_card_body,
    first_family_source_matches,
    gap_repeats,
    normalize_source,
    repeated_blocks,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--mode", choices=("letters", "spaces"), default="letters")
    parser.add_argument("--transliterate-finnish", action="store_true")
    parser.add_argument(
        "--html-card-body",
        action="store_true",
        help="extract only card-body prose from HTML pages",
    )
    parser.add_argument("--show-triples", type=int, default=0)
    parser.add_argument(
        "--show-context",
        type=int,
        default=0,
        help="show this many normalized characters around each first match",
    )
    args = parser.parse_args()
    files = []
    for pattern in args.paths:
        matches = (
            [Path(value) for value in sorted(glob.glob(pattern))]
            if any(character in pattern for character in "*?[")
            else [Path(pattern)]
        )
        files.extend(path for path in matches if path.is_file())
    texts = {}
    for path in files:
        source = path.read_text(errors="ignore")
        if args.html_card_body:
            source = extract_card_body(source)
        texts[str(path)] = normalize_source(
            source,
            args.mode,
            transliterate_finnish=args.transliterate_finnish,
        )
    print("files:", len(texts), "normalized characters:", sum(map(len, texts.values())))
    for length, gap in ((18, 30), (18, 35), (9, 28)):
        occurrences = sum(
            len(positions)
            for text in texts.values()
            for positions in gap_repeats(text, length=length, gap=gap).values()
        )
        print(f"length={length} gap={gap} repeat pairs={occurrences}")
    matches = first_family_source_matches(texts)
    print("complete first-family fingerprints:", len(matches))
    for match in matches:
        print(
            repr(match.block),
            "gap30=", len(match.gap30), match.gap30[:3],
            "gap35=", len(match.gap35), match.gap35[:3],
            "inner=", len(match.inner_gap28), match.inner_gap28[:3],
        )
        if args.show_context:
            for label, locations in (
                ("gap30", match.gap30),
                ("gap35", match.gap35),
                ("inner", match.inner_gap28),
            ):
                name, position = locations[0]
                radius = args.show_context
                print(
                    f"  {label}:",
                    texts[name][max(0, position - radius) : position + radius],
                )

    if args.show_triples:
        triples = repeated_blocks(texts, length=30, minimum_occurrences=3)
        ordered = sorted(
            triples.items(), key=lambda item: (-len(item[1]), item[0])
        )
        print("length-30 blocks occurring at least three times:", len(ordered))
        for block, positions in ordered[: args.show_triples]:
            print(len(positions), repr(block), positions[:5])


if __name__ == "__main__":
    main()
