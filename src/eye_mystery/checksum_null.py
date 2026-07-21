"""Null calculations for common divisors among message-value sums."""

from __future__ import annotations

from bisect import bisect_left
from collections.abc import Sequence
from itertools import combinations, permutations
from math import gcd
from random import Random


TWO_DIGIT_PRIMES = (
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
)


def uniform_sum_counts(length: int, high: int = 82) -> tuple[int, ...]:
    """Exact counts for sums of ``length`` independent integers in 0..high."""

    if length < 1 or high < 0:
        raise ValueError("length must be positive and high nonnegative")
    counts = [1]
    for _ in range(length):
        result = [0] * (len(counts) + high)
        window = 0
        for index in range(len(result)):
            if index < len(counts):
                window += counts[index]
            if index - high - 1 >= 0:
                window -= counts[index - high - 1]
            result[index] = window
        counts = result
    return tuple(counts)


def gcd_at_least_probability(
    lengths: tuple[int, ...], *, threshold: int, high: int = 82
) -> float:
    """Exact-marginal probability that independent sums have gcd >= threshold."""

    if len(lengths) < 2 or threshold < 1:
        raise ValueError("need at least two lengths and a positive threshold")
    distributions = tuple(uniform_sum_counts(length, high) for length in lengths)
    totals = tuple(float(sum(counts)) for counts in distributions)
    all_zero = 1.0
    for total in totals:
        all_zero /= total

    maximum = min(len(counts) - 1 for counts in distributions)
    divisible = [0.0] * (maximum + 1)
    for divisor in range(1, maximum + 1):
        probability = 1.0
        for counts, total in zip(distributions, totals, strict=True):
            probability *= sum(counts[::divisor]) / total
        divisible[divisor] = probability - all_zero

    exact = [0.0] * (maximum + 1)
    for divisor in range(maximum, 0, -1):
        exact[divisor] = divisible[divisor] - sum(
            exact[multiple]
            for multiple in range(divisor * 2, maximum + 1, divisor)
        )
    return sum(exact[threshold:])


def avoids_divisors(value: int, divisors: Sequence[int]) -> bool:
    """Return whether ``value`` is indivisible by every supplied divisor."""

    if any(divisor < 2 for divisor in divisors):
        raise ValueError("divisors must be at least two")
    return all(value % divisor for divisor in divisors)


def all_sums_avoid_divisors_probability(
    lengths: tuple[int, ...],
    *,
    divisors: Sequence[int] = TWO_DIGIT_PRIMES,
    high: int = 82,
) -> float:
    """Exact-marginal probability that every independent sum avoids divisors."""

    if not lengths:
        raise ValueError("need at least one length")
    probability = 1.0
    for length in lengths:
        counts = uniform_sum_counts(length, high)
        good = sum(
            count
            for value, count in enumerate(counts)
            if avoids_divisors(value, divisors)
        )
        probability *= good / sum(counts)
    return probability


def _cdf(counts: tuple[int, ...]) -> tuple[float, ...]:
    total = float(sum(counts))
    running = 0
    result = []
    for count in counts:
        running += count
        result.append(running / total)
    result[-1] = 1.0
    return tuple(result)


def simulate_gcd_events(
    lengths: tuple[int, ...],
    *,
    fixed_indices: tuple[int, int, int],
    threshold: int = 101,
    trials: int = 1_000_000,
    seed: int = 0,
    high: int = 82,
) -> tuple[int, int]:
    """Sample exact sum marginals; return fixed-triple and any-triple counts."""

    if trials < 1:
        raise ValueError("trials must be positive")
    cdfs = tuple(_cdf(uniform_sum_counts(length, high)) for length in lengths)
    triples = tuple(combinations(range(len(lengths)), 3))
    random = Random(seed)
    fixed_hits = 0
    any_hits = 0
    for _ in range(trials):
        totals = tuple(bisect_left(cdf, random.random()) for cdf in cdfs)
        fixed_gcd = gcd(
            gcd(totals[fixed_indices[0]], totals[fixed_indices[1]]),
            totals[fixed_indices[2]],
        )
        fixed_hits += fixed_gcd >= threshold

        pair_gcds = {
            (left, middle): gcd(totals[left], totals[middle])
            for left, middle in combinations(range(len(lengths)), 2)
        }
        any_hits += any(
            gcd(pair_gcds[(left, middle)], totals[right]) >= threshold
            for left, middle, right in triples
        )
    return fixed_hits, any_hits


def simulate_partition_gcd_events(
    values: Sequence[int],
    lengths: tuple[int, ...],
    *,
    fixed_indices: tuple[int, int, int],
    threshold: int = 101,
    trials: int = 100_000,
    seed: int = 0,
    markers: tuple[int, ...] | None = None,
) -> tuple[int, int]:
    """Shuffle the observed corpus into fixed lengths and test sum gcds.

    If ``markers`` is supplied, the values are shuffled only into message
    bodies of lengths one smaller, and the fixed markers are added afterward.
    """

    if trials < 1:
        raise ValueError("trials must be positive")
    if markers is not None and len(markers) != len(lengths):
        raise ValueError("markers and lengths must have equal sizes")
    chunk_lengths = (
        tuple(length - 1 for length in lengths) if markers else lengths
    )
    if sum(chunk_lengths) != len(values):
        raise ValueError("values do not fill the requested message lengths")

    pool = list(values)
    random = Random(seed)
    triples = tuple(combinations(range(len(lengths)), 3))
    fixed_hits = 0
    any_hits = 0
    for _ in range(trials):
        random.shuffle(pool)
        totals = []
        start = 0
        for index, length in enumerate(chunk_lengths):
            total = sum(pool[start : start + length])
            if markers is not None:
                total += markers[index]
            totals.append(total)
            start += length
        fixed_gcd = gcd(
            gcd(totals[fixed_indices[0]], totals[fixed_indices[1]]),
            totals[fixed_indices[2]],
        )
        fixed_hits += fixed_gcd >= threshold
        any_hits += any(
            gcd(gcd(totals[left], totals[middle]), totals[right]) >= threshold
            for left, middle, right in triples
        )
    return fixed_hits, any_hits


def marker_permutation_event_counts(
    bodies: tuple[int, ...],
    markers: tuple[int, ...],
    *,
    modulus: int,
    fixed_indices: tuple[int, int, int],
    families: tuple[tuple[int, ...], ...],
) -> dict[str, int]:
    """Exactly count checksum events over all assignments of observed markers."""

    if len(bodies) != len(markers):
        raise ValueError("bodies and markers must have equal sizes")
    targets = tuple((-body) % modulus for body in bodies)
    counts = {"total": 0, "fixed": 0, "any_three": 0, "family_cover": 0}
    for assignment in permutations(markers):
        matches = tuple(
            assignment[index] == targets[index]
            for index in range(len(markers))
        )
        counts["total"] += 1
        counts["fixed"] += all(matches[index] for index in fixed_indices)
        counts["any_three"] += sum(matches) >= 3
        counts["family_cover"] += all(
            any(matches[index] for index in family) for family in families
        )
    return counts


def marker_permutation_divisor_counts(
    bodies: tuple[int, ...],
    markers: tuple[int, ...],
    *,
    divisors: Sequence[int] = TWO_DIGIT_PRIMES,
    modulus: int,
    fixed_indices: tuple[int, ...],
) -> dict[str, int]:
    """Count divisor avoidance and a checksum jointly over marker assignments."""

    if len(bodies) != len(markers):
        raise ValueError("bodies and markers must have equal sizes")
    counts = {"total": 0, "avoid": 0, "checksum": 0, "both": 0}
    for assignment in permutations(markers):
        totals = tuple(
            body + marker
            for body, marker in zip(bodies, assignment, strict=True)
        )
        avoids = all(avoids_divisors(total, divisors) for total in totals)
        checksum = all(totals[index] % modulus == 0 for index in fixed_indices)
        counts["total"] += 1
        counts["avoid"] += avoids
        counts["checksum"] += checksum
        counts["both"] += avoids and checksum
    return counts
