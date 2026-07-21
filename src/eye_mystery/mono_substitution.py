"""Simulated-annealing monoalphabetic substitution for numeric streams."""

from __future__ import annotations

import math
import random
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass

from .ngram import TetragramModel, tetragram_code


@dataclass(frozen=True)
class MonoSubstitutionResult:
    score: float
    key: tuple[int, ...]
    states: tuple[int, ...]
    plaintexts: tuple[str, ...]


def solve_mono_substitution(
    messages: Sequence[Sequence[int]],
    model: TetragramModel,
    *,
    restarts: int = 12,
    iterations: int = 150_000,
    seed: int = 20260721,
    injective: bool = True,
    target_frequencies: Sequence[float] | None = None,
    frequency_weight: float = 0.0,
) -> MonoSubstitutionResult:
    states = tuple(sorted({value for message in messages for value in message}))
    if len(states) > 26:
        raise ValueError("monoalphabetic A-Z solver supports at most 26 states")
    state_index = {value: index for index, value in enumerate(states)}
    token_messages = tuple(
        tuple(state_index[value] for value in message) for message in messages
    )
    windows = tuple(
        tuple(message[index : index + 4])
        for message in token_messages
        for index in range(len(message) - 3)
    )
    affected = {slot: set() for slot in range(26)}
    for window_index, window in enumerate(windows):
        for token in set(window):
            affected[token].add(window_index)

    frequencies = Counter(token for message in token_messages for token in message)
    common = tuple(ord(char) - ord("A") for char in "ETAOINSHRDLCUMWFGYPBVKJXQZ")
    rng = random.Random(seed)
    best_score = -math.inf
    best_key = None
    for restart in range(restarts):
        key = list(range(26))
        if restart == 0:
            ranked = sorted(
                range(len(states)), key=frequencies.__getitem__, reverse=True
            )
            unused = [slot for slot in range(26) if slot not in ranked]
            for rank, slot in enumerate(ranked + unused):
                key[slot] = common[rank]
        else:
            rng.shuffle(key)

        def score_window(index: int) -> float:
            letters = tuple(key[token] for token in windows[index])
            return model.log_probabilities[tetragram_code(letters)]  # type: ignore[arg-type]

        def score_frequencies() -> float:
            if target_frequencies is None or frequency_weight == 0:
                return 0.0
            if len(target_frequencies) != 26:
                raise ValueError("target frequencies must contain 26 values")
            counts = [0] * 26
            for slot in range(len(states)):
                counts[key[slot]] += frequencies[slot]
            total = sum(counts)
            chi_square = sum(
                (observed - total * expected) ** 2 / (total * expected)
                for observed, expected in zip(
                    counts, target_frequencies, strict=True
                )
                if expected > 0
            )
            return -frequency_weight * chi_square

        window_scores = [score_window(index) for index in range(len(windows))]
        frequency_score = score_frequencies()
        current = sum(window_scores) + frequency_score
        for iteration in range(iterations):
            left = rng.randrange(len(states))
            if injective:
                right = rng.randrange(26)
                while right == left:
                    right = rng.randrange(26)
                old_letters = (key[left], key[right])
                changed = affected[left] | affected[right]
                key[left], key[right] = old_letters[::-1]
            else:
                right = -1
                old_letters = (key[left],)
                changed = affected[left]
                replacement = rng.randrange(26)
                while replacement == key[left]:
                    replacement = rng.randrange(26)
                key[left] = replacement
            old = sum(window_scores[index] for index in changed)
            replacements = {index: score_window(index) for index in changed}
            replacement_frequency_score = score_frequencies()
            delta = (
                sum(replacements.values())
                - old
                + replacement_frequency_score
                - frequency_score
            )
            progress = iteration / max(1, iterations - 1)
            temperature = 18.0 * (0.15 / 18.0) ** progress
            if delta >= 0 or rng.random() < math.exp(delta / temperature):
                current += delta
                for index, value in replacements.items():
                    window_scores[index] = value
                frequency_score = replacement_frequency_score
            else:
                key[left] = old_letters[0]
                if injective:
                    key[right] = old_letters[1]
            if current > best_score:
                best_score = current
                best_key = tuple(key)

    assert best_key is not None
    plaintexts = tuple(
        "".join(chr(ord("A") + best_key[token]) for token in message)
        for message in token_messages
    )
    language_score = sum(
        model.score(tuple(best_key[token] for token in message))
        for message in token_messages
    )
    return MonoSubstitutionResult(language_score, best_key, states, plaintexts)
