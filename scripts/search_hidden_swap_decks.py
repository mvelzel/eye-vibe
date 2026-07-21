#!/usr/bin/env python3
"""Search standard bases plus a plaintext-selected non-top hidden swap."""

from __future__ import annotations

import argparse
import heapq
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.deck_base_generic import (
    build_base_orbit_tables,
    decode_base_top_swap_hidden_with_tables,
)
from eye_mystery.deck_shuffles import is_affine_mod_size, standard_base_candidates
from search_standard_base_decks import mismatch_count


REQUIRED_ENDS = {
    "east1": 77,
    "west1": 82,
    "east2": 92,
    "west2": 6,
    "east3": 6,
    "west3": 6,
    "east4": 98,
    "west4": 101,
    "east5": 99,
}


@dataclass(frozen=True)
class Result:
    mismatches: int
    unique: int
    name: str


def hidden_rule(kind: str, parameter: int):
    if kind == "ring":
        return lambda position, size: (
            1 + position % (size - 1),
            1 + (position + parameter) % (size - 1),
        )
    if kind == "anchor":
        return lambda position, size: (1, 1 + position % (size - 1))
    if kind == "mirror":
        return lambda position, size: (
            1 + position % (size - 1),
            1 + (-position - parameter) % (size - 1),
        )
    raise ValueError(kind)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--max-offset", type=int, default=12)
    parser.add_argument(
        "--marker-mode", choices=("full", "reset"), default="reset"
    )
    args = parser.parse_args()
    messages = {
        name: trigram_values(MESSAGES[name])[: REQUIRED_ENDS[name]]
        for name in MESSAGE_ORDER
    }
    variants = [("anchor", 0)] + [
        (kind, offset)
        for kind in ("ring", "mirror")
        for offset in range(1, args.max_offset + 1)
    ]
    best: list[tuple[int, int, Result]] = []
    tested = 0
    serial = 0
    for base_name, base in standard_base_candidates(83):
        if is_affine_mod_size(base):
            continue
        tables = build_base_orbit_tables(base, max(REQUIRED_ENDS.values()))
        for kind, parameter in variants:
            rule = hidden_rule(kind, parameter)
            if args.marker_mode == "reset":
                streams = {
                    name: (None,)
                    + decode_base_top_swap_hidden_with_tables(
                        message[1:], tables, rule
                    )
                    for name, message in messages.items()
                }
            else:
                streams = {
                    name: decode_base_top_swap_hidden_with_tables(
                        message, tables, rule
                    )
                    for name, message in messages.items()
                }
            mismatches, _ = mismatch_count(streams)
            unique = len(
                {
                    value
                    for stream in streams.values()
                    for value in stream
                    if value is not None
                }
            )
            result = Result(
                mismatches,
                unique,
                f"{base_name}+{kind}-{parameter}",
            )
            item = (-mismatches, serial, result)
            serial += 1
            tested += 1
            if len(best) < args.limit:
                heapq.heappush(best, item)
            elif item > best[0]:
                heapq.heapreplace(best, item)
    print(
        "models tested:", tested,
        "variants per base:", len(variants),
        "marker mode:", args.marker_mode,
    )
    print("mismatch unique name")
    for _, _, result in sorted(best, key=lambda item: item[2].mismatches):
        print(f"{result.mismatches:>8} {result.unique:>6} {result.name}")


if __name__ == "__main__":
    main()
