"""Calibrated factor screens for sdlwdr practice cipher 4's 57-rank band."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from math import log2
import random


def entropy(values: Sequence[int]) -> float:
    """Shannon entropy in bits per symbol."""

    if not values:
        return 0.0
    counts = Counter(values)
    total = len(values)
    return -sum(
        count / total * log2(count / total) for count in counts.values()
    )


def normalized_ioc(values: Sequence[int], alphabet_size: int) -> float:
    """Index of coincidence multiplied by the declared alphabet size."""

    if len(values) < 2:
        return 0.0
    counts = Counter(values)
    numerator = sum(count * (count - 1) for count in counts.values())
    return alphabet_size * numerator / (len(values) * (len(values) - 1))


def mutual_information(left: Sequence[int], right: Sequence[int]) -> float:
    """Empirical mutual information in bits."""

    if len(left) != len(right):
        raise ValueError("paired sequences must have equal lengths")
    if not left:
        return 0.0
    left_counts = Counter(left)
    right_counts = Counter(right)
    joint = Counter(zip(left, right, strict=True))
    total = len(left)
    return sum(
        count / total
        * log2(count * total / (left_counts[a] * right_counts[b]))
        for (a, b), count in joint.items()
    )


def serial_mutual_information(streams: Sequence[Sequence[int]]) -> float:
    """First-order MI without adding transitions across portion boundaries."""

    left = []
    right = []
    for stream in streams:
        left.extend(stream[:-1])
        right.extend(stream[1:])
    return mutual_information(left, right)


@dataclass(frozen=True)
class NullAudit:
    observed: float
    null_minimum: float
    null_mean: float
    null_maximum: float
    upper_tail: float
    lower_tail: float


@dataclass(frozen=True)
class WidthScreen:
    width: int
    quotient_symbols: int
    remainder_symbols: int
    quotient_observed: float
    quotient_null_mean: float
    remainder_observed: float
    remainder_null_mean: float

    @property
    def quotient_excess(self) -> float:
        return self.quotient_observed - self.quotient_null_mean

    @property
    def remainder_excess(self) -> float:
        return self.remainder_observed - self.remainder_null_mean


def _summarize(observed: float, null: Sequence[float]) -> NullAudit:
    if not null:
        raise ValueError("at least one control is required")
    denominator = len(null) + 1
    return NullAudit(
        observed,
        min(null),
        sum(null) / len(null),
        max(null),
        (1 + sum(value >= observed for value in null)) / denominator,
        (1 + sum(value <= observed for value in null)) / denominator,
    )


def serial_shuffle_audit(
    streams: Sequence[Sequence[int]], *, controls: int, seed: int
) -> NullAudit:
    """Compare serial MI with within-portion frequency-preserving shuffles."""

    if controls < 1:
        raise ValueError("at least one control is required")
    frozen = tuple(tuple(stream) for stream in streams)
    observed = serial_mutual_information(frozen)
    rng = random.Random(seed)
    null = []
    for _ in range(controls):
        shuffled = []
        for stream in frozen:
            values = list(stream)
            rng.shuffle(values)
            shuffled.append(values)
        null.append(serial_mutual_information(shuffled))
    return _summarize(observed, null)


def contiguous_width_screen(
    ranks: Sequence[Sequence[int]],
    *,
    widths: Sequence[int],
    controls: int,
    seed: int,
) -> tuple[WidthScreen, ...]:
    """Compare quotient/remainder serial structure for several band widths."""

    if controls < 1:
        raise ValueError("at least one control is required")
    frozen = tuple(tuple(stream) for stream in ranks)
    if any(value not in range(57) for stream in frozen for value in stream):
        raise ValueError("ranks must lie in 0..56")
    rng = random.Random(seed)
    shuffled_controls = []
    for _ in range(controls):
        shuffled = []
        for stream in frozen:
            values = list(stream)
            rng.shuffle(values)
            shuffled.append(tuple(values))
        shuffled_controls.append(tuple(shuffled))

    rows = []
    for width in widths:
        if not 2 <= width <= 56:
            raise ValueError("screen widths must lie in 2..56")
        quotient = tuple(
            tuple(value // width for value in stream) for stream in frozen
        )
        remainder = tuple(
            tuple(value % width for value in stream) for stream in frozen
        )
        quotient_null = []
        remainder_null = []
        for control in shuffled_controls:
            quotient_null.append(
                serial_mutual_information(
                    tuple(
                        tuple(value // width for value in stream)
                        for stream in control
                    )
                )
            )
            remainder_null.append(
                serial_mutual_information(
                    tuple(
                        tuple(value % width for value in stream)
                        for stream in control
                    )
                )
            )
        rows.append(
            WidthScreen(
                width,
                len({value for stream in quotient for value in stream}),
                len({value for stream in remainder for value in stream}),
                serial_mutual_information(quotient),
                sum(quotient_null) / len(quotient_null),
                serial_mutual_information(remainder),
                sum(remainder_null) / len(remainder_null),
            )
        )
    return tuple(rows)


def coordinate_mutual_information(
    ranks: Sequence[int], divisor: int
) -> float:
    """MI between quotient and remainder under ``divmod(rank, divisor)``."""

    if any(rank not in range(57) for rank in ranks):
        raise ValueError("ranks must lie in 0..56")
    coordinates = tuple(divmod(rank, divisor) for rank in ranks)
    return mutual_information(
        tuple(quotient for quotient, _ in coordinates),
        tuple(remainder for _, remainder in coordinates),
    )


def label_shuffle_audit(
    ranks: Sequence[int], *, divisor: int, controls: int, seed: int
) -> NullAudit:
    """Test whether the authored numeric order unusually factors the counts.

    Each control randomly relabels all 57 positions before placing them in the
    same quotient/remainder grid.  Symbol frequencies, including the four
    zero-frequency positions, are therefore fixed.
    """

    if controls < 1:
        raise ValueError("at least one control is required")
    frozen = tuple(ranks)
    observed = coordinate_mutual_information(frozen, divisor)
    rng = random.Random(seed)
    null = []
    labels = list(range(57))
    for _ in range(controls):
        rng.shuffle(labels)
        relabeled = tuple(labels[rank] for rank in frozen)
        null.append(coordinate_mutual_information(relabeled, divisor))
    return _summarize(observed, null)


def difference_ladder(
    streams: Sequence[Sequence[int]], *, modulus: int, orders: int
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    """Return successive finite-difference layers modulo ``modulus``."""

    layers = []
    current = tuple(tuple(stream) for stream in streams)
    for _ in range(orders):
        layers.append(current)
        current = tuple(
            tuple(
                (following - value) % modulus
                for value, following in zip(stream, stream[1:])
            )
            for stream in current
        )
    return tuple(layers)
