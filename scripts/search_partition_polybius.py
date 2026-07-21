#!/usr/bin/env python3
"""Test the two five-state sibling-delta tapes as Polybius coordinates."""

from __future__ import annotations

import argparse
import itertools
from collections import Counter
from dataclasses import dataclass
from math import log
from pathlib import Path

import numpy as np

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.snapshot_delta import partition_tape


ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
PERMUTATIONS = np.array(tuple(itertools.permutations(range(5))), dtype=np.int32)


@dataclass(frozen=True)
class SearchResult:
    score: float
    reverse_upper: int
    reverse_lower: int
    row_permutation: int
    column_permutation: int
    values: tuple[int, ...]


def train_table(text: str) -> np.ndarray:
    normalized = "".join(
        character
        for character in text.upper().replace("J", "I")
        if character in ALPHABET
    )
    counts = Counter(
        normalized[index : index + 4]
        for index in range(len(normalized) - 3)
    )
    total = sum(counts.values())
    table = np.full(25**4, log(0.05 / total))
    for gram, count in counts.items():
        code = 0
        for character in gram:
            code = 25 * code + ALPHABET.index(character)
        table[code] = log(count / total)
    return table


def best_polybius(
    upper: np.ndarray, lower: np.ndarray, table: np.ndarray
) -> SearchResult:
    best = SearchResult(float("-inf"), 0, 0, 0, 0, ())
    for reverse_upper, upper_ordered in enumerate((upper, upper[::-1])):
        for reverse_lower, lower_ordered in enumerate((lower, lower[::-1])):
            length = min(len(upper_ordered), len(lower_ordered))
            upper_used = upper_ordered[:length]
            lower_used = lower_ordered[:length]
            columns = PERMUTATIONS[:, lower_used]
            for row_index, row_permutation in enumerate(PERMUTATIONS):
                outputs = 5 * row_permutation[upper_used][None, :] + columns
                codes = (
                    (
                        (outputs[:, :-3] * 25 + outputs[:, 1:-2]) * 25
                        + outputs[:, 2:-1]
                    )
                    * 25
                    + outputs[:, 3:]
                )
                scores = table[codes].mean(axis=1)
                column_index = int(scores.argmax())
                score = float(scores[column_index])
                if score > best.score:
                    best = SearchResult(
                        score,
                        reverse_upper,
                        reverse_lower,
                        row_index,
                        column_index,
                        tuple(int(value) for value in outputs[column_index]),
                    )
    return best


def minimum_high_trigrams(tapes: tuple[np.ndarray, ...]) -> int:
    """Minimize base-five trigrams outside the canonical Eye range ``0..82``."""
    best = sum(len(tape) // 3 for tape in tapes)
    for permutation in PERMUTATIONS:
        for reverse in (0, 1):
            for offset in range(3):
                high = 0
                for tape in tapes:
                    ordered = tape[::-1] if reverse else tape
                    digits = permutation[ordered]
                    values = (
                        25 * digits[offset:-2:3]
                        + 5 * digits[offset + 1 : -1 : 3]
                        + digits[offset + 2 :: 3]
                    )
                    high += int((values > 82).sum())
                best = min(best, high)
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus", type=Path)
    parser.add_argument("--controls", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260721)
    args = parser.parse_args()

    streams = {
        name: trigram_values(MESSAGES[name])[1:] for name in MESSAGE_ORDER
    }
    upper = np.array(
        partition_tape(
            tuple(streams[name] for name in ("east1", "west1", "east2"))
        )[24:],
        dtype=np.int32,
    )
    lower = np.array(
        partition_tape(
            tuple(streams[name] for name in ("east4", "west4", "east5"))
        )[20:],
        dtype=np.int32,
    )
    table = train_table(args.corpus.read_text(errors="ignore"))
    observed = best_polybius(upper, lower, table)
    observed_high = minimum_high_trigrams((upper, lower))
    preview = "".join(ALPHABET[value] for value in observed.values)
    print(f"branch tape lengths          {len(upper)}, {len(lower)}")
    print(f"selected score              {observed.score:.12f}")
    print(
        "selected model              "
        f"reverse={observed.reverse_upper},{observed.reverse_lower} "
        f"permutations={observed.row_permutation},{observed.column_permutation}"
    )
    print(f"preview                     {preview}")
    print(f"best direct >82 trigrams     {observed_high}")

    randomizer = np.random.default_rng(args.seed)
    at_least = 0
    at_most_high = 0
    control_scores = []
    for _ in range(args.controls):
        control_upper = randomizer.permutation(upper)
        control_lower = randomizer.permutation(lower)
        score = best_polybius(control_upper, control_lower, table).score
        control_scores.append(score)
        at_least += score >= observed.score
        at_most_high += (
            minimum_high_trigrams((control_upper, control_lower)) <= observed_high
        )
    print(
        "control score range         "
        f"{min(control_scores):.12f}..{max(control_scores):.12f}"
    )
    print(f"selection-corrected upper    {(at_least + 1) / (args.controls + 1):.9f}")
    print(
        "direct-range lower tail     "
        f"{(at_most_high + 1) / (args.controls + 1):.9f}"
    )


if __name__ == "__main__":
    main()
