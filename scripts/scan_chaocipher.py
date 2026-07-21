#!/usr/bin/env python3
"""Scan constrained 83-symbol generalizations of the historical Chaocipher."""

from __future__ import annotations

import heapq
from dataclasses import dataclass

from eye_mystery.chaocipher import decrypt
from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.metrics import index_of_coincidence
from search_standard_base_decks import mismatch_count


def keyword_alphabet(keyword: str, size: int = 83) -> tuple[int, ...]:
    front = []
    for character in keyword.upper():
        value = ord(character) - 32
        if not 0 <= value < size:
            raise ValueError("keyword is outside the ASCII+32 Eye alphabet")
        if value not in front:
            front.append(value)
    return tuple(front + [value for value in range(size) if value not in front])


@dataclass(frozen=True)
class Result:
    mismatches: int
    unique: int
    body_unique: int
    ioc: float
    marker_mode: str
    nadir: int
    left: str
    right: str

    @property
    def key(self) -> tuple[int, int, int, float]:
        return self.mismatches, self.body_unique, self.unique, -self.ioc


def main() -> None:
    historical_left = "HXUCZVAMDSLKPEFJRIGTWOBNYQ"
    historical_right = "PTLNBQDEOYSFAVZKGJRIHWXUMC"
    keywords = {
        "natural": "",
        "reverse": "",
        "historical-left": historical_left,
        "historical-right": historical_right,
        "noita-altar": "BDMAGICKEFHJLNOPQRSTUVWXYZ",
        "LUMIKKI": "LUMIKKI",
        "SNOWWHITE": "SNOWWHITE",
        "MAGICK": "MAGICK",
        "NOITA": "NOITA",
        "CESSATION": "CESSATION",
        "RUBEDO": "RUBEDO",
        "EXIT": "EXIT",
        "BEXIT": "BEXIT",
    }
    alphabets = {
        name: (
            tuple(reversed(range(83)))
            if name == "reverse"
            else keyword_alphabet(keyword)
        )
        for name, keyword in keywords.items()
    }
    messages = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    best: list[tuple[tuple[int, int, int, float], int, Result]] = []
    serial = 0
    tested = 0
    for left_name, left in alphabets.items():
        for right_name, right in alphabets.items():
            for nadir in (41, 42):
                for reset_marker in (False, True):
                    if reset_marker:
                        streams = {
                            name: (None,)
                            + decrypt(message[1:], left, right, nadir=nadir)
                            for name, message in messages.items()
                        }
                    else:
                        streams = {
                            name: decrypt(message, left, right, nadir=nadir)
                            for name, message in messages.items()
                        }
                    combined = tuple(
                        value
                        for stream in streams.values()
                        for value in stream
                        if value is not None
                    )
                    body = tuple(
                        value
                        for stream in streams.values()
                        for value in stream[1:]
                    )
                    mismatches, _ = mismatch_count(streams)
                    result = Result(
                        mismatches=mismatches,
                        unique=len(set(combined)),
                        body_unique=len(set(body)),
                        ioc=index_of_coincidence(combined, len(set(combined))),
                        marker_mode="reset" if reset_marker else "full",
                        nadir=nadir,
                        left=left_name,
                        right=right_name,
                    )
                    tested += 1
                    item = (tuple(-value for value in result.key), serial, result)
                    serial += 1
                    if len(best) < 30:
                        heapq.heappush(best, item)
                    elif item > best[0]:
                        heapq.heapreplace(best, item)

    print("alphabets:", len(alphabets), "candidates:", tested)
    print("mismatch unique body_unique ioc mode nadir left right")
    for _, _, result in sorted(best, key=lambda item: item[2].key):
        print(
            f"{result.mismatches:>8} {result.unique:>6} "
            f"{result.body_unique:>11} {result.ioc:>6.3f} "
            f"{result.marker_mode:<5} {result.nadir:>5} "
            f"{result.left} {result.right}"
        )


if __name__ == "__main__":
    main()
