#!/usr/bin/env python3
"""Audit source-backed community cribs without treating compatibility as proof."""

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.isomorphs import pattern
from eye_mystery.known_plaintext import first_isomorphism_conflict


EAST1_WALL_CRIB = (
    "TO GAIN TRUE KNOWLEDGE, KNOW THIS: WHY ELSE WOULD YOU BE HERE? "
    "WHY ELSE WOULD YOU BE READING THIS?"
)


def occurrences(text: str, fragment: str) -> tuple[int, ...]:
    starts = []
    cursor = 0
    while True:
        cursor = text.find(fragment, cursor)
        if cursor < 0:
            return tuple(starts)
        starts.append(cursor)
        cursor += 1


def main() -> None:
    body = trigram_values(MESSAGES["east1"])[1:]
    print("East-1 body/candidate lengths:", len(body), len(EAST1_WALL_CRIB))
    conflict = first_isomorphism_conflict(
        {"east1": EAST1_WALL_CRIB},
        {"east1": body},
        min_length=2,
        max_length=40,
    )
    print("perfect-isomorphism conflict:", conflict)

    for fragment in (
        "WHY ELSE WOULD YOU BE",
        "ELSE WOULD YOU BE",
    ):
        starts = occurrences(EAST1_WALL_CRIB, fragment)
        print(repr(fragment), "positions=", starts)
        for start in starts:
            print(" ", start, pattern(body[start : start + len(fragment)]))

    print(
        "interpretation: compatible only; the same repeated-isomorph locations "
        "also admit other repeated plaintext labels (for example THAT WHICH)."
    )


if __name__ == "__main__":
    main()
