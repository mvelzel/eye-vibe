#!/usr/bin/env python3
"""Search physical deck shuffles as a common base plus one top swap."""

from __future__ import annotations

import argparse
import heapq
from collections import Counter
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.deck_base_generic import (
    build_base_orbit_tables,
    decode_base_top_swap_with_tables,
)
from eye_mystery.deck_shuffles import is_affine_mod_size, standard_base_candidates
from eye_mystery.metrics import index_of_coincidence


@dataclass(frozen=True)
class Result:
    name: str
    marker_mode: str
    mismatches: int
    comparisons: int
    unique: int
    skip_unique: int
    ioc: float

    @property
    def key(self) -> tuple[int, int, int, float]:
        return (self.mismatches, self.skip_unique, self.unique, -self.ioc)


def mismatch_count(streams: dict[str, tuple[int, ...]]) -> tuple[int, int]:
    comparisons: list[tuple[tuple[int, ...], tuple[int, ...]]] = []

    def compare(anchor_name, anchor_start, other_name, other_start, length):
        comparisons.append(
            (
                streams[anchor_name][anchor_start : anchor_start + length],
                streams[other_name][other_start : other_start + length],
            )
        )

    for anchor, others, length in (
        ("east1", ("west1", "east2"), 24),
        ("west2", ("east3", "west3"), 5),
        ("east4", ("west4", "east5"), 20),
    ):
        for other in others:
            compare(anchor, 1, other, 1, length)
    for other_name, other_start in (
        ("west1", 64),
        ("east2", 39),
        ("east2", 74),
    ):
        compare("west1", 34, other_name, other_start, 18)
    for other_start in (40, 68):
        compare("west1", 40, "east1", other_start, 9)
    for other_name, other_start in (("west4", 71), ("east5", 69)):
        compare("east4", 68, other_name, other_start, 30)

    total = sum(len(left) for left, _ in comparisons)
    mismatches = sum(
        left_value != right_value
        for left, right in comparisons
        for left_value, right_value in zip(left, right, strict=True)
    )
    return mismatches, total


def evaluate(name, base, messages, *, reset_marker: bool) -> Result:
    tables = build_base_orbit_tables(base, max(map(len, messages.values())))
    if reset_marker:
        streams = {
            message_name: (None,)
            + decode_base_top_swap_with_tables(message[1:], tables)
            for message_name, message in messages.items()
        }
        combined = tuple(
            value for stream in streams.values() for value in stream[1:]
        )
        skipped = combined
    else:
        streams = {
            message_name: decode_base_top_swap_with_tables(message, tables)
            for message_name, message in messages.items()
        }
        combined = tuple(value for stream in streams.values() for value in stream)
        skipped = tuple(
            value for stream in streams.values() for value in stream[1:]
        )
    mismatches, comparisons = mismatch_count(streams)
    unique = len(set(combined))
    return Result(
        name,
        "reset" if reset_marker else "full",
        mismatches,
        comparisons,
        unique,
        len(set(skipped)),
        index_of_coincidence(combined, unique),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument(
        "--include-affine-83",
        action="store_true",
        help="retain standard shuffles that duplicate the prior affine scan",
    )
    args = parser.parse_args()
    messages = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    best: list[tuple[tuple[int, int, int, float], int, Result]] = []
    families: Counter[str] = Counter()
    affine_duplicates = 0
    tested = 0
    serial = 0
    for name, base in standard_base_candidates(83):
        if is_affine_mod_size(base) and not args.include_affine_83:
            affine_duplicates += 1
            continue
        family = name.split("-", 1)[0]
        families[family] += 1
        for reset_marker in (False, True):
            result = evaluate(
                name, base, messages, reset_marker=reset_marker
            )
            tested += 1
            # Keep a max heap by negating the lexicographic quality tuple.
            heap_key = tuple(-value for value in result.key)
            item = (heap_key, serial, result)
            serial += 1
            if len(best) < args.limit:
                heapq.heappush(best, item)
            elif item > best[0]:
                heapq.heapreplace(best, item)

    print("tested:", tested, "affine-83 duplicates skipped:", affine_duplicates)
    print("families:", dict(families))
    print("mismatch comparisons per candidate:", best[0][2].comparisons if best else 0)
    print("mismatch unique skip_unique ioc marker name")
    for _, _, result in sorted(best, key=lambda item: item[2].key):
        print(
            f"{result.mismatches:>8} {result.unique:>6} "
            f"{result.skip_unique:>11} {result.ioc:>6.3f} "
            f"{result.marker_mode:<6} {result.name}"
        )


if __name__ == "__main__":
    main()
