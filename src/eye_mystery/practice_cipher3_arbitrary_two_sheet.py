"""Arbitrary static 83-to-42 two-sheet attack for practice Cipher 3."""

from __future__ import annotations

import math
import random
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.practice_cipher3_wide import (
    TrigramModel42,
    normalize_plaintext42,
)
from eye_mystery.practice_sdlwdr import PLAINTEXT_ALPHABET


RAW_SIZE = 83
PLAIN_SIZE = 42


def validate_key(key: Sequence[int]) -> None:
    """Require 41 doubleton plaintext classes and one singleton."""
    if len(key) != RAW_SIZE or any(value not in range(PLAIN_SIZE) for value in key):
        raise ValueError("key must map 83 raw symbols into 42 plaintext symbols")
    multiplicities = sorted(Counter(key).values())
    if multiplicities != [1] + [2] * (PLAIN_SIZE - 1):
        raise ValueError("key must have one singleton and 41 doubletons")


def random_key(rng: random.Random) -> tuple[int, ...]:
    singleton = rng.randrange(PLAIN_SIZE)
    slots = [
        plaintext
        for plaintext in range(PLAIN_SIZE)
        for _copy in range(1 if plaintext == singleton else 2)
    ]
    rng.shuffle(slots)
    result = tuple(slots)
    validate_key(result)
    return result


def decode_streams(
    streams: Sequence[Sequence[int]],
    key: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    validate_key(key)
    return tuple(
        tuple(key[value] for value in stream)
        for stream in streams
    )


def encode_streams(
    plaintexts: Sequence[Sequence[int]],
    key: Sequence[int],
    *,
    seed: int,
) -> tuple[tuple[int, ...], ...]:
    """Encode with balanced deterministic use of each homophone class."""
    validate_key(key)
    representatives = tuple(
        tuple(raw for raw, value in enumerate(key) if value == plaintext)
        for plaintext in range(PLAIN_SIZE)
    )
    rng = random.Random(seed)
    counters = [
        rng.randrange(len(options))
        for options in representatives
    ]
    output = []
    for plaintext in plaintexts:
        message = []
        for value in plaintext:
            if value not in range(PLAIN_SIZE):
                raise ValueError("plaintext value lies outside the alphabet")
            options = representatives[value]
            message.append(options[counters[value] % len(options)])
            counters[value] += 1
        output.append(tuple(message))
    return tuple(output)


def render_streams(streams: Sequence[Sequence[int]]) -> tuple[str, ...]:
    return tuple(
        "".join(PLAINTEXT_ALPHABET[value] for value in stream)
        for stream in streams
    )


@dataclass(frozen=True)
class StaticTwoSheetResult:
    score: float
    windows: int
    key: tuple[int, ...]

    @property
    def score_per_window(self) -> float:
        return self.score / self.windows if self.windows else float("-inf")


def _frequency_key(
    streams: Sequence[Sequence[int]],
    training_text: str,
) -> tuple[int, ...]:
    raw_counts = Counter(value for stream in streams for value in stream)
    plaintext_counts = Counter(normalize_plaintext42(training_text))
    singleton = min(
        range(PLAIN_SIZE),
        key=lambda value: (plaintext_counts[value], value),
    )
    slots = []
    for plaintext in range(PLAIN_SIZE):
        copies = 1 if plaintext == singleton else 2
        expected = plaintext_counts[plaintext] / copies
        slots.extend((expected, plaintext) for _copy in range(copies))
    raw_order = sorted(
        range(RAW_SIZE),
        key=lambda value: (-raw_counts[value], value),
    )
    slot_order = sorted(slots, key=lambda item: (-item[0], item[1]))
    key = [-1] * RAW_SIZE
    for raw, (_expected, plaintext) in zip(
        raw_order,
        slot_order,
        strict=True,
    ):
        key[raw] = plaintext
    result = tuple(key)
    validate_key(result)
    return result


def trigram_score(
    streams: Sequence[Sequence[int]],
    key: Sequence[int],
    model: TrigramModel42,
) -> tuple[float, int]:
    table = model.log_probabilities
    score = 0.0
    windows = 0
    for stream in streams:
        for left, middle, right in zip(stream, stream[1:], stream[2:]):
            score += table[
                (PLAIN_SIZE * key[left] + key[middle]) * PLAIN_SIZE
                + key[right]
            ]
            windows += 1
    return score, windows


def optimize_key(
    streams: Sequence[Sequence[int]],
    model: TrigramModel42,
    training_text: str,
    *,
    restarts: int,
    iterations: int,
    start_temperature: float,
    end_temperature: float,
    seed: int,
) -> StaticTwoSheetResult:
    """Anneal the exact two-sheet key without changing its capacities."""
    if restarts < 1 or iterations < 1:
        raise ValueError("restarts and iterations must be positive")
    if start_temperature <= 0 or end_temperature <= 0:
        raise ValueError("temperatures must be positive")

    windows = tuple(
        (left, middle, right)
        for stream in streams
        for left, middle, right in zip(stream, stream[1:], stream[2:])
    )
    affected = [set() for _ in range(RAW_SIZE)]
    for index, window in enumerate(windows):
        for raw in set(window):
            affected[raw].add(index)
    table = model.log_probabilities
    rng = random.Random(seed)
    best_score = float("-inf")
    best_key: tuple[int, ...] | None = None

    def window_score(key: Sequence[int], index: int) -> float:
        left, middle, right = windows[index]
        return table[
            (PLAIN_SIZE * key[left] + key[middle]) * PLAIN_SIZE
            + key[right]
        ]

    for restart in range(restarts):
        key = list(
            _frequency_key(streams, training_text)
            if restart == 0
            else random_key(rng)
        )
        scores = [
            window_score(key, index)
            for index in range(len(windows))
        ]
        score = sum(scores)
        if score > best_score:
            best_score = score
            best_key = tuple(key)

        for iteration in range(iterations):
            progress = iteration / max(1, iterations - 1)
            temperature = start_temperature * (
                end_temperature / start_temperature
            ) ** progress

            singleton = Counter(key).most_common()[-1][0]
            if rng.random() < 0.08:
                target = rng.choice(
                    [
                        plaintext
                        for plaintext in range(PLAIN_SIZE)
                        if plaintext != singleton
                    ]
                )
                raw = rng.choice(
                    [
                        candidate
                        for candidate, plaintext in enumerate(key)
                        if plaintext == target
                    ]
                )
                changed_raws = (raw,)
                previous = (target,)
                key[raw] = singleton
            else:
                left, right = rng.sample(range(RAW_SIZE), 2)
                if key[left] == key[right]:
                    continue
                changed_raws = (left, right)
                previous = (key[left], key[right])
                key[left], key[right] = key[right], key[left]

            changed_windows = set().union(
                *(affected[raw] for raw in changed_raws)
            )
            before = sum(scores[index] for index in changed_windows)
            replacements = {
                index: window_score(key, index)
                for index in changed_windows
            }
            delta = sum(replacements.values()) - before
            if delta >= 0 or rng.random() < math.exp(delta / temperature):
                score += delta
                for index, replacement in replacements.items():
                    scores[index] = replacement
                if score > best_score:
                    best_score = score
                    best_key = tuple(key)
            else:
                for raw, plaintext in zip(
                    changed_raws,
                    previous,
                    strict=True,
                ):
                    key[raw] = plaintext

    assert best_key is not None
    validate_key(best_key)
    return StaticTwoSheetResult(best_score, len(windows), best_key)


def event_accuracy(
    decoded: Sequence[Sequence[int]],
    expected: Sequence[Sequence[int]],
) -> float:
    correct = total = 0
    for observed, truth in zip(decoded, expected, strict=True):
        if len(observed) != len(truth):
            raise ValueError("decoded and expected lengths differ")
        correct += sum(
            left == right
            for left, right in zip(observed, truth, strict=True)
        )
        total += len(observed)
    return correct / total if total else 0.0


def group_streams(
    streams: Mapping[str, Sequence[Sequence[int]]],
    groups: Sequence[str],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(message)
        for group in groups
        for message in streams[group]
    )
