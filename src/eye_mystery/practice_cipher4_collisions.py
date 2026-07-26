"""Matched cyclic-shift null for sdlwdr practice cipher 4."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import combinations, product


MODULUS = 83


def aligned_collision_profile(
    left: Sequence[int],
    right: Sequence[int],
    modulus: int = MODULUS,
) -> tuple[int, ...]:
    """Count aligned symbol matches for every relative additive shift.

    Entry ``d`` counts matches after shifts satisfying
    ``left_shift - right_shift == d (mod modulus)``.
    """

    counts = [0] * modulus
    for left_value, right_value in zip(left, right):
        counts[(right_value - left_value) % modulus] += 1
    return tuple(counts)


def bigram_collision_profile(
    left: Sequence[int],
    right: Sequence[int],
    modulus: int = MODULUS,
) -> tuple[int, ...]:
    """Count exact cross-message bigram matches for every relative shift."""

    left_counts = Counter(zip(left, left[1:]))
    right_counts = Counter(zip(right, right[1:]))
    counts = [0] * modulus
    for (left_a, left_b), left_count in left_counts.items():
        for (right_a, right_b), right_count in right_counts.items():
            offset = (right_a - left_a) % modulus
            if (right_b - left_b) % modulus == offset:
                counts[offset] += left_count * right_count
    return tuple(counts)


def within_message_bigram_collisions(messages: Sequence[Sequence[int]]) -> int:
    """Return repeated-bigram pairs that no whole-message shift can change."""

    total = 0
    for message in messages:
        for count in Counter(zip(message, message[1:])).values():
            total += count * (count - 1) // 2
    return total


@dataclass(frozen=True)
class CollisionMetrics:
    aligned_unigrams: int
    cross_message_bigrams: int


@dataclass(frozen=True)
class PhaseShiftAudit:
    observed: CollisionMetrics
    configurations: int
    unigram_lower_or_equal: int
    bigram_upper_or_equal: int
    joint_tail: int
    cross_bigram_minimum: int
    cross_bigram_maximum: int
    cross_bigram_sum: int
    within_bigram_collisions: int
    bigram_positions: int

    @staticmethod
    def corrected_tail(count: int, configurations: int) -> float:
        """Return the add-one corrected exhaustive tail."""

        return (count + 1) / (configurations + 1)


def phase_shift_audit(
    messages: Sequence[Sequence[int]],
    modulus: int = MODULUS,
) -> PhaseShiftAudit:
    """Exhaust independent additive phase shifts of three cyclic streams.

    The first stream is fixed at shift zero to remove the irrelevant global
    shift. Every within-message difference and complete action stream is
    preserved.
    """

    if len(messages) != 3:
        raise ValueError("the audit requires exactly three messages")

    pairs = tuple(combinations(range(3), 2))
    unigram_profiles = {
        pair: aligned_collision_profile(
            messages[pair[0]], messages[pair[1]], modulus
        )
        for pair in pairs
    }
    bigram_profiles = {
        pair: bigram_collision_profile(
            messages[pair[0]], messages[pair[1]], modulus
        )
        for pair in pairs
    }

    metrics = []
    for second_shift, third_shift in product(range(modulus), repeat=2):
        shifts = (0, second_shift, third_shift)
        unigram_total = 0
        bigram_total = 0
        for left_index, right_index in pairs:
            offset = (shifts[left_index] - shifts[right_index]) % modulus
            unigram_total += unigram_profiles[(left_index, right_index)][offset]
            bigram_total += bigram_profiles[(left_index, right_index)][offset]
        metrics.append(CollisionMetrics(unigram_total, bigram_total))

    observed = metrics[0]
    unigram_tail = sum(
        metric.aligned_unigrams <= observed.aligned_unigrams
        for metric in metrics
    )
    bigram_tail = sum(
        metric.cross_message_bigrams >= observed.cross_message_bigrams
        for metric in metrics
    )
    joint_tail = sum(
        metric.aligned_unigrams <= observed.aligned_unigrams
        and metric.cross_message_bigrams >= observed.cross_message_bigrams
        for metric in metrics
    )
    bigram_values = tuple(metric.cross_message_bigrams for metric in metrics)

    return PhaseShiftAudit(
        observed=observed,
        configurations=len(metrics),
        unigram_lower_or_equal=unigram_tail,
        bigram_upper_or_equal=bigram_tail,
        joint_tail=joint_tail,
        cross_bigram_minimum=min(bigram_values),
        cross_bigram_maximum=max(bigram_values),
        cross_bigram_sum=sum(bigram_values),
        within_bigram_collisions=within_message_bigram_collisions(messages),
        bigram_positions=sum(max(0, len(message) - 1) for message in messages),
    )
