#!/usr/bin/env python3
"""Check one Noita localization column as literal Eye plaintexts."""

from __future__ import annotations

import argparse
import csv

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.source_fingerprints import (
    first_family_source_matches,
    normalize_source,
)
from eye_mystery.source_message_tree import (
    SourceEntry,
    message_tree_matches,
    message_tree_partials,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("common_csv", help="path to Noita translations/common.csv")
    parser.add_argument("--column", type=int, default=1)
    parser.add_argument("--label", default="localization")
    parser.add_argument("--transliterate-finnish", action="store_true")
    args = parser.parse_args()

    texts = {}
    with open(args.common_csv, encoding="utf-8-sig", newline="") as handle:
        for row in csv.reader(handle):
            if len(row) > args.column and row[0] and row[args.column]:
                texts[row[0]] = row[args.column].replace("\\n", " ")

    target_lengths = {
        len(trigram_values(MESSAGES[name])) for name in MESSAGE_ORDER
    }
    print(f"{args.label} rows: {len(texts)}")
    for mode in ("letters", "spaces"):
        normalized = {
            key: normalize_source(
                value,
                mode,
                transliterate_finnish=args.transliterate_finnish,
            )
            for key, value in texts.items()
        }
        exact = sorted(
            (key, len(value))
            for key, value in normalized.items()
            if len(value) in target_lengths
        )
        matches = first_family_source_matches(normalized)
        entries = tuple(
            SourceEntry(key, value) for key, value in normalized.items()
        )
        trees = message_tree_matches(entries)
        partials = message_tree_partials(entries)
        print(f"{mode}: exact target lengths={len(exact)} {exact}")
        print(f"{mode}: complete first-family fingerprints={len(matches)}")
        print(f"{mode}: complete message trees={len(trees)}")
        print(
            f"{mode}: tree partials "
            f"upper24={len(partials.upper24)} "
            f"deep20={len(partials.deep20)} "
            f"nested9={len(partials.nested9)} "
            f"lower6={len(partials.lower6)} "
            f"roots={len(partials.roots)}"
        )


if __name__ == "__main__":
    main()
