#!/usr/bin/env python3
"""Solve sdlwdr #4 after reducing its cyclic deck to substitutions.

For a cyclic deck, the first ciphertext value and each following modular
difference are the fixed rotation selected by one plaintext character.  The
published sample uses 53 such rotations.  A natural explanation for exactly
53 used symbols is the straightforward PTA ``A-Z a-z space``.  This turns the
result into an ordinary 53-symbol substitution cipher.

This program solves that reduced problem with incremental case-sensitive
tetragram simulated annealing.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from math import exp, log
from pathlib import Path
import random
import string
from typing import Iterable


MODULUS = 83
PTA = string.ascii_uppercase + string.ascii_lowercase + " "
SPACE = len(PTA) - 1
ROOT = Path(__file__).resolve().parents[1]


def normalize(text: str) -> tuple[int, ...]:
    result: list[int] = []
    in_space = True
    for character in text:
        if character in string.ascii_letters:
            result.append(PTA.index(character))
            in_space = False
        elif not in_space:
            result.append(SPACE)
            in_space = True
    if result and result[-1] == SPACE:
        result.pop()
    return tuple(result)


def rotation_stream(message: Iterable[int]) -> tuple[int, ...]:
    values = tuple(message)
    if not values:
        return ()
    return (values[0],) + tuple(
        (right - left) % MODULUS for left, right in zip(values, values[1:])
    )


def train_tetragrams(text: str) -> tuple[dict[tuple[int, ...], float], float]:
    values = normalize(text)
    counts = Counter(values[index : index + 4] for index in range(len(values) - 3))
    total = sum(counts.values())
    return (
        {gram: log(count / total) for gram, count in counts.items()},
        log(0.01 / total),
    )


def render(values: Iterable[int]) -> str:
    return "".join(PTA[value] for value in values)


class Annealer:
    def __init__(
        self,
        streams: tuple[tuple[int, ...], ...],
        scores: dict[tuple[int, ...], float],
        floor: float,
        space_symbol: int,
        rng: random.Random,
    ) -> None:
        self.streams = streams
        self.scores = scores
        self.floor = floor
        self.space_symbol = space_symbol
        self.rng = rng
        self.symbols = sorted({value for stream in streams for value in stream})
        if len(self.symbols) != 53:
            raise ValueError(f"expected 53 used rotations, found {len(self.symbols)}")
        if space_symbol not in self.symbols:
            raise ValueError("space candidate is not a used rotation")

        self.positions: dict[int, list[tuple[int, int]]] = defaultdict(list)
        for stream_index, stream in enumerate(streams):
            for position, symbol in enumerate(stream):
                self.positions[symbol].append((stream_index, position))

    def random_key(self) -> list[int]:
        nonspace = [symbol for symbol in self.symbols if symbol != self.space_symbol]
        labels = list(range(SPACE))
        self.rng.shuffle(labels)
        key = [-1] * MODULUS
        key[self.space_symbol] = SPACE
        for symbol, label in zip(nonspace, labels):
            key[symbol] = label
        return key

    def decode(self, key: list[int]) -> list[list[int]]:
        return [[key[symbol] for symbol in stream] for stream in self.streams]

    def gram_score(self, decoded: list[list[int]], stream: int, start: int) -> float:
        values = decoded[stream]
        if start < 0 or start + 4 > len(values):
            return 0.0
        return self.scores.get(tuple(values[start : start + 4]), self.floor)

    def total_score(self, decoded: list[list[int]]) -> float:
        return sum(
            self.gram_score(decoded, stream, start)
            for stream, values in enumerate(decoded)
            for start in range(len(values) - 3)
        )

    def affected_starts(self, left: int, right: int) -> set[tuple[int, int]]:
        starts: set[tuple[int, int]] = set()
        for symbol in (left, right):
            for stream, position in self.positions[symbol]:
                for start in range(position - 3, position + 1):
                    if 0 <= start <= len(self.streams[stream]) - 4:
                        starts.add((stream, start))
        return starts

    def run(self, iterations: int, start_temperature: float) -> tuple[float, list[int]]:
        key = self.random_key()
        decoded = self.decode(key)
        score = self.total_score(decoded)
        best_score = score
        best_key = key.copy()
        movable = [symbol for symbol in self.symbols if symbol != self.space_symbol]

        for iteration in range(iterations):
            left, right = self.rng.sample(movable, 2)
            affected = self.affected_starts(left, right)
            before = sum(self.gram_score(decoded, stream, start) for stream, start in affected)
            key[left], key[right] = key[right], key[left]
            for stream, position in self.positions[left]:
                decoded[stream][position] = key[left]
            for stream, position in self.positions[right]:
                decoded[stream][position] = key[right]
            after = sum(self.gram_score(decoded, stream, start) for stream, start in affected)
            change = after - before
            temperature = start_temperature * (1.0 - iteration / iterations) + 0.05
            if change >= 0 or self.rng.random() < exp(change / temperature):
                score += change
                if score > best_score:
                    best_score = score
                    best_key = key.copy()
            else:
                key[left], key[right] = key[right], key[left]
                for stream, position in self.positions[left]:
                    decoded[stream][position] = key[left]
                for stream, position in self.positions[right]:
                    decoded[stream][position] = key[right]

        return best_score, best_key


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        type=Path,
        default=ROOT / "artifacts/practice-sdlwdr/cipher4.json",
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        default=Path(
            "/private/tmp/noita-eye-puzzle-scratchpad/"
            "research/data/lang/english-corpus-large.txt"
        ),
    )
    parser.add_argument("--space", type=int, default=62)
    parser.add_argument("--restarts", type=int, default=24)
    parser.add_argument("--iterations", type=int, default=250_000)
    parser.add_argument("--temperature", type=float, default=18.0)
    parser.add_argument("--seed", type=int, default=0x53444C57445204)
    args = parser.parse_args()

    messages = json.loads(args.data.read_text())
    streams = tuple(rotation_stream(message) for message in messages)
    scores, floor = train_tetragrams(args.corpus.read_text(errors="ignore"))
    rng = random.Random(args.seed)
    annealer = Annealer(streams, scores, floor, args.space, rng)

    overall_score = float("-inf")
    overall_key: list[int] | None = None
    for restart in range(args.restarts):
        score, key = annealer.run(args.iterations, args.temperature)
        if score > overall_score:
            overall_score = score
            overall_key = key
        print(f"restart={restart + 1:>2} score={score:>12.2f} best={overall_score:>12.2f}")
        assert overall_key is not None
        for decoded in annealer.decode(overall_key):
            print(render(decoded[:160]))
        print()

    assert overall_key is not None
    print("final key")
    print({symbol: overall_key[symbol] for symbol in annealer.symbols})
    print("final plaintext (case folded)")
    for decoded in annealer.decode(overall_key):
        print(render(decoded))


if __name__ == "__main__":
    main()
