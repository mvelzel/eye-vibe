"""Exact conditional audit of the odd-East checksum self-pointer."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb

from eye_mystery.corpus import MESSAGES, trigram_values


MESSAGES_UNDER_TEST = ("east1", "east3", "east5")
HOLDOUT_MESSAGES = ("west1", "east2", "west2", "west3", "east4", "west4")
TYPED_TARGETS = (7, 11, 30)
CONSTRUCTION_LEDGER = (6, 7, 9, 11, 15, 16, 17, 18, 20, 21, 25, 26, 28, 29, 30, 34)
MACHINE_SCALAR_LEDGER = (3, 4, 6, 7, 11, 13, 15, 17, 20, 21, 25, 28, 29, 30, 34)
PACKET_SUM_TARGETS = (20, 45, 30)
ODD_EAST_HEADERS = (50, 63, 33)
HEADER_RESIDUALS = (30, 18, 3)
FIELD_SETS = (
    frozenset((27, 77, 33)),
    frozenset((40, 56, 45)),
    frozenset((75, 81, 48)),
)
FIELD_NAMES = ("final-headers", "checksum-quotients", "final-anchors")


@dataclass(frozen=True)
class SelfPointerProfile:
    name: str
    length: int
    total: int
    quotient: int
    remainder: int
    positions: tuple[int, ...]
    distances: tuple[int, ...]

    @property
    def body_occurrences(self) -> int:
        return len(self.positions)


@dataclass(frozen=True)
class SelfPointerAudit:
    profiles: tuple[SelfPointerProfile, ...]
    exact_typed_probability: Fraction
    permutation_probability: Fraction
    permutation_numerator: int
    permutation_denominator: int
    typed_coordinate_probability: Fraction
    any_hit_assignment_probability: Fraction
    all_hit_assignment_probability: Fraction
    typed_coordinate_observed: bool
    any_hit_assignment_observed: bool
    all_hit_assignment_observed: bool
    circular_packets: tuple[tuple[int, ...], ...]
    ledger_containment_probability: Fraction
    packet_sum_probability: Fraction
    packet_sum_permutation_probability: Fraction
    holdout_profiles: tuple[SelfPointerProfile, ...]
    holdout_packets: tuple[tuple[int, ...], ...]
    holdout_viable: bool
    holdout_in_ledger: bool
    holdout_ledger_probability: Fraction
    header_residual_assignment_probability: Fraction


def euclidean_profile(name: str) -> SelfPointerProfile:
    values = trigram_values(MESSAGES[name])
    total = sum(values)
    quotient, remainder = divmod(total, 101)
    positions = tuple(
        position
        for position, value in enumerate(values)
        if position > 0 and value == quotient
    )
    return SelfPointerProfile(
        name=name,
        length=len(values),
        total=total,
        quotient=quotient,
        remainder=remainder,
        positions=positions,
        distances=tuple(abs(position - quotient) for position in positions),
    )


def profile(name: str) -> SelfPointerProfile:
    item = euclidean_profile(name)
    if item.remainder:
        raise ValueError(f"{name} full sum is not divisible by 101")
    return item


def canonical_profiles() -> tuple[SelfPointerProfile, ...]:
    return tuple(profile(name) for name in MESSAGES_UNDER_TEST)


def holdout_profiles() -> tuple[SelfPointerProfile, ...]:
    return tuple(euclidean_profile(name) for name in HOLDOUT_MESSAGES)


def _eligible_position_count(item: SelfPointerProfile, target: int) -> int:
    return sum(
        abs(position - item.quotient) == target
        for position in range(1, item.length)
    )


def target_hit_probability(item: SelfPointerProfile, target: int) -> Fraction:
    """Probability that at least one conditioned occurrence hits a target."""

    body_positions = item.length - 1
    occurrences = item.body_occurrences
    eligible = _eligible_position_count(item, target)
    total = comb(body_positions, occurrences)
    misses = comb(body_positions - eligible, occurrences)
    return Fraction(total - misses, total)


def exact_typed_probability(
    profiles: tuple[SelfPointerProfile, ...] | None = None,
) -> Fraction:
    profiles = canonical_profiles() if profiles is None else profiles
    probability = Fraction(1, 1)
    for item, target in zip(profiles, TYPED_TARGETS, strict=True):
        probability *= target_hit_probability(item, target)
    return probability


def target_mask_distribution(
    item: SelfPointerProfile,
    targets: tuple[int, ...] = TYPED_TARGETS,
) -> Counter[int]:
    """Count conditioned position subsets by the targets that they hit."""

    counts: Counter[int] = Counter()
    for positions in combinations(
        range(1, item.length),
        item.body_occurrences,
    ):
        mask = 0
        for target_index, target in enumerate(targets):
            if any(abs(position - item.quotient) == target for position in positions):
                mask |= 1 << target_index
        counts[mask] += 1
    return counts


def _has_perfect_target_matching(masks: tuple[int, ...]) -> bool:
    return any(
        all(mask & (1 << target) for mask, target in zip(masks, order, strict=True))
        for order in permutations(range(len(masks)))
    )


def _matching_probability(
    distributions: tuple[Counter[int], ...],
) -> Fraction:
    numerator = 0
    for entries in product(*(tuple(counts.items()) for counts in distributions)):
        masks = tuple(mask for mask, _count in entries)
        if _has_perfect_target_matching(masks):
            numerator += product_int(count for _mask, count in entries)
    denominator = product_int(sum(counts.values()) for counts in distributions)
    return Fraction(numerator, denominator)


def permutation_probability(
    profiles: tuple[SelfPointerProfile, ...] | None = None,
) -> tuple[int, int, Fraction]:
    """Exact null probability after allowing every target-to-message assignment."""

    profiles = canonical_profiles() if profiles is None else profiles
    distributions = tuple(target_mask_distribution(item) for item in profiles)
    numerator = 0
    for entries in product(*(tuple(counts.items()) for counts in distributions)):
        masks = tuple(mask for mask, _count in entries)
        if _has_perfect_target_matching(masks):
            numerator += product_int(count for _mask, count in entries)
    denominator = product_int(sum(counts.values()) for counts in distributions)
    return numerator, denominator, Fraction(numerator, denominator)


def _field_mask_distribution(
    item: SelfPointerProfile,
    *,
    require_all: bool,
) -> Counter[int]:
    counts: Counter[int] = Counter()
    for positions in combinations(
        range(1, item.length),
        item.body_occurrences,
    ):
        position_set = frozenset(positions)
        mask = 0
        for field_index, field in enumerate(FIELD_SETS):
            matches = (
                position_set <= field
                if require_all
                else not position_set.isdisjoint(field)
            )
            if matches:
                mask |= 1 << field_index
        counts[mask] += 1
    return counts


def field_assignment_probability(
    profiles: tuple[SelfPointerProfile, ...] | None = None,
    *,
    require_all: bool,
) -> Fraction:
    profiles = canonical_profiles() if profiles is None else profiles
    distributions = tuple(
        _field_mask_distribution(item, require_all=require_all)
        for item in profiles
    )
    return _matching_probability(distributions)


def typed_coordinate_probability(
    profiles: tuple[SelfPointerProfile, ...] | None = None,
) -> Fraction:
    profiles = canonical_profiles() if profiles is None else profiles
    probability = Fraction(
        comb(len(FIELD_SETS[0]), profiles[0].body_occurrences),
        comb(profiles[0].length - 1, profiles[0].body_occurrences),
    )
    for item, field in zip(profiles[1:], FIELD_SETS[1:], strict=True):
        body_positions = item.length - 1
        eligible = len(field)
        probability *= Fraction(
            comb(body_positions, item.body_occurrences)
            - comb(body_positions - eligible, item.body_occurrences),
            comb(body_positions, item.body_occurrences),
        )
    return probability


def observed_field_event(
    profiles: tuple[SelfPointerProfile, ...] | None = None,
    *,
    require_all: bool,
) -> bool:
    profiles = canonical_profiles() if profiles is None else profiles
    masks = []
    for item in profiles:
        position_set = frozenset(item.positions)
        mask = 0
        for field_index, field in enumerate(FIELD_SETS):
            matches = (
                position_set <= field
                if require_all
                else not position_set.isdisjoint(field)
            )
            if matches:
                mask |= 1 << field_index
        masks.append(mask)
    return _has_perfect_target_matching(tuple(masks))


def observed_typed_coordinate_event(
    profiles: tuple[SelfPointerProfile, ...] | None = None,
) -> bool:
    profiles = canonical_profiles() if profiles is None else profiles
    return (
        frozenset(profiles[0].positions) <= FIELD_SETS[0]
        and not frozenset(profiles[1].positions).isdisjoint(FIELD_SETS[1])
        and not frozenset(profiles[2].positions).isdisjoint(FIELD_SETS[2])
    )


def circular_distance(position: int, quotient: int) -> int:
    forward = (position - quotient) % 83
    backward = (quotient - position) % 83
    return min(forward, backward)


def circular_packet(item: SelfPointerProfile) -> tuple[int, ...]:
    return tuple(
        circular_distance(position, item.quotient)
        for position in item.positions
    )


def ledger_containment_probability(
    profiles: tuple[SelfPointerProfile, ...] | None = None,
) -> Fraction:
    profiles = canonical_profiles() if profiles is None else profiles
    ledger = frozenset(MACHINE_SCALAR_LEDGER)
    probability = Fraction(1, 1)
    for item in profiles:
        eligible = sum(
            circular_distance(position, item.quotient) in ledger
            for position in range(1, item.length)
        )
        probability *= Fraction(
            comb(eligible, item.body_occurrences),
            comb(item.length - 1, item.body_occurrences),
        )
    return probability


def packet_sum_distribution(item: SelfPointerProfile) -> Counter[int]:
    counts: Counter[int] = Counter()
    for positions in combinations(
        range(1, item.length),
        item.body_occurrences,
    ):
        counts[
            sum(circular_distance(position, item.quotient) for position in positions)
        ] += 1
    return counts


def packet_sum_probability(
    profiles: tuple[SelfPointerProfile, ...] | None = None,
) -> Fraction:
    profiles = canonical_profiles() if profiles is None else profiles
    distributions = tuple(packet_sum_distribution(item) for item in profiles)
    numerator = product_int(
        distribution[target]
        for distribution, target in zip(
            distributions,
            PACKET_SUM_TARGETS,
            strict=True,
        )
    )
    denominator = product_int(
        sum(distribution.values())
        for distribution in distributions
    )
    return Fraction(numerator, denominator)


def packet_sum_permutation_probability(
    profiles: tuple[SelfPointerProfile, ...] | None = None,
) -> Fraction:
    profiles = canonical_profiles() if profiles is None else profiles
    sum_distributions = tuple(packet_sum_distribution(item) for item in profiles)
    mask_distributions = []
    for distribution in sum_distributions:
        masks: Counter[int] = Counter()
        for packet_sum, count in distribution.items():
            mask = 0
            for target_index, target in enumerate(PACKET_SUM_TARGETS):
                if packet_sum == target:
                    mask |= 1 << target_index
            masks[mask] += count
        mask_distributions.append(masks)
    return _matching_probability(tuple(mask_distributions))


def header_residual_assignment_probability(
    profiles: tuple[SelfPointerProfile, ...] | None = None,
) -> Fraction:
    profiles = canonical_profiles() if profiles is None else profiles
    sum_distributions = tuple(packet_sum_distribution(item) for item in profiles)
    mask_distributions = []
    for header, distribution in zip(
        ODD_EAST_HEADERS,
        sum_distributions,
        strict=True,
    ):
        masks: Counter[int] = Counter()
        for packet_sum, count in distribution.items():
            mask = 0
            for residual_index, residual in enumerate(HEADER_RESIDUALS):
                if packet_sum == header - residual:
                    mask |= 1 << residual_index
            masks[mask] += count
        mask_distributions.append(masks)
    return _matching_probability(tuple(mask_distributions))


def product_int(values: Iterable[int]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def run_audit() -> SelfPointerAudit:
    profiles = canonical_profiles()
    holdouts = holdout_profiles()
    holdout_packets = tuple(circular_packet(item) for item in holdouts)
    ledger = frozenset(MACHINE_SCALAR_LEDGER)
    numerator, denominator, broad = permutation_probability(profiles)
    return SelfPointerAudit(
        profiles=profiles,
        exact_typed_probability=exact_typed_probability(profiles),
        permutation_probability=broad,
        permutation_numerator=numerator,
        permutation_denominator=denominator,
        typed_coordinate_probability=typed_coordinate_probability(profiles),
        any_hit_assignment_probability=field_assignment_probability(
            profiles,
            require_all=False,
        ),
        all_hit_assignment_probability=field_assignment_probability(
            profiles,
            require_all=True,
        ),
        typed_coordinate_observed=observed_typed_coordinate_event(profiles),
        any_hit_assignment_observed=observed_field_event(
            profiles,
            require_all=False,
        ),
        all_hit_assignment_observed=observed_field_event(
            profiles,
            require_all=True,
        ),
        circular_packets=tuple(circular_packet(item) for item in profiles),
        ledger_containment_probability=ledger_containment_probability(profiles),
        packet_sum_probability=packet_sum_probability(profiles),
        packet_sum_permutation_probability=packet_sum_permutation_probability(
            profiles
        ),
        holdout_profiles=holdouts,
        holdout_packets=holdout_packets,
        holdout_viable=all(holdout_packets),
        holdout_in_ledger=all(
            distance in ledger
            for packet in holdout_packets
            for distance in packet
        ),
        holdout_ledger_probability=ledger_containment_probability(holdouts),
        header_residual_assignment_probability=(
            header_residual_assignment_probability(profiles)
        ),
    )
