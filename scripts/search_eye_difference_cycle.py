#!/usr/bin/env python3
"""Test an 82-cycle/Wadsworth reading induced by Eye differences.

The Eye messages contain no adjacent repeated trigram values.  Consequently
their adjacent differences modulo 83 lie in ``F_83*``, a cyclic group of order
82.  Sdlwdr practice ciphers #1 and #2 show that an 82-position ciphertext
cycle can drive a smaller plaintext wheel, with independently reset sections
carrying unknown plaintext-wheel phases.

This script gives that analogy its strongest finite test.  It orders every
nonzero Eye difference by each primitive root of ``F_83*`` and tests direct,
successive-distance, and accumulated-step readings on plaintext rings of size
26 through 42, in both directions.  Per-message output phases are optimized
exactly against the published high-confidence repeated-plaintext contexts.
Natural plaintext orders are then language-scored only as a secondary check.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import product
from math import log
from pathlib import Path
import string
from typing import Iterable, Sequence

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values


MODULUS = 83
GROUP_ORDER = 82
ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Context:
    name: str
    length: int
    occurrences: tuple[tuple[str, int], ...]


CONTEXTS = (
    Context(
        "first-six",
        9,
        (
            ("east1", 40),
            ("east1", 68),
            ("west1", 40),
            ("west1", 70),
            ("east2", 45),
            ("east2", 80),
        ),
    ),
    Context(
        "first-long",
        18,
        (
            ("west1", 34),
            ("west1", 64),
            ("east2", 39),
            ("east2", 74),
        ),
    ),
    Context(
        "last-three",
        30,
        (("east4", 68), ("west4", 71), ("east5", 69)),
    ),
    Context(
        "last-nested",
        25,
        (("east4", 73), ("west4", 76), ("east5", 74), ("east3", 64)),
    ),
)


def primitive_roots() -> tuple[int, ...]:
    return tuple(
        value
        for value in range(2, MODULUS)
        if len({pow(value, exponent, MODULUS) for exponent in range(GROUP_ORDER)})
        == GROUP_ORDER
    )


def logarithm_table(generator: int) -> dict[int, int]:
    table: dict[int, int] = {}
    value = 1
    for exponent in range(GROUP_ORDER):
        table[value] = exponent
        value = value * generator % MODULUS
    if len(table) != GROUP_ORDER:
        raise ValueError(f"{generator} is not primitive modulo {MODULUS}")
    return table


def log_difference_coordinates(message: Sequence[int], generator: int) -> tuple[int, ...]:
    table = logarithm_table(generator)
    return tuple(
        table[(right - left) % MODULUS]
        for left, right in zip(message, message[1:])
    )


def read_coordinates(
    message: Sequence[int], generator: int, plaintext_modulus: int, mode: str, direction: int
) -> dict[int, int]:
    """Map complete-message positions to plaintext-wheel coordinates."""

    logs = log_difference_coordinates(message, generator)
    if direction not in (-1, 1):
        raise ValueError("direction must be -1 or +1")
    result: dict[int, int] = {}
    if mode == "log-direct":
        for full_position, coordinate in enumerate(logs, start=1):
            result[full_position] = direction * coordinate % plaintext_modulus
    elif mode == "log-step":
        accumulator = 0
        for full_position, coordinate in enumerate(logs, start=1):
            accumulator = (accumulator + direction * coordinate) % plaintext_modulus
            result[full_position] = accumulator
    elif mode in ("log-distance", "log-distance-direct"):
        accumulator = 0
        for full_position, (previous, current) in enumerate(
            zip(logs, logs[1:]), start=2
        ):
            distance = direction * ((current - previous) % GROUP_ORDER)
            if mode == "log-distance":
                accumulator = (accumulator + distance) % plaintext_modulus
                result[full_position] = accumulator
            else:
                result[full_position] = distance % plaintext_modulus
    else:
        raise ValueError(f"unknown mode: {mode}")
    return result


def equations(
    decoded: dict[str, dict[int, int]], modulus: int
) -> tuple[int, int, dict[tuple[str, str], Counter[int]]]:
    """Build phase-difference votes and count unavoidable self mismatches."""

    self_mismatches = 0
    self_comparisons = 0
    votes: dict[tuple[str, str], Counter[int]] = defaultdict(Counter)
    for context in CONTEXTS:
        reference_message, reference_start = context.occurrences[0]
        for displacement in range(context.length):
            reference_position = reference_start + displacement
            if reference_position not in decoded[reference_message]:
                continue
            reference_value = decoded[reference_message][reference_position]
            for message, start in context.occurrences[1:]:
                position = start + displacement
                if position not in decoded[message]:
                    continue
                value = decoded[message][position]
                required = (reference_value - value) % modulus
                if message == reference_message:
                    self_comparisons += 1
                    self_mismatches += required != 0
                else:
                    pair = (reference_message, message)
                    votes[pair][required] += 1
    return self_mismatches, self_comparisons, votes


def connected_components(edges: Iterable[tuple[str, str]]) -> tuple[tuple[str, ...], ...]:
    graph: dict[str, set[str]] = defaultdict(set)
    for left, right in edges:
        graph[left].add(right)
        graph[right].add(left)
    result: list[tuple[str, ...]] = []
    seen: set[str] = set()
    for start in graph:
        if start in seen:
            continue
        stack = [start]
        component: list[str] = []
        seen.add(start)
        while stack:
            node = stack.pop()
            component.append(node)
            for neighbour in graph[node]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        result.append(tuple(sorted(component)))
    return tuple(result)


def optimize_phases(
    decoded: dict[str, dict[int, int]], modulus: int
) -> tuple[int, int, dict[str, int]]:
    """Exactly maximize repeat equalities over independent message phases."""

    self_mismatches, self_comparisons, votes = equations(decoded, modulus)
    total = self_comparisons + sum(sum(counter.values()) for counter in votes.values())
    satisfied = self_comparisons - self_mismatches
    phases = {name: 0 for name in MESSAGE_ORDER}
    for component in connected_components(votes):
        anchor = component[0]
        rest = component[1:]
        best_score = -1
        best_values: tuple[int, ...] | None = None
        for values in product(range(modulus), repeat=len(rest)):
            local = {anchor: 0, **dict(zip(rest, values, strict=True))}
            score = 0
            for (left, right), counter in votes.items():
                if left in local and right in local:
                    score += counter[(local[right] - local[left]) % modulus]
            if score > best_score:
                best_score = score
                best_values = values
        assert best_values is not None
        satisfied += best_score
        phases.update({anchor: 0, **dict(zip(rest, best_values, strict=True))})
    return total - satisfied, total, phases


def alphabet_for(modulus: int) -> str | None:
    if modulus <= 26:
        return string.ascii_uppercase[:modulus]
    natural = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + " " + string.digits + ".,-’?!"
    if len(natural) < modulus:
        return None
    return natural[:modulus]


def normalized_fixed(text: str) -> tuple[int, ...]:
    return tuple(
        ord(character) - ord("A") if character in string.ascii_uppercase else 26
        for character in text.upper()
    )


@dataclass(frozen=True)
class Tetragrams:
    scores: dict[tuple[int, ...], float]
    floor: float

    @classmethod
    def train(cls, text: str) -> "Tetragrams":
        values = normalized_fixed(text)
        counts = Counter(values[index : index + 4] for index in range(len(values) - 3))
        total = sum(counts.values())
        return cls(
            {gram: log(count / total) for gram, count in counts.items()},
            log(0.01 / total),
        )

    def score(self, texts: Iterable[str]) -> float:
        return sum(
            self.scores.get(values[index : index + 4], self.floor)
            for text in texts
            for values in (normalized_fixed(text),)
            for index in range(len(values) - 3)
        )


@dataclass(frozen=True)
class Candidate:
    mismatches: int
    comparisons: int
    language_score: float
    generator: int
    plaintext_modulus: int
    mode: str
    direction: int
    phases: tuple[tuple[str, int], ...]
    texts: tuple[str, ...]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--corpus",
        type=Path,
        default=Path(
            "/private/tmp/noita-eye-puzzle-scratchpad/"
            "research/data/lang/english-corpus-large.txt"
        ),
    )
    parser.add_argument("--minimum-modulus", type=int, default=26)
    parser.add_argument("--maximum-modulus", type=int, default=42)
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    messages = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    model = Tetragrams.train(args.corpus.read_text(errors="ignore"))
    candidates: list[Candidate] = []
    for generator in primitive_roots():
        for plaintext_modulus in range(args.minimum_modulus, args.maximum_modulus + 1):
            alphabet = alphabet_for(plaintext_modulus)
            if alphabet is None:
                continue
            for mode in ("log-direct", "log-step", "log-distance", "log-distance-direct"):
                for direction in (-1, 1):
                    decoded = {
                        name: read_coordinates(
                            message, generator, plaintext_modulus, mode, direction
                        )
                        for name, message in messages.items()
                    }
                    mismatches, comparisons, phases = optimize_phases(
                        decoded, plaintext_modulus
                    )
                    texts = tuple(
                        "".join(
                            alphabet[(coordinate + phases[name]) % plaintext_modulus]
                            for _, coordinate in sorted(decoded[name].items())
                        )
                        for name in MESSAGE_ORDER
                    )
                    candidates.append(
                        Candidate(
                            mismatches,
                            comparisons,
                            model.score(texts),
                            generator,
                            plaintext_modulus,
                            mode,
                            direction,
                            tuple(sorted(phases.items())),
                            texts,
                        )
                    )
    candidates.sort(key=lambda candidate: (candidate.mismatches, -candidate.language_score))
    print("primitive roots:", len(primitive_roots()))
    print("candidates:", len(candidates))
    for candidate in candidates[: args.top]:
        print(
            f"mismatches={candidate.mismatches}/{candidate.comparisons} "
            f"score={candidate.language_score:.2f} generator={candidate.generator} "
            f"modulus={candidate.plaintext_modulus} mode={candidate.mode} "
            f"direction={candidate.direction:+d}"
        )
        print("phases", dict(candidate.phases))
        for text in candidate.texts:
            print(text[:180])
        print()


if __name__ == "__main__":
    main()
