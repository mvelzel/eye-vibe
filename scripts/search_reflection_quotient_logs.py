#!/usr/bin/env python3
"""Test the canonical multiplicative ordering of the 83-to-42 quotient."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from math import log
from pathlib import Path
from random import Random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.practice_sdlwdr import PLAINTEXT_ALPHABET
from eye_mystery.wide_complements import (
    primitive_roots_f83,
    reflection_log_quotient,
)


TRANSLATION = str.maketrans({"Ä": "A", "Å": "A", "Ö": "O", "'": "’"})


def normalize(text: str) -> str:
    output: list[str] = []
    in_space = True
    for character in text.upper().translate(TRANSLATION):
        if character in PLAINTEXT_ALPHABET and character != " ":
            output.append(character)
            in_space = False
        elif not in_space:
            output.append(" ")
            in_space = True
    if output and output[-1] == " ":
        output.pop()
    return "".join(output)


@dataclass(frozen=True)
class Ngrams:
    probabilities: dict[str, float]
    floor: float

    @classmethod
    def train(cls, text: str, order: int = 4) -> "Ngrams":
        normalized = normalize(text)
        counts = Counter(
            normalized[index : index + order]
            for index in range(len(normalized) - order + 1)
        )
        total = sum(counts.values())
        return cls(
            {gram: log(count / total) for gram, count in counts.items()},
            log(0.05 / total),
        )

    def score(self, texts: tuple[str, ...]) -> float:
        total = 0.0
        grams = 0
        for text in texts:
            for index in range(len(text) - 3):
                total += self.probabilities.get(text[index : index + 4], self.floor)
                grams += 1
        return total / grams


@dataclass(frozen=True)
class Candidate:
    score: float
    centers: str
    generator: int
    zero_class: int
    texts: tuple[str, ...]


def render(values: tuple[int, ...]) -> str:
    return "".join(PLAINTEXT_ALPHABET[value] for value in values)


def candidates(
    bodies: dict[str, tuple[int, ...]],
    headers: dict[str, int],
    model: Ngrams,
) -> tuple[Candidate, ...]:
    results = []
    for generator in primitive_roots_f83():
        for zero_class in (36, 41):
            marker_texts = tuple(
                render(
                    reflection_log_quotient(
                        bodies[name],
                        headers[name],
                        generator,
                        zero_class=zero_class,
                    )
                )
                for name in MESSAGE_ORDER
            )
            results.append(
                Candidate(
                    model.score(marker_texts),
                    "per-marker",
                    generator,
                    zero_class,
                    marker_texts,
                )
            )
            for center in range(83):
                texts = tuple(
                    render(
                        reflection_log_quotient(
                            bodies[name],
                            center,
                            generator,
                            zero_class=zero_class,
                        )
                    )
                    for name in MESSAGE_ORDER
                )
                results.append(
                    Candidate(
                        model.score(texts),
                        f"global-{center}",
                        generator,
                        zero_class,
                        texts,
                    )
                )
    return tuple(sorted(results, key=lambda item: item.score, reverse=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpora", nargs="+", type=Path)
    parser.add_argument("--uniform-controls", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260721)
    args = parser.parse_args()

    streams = {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}
    bodies = {name: stream[1:] for name, stream in streams.items()}
    headers = {name: stream[0] for name, stream in streams.items()}
    lengths = tuple(len(bodies[name]) for name in MESSAGE_ORDER)
    rng = Random(args.seed)

    for corpus in args.corpora:
        model = Ngrams.train(corpus.read_text(errors="ignore"))
        ranked = candidates(bodies, headers, model)
        controls = []
        for _ in range(args.uniform_controls):
            texts = tuple(
                render(tuple(rng.randrange(42) for _ in range(length)))
                for length in lengths
            )
            controls.append(model.score(texts))
        normalized = normalize(corpus.read_text(errors="ignore"))
        held_in_values = []
        cursor = 0
        for length in lengths:
            held_in_values.append(normalized[cursor : cursor + length])
            cursor += length
        held_in = tuple(held_in_values)
        print("corpus:", corpus)
        print("  model held-in score:", model.score(held_in))
        print("  uniform control range:", min(controls), max(controls))
        for candidate in ranked[:5]:
            print(
                " ",
                candidate.score,
                candidate.centers,
                "generator",
                candidate.generator,
                "zero",
                candidate.zero_class,
            )
            print("   ", candidate.texts[0][:120])


if __name__ == "__main__":
    main()
