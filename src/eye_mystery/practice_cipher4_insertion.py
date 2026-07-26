"""Bounded arithmetic-insertion audit for sdlwdr practice cipher 4.

The operation family comes from a later public suggestion by the puzzle
author: insert a sum, difference, or product of the preceding symbols.  It is
not treated as a puzzle-specific hint.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Callable, Sequence


Relation = Callable[[int, int, int], int]


def _raw_sum(first: int, second: int, modulus: int) -> int:
    return first + second if first + second < modulus else -1


def _raw_product(first: int, second: int, modulus: int) -> int:
    return first * second if first * second < modulus else -1


RELATIONS: tuple[tuple[str, Relation], ...] = (
    ("sum_mod", lambda first, second, modulus: (first + second) % modulus),
    (
        "forward_diff_mod",
        lambda first, second, modulus: (second - first) % modulus,
    ),
    (
        "backward_diff_mod",
        lambda first, second, modulus: (first - second) % modulus,
    ),
    (
        "product_mod",
        lambda first, second, modulus: (first * second) % modulus,
    ),
    ("sum_raw", _raw_sum),
    ("absdiff_raw", lambda first, second, modulus: abs(first - second)),
    ("product_raw", _raw_product),
)


@dataclass(frozen=True)
class PhaseCandidate:
    coordinate: str
    relation: str
    period: int
    phase: int
    support: int
    hits: int

    @property
    def rate(self) -> float:
        return self.hits / self.support


def _phase_supports(
    lengths: Sequence[int],
    period: int,
) -> tuple[int, ...]:
    supports = [0] * period
    for length in lengths:
        for position in range(length - 2):
            supports[position % period] += 1
    return tuple(supports)


def arithmetic_phase_candidates(
    action_streams: Sequence[Sequence[int]],
    *,
    maximum_period: int = 32,
    minimum_support: int = 30,
) -> tuple[PhaseCandidate, ...]:
    """Score the complete fixed arithmetic/coordinate/phase family."""

    frozen = tuple(tuple(stream) for stream in action_streams)
    if any(value not in range(22, 79) for stream in frozen for value in stream):
        raise ValueError("actions must occupy the recovered 22..78 band")
    lengths = tuple(len(stream) for stream in frozen)
    output = []
    coordinate_spaces = (
        ("action83", frozen, 83),
        (
            "rank57",
            tuple(tuple(value - 22 for value in stream) for stream in frozen),
            57,
        ),
    )
    for coordinate, streams, modulus in coordinate_spaces:
        for relation_name, relation in RELATIONS:
            hit_positions = []
            for stream_index, stream in enumerate(streams):
                hit_positions.extend(
                    (stream_index, position)
                    for position, (first, second, current) in enumerate(
                        zip(stream, stream[1:], stream[2:])
                    )
                    if current == relation(first, second, modulus)
                )
            for period in range(1, maximum_period + 1):
                supports = _phase_supports(lengths, period)
                hits = [0] * period
                for _, position in hit_positions:
                    hits[position % period] += 1
                output.extend(
                    PhaseCandidate(
                        coordinate,
                        relation_name,
                        period,
                        phase,
                        support,
                        hits[phase],
                    )
                    for phase, support in enumerate(supports)
                    if support >= minimum_support
                )
    return tuple(output)


@dataclass(frozen=True)
class ArithmeticInsertionAudit:
    candidates: int
    best: PhaseCandidate
    best_z: float
    null_minimum: float
    null_mean: float
    null_maximum: float
    corrected_tail: float


def arithmetic_insertion_audit(
    action_streams: Sequence[Sequence[int]],
    *,
    controls: int = 500,
    seed: int = 0x53444C,
    maximum_period: int = 32,
    minimum_support: int = 30,
) -> ArithmeticInsertionAudit:
    """Reselect the whole insertion family in frequency-matched controls."""

    if controls < 2:
        raise ValueError("at least two controls are required")
    frozen = tuple(tuple(stream) for stream in action_streams)
    observed = arithmetic_phase_candidates(
        frozen,
        maximum_period=maximum_period,
        minimum_support=minimum_support,
    )
    rng = random.Random(seed)
    means = [0.0] * len(observed)
    m2 = [0.0] * len(observed)

    def shuffled_candidates() -> tuple[PhaseCandidate, ...]:
        shuffled = []
        for stream in frozen:
            values = list(stream)
            rng.shuffle(values)
            shuffled.append(tuple(values))
        return arithmetic_phase_candidates(
            shuffled,
            maximum_period=maximum_period,
            minimum_support=minimum_support,
        )

    for sample_index in range(1, controls + 1):
        row = shuffled_candidates()
        for index, candidate in enumerate(row):
            delta = candidate.rate - means[index]
            means[index] += delta / sample_index
            m2[index] += delta * (candidate.rate - means[index])
    standard_deviations = tuple(
        math.sqrt(value / controls) for value in m2
    )

    def standardized_max(row: Sequence[PhaseCandidate]) -> float:
        return max(
            (
                (candidate.rate - mean) / standard_deviation
                if standard_deviation
                else 0.0
            )
            for candidate, mean, standard_deviation in zip(
                row, means, standard_deviations, strict=True
            )
        )

    observed_z = tuple(
        (
            (candidate.rate - mean) / standard_deviation
            if standard_deviation
            else 0.0
        )
        for candidate, mean, standard_deviation in zip(
            observed, means, standard_deviations, strict=True
        )
    )
    best_index = max(range(len(observed)), key=observed_z.__getitem__)

    rng = random.Random(seed)
    null_maxima = tuple(
        standardized_max(shuffled_candidates()) for _ in range(controls)
    )
    best_z = observed_z[best_index]
    return ArithmeticInsertionAudit(
        len(observed),
        observed[best_index],
        best_z,
        min(null_maxima),
        sum(null_maxima) / len(null_maxima),
        max(null_maxima),
        (1 + sum(value >= best_z for value in null_maxima)) / (controls + 1),
    )
