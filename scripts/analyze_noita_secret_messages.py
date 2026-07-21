#!/usr/bin/env python3
"""Measure whether the buried glyph texts supply Eye-like structure."""

from __future__ import annotations

from collections import Counter
from itertools import combinations

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.noita_secret_messages import (
    SECRET_MESSAGES,
    letters_only,
    words_only,
)


def longest_common_word_run(left: str, right: str) -> tuple[str, ...]:
    a = words_only(left).split()
    b = words_only(right).split()
    previous = [0] * (len(b) + 1)
    best_length = 0
    best_end = 0
    for left_index, left_word in enumerate(a, 1):
        current = [0] * (len(b) + 1)
        for right_index, right_word in enumerate(b, 1):
            if left_word == right_word:
                current[right_index] = previous[right_index - 1] + 1
                if current[right_index] > best_length:
                    best_length = current[right_index]
                    best_end = left_index
        previous = current
    return tuple(a[best_end - best_length : best_end])


def suffix_prefix_overlap(left: tuple[str, ...], right: tuple[str, ...]) -> int:
    for length in range(min(len(left), len(right)), 0, -1):
        if left[-length:] == right[:length]:
            return length
    return 0


def main() -> None:
    eye_lengths = {
        name: len(trigram_values(MESSAGES[name])) for name in MESSAGE_ORDER
    }
    print("Eye accepted-symbol lengths:")
    print(" ".join(f"{name}={length}" for name, length in eye_lengths.items()))
    print("\nBuried glyph-message lengths:")
    for name, text in SECRET_MESSAGES.items():
        print(
            f"  {name:>3} letters={len(letters_only(text)):>3} "
            f"words+spaces={len(words_only(text)):>3} words={len(words_only(text).split()):>3}"
        )

    all_letters = "".join(letters_only(text) for text in SECRET_MESSAGES.values())
    counts = Counter(all_letters)
    print("\nCombined letter census:")
    print(" ".join(f"{letter}:{counts[letter]}" for letter in "abcdefghijklmnopqrstuvwxyz"))
    print("missing:", "".join(letter for letter in "abcdefghijklmnopqrstuvwxyz" if not counts[letter]))

    repeated = []
    for left_name, right_name in combinations(SECRET_MESSAGES, 2):
        run = longest_common_word_run(
            SECRET_MESSAGES[left_name], SECRET_MESSAGES[right_name]
        )
        if len(run) >= 3:
            repeated.append((len(run), left_name, right_name, " ".join(run)))
    print("\nLongest inter-message exact word runs (at least three words):")
    for length, left_name, right_name, run in sorted(repeated, reverse=True):
        print(f"  {length:>2} {left_name}-{right_name}: {run}")

    tokenized = {
        name: tuple(words_only(text).split()) for name, text in SECRET_MESSAGES.items()
    }
    overlaps = []
    for left_name, right_name in combinations(SECRET_MESSAGES, 2):
        for source, target in ((left_name, right_name), (right_name, left_name)):
            length = suffix_prefix_overlap(tokenized[source], tokenized[target])
            if length:
                overlaps.append((length, source, target))
    print("\nDirected whole-message suffix/prefix overlaps:")
    if overlaps:
        for length, source, target in sorted(overlaps, reverse=True):
            print(f"  {length:>2} words {source}->{target}")
    else:
        print("  none, even at one word")


if __name__ == "__main__":
    main()
