#!/usr/bin/env python3
"""Classify the six first-family windows proposed as ``THAT WHICH``.

For a perfectly isomorphic cipher, equal plaintext strings must produce
ciphertext windows with the same equality pattern.  This script determines
how far the six observed windows remain in one isomorph class.  It does not
assume that the ciphertext pattern equals the plaintext's substitution
pattern, nor does it claim that ``THAT WHICH`` has been decrypted.
"""

from __future__ import annotations

from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.isomorphs import pattern


@dataclass(frozen=True)
class Window:
    message: str
    offset: int


WINDOWS = (
    Window("east1", 40),
    Window("east1", 68),
    Window("west1", 40),
    Window("west1", 70),
    Window("east2", 45),
    Window("east2", 80),
)

PAIRS = tuple((WINDOWS[index], WINDOWS[index + 1]) for index in range(0, 6, 2))


def equality_pattern(window: Window, *, left: int = 0, right: int) -> str:
    stream = trigram_values(MESSAGES[window.message])
    return pattern(stream[window.offset - left : window.offset + right])


def patterns(*, left: int = 0, right: int) -> tuple[str, ...]:
    return tuple(
        equality_pattern(window, left=left, right=right) for window in WINDOWS
    )


def common_right_prefix() -> int:
    limit = min(
        len(trigram_values(MESSAGES[window.message])) - window.offset
        for window in WINDOWS
    )
    for right in range(1, limit + 1):
        if len(set(patterns(right=right))) != 1:
            return right - 1
    return limit


def pair_right_prefix(first: Window, second: Window) -> int:
    first_stream = trigram_values(MESSAGES[first.message])
    second_stream = trigram_values(MESSAGES[second.message])
    limit = min(len(first_stream) - first.offset, len(second_stream) - second.offset)
    for right in range(1, limit + 1):
        if equality_pattern(first, right=right) != equality_pattern(
            second, right=right
        ):
            return right - 1
    return limit


def pair_maximal_context(first: Window, second: Window) -> tuple[int, int]:
    """Return the longest isomorphic context as ``(left, right)``."""

    first_stream = trigram_values(MESSAGES[first.message])
    second_stream = trigram_values(MESSAGES[second.message])
    max_left = min(first.offset, second.offset)
    max_right = min(
        len(first_stream) - first.offset,
        len(second_stream) - second.offset,
    )
    candidates: list[tuple[int, int, int]] = []
    for left in range(max_left + 1):
        for right in range(1, max_right + 1):
            if equality_pattern(
                first, left=left, right=right
            ) == equality_pattern(second, left=left, right=right):
                candidates.append((left + right, left, right))
    _, left, right = max(candidates)
    return left, right


def main() -> None:
    common = common_right_prefix()
    print(f"six-window common right prefix: {common}")
    for length in (10, 11, 18):
        values = patterns(right=length)
        print(f"length={length} classes={len(set(values))}")
        for window, value in zip(WINDOWS, values, strict=True):
            print(f"  {window.message}:{window.offset} {value}")
    for first, second in PAIRS:
        print(
            f"pair={first.message}:{first.offset}/{second.offset} "
            f"right={pair_right_prefix(first, second)} "
            f"context={pair_maximal_context(first, second)}"
        )
    print(
        "verdict: under perfect GAK/XGAK, one common plaintext can occupy all "
        "six windows for at most ten characters; an eleventh common character "
        "is contradicted"
    )


if __name__ == "__main__":
    main()
