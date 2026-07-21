#!/usr/bin/env python3
"""Test an ASCII+32 keyword as the initial order of structured deck models."""

from __future__ import annotations

import argparse
import heapq
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.deck_base_generic import (
    build_base_orbit_tables,
    decode_base_top_swap_with_tables,
)
from eye_mystery.deck_shuffles import standard_base_candidates
from search_standard_base_decks import mismatch_count


@dataclass(frozen=True)
class Result:
    unique: int
    mismatches: int
    marker_mode: str
    base_name: str

    @property
    def key(self) -> tuple[int, int]:
        return self.unique, self.mismatches


def keyword_coordinates(keyword: str, size: int = 83) -> tuple[int, ...]:
    key_cards = []
    for character in keyword.upper():
        card = ord(character) - 32
        if not 0 <= card < size:
            raise ValueError("keyword must use the ASCII+32 eye alphabet")
        if card not in key_cards:
            key_cards.append(card)
    deck = key_cards + [card for card in range(size) if card not in key_cards]
    coordinates = [0] * size
    for coordinate, card in enumerate(deck):
        coordinates[card] = coordinate
    return tuple(coordinates)


def affine_bases(size: int = 83):
    for multiplier in range(1, size):
        for offset in range(size):
            yield (
                f"affine-{size}-{multiplier}-{offset}",
                tuple(
                    (multiplier * position + offset) % size
                    for position in range(size)
                ),
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", nargs="?", default="EXIT")
    parser.add_argument("--limit", type=int, default=30)
    args = parser.parse_args()

    messages = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    coordinates = keyword_coordinates(args.keyword)
    seen = set()
    best: list[tuple[tuple[int, int], int, Result]] = []
    serial = 0
    for base_name, base in (*affine_bases(), *standard_base_candidates(83)):
        if base in seen:
            continue
        seen.add(base)
        tables = build_base_orbit_tables(base, max(map(len, messages.values())))
        for reset_marker in (False, True):
            if reset_marker:
                streams = {
                    name: (None,)
                    + decode_base_top_swap_with_tables(
                        message[1:], tables, coordinates
                    )
                    for name, message in messages.items()
                }
                combined = tuple(
                    value
                    for stream in streams.values()
                    for value in stream[1:]
                )
            else:
                streams = {
                    name: decode_base_top_swap_with_tables(
                        message, tables, coordinates
                    )
                    for name, message in messages.items()
                }
                combined = tuple(
                    value for stream in streams.values() for value in stream
                )
            mismatches, _ = mismatch_count(streams)
            result = Result(
                len(set(combined)),
                mismatches,
                "reset" if reset_marker else "full",
                base_name,
            )
            item = ((-result.unique, -result.mismatches), serial, result)
            serial += 1
            if len(best) < args.limit:
                heapq.heappush(best, item)
            elif item > best[0]:
                heapq.heapreplace(best, item)

    print(f"keyword={args.keyword.upper()} bases={len(seen)} candidates={serial}")
    print("unique mismatch marker base")
    for _, _, result in sorted(best, key=lambda item: item[2].key):
        print(
            f"{result.unique:>6} {result.mismatches:>8} "
            f"{result.marker_mode:<5} {result.base_name}"
        )


if __name__ == "__main__":
    main()
