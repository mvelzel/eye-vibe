#!/usr/bin/env python3
"""Test visual row-pair resets in the common-base plus top-swap deck model."""

from __future__ import annotations

import heapq
from dataclasses import dataclass

from eye_mystery.corpus import (
    MESSAGE_ORDER,
    MESSAGES,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)
from eye_mystery.deck_base_generic import (
    build_base_orbit_tables,
    decode_base_top_swap_with_tables,
)
from eye_mystery.deck_shuffles import standard_base_candidates
from search_standard_base_decks import mismatch_count


@dataclass(frozen=True)
class Result:
    mismatches: int
    unique: int
    mode: str
    base: str

    @property
    def key(self) -> tuple[int, int]:
        return self.mismatches, self.unique


def split_message(message: tuple[int, ...], lengths: tuple[int, ...]):
    start = 0
    for length in lengths:
        yield message[start : start + length]
        start += length
    if start != len(message):
        raise ValueError("row-pair lengths do not cover the message")


def decode_rows(message, lengths, tables, *, drop_marker: bool):
    segments = tuple(split_message(message, lengths))
    if drop_marker:
        segments = (segments[0][1:],) + segments[1:]
        prefix = (None,)
    else:
        prefix = ()
    return prefix + tuple(
        value
        for segment in segments
        for value in decode_base_top_swap_with_tables(segment, tables)
    )


def main() -> None:
    messages = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    candidates = [("identity", tuple(range(83)))]
    candidates.extend(standard_base_candidates(83))
    best: list[tuple[tuple[int, int], int, Result]] = []
    serial = 0
    for base_name, base in candidates:
        tables = build_base_orbit_tables(base, 26)
        for drop_marker, mode in ((False, "rows"), (True, "body-rows")):
            streams = {
                name: decode_rows(
                    message,
                    ROW_PAIR_TRIGRAM_LENGTHS[name],
                    tables,
                    drop_marker=drop_marker,
                )
                for name, message in messages.items()
            }
            mismatches, comparisons = mismatch_count(streams)
            combined = tuple(
                value
                for stream in streams.values()
                for value in stream
                if value is not None
            )
            result = Result(mismatches, len(set(combined)), mode, base_name)
            item = (tuple(-value for value in result.key), serial, result)
            serial += 1
            if len(best) < 30:
                heapq.heappush(best, item)
            elif item > best[0]:
                heapq.heapreplace(best, item)

    print(
        f"tested: {len(candidates) * 2} "
        f"({len(candidates)} bases x 2 row-reset modes)"
    )
    print("context comparisons:", comparisons)
    print("mismatch unique mode base")
    for _, _, result in sorted(best, key=lambda item: item[2].key):
        print(
            f"{result.mismatches:>8} {result.unique:>6} "
            f"{result.mode:<9} {result.base}"
        )


if __name__ == "__main__":
    main()
