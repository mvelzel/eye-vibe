"""Two-alphabet substitution search for an alternating state stream."""

from __future__ import annotations

import math
import random
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass

from .ngram import TetragramModel, tetragram_code

Token = tuple[int, int]


@dataclass(frozen=True)
class SubstitutionResult:
    score: float
    keys: tuple[tuple[int, ...], tuple[int, ...]]
    states: tuple[tuple[int, ...], tuple[int, ...]]
    plaintexts: tuple[str, ...]


def _prepare(
    messages: Sequence[Sequence[int]],
) -> tuple[
    tuple[tuple[Token, ...], ...],
    tuple[tuple[int, ...], tuple[int, ...]],
    tuple[tuple[Token, Token, Token, Token], ...],
]:
    states = tuple(
        tuple(sorted({value for message in messages for value in message[parity::2]}))
        for parity in (0, 1)
    )
    indices = tuple({value: index for index, value in enumerate(side)} for side in states)
    token_messages = tuple(
        tuple((position % 2, indices[position % 2][value]) for position, value in enumerate(message))
        for message in messages
    )
    windows = tuple(
        tuple(message[index : index + 4])
        for message in token_messages
        for index in range(len(message) - 3)
    )
    return token_messages, states, windows  # type: ignore[return-value]


def _plaintexts(
    token_messages: Sequence[Sequence[Token]], keys: Sequence[Sequence[int]]
) -> tuple[str, ...]:
    return tuple(
        "".join(chr(ord("A") + keys[parity][state]) for parity, state in message)
        for message in token_messages
    )


def solve(
    messages: Sequence[Sequence[int]],
    model: TetragramModel,
    *,
    restarts: int = 12,
    iterations: int = 150_000,
    seed: int = 20260720,
    injective: bool = True,
    target_frequencies: Sequence[float] | None = None,
    frequency_weight: float = 0.0,
) -> SubstitutionResult:
    """Optimize A-Z readout keys for even and odd positions."""
    rng = random.Random(seed)
    token_messages, states, windows = _prepare(messages)
    affected = {
        (parity, slot): set()
        for parity in (0, 1)
        for slot in range(26)
    }
    for window_index, window in enumerate(windows):
        for token in set(window):
            affected[token].add(window_index)

    frequencies = Counter(token for message in token_messages for token in message)
    common = tuple(map(lambda char: ord(char) - ord("A"), "ETAOINSHRDLCUMWFGYPBVKJXQZ"))

    best_score = -math.inf
    best_keys: tuple[tuple[int, ...], tuple[int, ...]] | None = None
    for restart in range(restarts):
        if restart == 0:
            keys = [list(range(26)), list(range(26))]
            for parity in (0, 1):
                ranked = sorted(
                    range(len(states[parity])),
                    key=lambda slot: frequencies[(parity, slot)],
                    reverse=True,
                )
                unused_slots = [slot for slot in range(26) if slot not in ranked]
                for rank, slot in enumerate(ranked + unused_slots):
                    keys[parity][slot] = common[rank]
        else:
            keys = [list(range(26)), list(range(26))]
            rng.shuffle(keys[0])
            rng.shuffle(keys[1])

        def score_window(window_index: int) -> float:
            letters = tuple(keys[parity][slot] for parity, slot in windows[window_index])
            return model.log_probabilities[tetragram_code(letters)]  # type: ignore[arg-type]

        def score_frequencies() -> float:
            if target_frequencies is None or frequency_weight == 0:
                return 0.0
            if len(target_frequencies) != 26:
                raise ValueError("target frequencies must contain 26 values")
            counts = [0] * 26
            for (side, slot), count in frequencies.items():
                counts[keys[side][slot]] += count
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
        local_best = current
        stagnation = 0
        for iteration in range(iterations):
            parity = rng.randrange(2)
            left = rng.randrange(len(states[parity]))
            if injective:
                right = rng.randrange(26)
                while right == left:
                    right = rng.randrange(26)
                old_letters = (keys[parity][left], keys[parity][right])
                changed = affected[(parity, left)] | affected[(parity, right)]
                keys[parity][left], keys[parity][right] = old_letters[::-1]
            else:
                right = -1
                old_letters = (keys[parity][left],)
                changed = affected[(parity, left)]
                replacement = rng.randrange(26)
                while replacement == keys[parity][left]:
                    replacement = rng.randrange(26)
                keys[parity][left] = replacement
            old = sum(window_scores[index] for index in changed)
            replacements = {index: score_window(index) for index in changed}
            replacement_frequency_score = score_frequencies()
            delta = (
                sum(replacements.values())
                - old
                + replacement_frequency_score
                - frequency_score
            )
            progress = iteration / iterations
            temperature = 18.0 * (0.15 / 18.0) ** progress
            if delta >= 0 or rng.random() < math.exp(delta / temperature):
                current += delta
                for index, value in replacements.items():
                    window_scores[index] = value
                frequency_score = replacement_frequency_score
                if current > local_best:
                    local_best = current
                    stagnation = 0
                else:
                    stagnation += 1
            else:
                keys[parity][left] = old_letters[0]
                if injective:
                    keys[parity][right] = old_letters[1]
                stagnation += 1

            if stagnation > 25_000:
                # Escape a frozen basin without discarding the entire restart.
                for _ in range(8):
                    side = rng.randrange(2)
                    a = rng.randrange(len(states[side]))
                    if injective:
                        b = rng.randrange(26)
                        while b == a:
                            b = rng.randrange(26)
                        keys[side][a], keys[side][b] = keys[side][b], keys[side][a]
                    else:
                        keys[side][a] = rng.randrange(26)
                window_scores = [score_window(index) for index in range(len(windows))]
                frequency_score = score_frequencies()
                current = sum(window_scores) + frequency_score
                stagnation = 0

            if current > best_score:
                best_score = current
                best_keys = (tuple(keys[0]), tuple(keys[1]))

    assert best_keys is not None
    language_score = sum(
        model.score(tuple(best_keys[parity][slot] for parity, slot in message))
        for message in token_messages
    )
    return SubstitutionResult(
        score=language_score,
        keys=best_keys,
        states=states,
        plaintexts=_plaintexts(token_messages, best_keys),
    )
