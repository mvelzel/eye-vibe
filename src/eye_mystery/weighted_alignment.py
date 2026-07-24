"""Exact cyclic-alignment audit for the marker-derived weights 3, 5, and 8."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass

from eye_mystery.fifteenth_second import trimmed_eye_words


MODULUS = 83
WEIGHTS = (3, 5, -8)
PANEL_ROWS = (
    ("east1", "west1", "east2"),
    ("west2", "east3", "west3"),
    ("east4", "west4", "east5"),
)


def weighted_score(columns: Sequence[Sequence[int]]) -> int:
    """Count positions satisfying ``3*x0 + 5*x1 = 8*x2 (mod 83)``."""

    if len(columns) != 3:
        raise ValueError("the weighted relation requires three columns")
    lengths = {len(column) for column in columns}
    if len(lengths) != 1:
        raise ValueError("weighted columns must have equal lengths")
    return sum(
        sum(weight * value for weight, value in zip(WEIGHTS, values, strict=True))
        % MODULUS
        == 0
        for values in zip(*columns, strict=True)
    )


def rotate(sequence: Sequence[int], offset: int) -> tuple[int, ...]:
    """Rotate left by ``offset`` positions."""

    values = tuple(sequence)
    if not values:
        raise ValueError("cannot rotate an empty sequence")
    normalized = offset % len(values)
    return values[normalized:] + values[:normalized]


def real_rows() -> tuple[
    tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]], ...
]:
    """Return copied-opening-trimmed natural rows at their common lengths."""

    words = trimmed_eye_words()
    output = []
    for names in PANEL_ROWS:
        length = min(len(words[name]) for name in names)
        output.append(tuple(words[name][:length] for name in names))
    return tuple(output)  # type: ignore[return-value]


def cyclic_alignment_histogram(
    columns: Sequence[Sequence[int]],
) -> Counter[int]:
    """Score every relative circular alignment of columns one and two."""

    if len(columns) != 3:
        raise ValueError("the cyclic null requires three columns")
    length = len(columns[0])
    if length == 0 or any(len(column) != length for column in columns):
        raise ValueError("cyclic columns must have one positive common length")
    first, second, third = (tuple(column) for column in columns)
    histogram: Counter[int] = Counter()
    for second_offset in range(length):
        shifted_second = rotate(second, second_offset)
        for third_offset in range(length):
            histogram[
                weighted_score((first, shifted_second, rotate(third, third_offset)))
            ] += 1
    return histogram


def convolve_histograms(
    left: Counter[int], right: Counter[int]
) -> Counter[int]:
    """Convolve two integer score histograms exactly."""

    output: Counter[int] = Counter()
    for left_score, left_count in left.items():
        for right_score, right_count in right.items():
            output[left_score + right_score] += left_count * right_count
    return output


def convolve_many(histograms: Sequence[Counter[int]]) -> Counter[int]:
    output: Counter[int] = Counter({0: 1})
    for histogram in histograms:
        output = convolve_histograms(output, histogram)
    return output


def weighted_plant(
    second: Sequence[int], third: Sequence[int]
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    """Construct a perfect synthetic fixture for the frozen equation."""

    if len(second) != len(third):
        raise ValueError("plant sources must have equal lengths")
    inverse_three = pow(3, -1, MODULUS)
    first = tuple(
        inverse_three * (8 * right - 5 * middle) % MODULUS
        for middle, right in zip(second, third, strict=True)
    )
    return first, tuple(second), tuple(third)


@dataclass(frozen=True)
class WeightedRowAudit:
    names: tuple[str, str, str]
    length: int
    real_score: int
    null_total: int
    null_upper: int
    null_min: int
    null_max: int

    @property
    def exact_tail(self) -> float:
        return self.null_upper / self.null_total


@dataclass(frozen=True)
class WeightedAlignmentAudit:
    rows: tuple[WeightedRowAudit, ...]
    real_total: int
    null_total: int
    null_upper: int
    null_min: int
    null_max: int

    @property
    def exact_tail(self) -> float:
        return self.null_upper / self.null_total


def weighted_alignment_audit() -> WeightedAlignmentAudit:
    rows = real_rows()
    histograms = tuple(cyclic_alignment_histogram(row) for row in rows)
    scores = tuple(weighted_score(row) for row in rows)
    row_audits = tuple(
        WeightedRowAudit(
            names=names,
            length=len(row[0]),
            real_score=score,
            null_total=sum(histogram.values()),
            null_upper=sum(
                count
                for candidate, count in histogram.items()
                if candidate >= score
            ),
            null_min=min(histogram),
            null_max=max(histogram),
        )
        for names, row, score, histogram in zip(
            PANEL_ROWS, rows, scores, histograms, strict=True
        )
    )
    combined = convolve_many(histograms)
    real_total = sum(scores)
    return WeightedAlignmentAudit(
        rows=row_audits,
        real_total=real_total,
        null_total=sum(combined.values()),
        null_upper=sum(
            count for score, count in combined.items() if score >= real_total
        ),
        null_min=min(combined),
        null_max=max(combined),
    )
