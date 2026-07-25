"""Cross-phase equality-class overlap audit for the final state trace."""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import cache
from fractions import Fraction
from itertools import combinations

from eye_mystery.factoradic_headers import header_ranks
from eye_mystery.gap_anchor import FINAL_MESSAGES
from eye_mystery.ninth_causal import equality_signature
from eye_mystery.phase_ledger import (
    NEWLINE_SYMBOL,
    row2_circulation,
    symbol_preimage,
)
from eye_mystery.synchronizing_bridge import (
    bridge_specs,
    canonical_streams,
    observed_metrics,
)


NEW_PHASE_LENGTH = 30
EAST_MESSAGES = ("east4", "east5")

ClassEdge = tuple[int, int]
MultiplicityType = tuple[int, int]


@dataclass(frozen=True)
class PanelOverlapProfile:
    message: str
    old_multiplicities: tuple[tuple[int, int], ...]
    new_multiplicities: tuple[tuple[int, int], ...]
    overlap_types: tuple[tuple[MultiplicityType, int], ...]
    observed_edges: tuple[ClassEdge, ...]

    def old_counts(self) -> dict[int, int]:
        return dict(self.old_multiplicities)

    def new_counts(self) -> dict[int, int]:
        return dict(self.new_multiplicities)

    def type_counts(self) -> Counter[MultiplicityType]:
        return Counter(dict(self.overlap_types))


@cache
def phase_sequences() -> dict[str, tuple[tuple[int, ...], tuple[int, ...]]]:
    streams = canonical_streams()
    specs = bridge_specs()
    return {
        name: (
            tuple(
                streams[name][
                    specs[name].endpoint_full :
                    specs[name].late_entry_full
                ]
            ),
            tuple(
                streams[name][
                    specs[name].late_entry_full :
                    specs[name].late_entry_full + NEW_PHASE_LENGTH
                ]
            ),
        )
        for name in FINAL_MESSAGES
    }


def _class_map(sequence: Sequence[int]) -> tuple[dict[int, int], Counter[int]]:
    signature = equality_signature(sequence)
    classes = {
        value: signature[index]
        for index, value in enumerate(sequence)
    }
    return classes, Counter(signature)


@cache
def panel_overlap_profiles() -> dict[str, PanelOverlapProfile]:
    profiles = {}
    for name, (old, new) in phase_sequences().items():
        old_classes, old_counts = _class_map(old)
        new_classes, new_counts = _class_map(new)
        edges = tuple(
            sorted(
                (old_classes[value], new_classes[value])
                for value in set(old_classes) & set(new_classes)
            )
        )
        types = Counter(
            (old_counts[left], new_counts[right])
            for left, right in edges
        )
        profiles[name] = PanelOverlapProfile(
            message=name,
            old_multiplicities=tuple(sorted(old_counts.items())),
            new_multiplicities=tuple(sorted(new_counts.items())),
            overlap_types=tuple(sorted(types.items())),
            observed_edges=edges,
        )
    return profiles


@dataclass(frozen=True)
class LedgerTarget:
    old_class: int
    new_class: int
    new_position: int
    budget: int
    common_phase: int
    east_newline_preimage: int

    @property
    def edge(self) -> ClassEdge:
        return self.old_class, self.new_class


@cache
def ledger_target() -> LedgerTarget:
    ranks = header_ranks()
    budget = row2_circulation(ranks)
    common = observed_metrics().triple_lcp
    newline = symbol_preimage(ranks["east4"], NEWLINE_SYMBOL)
    new_class = budget + common
    new_position = new_class + newline
    return LedgerTarget(
        old_class=budget,
        new_class=new_class,
        new_position=new_position,
        budget=budget,
        common_phase=common,
        east_newline_preimage=newline,
    )


@cache
def new_class_positions(message: str, class_id: int) -> tuple[int, ...]:
    new = phase_sequences()[message][1]
    signature = equality_signature(new)
    return tuple(
        index for index, value in enumerate(signature) if value == class_id
    )


@dataclass(frozen=True)
class OverlapMetrics:
    east_target: bool
    east_only: bool
    shared_offset17: bool
    any_shared_edge: bool
    shared_edges: tuple[tuple[tuple[str, str], ClassEdge], ...]


def overlap_metrics(
    edges: Mapping[str, Sequence[ClassEdge]],
) -> OverlapMetrics:
    edge_sets = {name: set(edges[name]) for name in FINAL_MESSAGES}
    target = ledger_target().edge
    east_target = all(target in edge_sets[name] for name in EAST_MESSAGES)
    shared = []
    for left, right in combinations(FINAL_MESSAGES, 2):
        for edge in sorted(edge_sets[left] & edge_sets[right]):
            shared.append(((left, right), edge))
    shared_offset17 = any(
        new - old == ledger_target().common_phase
        for _pair, (old, new) in shared
    )
    return OverlapMetrics(
        east_target=east_target,
        east_only=east_target and target not in edge_sets["west4"],
        shared_offset17=shared_offset17,
        any_shared_edge=bool(shared),
        shared_edges=tuple(shared),
    )


def observed_overlap_metrics() -> OverlapMetrics:
    profiles = panel_overlap_profiles()
    return overlap_metrics(
        {
            name: profile.observed_edges
            for name, profile in profiles.items()
        }
    )


def sample_overlap_edges(
    profile: PanelOverlapProfile,
    rng: random.Random,
) -> tuple[ClassEdge, ...]:
    """Randomize compatible class links while preserving every type count."""

    tokens = [
        overlap_type
        for overlap_type, count in profile.overlap_types
        for _ in range(count)
    ]
    old_counts = profile.old_counts()
    new_counts = profile.new_counts()
    old_assignment: list[int | None] = [None] * len(tokens)
    new_assignment: list[int | None] = [None] * len(tokens)
    for multiplicity in sorted(set(old_count for old_count, _ in tokens)):
        indices = [
            index
            for index, (old_count, _new_count) in enumerate(tokens)
            if old_count == multiplicity
        ]
        candidates = [
            class_id
            for class_id, count in old_counts.items()
            if count == multiplicity
        ]
        selected = rng.sample(candidates, len(indices))
        for index, class_id in zip(indices, selected, strict=True):
            old_assignment[index] = class_id
    for multiplicity in sorted(set(new_count for _, new_count in tokens)):
        indices = [
            index
            for index, (_old_count, new_count) in enumerate(tokens)
            if new_count == multiplicity
        ]
        candidates = [
            class_id
            for class_id, count in new_counts.items()
            if count == multiplicity
        ]
        selected = rng.sample(candidates, len(indices))
        for index, class_id in zip(indices, selected, strict=True):
            new_assignment[index] = class_id
    if any(value is None for value in old_assignment + new_assignment):
        raise AssertionError("overlap token was not assigned")
    return tuple(
        sorted(
            (int(old), int(new))
            for old, new in zip(
                old_assignment,
                new_assignment,
                strict=True,
            )
        )
    )


def overlap_type_profile(
    profile: PanelOverlapProfile,
    edges: Sequence[ClassEdge],
) -> Counter[MultiplicityType]:
    old_counts = profile.old_counts()
    new_counts = profile.new_counts()
    return Counter(
        (old_counts[left], new_counts[right])
        for left, right in edges
    )


def exact_edge_probability(
    profile: PanelOverlapProfile,
    edge: ClassEdge,
) -> Fraction:
    """Return the exact marginal probability of one compatible class edge."""

    old, new = edge
    old_counts = profile.old_counts()
    new_counts = profile.new_counts()
    overlap_type = (old_counts[old], new_counts[new])
    tokens = profile.type_counts()[overlap_type]
    old_slots = sum(
        count == overlap_type[0]
        for count in old_counts.values()
    )
    new_slots = sum(
        count == overlap_type[1]
        for count in new_counts.values()
    )
    return Fraction(tokens, old_slots * new_slots)


@dataclass(frozen=True)
class OverlapControlAudit:
    controls: int
    seed: int
    observed: OverlapMetrics
    east_target_exceedances: int
    east_only_exceedances: int
    shared_offset17_exceedances: int
    any_shared_edge_exceedances: int
    exact_east_target_probability: Fraction
    exact_east_only_probability: Fraction

    @staticmethod
    def corrected_tail(exceedances: int, controls: int) -> float:
        return (exceedances + 1) / (controls + 1)


def audit_controls(
    *,
    controls: int = 50000,
    seed: int = 0xCACE17,
) -> OverlapControlAudit:
    if controls < 1:
        raise ValueError("at least one control is required")
    rng = random.Random(seed)
    profiles = panel_overlap_profiles()
    observed = observed_overlap_metrics()
    target = ledger_target().edge
    target_probabilities = {
        name: exact_edge_probability(profile, target)
        for name, profile in profiles.items()
    }
    exact_east = (
        target_probabilities["east4"]
        * target_probabilities["east5"]
    )
    exact_east_only = exact_east * (
        1 - target_probabilities["west4"]
    )
    counts = {
        "target": 0,
        "only": 0,
        "offset": 0,
        "shared": 0,
    }
    for _ in range(controls):
        edges = {
            name: sample_overlap_edges(profile, rng)
            for name, profile in profiles.items()
        }
        metrics = overlap_metrics(edges)
        counts["target"] += metrics.east_target
        counts["only"] += metrics.east_only
        counts["offset"] += metrics.shared_offset17
        counts["shared"] += metrics.any_shared_edge
    return OverlapControlAudit(
        controls=controls,
        seed=seed,
        observed=observed,
        east_target_exceedances=counts["target"],
        east_only_exceedances=counts["only"],
        shared_offset17_exceedances=counts["offset"],
        any_shared_edge_exceedances=counts["shared"],
        exact_east_target_probability=exact_east,
        exact_east_only_probability=exact_east_only,
    )
