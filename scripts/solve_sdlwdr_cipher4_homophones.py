#!/usr/bin/env python3
"""Attack sdlwdr #4 as a homophonic substitution after cyclic reduction.

For the hinted standard cyclic deck, the first ciphertext value followed by
mod-83 adjacent differences is the stream of plaintext actions.  There are 53
observed actions and their unusually flat frequency distribution is compatible
with a homophonic alphabet: several action symbols may render the same ordinary
plaintext character.

Unlike the earlier exploratory version of this program, this solver makes no
one-to-one or case-sensitive-alphabet assumption and does not guess a space
symbol in advance.  It optimizes an unrestricted mapping from the 53 action
symbols to ``A-Z`` plus space using incremental tetragram simulated annealing.
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
PTA = string.ascii_uppercase + " "
SPACE = 26
ROOT = Path(__file__).resolve().parents[1]


def normalize(text: str) -> tuple[int, ...]:
    result: list[int] = []
    in_space = True
    for character in text.upper():
        if character in string.ascii_uppercase:
            result.append(ord(character) - ord("A"))
            in_space = False
        elif not in_space:
            result.append(SPACE)
            in_space = True
    if result and result[-1] == SPACE:
        result.pop()
    return tuple(result)


def action_stream(message: Sequence[int]) -> tuple[int, ...]:
    if not message:
        return ()
    return (message[0],) + tuple(
        (right - left) % MODULUS for left, right in zip(message, message[1:])
    )


@dataclass(frozen=True)
class Ngrams:
    order: int
    scores: dict[tuple[int, ...], float]
    floor: float
    unigrams: tuple[float, ...]

    @classmethod
    def train(cls, text: str, order: int = 4) -> "Ngrams":
        values = normalize(text)
        counts = Counter(
            values[index : index + order]
            for index in range(len(values) - order + 1)
        )
        total = sum(counts.values())
        letter_counts = Counter(values)
        letter_total = sum(letter_counts.values())
        return cls(
            order,
            {gram: log(count / total) for gram, count in counts.items()},
            log(0.01 / total),
            tuple((letter_counts[value] + 1) / (letter_total + len(PTA)) for value in range(len(PTA))),
        )


def render(values: Iterable[int]) -> str:
    return "".join(PTA[value] for value in values)


class Annealer:
    def __init__(
        self,
        streams: tuple[tuple[int, ...], ...],
        model: Ngrams,
        rng: random.Random,
        allocation: str,
    ) -> None:
        self.streams = streams
        self.model = model
        self.rng = rng
        self.symbols = sorted({value for stream in streams for value in stream})
        self.frequencies = Counter(value for stream in streams for value in stream)
        self.positions: dict[int, list[tuple[int, int]]] = defaultdict(list)
        for stream_index, stream in enumerate(streams):
            for position, symbol in enumerate(stream):
                self.positions[symbol].append((stream_index, position))
        self.slot_counts = self._slot_counts(allocation)

    def _slot_counts(self, allocation: str) -> tuple[int, ...]:
        """Allocate all 53 homophones while retaining every PT character."""

        if allocation == "paired":
            return (2,) * 26 + (1,)
        if allocation != "frequency":
            raise ValueError(f"unknown allocation: {allocation}")
        counts = [1] * len(PTA)
        while sum(counts) < len(self.symbols):
            value = max(
                range(len(PTA)),
                key=lambda candidate: self.model.unigrams[candidate]
                * len(self.symbols)
                - counts[candidate],
            )
            counts[value] += 1
        return tuple(counts)

    def random_key(self) -> list[int]:
        """Create a frequency-balanced but randomized homophone assignment."""

        total = sum(self.frequencies.values())
        targets = [probability * total for probability in self.model.unigrams]
        assigned = [0] * len(PTA)
        remaining = list(self.slot_counts)
        key = [-1] * MODULUS
        symbols = sorted(
            self.symbols,
            key=lambda symbol: (self.frequencies[symbol], self.rng.random()),
            reverse=True,
        )
        for symbol in symbols:
            weight = self.frequencies[symbol]
            deficits = [
                target - count if remaining[value] else float("-inf")
                for value, (target, count) in enumerate(zip(targets, assigned))
            ]
            best_deficit = max(deficits)
            choices = [
                value
                for value, deficit in enumerate(deficits)
                if deficit >= best_deficit - weight * self.rng.uniform(0.25, 1.5)
            ]
            value = self.rng.choice(choices)
            key[symbol] = value
            assigned[value] += weight
            remaining[value] -= 1
        assert not any(remaining)
        return key

    def decode(self, key: Sequence[int]) -> list[list[int]]:
        return [[key[symbol] for symbol in stream] for stream in self.streams]

    def gram_score(self, decoded: list[list[int]], stream: int, start: int) -> float:
        values = decoded[stream]
        if start < 0 or start + self.model.order > len(values):
            return 0.0
        gram = tuple(values[start : start + self.model.order])
        return self.model.scores.get(gram, self.model.floor)

    def total_score(self, decoded: list[list[int]]) -> float:
        return sum(
            self.gram_score(decoded, stream, start)
            for stream, values in enumerate(decoded)
            for start in range(len(values) - self.model.order + 1)
        )

    def affected_starts(self, symbols: Iterable[int]) -> set[tuple[int, int]]:
        starts: set[tuple[int, int]] = set()
        for symbol in symbols:
            for stream, position in self.positions[symbol]:
                for start in range(position - self.model.order + 1, position + 1):
                    if 0 <= start <= len(self.streams[stream]) - self.model.order:
                        starts.add((stream, start))
        return starts

    def run(self, iterations: int, start_temperature: float) -> tuple[float, list[int]]:
        key = self.random_key()
        decoded = self.decode(key)
        score = self.total_score(decoded)
        best_score = score
        best_key = key.copy()

        for iteration in range(iterations):
            left, right = self.rng.sample(self.symbols, 2)
            if key[left] == key[right]:
                continue
            changed = (left, right)
            before_values = (key[left], key[right])
            after_values = (key[right], key[left])

            affected = self.affected_starts(changed)
            before = sum(
                self.gram_score(decoded, stream, start)
                for stream, start in affected
            )
            for symbol, value in zip(changed, after_values, strict=True):
                key[symbol] = value
                for stream, position in self.positions[symbol]:
                    decoded[stream][position] = value
            after = sum(
                self.gram_score(decoded, stream, start)
                for stream, start in affected
            )
            change = after - before
            progress = iteration / iterations
            temperature = start_temperature * (1.0 - progress) + 0.05
            if change >= 0 or self.rng.random() < exp(change / temperature):
                score += change
                if score > best_score:
                    best_score = score
                    best_key = key.copy()
            else:
                for symbol, value in zip(changed, before_values, strict=True):
                    key[symbol] = value
                    for stream, position in self.positions[symbol]:
                        decoded[stream][position] = value

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
    parser.add_argument("--restarts", type=int, default=32)
    parser.add_argument("--iterations", type=int, default=350_000)
    parser.add_argument("--temperature", type=float, default=18.0)
    parser.add_argument("--seed", type=int, default=0x53444C57445204)
    parser.add_argument(
        "--allocation",
        choices=("paired", "frequency"),
        default="paired",
        help="two case-folded representatives per letter, or frequency-weighted slots",
    )
    args = parser.parse_args()

    messages = json.loads(args.data.read_text())
    streams = tuple(action_stream(message) for message in messages)
    model = Ngrams.train(args.corpus.read_text(errors="ignore"))
    rng = random.Random(args.seed)
    annealer = Annealer(streams, model, rng, args.allocation)
    print(
        "homophone slots",
        {PTA[value]: count for value, count in enumerate(annealer.slot_counts)},
    )

    overall_score = float("-inf")
    overall_key: list[int] | None = None
    for restart in range(args.restarts):
        score, key = annealer.run(args.iterations, args.temperature)
        if score > overall_score:
            overall_score = score
            overall_key = key
        assert overall_key is not None
        print(
            f"restart={restart + 1:>2} score={score:>12.2f} "
            f"best={overall_score:>12.2f}",
            flush=True,
        )
        for decoded in annealer.decode(overall_key):
            print(render(decoded[:200]))
        print(flush=True)

    assert overall_key is not None
    print("final key")
    print({symbol: PTA[overall_key[symbol]] for symbol in annealer.symbols})
    print("final plaintext")
    for decoded in annealer.decode(overall_key):
        print(render(decoded))


if __name__ == "__main__":
    main()
