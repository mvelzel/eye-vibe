#!/usr/bin/env python3
"""Test whether the nine panels are chunks of one continuous deck stream."""

from __future__ import annotations

import heapq
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.deck_base import decode_affine_base_swap
from search_standard_base_decks import mismatch_count


@dataclass(frozen=True)
class Result:
    mismatches: int
    unique: int
    rotation: int
    multiplier: int
    offset: int

    @property
    def key(self):
        return self.unique, self.mismatches


def split_stream(stream, order, lengths):
    result = {}
    position = 0
    for name in order:
        length = lengths[name]
        result[name] = tuple(stream[position : position + length])
        position += length
    return result


def main() -> None:
    messages = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    lengths = {name: len(message) for name, message in messages.items()}
    best: list[tuple[tuple[int, int], int, Result]] = []
    serial = 0
    for rotation in range(len(MESSAGE_ORDER)):
        order = MESSAGE_ORDER[rotation:] + MESSAGE_ORDER[:rotation]
        ciphertext = tuple(
            value for name in order for value in messages[name]
        )
        for multiplier in range(1, 83):
            for offset in range(83):
                decoded = decode_affine_base_swap(
                    ciphertext, multiplier, offset
                )
                streams = split_stream(decoded, order, lengths)
                mismatches, _ = mismatch_count(streams)
                result = Result(
                    mismatches,
                    len(set(decoded)),
                    rotation,
                    multiplier,
                    offset,
                )
                item = (
                    (-result.unique, -result.mismatches),
                    serial,
                    result,
                )
                serial += 1
                if len(best) < 30:
                    heapq.heappush(best, item)
                elif item > best[0]:
                    heapq.heapreplace(best, item)

    print(f"tested={serial}")
    print("unique mismatch start a b")
    for _, _, result in sorted(best, key=lambda item: item[2].key):
        print(
            f"{result.unique:>6} {result.mismatches:>8} "
            f"{MESSAGE_ORDER[result.rotation]:>5} "
            f"{result.multiplier:>2} {result.offset:>2}"
        )


if __name__ == "__main__":
    main()
