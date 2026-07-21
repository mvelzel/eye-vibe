"""Reproducible checks for proposed entropy pivots in the Eye Messages."""

from __future__ import annotations

from collections import Counter
from math import log2, sqrt
from typing import Iterable, Sequence


def shannon_entropy(values: Sequence[int]) -> float:
    """Return the empirical Shannon entropy of a non-empty sequence."""
    if not values:
        raise ValueError("entropy requires at least one value")
    length = len(values)
    return -sum(
        (count / length) * log2(count / length)
        for count in Counter(values).values()
    )


def rolling_entropies(values: Sequence[int], window: int = 5) -> tuple[float, ...]:
    """Return entropy for every consecutive ``window``-value slice."""
    if window <= 0:
        raise ValueError("window must be positive")
    if window > len(values):
        return ()
    return tuple(
        shannon_entropy(values[start : start + window])
        for start in range(len(values) - window + 1)
    )


def lag_autocorrelation(values: Sequence[int], lag: int) -> float:
    """Return Pearson correlation between a stream and its lagged copy."""
    if lag <= 0 or lag >= len(values):
        raise ValueError("lag must be between zero and the stream length")
    left = values[:-lag]
    right = values[lag:]
    left_mean = sum(left) / len(left)
    right_mean = sum(right) / len(right)
    numerator = sum(
        (x - left_mean) * (y - right_mean) for x, y in zip(left, right)
    )
    left_ss = sum((x - left_mean) ** 2 for x in left)
    right_ss = sum((y - right_mean) ** 2 for y in right)
    denominator = sqrt(left_ss * right_ss)
    return numerator / denominator if denominator else 0.0


def mod_five_counts(values: Iterable[int]) -> tuple[int, int, int, int, int]:
    """Count residues 0 through 4 after reducing values modulo five."""
    counts = Counter(value % 5 for value in values)
    return tuple(counts[residue] for residue in range(5))  # type: ignore[return-value]
