"""Cheap probes for the second breadth-first Eye architecture fan-out."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import lru_cache
from math import log2


EYE_MODULUS = 83


def primitive_roots_f83() -> tuple[int, ...]:
    """Return all generators of the 82-element multiplicative group."""

    return tuple(
        value
        for value in range(2, EYE_MODULUS)
        if len(
            {
                pow(value, exponent, EYE_MODULUS)
                for exponent in range(EYE_MODULUS - 1)
            }
        )
        == EYE_MODULUS - 1
    )


@lru_cache(maxsize=None)
def _logarithms_f83(generator: int) -> tuple[int, ...]:
    table = [-1] * EYE_MODULUS
    value = 1
    for exponent in range(EYE_MODULUS - 1):
        table[value] = exponent
        value = value * generator % EYE_MODULUS
    if value != 1 or any(exponent < 0 for exponent in table[1:]):
        raise ValueError("generator is not primitive in F83")
    return tuple(table)


def reflection_log_orbit(
    value: int,
    center: int,
    generator: int,
    *,
    zero_class: int = 41,
) -> int:
    """Label ``F83*/±1`` by discrete log and add one class for zero."""

    if value not in range(EYE_MODULUS) or center not in range(EYE_MODULUS):
        raise ValueError("value and center must lie in F83")
    if zero_class not in range(42):
        raise ValueError("zero_class must lie in the 42-symbol alphabet")
    difference = (value - center) % EYE_MODULUS
    if difference == 0:
        return zero_class
    exponent = _logarithms_f83(generator)[difference] % 41
    if zero_class == 41:
        return exponent
    return exponent if exponent < zero_class else exponent + 1


def reflection_log_quotient(
    stream: Sequence[int],
    center: int,
    generator: int,
    *,
    zero_class: int = 41,
) -> tuple[int, ...]:
    """Apply the multiplicatively ordered 42-class reflection quotient."""

    return tuple(
        reflection_log_orbit(
            value,
            center,
            generator,
            zero_class=zero_class,
        )
        for value in stream
    )


def reflection_orbit(value: int, center: int, *, modulus: int = EYE_MODULUS) -> int:
    """Return the unoriented circular distance from ``center`` to ``value``."""

    if value not in range(modulus) or center not in range(modulus):
        raise ValueError("value and center must lie in the cyclic alphabet")
    forward = (value - center) % modulus
    return min(forward, (-forward) % modulus)


def reflection_quotient(
    stream: Sequence[int], center: int, *, modulus: int = EYE_MODULUS
) -> tuple[int, ...]:
    """Collapse a cyclic stream into the orbits of reflection about a center."""

    return tuple(reflection_orbit(value, center, modulus=modulus) for value in stream)


def rolling_reflection_quotient(
    stream: Sequence[int], *, modulus: int = EYE_MODULUS
) -> tuple[int, ...]:
    """Use each previous symbol as the reflection center for the next."""

    return tuple(
        reflection_orbit(following, current, modulus=modulus)
        for current, following in zip(stream, stream[1:])
    )


def exclusion_rank(
    current: int, following: int, *, modulus: int = EYE_MODULUS
) -> int:
    """Rank ``following`` after removing the forbidden current label."""

    if current not in range(modulus) or following not in range(modulus):
        raise ValueError("symbols must lie in the cyclic alphabet")
    if current == following:
        raise ValueError("a self-transition has no exclusion rank")
    return following if following < current else following - 1


def exclusion_ranks(
    stream: Sequence[int], *, modulus: int = EYE_MODULUS
) -> tuple[int, ...]:
    """Encode a no-self-loop stream as ranks in ``0..modulus-2``."""

    return tuple(
        exclusion_rank(current, following, modulus=modulus)
        for current, following in zip(stream, stream[1:])
    )


@dataclass(frozen=True)
class ContextDeterminism:
    order: int
    transitions: int
    contexts: int
    conflicting_contexts: int
    majority_correct: int

    @property
    def accuracy(self) -> float:
        return self.majority_correct / self.transitions if self.transitions else 0.0


def context_determinism(
    streams: Sequence[Sequence[int]], order: int
) -> ContextDeterminism:
    """Measure the best arbitrary deterministic next-symbol rule of one order."""

    if order < 1:
        raise ValueError("order must be positive")
    followers: dict[tuple[int, ...], Counter[int]] = {}
    transitions = 0
    for stream in streams:
        for index in range(order, len(stream)):
            context = tuple(stream[index - order : index])
            followers.setdefault(context, Counter())[stream[index]] += 1
            transitions += 1
    return ContextDeterminism(
        order=order,
        transitions=transitions,
        contexts=len(followers),
        conflicting_contexts=sum(len(counts) > 1 for counts in followers.values()),
        majority_correct=sum(max(counts.values()) for counts in followers.values()),
    )


def mutual_information(left: Sequence[int], right: Sequence[int]) -> float:
    """Return empirical mutual information in bits for aligned sequences."""

    if len(left) != len(right):
        raise ValueError("sequences must have equal length")
    if not left:
        return 0.0
    joint = Counter(zip(left, right, strict=True))
    left_counts = Counter(left)
    right_counts = Counter(right)
    length = len(left)
    return sum(
        (count / length)
        * log2(count * length / (left_counts[first] * right_counts[second]))
        for (first, second), count in joint.items()
    )


@dataclass(frozen=True)
class TapeDependence:
    information: float
    left_tape: int
    right_tape: int
    lag: int
    samples: int


def best_tape_dependence(
    streams: Sequence[Sequence[int]], *, maximum_lag: int = 8
) -> TapeDependence:
    """Find the strongest delayed dependence among three base-five digit tapes."""

    if maximum_lag < 0:
        raise ValueError("maximum_lag must be nonnegative")
    tapes = tuple(
        tuple(
            tuple((value // (5 ** (2 - tape))) % 5 for value in stream)
            for tape in range(3)
        )
        for stream in streams
    )
    best = TapeDependence(-1.0, 0, 1, 0, 0)
    for left_tape in range(3):
        for right_tape in range(3):
            if left_tape == right_tape:
                continue
            for lag in range(-maximum_lag, maximum_lag + 1):
                left_values: list[int] = []
                right_values: list[int] = []
                for stream_tapes in tapes:
                    left = stream_tapes[left_tape]
                    right = stream_tapes[right_tape]
                    if lag >= 0:
                        usable = len(left) - lag
                        if usable <= 0:
                            continue
                        left_values.extend(left[:usable])
                        right_values.extend(right[lag : lag + usable])
                    else:
                        left_values.extend(left[-lag:])
                        right_values.extend(right[: len(right) + lag])
                information = mutual_information(left_values, right_values)
                candidate = TapeDependence(
                    information,
                    left_tape,
                    right_tape,
                    lag,
                    len(left_values),
                )
                if (
                    candidate.information,
                    -abs(candidate.lag),
                    -candidate.left_tape,
                    -candidate.right_tape,
                ) > (
                    best.information,
                    -abs(best.lag),
                    -best.left_tape,
                    -best.right_tape,
                ):
                    best = candidate
    return best


@dataclass(frozen=True)
class HeaderFeatureRule:
    matches: int
    feature_name: str
    modulus: int
    sign: int
    offset: int
    matched_names: tuple[str, ...]


def best_header_feature_rule(
    streams: Mapping[str, Sequence[int]],
    features: Mapping[str, Mapping[str, int]],
    *,
    moduli: Sequence[int] = (5, 13, 26, 83, 101),
) -> HeaderFeatureRule:
    """Exhaust signed-offset header rules over predeclared scalar features."""

    if not streams or set(streams) != set(features):
        raise ValueError("streams and feature rows must have the same names")
    feature_names = tuple(next(iter(features.values())))
    if any(tuple(row) != feature_names for row in features.values()):
        raise ValueError("every feature row must use the same ordered fields")
    best = HeaderFeatureRule(-1, "", 0, 0, 0, ())
    for feature_name in feature_names:
        for modulus in moduli:
            if modulus < 2:
                raise ValueError("moduli must be at least two")
            for sign in (-1, 1):
                for offset in range(modulus):
                    matched = tuple(
                        name
                        for name, stream in streams.items()
                        if stream[0] % modulus
                        == (sign * features[name][feature_name] + offset) % modulus
                    )
                    candidate = HeaderFeatureRule(
                        len(matched),
                        feature_name,
                        modulus,
                        sign,
                        offset,
                        matched,
                    )
                    if (
                        candidate.matches,
                        -modulus,
                        -feature_names.index(feature_name),
                        -abs(offset),
                        sign,
                    ) > (
                        best.matches,
                        -best.modulus,
                        -feature_names.index(best.feature_name)
                        if best.feature_name
                        else -len(feature_names),
                        -abs(best.offset),
                        best.sign,
                    ):
                        best = candidate
    return best
