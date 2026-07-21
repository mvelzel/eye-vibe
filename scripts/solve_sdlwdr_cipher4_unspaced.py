#!/usr/bin/env python3
"""Attack Cipher 4 as two case homophones per unspaced English letter.

The cyclic reduction of sdlwdr #4 uses exactly 53 symbols and has no symbol
frequent enough to be ordinary English space.  A natural 53-entry PTA is
``A-Z``, ``a-z``, plus one formatting character.  After case folding, that is
two homophones per letter and one rare extra symbol.  This solver removes
spaces from its training corpus, allocates two action symbols to every letter,
and gives a third representative to one letter as a harmless approximation to
the single formatting entry.  It scans all 26 choices for that extra slot.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import json
from math import exp, log
from pathlib import Path
import random
import string
from typing import Iterable, Sequence


MODULUS = 83
ALPHABET = string.ascii_uppercase
ROOT = Path(__file__).resolve().parents[1]


def letters_only(text: str) -> tuple[int, ...]:
    return tuple(
        ord(character) - ord("A")
        for character in text.upper()
        if character in string.ascii_uppercase
    )


def action_stream(message: Sequence[int]) -> tuple[int, ...]:
    if not message:
        return ()
    return (message[0],) + tuple(
        (right - left) % MODULUS for left, right in zip(message, message[1:])
    )


@dataclass(frozen=True)
class Model:
    order: int
    scores: dict[tuple[int, ...], float]
    floor: float
    unigrams: tuple[float, ...]

    @classmethod
    def train(cls, text: str, order: int) -> "Model":
        values = letters_only(text)
        counts = Counter(
            values[index : index + order]
            for index in range(len(values) - order + 1)
        )
        total = sum(counts.values())
        singles = Counter(values)
        return cls(
            order,
            {gram: log(count / total) for gram, count in counts.items()},
            log(0.01 / total),
            tuple((singles[value] + 1) / (len(values) + 26) for value in range(26)),
        )


class Annealer:
    def __init__(
        self,
        streams: tuple[tuple[int, ...], ...],
        model: Model,
        extra_letter: int,
        rng: random.Random,
    ) -> None:
        self.streams = streams
        self.model = model
        self.extra_letter = extra_letter
        self.rng = rng
        self.symbols = sorted({symbol for stream in streams for symbol in stream})
        if len(self.symbols) != 53:
            raise ValueError(f"expected 53 reduced symbols, got {len(self.symbols)}")
        self.frequencies = Counter(symbol for stream in streams for symbol in stream)
        self.positions: dict[int, list[tuple[int, int]]] = defaultdict(list)
        for stream_index, stream in enumerate(streams):
            for position, symbol in enumerate(stream):
                self.positions[symbol].append((stream_index, position))

    def random_key(self) -> list[int]:
        slots = [value for value in range(26) for _ in range(2)] + [self.extra_letter]
        total = sum(self.frequencies.values())
        targets = [probability * total for probability in self.model.unigrams]
        assigned = [0] * 26
        remaining = Counter(slots)
        key = [-1] * MODULUS
        for symbol in sorted(
            self.symbols,
            key=lambda value: (self.frequencies[value], self.rng.random()),
            reverse=True,
        ):
            weight = self.frequencies[symbol]
            available = [value for value in range(26) if remaining[value]]
            best = max(targets[value] - assigned[value] for value in available)
            choices = [
                value
                for value in available
                if targets[value] - assigned[value]
                >= best - weight * self.rng.uniform(0.2, 1.2)
            ]
            value = self.rng.choice(choices)
            key[symbol] = value
            remaining[value] -= 1
            assigned[value] += weight
        return key

    def decode(self, key: Sequence[int]) -> list[list[int]]:
        return [[key[symbol] for symbol in stream] for stream in self.streams]

    def gram(self, decoded: list[list[int]], stream: int, start: int) -> float:
        values = decoded[stream]
        if not 0 <= start <= len(values) - self.model.order:
            return 0.0
        return self.model.scores.get(
            tuple(values[start : start + self.model.order]), self.model.floor
        )

    def score(self, decoded: list[list[int]]) -> float:
        return sum(
            self.gram(decoded, stream, start)
            for stream, values in enumerate(decoded)
            for start in range(len(values) - self.model.order + 1)
        )

    def affected(self, left: int, right: int) -> set[tuple[int, int]]:
        starts: set[tuple[int, int]] = set()
        for symbol in (left, right):
            for stream, position in self.positions[symbol]:
                for start in range(position - self.model.order + 1, position + 1):
                    if 0 <= start <= len(self.streams[stream]) - self.model.order:
                        starts.add((stream, start))
        return starts

    def run(self, iterations: int, temperature: float) -> tuple[float, list[int]]:
        key = self.random_key()
        decoded = self.decode(key)
        score = self.score(decoded)
        best = (score, key.copy())
        for iteration in range(iterations):
            left, right = self.rng.sample(self.symbols, 2)
            if key[left] == key[right]:
                continue
            starts = self.affected(left, right)
            before = sum(self.gram(decoded, stream, start) for stream, start in starts)
            key[left], key[right] = key[right], key[left]
            for symbol in (left, right):
                for stream, position in self.positions[symbol]:
                    decoded[stream][position] = key[symbol]
            after = sum(self.gram(decoded, stream, start) for stream, start in starts)
            change = after - before
            current_temperature = temperature * (1 - iteration / iterations) + 0.05
            if change >= 0 or self.rng.random() < exp(change / current_temperature):
                score += change
                if score > best[0]:
                    best = (score, key.copy())
            else:
                key[left], key[right] = key[right], key[left]
                for symbol in (left, right):
                    for stream, position in self.positions[symbol]:
                        decoded[stream][position] = key[symbol]
        return best


def render(values: Iterable[int]) -> str:
    return "".join(ALPHABET[value] for value in values)


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
    parser.add_argument("--order", type=int, default=5)
    parser.add_argument("--scan-iterations", type=int, default=35_000)
    parser.add_argument("--temperature", type=float, default=14.0)
    parser.add_argument("--seed", type=int, default=0x53444C57445204)
    parser.add_argument("--top", type=int, default=6)
    parser.add_argument(
        "--extra-letters",
        default=ALPHABET,
        help="letters whose third homophone allocation should be tested",
    )
    args = parser.parse_args()

    messages = json.loads(args.data.read_text())
    streams = tuple(action_stream(message) for message in messages)
    model = Model.train(args.corpus.read_text(errors="ignore"), args.order)
    rng = random.Random(args.seed)
    best: list[tuple[float, int, list[int]]] = []
    extra_letters = tuple(
        ord(character) - ord("A")
        for character in args.extra_letters.upper()
        if character in ALPHABET
    )
    if not extra_letters:
        raise ValueError("--extra-letters must contain at least one A-Z letter")
    for extra_letter in dict.fromkeys(extra_letters):
        annealer = Annealer(streams, model, extra_letter, rng)
        score, key = annealer.run(args.scan_iterations, args.temperature)
        best.append((score, extra_letter, key))
        print(
            f"extra={ALPHABET[extra_letter]} score={score:.2f}", flush=True
        )

    print("\nbest candidates")
    for score, extra_letter, key in sorted(best, reverse=True)[: args.top]:
        annealer = Annealer(streams, model, extra_letter, rng)
        print(f"score={score:.2f} extra={ALPHABET[extra_letter]}")
        for decoded in annealer.decode(key):
            print(render(decoded))
        print()


if __name__ == "__main__":
    main()
