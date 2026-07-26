"""Affine two-sheet quotient attack for sdlwdr practice Cipher 3."""

from __future__ import annotations

import math
import random
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.practice_cipher3_wide import TrigramModel42
from eye_mystery.practice_sdlwdr import PLAINTEXT_ALPHABET


SIZE = 83
QUOTIENT_SIZE = 42


@dataclass(frozen=True)
class TwoSheetLanguageModel:
    """A 42-symbol trigram model plus its plaintext frequency order."""

    trigrams: TrigramModel42
    frequency_order: tuple[int, ...]

    @classmethod
    def train(cls, text: str) -> "TwoSheetLanguageModel":
        from eye_mystery.practice_cipher3_wide import normalize_plaintext42

        values = normalize_plaintext42(text)
        counts = Counter(values)
        return cls(
            TrigramModel42.train(text),
            tuple(
                sorted(
                    range(QUOTIENT_SIZE),
                    key=lambda value: (-counts[value], value),
                )
            ),
        )


def involution_orbits(reflection: int) -> tuple[tuple[int, ...], ...]:
    """Return the 42 orbits of ``x -> reflection - x (mod 83)``."""

    if reflection not in range(SIZE):
        raise ValueError("reflection must lie in 0..82")
    unseen = set(range(SIZE))
    orbits = []
    while unseen:
        value = min(unseen)
        partner = (reflection - value) % SIZE
        orbit = tuple(sorted({value, partner}))
        orbits.append(orbit)
        unseen.difference_update(orbit)
    result = tuple(sorted(orbits))
    if len(result) != QUOTIENT_SIZE:
        raise AssertionError("an affine involution must have 42 orbits")
    if sum(len(orbit) == 1 for orbit in result) != 1:
        raise AssertionError("an affine involution must have one fixed point")
    return result


def involution_quotient_table(reflection: int) -> tuple[int, ...]:
    """Map every raw symbol to its dense affine-involution orbit."""

    table = [-1] * SIZE
    for orbit_index, orbit in enumerate(involution_orbits(reflection)):
        for value in orbit:
            table[value] = orbit_index
    if any(value < 0 for value in table):
        raise AssertionError("quotient table is incomplete")
    return tuple(table)


def quotient_streams(
    streams: Sequence[Sequence[int]],
    reflection: int,
) -> tuple[tuple[int, ...], ...]:
    table = involution_quotient_table(reflection)
    return tuple(
        tuple(table[value] for value in stream)
        for stream in streams
    )


def render_plaintext(values: Sequence[int]) -> str:
    return "".join(PLAINTEXT_ALPHABET[value] for value in values)


def decode_with_key(
    streams: Sequence[Sequence[int]],
    key: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    if sorted(key) != list(range(QUOTIENT_SIZE)):
        raise ValueError("key must permute the 42-symbol plaintext alphabet")
    return tuple(
        tuple(key[value] for value in stream)
        for stream in streams
    )


def language_score(
    streams: Sequence[Sequence[int]],
    key: Sequence[int],
    model: TwoSheetLanguageModel,
) -> tuple[float, int]:
    table = model.trigrams.log_probabilities
    total = 0.0
    windows = 0
    for stream in streams:
        for index in range(len(stream) - 2):
            left, middle, right = (
                key[stream[index]],
                key[stream[index + 1]],
                key[stream[index + 2]],
            )
            total += table[(QUOTIENT_SIZE * left + middle) * QUOTIENT_SIZE + right]
            windows += 1
    return total, windows


@dataclass(frozen=True)
class SubstitutionResult:
    reflection: int
    score: float
    windows: int
    key: tuple[int, ...]

    @property
    def score_per_window(self) -> float:
        return self.score / self.windows if self.windows else float("-inf")


def optimize_substitution(
    raw_streams: Sequence[Sequence[int]],
    model: TwoSheetLanguageModel,
    reflection: int,
    *,
    restarts: int,
    iterations: int,
    seed: int,
) -> SubstitutionResult:
    """Optimize one injective 42-symbol substitution for one reflection."""

    if restarts < 1 or iterations < 1:
        raise ValueError("restarts and iterations must be positive")
    streams = quotient_streams(raw_streams, reflection)
    windows = tuple(
        tuple(stream[index : index + 3])
        for stream in streams
        for index in range(len(stream) - 2)
    )
    affected = [set() for _ in range(QUOTIENT_SIZE)]
    for window_index, window in enumerate(windows):
        for value in set(window):
            affected[value].add(window_index)
    counts = Counter(value for stream in streams for value in stream)
    rng = random.Random(seed)
    table = model.trigrams.log_probabilities
    best_score = float("-inf")
    best_key: tuple[int, ...] | None = None

    for restart in range(restarts):
        if restart == 0:
            state_order = sorted(
                range(QUOTIENT_SIZE),
                key=lambda value: (-counts[value], value),
            )
            key = [-1] * QUOTIENT_SIZE
            for state, plaintext in zip(
                state_order,
                model.frequency_order,
                strict=True,
            ):
                key[state] = plaintext
        else:
            key = list(range(QUOTIENT_SIZE))
            rng.shuffle(key)

        def window_score(window_index: int) -> float:
            left, middle, right = windows[window_index]
            return table[
                (QUOTIENT_SIZE * key[left] + key[middle])
                * QUOTIENT_SIZE
                + key[right]
            ]

        window_scores = [
            window_score(window_index)
            for window_index in range(len(windows))
        ]
        score = sum(window_scores)
        if score > best_score:
            best_score = score
            best_key = tuple(key)

        for iteration in range(iterations):
            left, right = rng.sample(range(QUOTIENT_SIZE), 2)
            changed = affected[left] | affected[right]
            before = sum(window_scores[index] for index in changed)
            key[left], key[right] = key[right], key[left]
            replacements = {
                index: window_score(index)
                for index in changed
            }
            delta = sum(replacements.values()) - before
            progress = iteration / max(1, iterations - 1)
            temperature = 18.0 * (0.08 / 18.0) ** progress
            if delta >= 0 or rng.random() < math.exp(delta / temperature):
                score += delta
                for index, value in replacements.items():
                    window_scores[index] = value
                if score > best_score:
                    best_score = score
                    best_key = tuple(key)
            else:
                key[left], key[right] = key[right], key[left]

    assert best_key is not None
    return SubstitutionResult(
        reflection,
        best_score,
        len(windows),
        best_key,
    )


def search_reflections(
    raw_streams: Sequence[Sequence[int]],
    model: TwoSheetLanguageModel,
    *,
    screen_iterations: int,
    refine_iterations: int,
    refine_restarts: int,
    shortlist: int,
    seed: int,
) -> tuple[SubstitutionResult, tuple[SubstitutionResult, ...]]:
    """Screen all 83 reflections, then refine a frozen top shortlist."""

    if shortlist not in range(1, SIZE + 1):
        raise ValueError("shortlist must lie in 1..83")
    screened = tuple(
        optimize_substitution(
            raw_streams,
            model,
            reflection,
            restarts=1,
            iterations=screen_iterations,
            seed=seed + 10_007 * reflection,
        )
        for reflection in range(SIZE)
    )
    selected = sorted(
        screened,
        key=lambda result: (-result.score_per_window, result.reflection),
    )[:shortlist]
    refined = tuple(
        optimize_substitution(
            raw_streams,
            model,
            result.reflection,
            restarts=refine_restarts,
            iterations=refine_iterations,
            seed=seed ^ (0x5EED0000 + result.reflection),
        )
        for result in selected
    )
    best = max(
        refined,
        key=lambda result: (
            result.score_per_window,
            -result.reflection,
        ),
    )
    return best, tuple(
        sorted(
            screened,
            key=lambda result: (-result.score_per_window, result.reflection),
        )
    )


def encode_two_sheet(
    plaintexts: Sequence[Sequence[int]],
    reflection: int,
    key: Sequence[int],
    *,
    seed: int,
) -> tuple[tuple[int, ...], ...]:
    """Encode plaintext through a quotient key, choosing orbit representatives."""

    if sorted(key) != list(range(QUOTIENT_SIZE)):
        raise ValueError("key must permute the 42-symbol plaintext alphabet")
    inverse_key = [0] * QUOTIENT_SIZE
    for orbit, plaintext in enumerate(key):
        inverse_key[plaintext] = orbit
    orbits = involution_orbits(reflection)
    rng = random.Random(seed)
    return tuple(
        tuple(
            rng.choice(orbits[inverse_key[value]])
            for value in plaintext
        )
        for plaintext in plaintexts
    )


def flatten_groups(
    streams: Mapping[str, Sequence[Sequence[int]]],
    groups: Sequence[str],
    *,
    body: bool,
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(message[1:] if body else message)
        for group in groups
        for message in streams[group]
    )
