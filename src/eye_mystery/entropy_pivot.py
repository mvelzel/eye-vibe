"""Reproducible checks for proposed entropy pivots in the Eye Messages."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from math import log2, sqrt
from random import Random
from typing import Iterable, Sequence

from .corpus import MESSAGE_ORDER


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


def glyph_projections(
    messages: Mapping[str, Sequence[int]],
) -> dict[str, dict[str, tuple[int, ...]]]:
    """Return the four natural five-valued projections of each trigram.

    The first three projections are the authored eye components.  The fourth
    is their sum modulo five.  Permuting the three eyes before base-five
    conversion produces no additional modulo-five projection: it merely picks
    one of the same three component streams.
    """

    projections = {
        "first_eye": {},
        "middle_eye": {},
        "third_eye": {},
        "eye_sum_mod5": {},
    }
    for name in MESSAGE_ORDER:
        message = tuple(messages[name])
        if len(message) % 3:
            raise ValueError("eye stream length must be divisible by three")
        projections["first_eye"][name] = message[0::3]
        projections["middle_eye"][name] = message[1::3]
        projections["third_eye"][name] = message[2::3]
        projections["eye_sum_mod5"][name] = tuple(
            sum(message[offset : offset + 3]) % 5
            for offset in range(0, len(message), 3)
        )
    return projections


def lag_match_count(values: Sequence[int], *, start: int, stop: int, lag: int) -> int:
    """Count exact lag matches in ``values[start:stop]``."""

    if lag < 1:
        raise ValueError("lag must be positive")
    if not 0 <= start <= stop <= len(values):
        raise ValueError("invalid slice")
    return sum(
        values[index] == values[index - lag]
        for index in range(start + lag, stop)
    )


@dataclass(frozen=True)
class ExactPivotRow:
    """Direct checks of a claimed uniform, lag-periodic payload block."""

    counts: tuple[int, int, int, int, int]
    lag_matches: int
    lag_comparisons: int

    @property
    def uniform(self) -> bool:
        return len(set(self.counts)) == 1

    @property
    def periodic(self) -> bool:
        return self.lag_matches == self.lag_comparisons


def exact_pivot_rows(
    streams: Mapping[str, Sequence[int]],
    *,
    pivot: int = 25,
    block_length: int = 25,
    lag: int = 5,
) -> dict[str, ExactPivotRow]:
    """Check the exact payload claim for every message."""

    rows = {}
    for name in MESSAGE_ORDER:
        stream = tuple(streams[name])
        stop = pivot + block_length
        if stop > len(stream):
            raise ValueError("claimed payload block exceeds a message")
        block = stream[pivot:stop]
        rows[name] = ExactPivotRow(
            mod_five_counts(block),
            lag_match_count(block, start=0, stop=len(block), lag=lag),
            len(block) - lag,
        )
    return rows


@dataclass(frozen=True)
class PeriodScan:
    """Best aggregate lag-periodicity score after selecting a finite family."""

    projection: str
    lag: int
    cut: int
    block_length: int
    matches: int
    comparisons: int

    @property
    def match_rate(self) -> float:
        return self.matches / self.comparisons


def best_period_scan(
    projections: Mapping[str, Mapping[str, Sequence[int]]],
    *,
    lags: Sequence[int],
    minimum_cut: int = 5,
    block_length: int = 25,
) -> PeriodScan:
    """Select the best projection, lag, and cut by aggregate exact matches."""

    if not lags or any(lag < 1 or lag >= block_length for lag in lags):
        raise ValueError("lags must be between one and block_length")
    minimum_length = min(
        len(stream)
        for streams in projections.values()
        for stream in streams.values()
    )
    maximum_cut = minimum_length - block_length
    if minimum_cut > maximum_cut:
        raise ValueError("no eligible cut")

    best: PeriodScan | None = None
    for projection, streams in projections.items():
        for lag in lags:
            comparisons = len(MESSAGE_ORDER) * (block_length - lag)
            for cut in range(minimum_cut, maximum_cut + 1):
                matches = sum(
                    lag_match_count(
                        streams[name],
                        start=cut,
                        stop=cut + block_length,
                        lag=lag,
                    )
                    for name in MESSAGE_ORDER
                )
                candidate = PeriodScan(
                    projection,
                    lag,
                    cut,
                    block_length,
                    matches,
                    comparisons,
                )
                if best is None or (
                    candidate.matches,
                    -candidate.lag,
                    -candidate.cut,
                    candidate.projection,
                ) > (
                    best.matches,
                    -best.lag,
                    -best.cut,
                    best.projection,
                ):
                    best = candidate
    if best is None:  # pragma: no cover - guarded by validation
        raise AssertionError("period scan produced no candidates")
    return best


def shuffle_glyph_positions(
    messages: Mapping[str, Sequence[int]], rng: Random
) -> dict[str, tuple[int, ...]]:
    """Shuffle complete trigrams within each message.

    This preserves every message's trigram multiset and every within-glyph
    component relation while removing positional phase.
    """

    shuffled = {}
    for name in MESSAGE_ORDER:
        message = tuple(messages[name])
        if len(message) % 3:
            raise ValueError("eye stream length must be divisible by three")
        glyphs = [
            message[offset : offset + 3]
            for offset in range(0, len(message), 3)
        ]
        rng.shuffle(glyphs)
        shuffled[name] = tuple(value for glyph in glyphs for value in glyph)
    return shuffled


def period_scan_control(
    messages: Mapping[str, Sequence[int]],
    *,
    lags: Sequence[int],
    trials: int,
    seed: int,
    minimum_cut: int = 5,
    block_length: int = 25,
) -> tuple[PeriodScan, tuple[int, ...]]:
    """Return the observed selected scan and selected control scores."""

    if trials < 1:
        raise ValueError("trials must be positive")
    observed = best_period_scan(
        glyph_projections(messages),
        lags=lags,
        minimum_cut=minimum_cut,
        block_length=block_length,
    )
    rng = Random(seed)
    controls = tuple(
        best_period_scan(
            glyph_projections(shuffle_glyph_positions(messages, rng)),
            lags=lags,
            minimum_cut=minimum_cut,
            block_length=block_length,
        ).matches
        for _ in range(trials)
    )
    return observed, controls
