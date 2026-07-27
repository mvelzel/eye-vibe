"""Audit physical-row-specific recurrence cooldowns in the Eye bodies."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import pairwise

from eye_mystery.fifteenth_second import (
    NATURAL_OPENING_TRIMS,
    trimmed_eye_words,
)
from eye_mystery.ninth_causal import CONTEXT_SPECS

PHYSICAL_ROWS = (
    ("east1", "west1", "east2"),
    ("west2", "east3", "west3"),
    ("east4", "west4", "east5"),
)
PANEL_ORDER = tuple(name for row in PHYSICAL_ROWS for name in row)
TARGET_VECTOR = (3, 3, 3, 2, 2, 2, 4, 4, 4)


@dataclass(frozen=True)
class SplitPrediction:
    """First-half row thresholds and untouched second-half minima."""

    thresholds: tuple[int, int, int]
    second_half_minima: tuple[int, ...]
    passes: bool


@dataclass(frozen=True)
class CooldownAudit:
    """Minimum recurrence and lag counts for one nine-word corpus."""

    minima: tuple[int, ...]
    lag_counts: tuple[tuple[int, ...], ...]
    first_half_minima: tuple[int, ...]
    second_half_minima: tuple[int, ...]
    split_prediction: SplitPrediction

    @property
    def row_minima(self) -> tuple[int, int, int]:
        return self.minima[0], self.minima[3], self.minima[6]

    @property
    def row_uniform(self) -> bool:
        return all(
            self.minima[offset]
            == self.minima[offset + 1]
            == self.minima[offset + 2]
            for offset in (0, 3, 6)
        )

    @property
    def row_uniform_distinct(self) -> bool:
        return self.row_uniform and len(set(self.row_minima)) == 3


@dataclass(frozen=True)
class CooldownNull:
    """Counts from one fixed matched-control family."""

    trials: int
    exact_vector: int
    row_uniform: int
    row_uniform_distinct: int
    split_prediction: int

    @staticmethod
    def corrected(count: int, trials: int) -> float:
        return (count + 1) / (trials + 1)

    @property
    def exact_tail(self) -> float:
        return self.corrected(self.exact_vector, self.trials)

    @property
    def uniform_tail(self) -> float:
        return self.corrected(self.row_uniform, self.trials)

    @property
    def uniform_distinct_tail(self) -> float:
        return self.corrected(self.row_uniform_distinct, self.trials)

    @property
    def split_tail(self) -> float:
        return self.corrected(self.split_prediction, self.trials)


def minimum_recurrence_distance(values: Sequence[int]) -> int:
    """Return the shortest distance between equal values."""

    last: dict[int, int] = {}
    minimum = len(values) + 1
    for index, value in enumerate(values):
        if value in last:
            minimum = min(minimum, index - last[value])
        last[value] = index
    return minimum


def lag_match_counts(
    values: Sequence[int],
    *,
    maximum_lag: int = 10,
) -> tuple[int, ...]:
    """Count equal pairs at each exact positive lag."""

    if maximum_lag < 1:
        raise ValueError("maximum_lag must be positive")
    return tuple(
        sum(left == right for left, right in zip(values, values[lag:]))
        for lag in range(1, maximum_lag + 1)
    )


def split_prediction(
    words: Mapping[str, Sequence[int]],
) -> SplitPrediction:
    """Fit row cooldown floors on first halves and test second halves."""

    first: dict[str, int] = {}
    second: dict[str, int] = {}
    for name in PANEL_ORDER:
        values = words[name]
        midpoint = len(values) // 2
        first[name] = minimum_recurrence_distance(values[:midpoint])
        second[name] = minimum_recurrence_distance(values[midpoint:])
    thresholds = tuple(
        min(first[name] for name in row)
        for row in PHYSICAL_ROWS
    )
    second_minima = tuple(second[name] for name in PANEL_ORDER)
    passes = all(
        second[name] >= threshold
        for row, threshold in zip(PHYSICAL_ROWS, thresholds, strict=True)
        for name in row
    )
    return SplitPrediction(thresholds, second_minima, passes)


def audit_cooldowns(
    words: Mapping[str, Sequence[int]] | None = None,
    *,
    maximum_lag: int = 10,
) -> CooldownAudit:
    """Return the frozen cooldown statistics."""

    corpus = trimmed_eye_words() if words is None else words
    if set(corpus) != set(PANEL_ORDER):
        raise ValueError("cooldown audit requires the canonical nine panels")
    minima = tuple(
        minimum_recurrence_distance(corpus[name])
        for name in PANEL_ORDER
    )
    lag_counts = tuple(
        lag_match_counts(corpus[name], maximum_lag=maximum_lag)
        for name in PANEL_ORDER
    )
    first = []
    second = []
    for name in PANEL_ORDER:
        values = corpus[name]
        midpoint = len(values) // 2
        first.append(minimum_recurrence_distance(values[:midpoint]))
        second.append(minimum_recurrence_distance(values[midpoint:]))
    return CooldownAudit(
        minima=minima,
        lag_counts=lag_counts,
        first_half_minima=tuple(first),
        second_half_minima=tuple(second),
        split_prediction=split_prediction(corpus),
    )


def registered_context_fixed_positions(
    words: Mapping[str, Sequence[int]] | None = None,
) -> dict[str, frozenset[int]]:
    """Return trimmed-word cells in the seven pre-registered contexts."""

    corpus = trimmed_eye_words() if words is None else words
    positions = {name: set() for name in PANEL_ORDER}
    for _, left, left_start, right, right_start, length in CONTEXT_SPECS[6:]:
        for name, full_start in ((left, left_start), (right, right_start)):
            # Context coordinates include the marker. Remove it, then remove
            # the independently established natural opening.
            start = full_start - 1 - NATURAL_OPENING_TRIMS[name]
            stop = start + length
            if start < 0 or stop > len(corpus[name]):
                raise ValueError("registered context falls outside trimmed word")
            positions[name].update(range(start, stop))
    return {
        name: frozenset(indices)
        for name, indices in positions.items()
    }


def _shuffle_word(
    values: Sequence[int],
    rng: random.Random,
    *,
    fixed_positions: frozenset[int],
    attempts: int = 2_000,
) -> tuple[int, ...]:
    free_positions = [
        index for index in range(len(values)) if index not in fixed_positions
    ]
    free_values = [values[index] for index in free_positions]
    for _ in range(attempts):
        rng.shuffle(free_values)
        candidate = list(values)
        for index, value in zip(free_positions, free_values, strict=True):
            candidate[index] = value
        if all(
            left != right
            for left, right in pairwise(candidate)
        ):
            return tuple(candidate)
    raise RuntimeError("failed to construct a no-double cooldown control")


def shuffled_words(
    words: Mapping[str, Sequence[int]],
    rng: random.Random,
    *,
    fixed_positions: Mapping[str, frozenset[int]] | None = None,
) -> dict[str, tuple[int, ...]]:
    """Shuffle each word's free multiset while preserving no doubles."""

    fixed = (
        {name: frozenset() for name in PANEL_ORDER}
        if fixed_positions is None
        else fixed_positions
    )
    return {
        name: _shuffle_word(
            words[name],
            rng,
            fixed_positions=fixed[name],
        )
        for name in PANEL_ORDER
    }


def run_cooldown_null(
    *,
    trials: int,
    seed: int,
    freeze_registered_contexts: bool,
) -> CooldownNull:
    """Run one frozen matched-control family."""

    if trials < 1:
        raise ValueError("trials must be positive")
    words = trimmed_eye_words()
    fixed = (
        registered_context_fixed_positions(words)
        if freeze_registered_contexts
        else None
    )
    rng = random.Random(seed)
    exact = uniform = distinct = split = 0
    for _ in range(trials):
        audit = audit_cooldowns(
            shuffled_words(words, rng, fixed_positions=fixed)
        )
        exact += audit.minima == TARGET_VECTOR
        uniform += audit.row_uniform
        distinct += audit.row_uniform_distinct
        split += audit.split_prediction.passes
    return CooldownNull(trials, exact, uniform, distinct, split)


def cooldown_process(
    length: int,
    *,
    alphabet_size: int,
    minimum_distance: int,
    rng: random.Random,
) -> tuple[int, ...]:
    """Generate one process forbidding the previous ``distance-1`` labels."""

    if length < 2 or alphabet_size < minimum_distance:
        raise ValueError("invalid cooldown-process dimensions")
    excluded = minimum_distance - 1
    for _ in range(10_000):
        values = []
        for _ in range(length):
            banned = set(values[-excluded:]) if excluded else set()
            choices = [
                value for value in range(alphabet_size) if value not in banned
            ]
            values.append(rng.choice(choices))
        if minimum_recurrence_distance(values) == minimum_distance:
            return tuple(values)
    raise RuntimeError("cooldown plant did not realize its boundary")


def planted_cooldown_words(
    *,
    seed: int = 0xC001D03,
    alphabet_size: int = 83,
) -> dict[str, tuple[int, ...]]:
    """Generate a deterministic positive control at the nine real lengths."""

    real = trimmed_eye_words()
    rng = random.Random(seed)
    thresholds = (3, 2, 4)
    return {
        name: cooldown_process(
            len(real[name]),
            alphabet_size=alphabet_size,
            minimum_distance=threshold,
            rng=rng,
        )
        for row, threshold in zip(PHYSICAL_ROWS, thresholds, strict=True)
        for name in row
    }
