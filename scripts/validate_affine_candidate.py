#!/usr/bin/env python3
"""Measure whether the best affine-walk signal survives null-model tests."""

from __future__ import annotations

import argparse
import random
from collections.abc import Sequence
from dataclasses import dataclass

from eye_mystery.affine_walk import trace_affine_walk
from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.metrics import index_of_coincidence


CANDIDATE = {
    "generator": 1,
    "translation_pair": (1, 3),
    "center_mode": "negation",
    "up_order": (0, 1, 2),
    "down_order": (2, 0, 1),
}


@dataclass(frozen=True)
class Score:
    unique: int
    ioc: float
    even_unique: int
    even_ioc: float
    odd_unique: int
    odd_ioc: float


def decode_trigrams(values: Sequence[int]) -> tuple[int, ...]:
    """Turn the canonical 0..82 symbols back into three base-five eyes."""
    result: list[int] = []
    for value in values:
        result.extend((value // 25, value // 5 % 5, value % 5))
    return tuple(result)


def score(messages: Sequence[Sequence[int]]) -> Score:
    streams = [trace_affine_walk(message, **CANDIDATE) for message in messages]
    combined = tuple(value for stream in streams for value in stream)
    even = tuple(value for stream in streams for value in stream[::2])
    odd = tuple(value for stream in streams for value in stream[1::2])
    return Score(
        unique=len(set(combined)),
        ioc=index_of_coincidence(combined, len(set(combined))),
        even_unique=len(set(even)),
        even_ioc=index_of_coincidence(even, len(set(even))),
        odd_unique=len(set(odd)),
        odd_ioc=index_of_coincidence(odd, len(set(odd))),
    )


def shuffled_messages(rng: random.Random) -> tuple[tuple[int, ...], ...]:
    result = []
    for name in MESSAGE_ORDER:
        values = list(trigram_values(MESSAGES[name]))
        rng.shuffle(values)
        result.append(decode_trigrams(values))
    return tuple(result)


def uniform_messages(rng: random.Random) -> tuple[tuple[int, ...], ...]:
    result = []
    for name in MESSAGE_ORDER:
        length = len(MESSAGES[name]) // 3
        result.append(decode_trigrams([rng.randrange(83) for _ in range(length)]))
    return tuple(result)


def summarize(label: str, observed: Score, samples: Sequence[Score]) -> None:
    unique_hits = sum(item.unique <= observed.unique for item in samples)
    joint_hits = sum(
        item.unique <= observed.unique and item.ioc >= observed.ioc
        for item in samples
    )
    minimum = min(item.unique for item in samples)
    median = sorted(item.unique for item in samples)[len(samples) // 2]
    maximum_ioc = max(item.ioc for item in samples)
    denominator = len(samples) + 1
    print(f"{label} ({len(samples):,} trials)")
    print(f"  unique states: min/median = {minimum}/{median}")
    print(f"  maximum normalized IoC = {maximum_ioc:.4f}")
    print(
        "  P(unique <= observed) = "
        f"{(unique_hits + 1) / denominator:.6f} ({unique_hits} hits)"
    )
    print(
        "  P(unique <= observed and IoC >= observed) = "
        f"{(joint_hits + 1) / denominator:.6f} ({joint_hits} hits)"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20260720)
    args = parser.parse_args()
    rng = random.Random(args.seed)

    observed = score(tuple(MESSAGES[name] for name in MESSAGE_ORDER))
    print("Observed candidate")
    print(
        f"  all:  {observed.unique} states, IoC {observed.ioc:.4f}\n"
        f"  even: {observed.even_unique} states, IoC {observed.even_ioc:.4f}\n"
        f"  odd:  {observed.odd_unique} states, IoC {observed.odd_ioc:.4f}"
    )

    shuffled = [score(shuffled_messages(rng)) for _ in range(args.trials)]
    summarize("Within-message trigram shuffle", observed, shuffled)

    uniform = [score(uniform_messages(rng)) for _ in range(args.trials)]
    summarize("Independent uniform 0..82 symbols", observed, uniform)


if __name__ == "__main__":
    main()
