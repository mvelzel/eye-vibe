#!/usr/bin/env python3
"""Exhaust the absolute trigram-sum indexing proposal for Orb lore."""

from __future__ import annotations

import argparse
import heapq
from collections import Counter
from itertools import permutations
from pathlib import Path

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER
from eye_mystery.ngram import TetragramModel, tetragram_code
from eye_mystery.noita_lore import ORB_LORE_KEYS, absolute_sum_key
def encode_finnish(text: str) -> str:
    return text.translate(str.maketrans({"ä": "q", "ö": "x", "å": "z", "Ä": "Q", "Ö": "X", "Å": "Z"}))


def normalized_letters(text: str) -> str:
    return "".join(character for character in encode_finnish(text).upper() if "A" <= character <= "Z")


def train_model(paths: list[Path]) -> tuple[TetragramModel, str]:
    source = "\n".join(path.read_text(errors="ignore") for path in paths)
    normalized = normalized_letters(source)
    return TetragramModel.train(encode_finnish(source)), normalized


def sum_tetragrams(message: tuple[int, ...], mapping: tuple[int, ...]) -> Counter[tuple[int, int, int, int]]:
    sums = tuple(
        sum(mapping[value] for value in message[offset : offset + 3])
        for offset in range(0, len(message), 3)
    )
    return Counter(zip(sums, sums[1:], sums[2:], sums[3:]))


def key_window_codes(key: str, start: int) -> tuple[int, ...]:
    window = normalized_letters(key[start : start + 13])
    if len(window) != 13:
        raise ValueError("normalized key window changed length")
    return tuple(ord(character) - ord("A") for character in window)


def score_counts(
    model: TetragramModel,
    counts: Counter[tuple[int, int, int, int]],
    window: tuple[int, ...],
) -> float:
    return sum(
        count * model.log_probabilities[tetragram_code(tuple(window[index] for index in indices))]
        for indices, count in counts.items()
    )


def best_assignment(matrix: tuple[tuple[float, ...], ...]) -> tuple[float, tuple[int, ...]]:
    states = {0: (0.0, ())}
    for row in matrix:
        next_states = {}
        for mask, (score, assignment) in states.items():
            for key_index, value in enumerate(row):
                bit = 1 << key_index
                if mask & bit:
                    continue
                candidate = (score + value, assignment + (key_index,))
                old = next_states.get(mask | bit)
                if old is None or candidate[0] > old[0]:
                    next_states[mask | bit] = candidate
        states = next_states
    return states[(1 << len(matrix)) - 1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language-corpus", type=Path, action="append", required=True)
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()
    model, corpus = train_model(args.language_corpus)
    total_windows = sum(len(MESSAGES[name]) // 3 - 3 for name in MESSAGE_ORDER)
    reference = corpus[-(total_windows + 3 * len(MESSAGE_ORDER)) :]
    reference_counts = Counter(zip(reference, reference[1:], reference[2:], reference[3:]))
    reference_score = sum(
        count
        * model.log_probabilities[
            tetragram_code(tuple(ord(character) - ord("A") for character in letters))
        ]
        for letters, count in reference_counts.items()
    ) / max(1, sum(reference_counts.values()))

    best = []
    serial = 0
    natural = None
    minimum_key_length = min(len(key) for _, key in ORB_LORE_KEYS)
    for mapping in permutations(range(5)):
        counts = tuple(sum_tetragrams(MESSAGES[name], mapping) for name in MESSAGE_ORDER)
        for reverse in (False, True):
            keys = tuple((key[::-1] if reverse else key) for _, key in ORB_LORE_KEYS)
            for start in range(minimum_key_length - 12):
                windows = tuple(key_window_codes(key, start) for key in keys)
                matrix = tuple(
                    tuple(score_counts(model, row_counts, window) for window in windows)
                    for row_counts in counts
                )
                score, assignment = best_assignment(matrix)
                normalized_score = score / max(1, total_windows)
                item = (normalized_score, serial, mapping, reverse, start, assignment)
                serial += 1
                if mapping == tuple(range(5)) and not reverse and start == 0:
                    natural = item
                if len(best) < args.top:
                    heapq.heappush(best, item)
                elif item > best[0]:
                    heapq.heapreplace(best, item)

    print("mechanisms tested:", serial)
    print("held-in Finnish reference:", f"{reference_score:.4f}")
    if natural is not None:
        print("natural engine-values/start-zero score:", f"{natural[0]:.4f}")
    print("best candidates:")
    display = str.maketrans({"Q": "Ä", "X": "Ö", "Z": "Å"})
    for score, _, mapping, reverse, start, assignment in sorted(best, reverse=True):
        print(
            f"  score={score:.4f} mapping={mapping} reverse={reverse} "
            f"shared-start={start}"
        )
        for message_index, key_index in enumerate(assignment[:3]):
            message_name = MESSAGE_ORDER[message_index]
            key_name, raw_key = ORB_LORE_KEYS[key_index]
            key = raw_key[::-1] if reverse else raw_key
            preview = absolute_sum_key(
                MESSAGES[message_name],
                key,
                direction_values=mapping,
                start=start,
            )[:100]
            print(f"    {message_name} <- {key_name}: {preview.translate(display)}")


if __name__ == "__main__":
    main()
