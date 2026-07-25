"""Label-invariant audit of the final-row reset-to-context bridges."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.gap_anchor import (
    FINAL_MESSAGES,
    GapAnchor,
    clean_gap_anchors,
    final_trimmed_bodies,
)
from eye_mystery.ninth_causal import (
    CONTEXT_SPECS,
    SynchronizationProfile,
    equality_signature,
    synchronization_profile,
)
from eye_mystery.seventeenth_state import shuffle_without_adjacent_doubles


TARGET_GAP = 11
FULL_FRAME_OFFSET = 21
TARGET_LCP = 17
EAST_PAIR = ("east4", "east5")
BOUNDARY_VARIANTS = (
    (True, False),
    (False, False),
    (True, True),
    (False, True),
)


@dataclass(frozen=True)
class BridgeSpec:
    message: str
    anchor_start_trimmed: int
    anchor_value: int
    endpoint_full: int
    late_entry_full: int

    @property
    def length(self) -> int:
        return self.late_entry_full - self.endpoint_full


def canonical_streams() -> dict[str, tuple[int, ...]]:
    return {
        name: tuple(trigram_values(MESSAGES[name]))
        for name in FINAL_MESSAGES
    }


def _late_entries() -> dict[str, int]:
    entries: dict[str, int] = {}
    for name, left, left_start, right, right_start, _length in CONTEXT_SPECS:
        if name not in {"last-west4", "last-east5"}:
            continue
        for message, start in ((left, left_start), (right, right_start)):
            previous = entries.setdefault(message, start)
            if previous != start:
                raise AssertionError("late contexts disagree on an entry")
    if set(entries) != set(FINAL_MESSAGES):
        raise AssertionError("late contexts do not cover the final row")
    return entries


def bridge_specs() -> dict[str, BridgeSpec]:
    """Derive bridge boundaries from the fixed anchors and late contexts."""

    trimmed = final_trimmed_bodies()
    late_entries = _late_entries()
    specs = {}
    for name in FINAL_MESSAGES:
        hits = clean_gap_anchors(
            trimmed[name],
            minimum_gap=TARGET_GAP,
            maximum_gap=TARGET_GAP,
        ).get(TARGET_GAP, ())
        if len(hits) != 1:
            raise AssertionError("final body lacks its unique gap-11 anchor")
        anchor = hits[0]
        endpoint_full = (
            FULL_FRAME_OFFSET + anchor.position + TARGET_GAP
        )
        specs[name] = BridgeSpec(
            message=name,
            anchor_start_trimmed=anchor.position,
            anchor_value=anchor.value,
            endpoint_full=endpoint_full,
            late_entry_full=late_entries[name],
        )
    return specs


def bridge_segments(
    streams: Mapping[str, Sequence[int]],
    *,
    include_endpoint: bool = True,
    include_entry: bool = False,
) -> dict[str, tuple[int, ...]]:
    specs = bridge_specs()
    return {
        name: tuple(
            streams[name][
                spec.endpoint_full + int(not include_endpoint) :
                spec.late_entry_full + int(include_entry)
            ]
        )
        for name, spec in specs.items()
    }


def common_prefix_length(sequences: Sequence[Sequence[int]]) -> int:
    if not sequences:
        return 0
    limit = min(map(len, sequences))
    for index in range(limit):
        if len({sequence[index] for sequence in sequences}) != 1:
            return index
    return limit


@dataclass(frozen=True)
class BridgeMetrics:
    signatures: tuple[tuple[int, ...], ...]
    triple_lcp: int
    east_profile: SynchronizationProfile
    east_complete: bool
    east_switch: bool

    @property
    def joint(self) -> bool:
        return (
            self.triple_lcp >= TARGET_LCP
            and self.east_complete
            and self.east_switch
        )


def bridge_metrics(
    segments: Mapping[str, Sequence[int]],
    entry_pair: tuple[int, int],
) -> BridgeMetrics:
    signatures = tuple(
        equality_signature(segments[name])
        for name in FINAL_MESSAGES
    )
    east_left = tuple(segments[EAST_PAIR[0]])
    east_right = tuple(segments[EAST_PAIR[1]])
    east_profile = synchronization_profile(east_left, east_right)
    east_complete = (
        len(east_left) == len(east_right)
        and east_profile.first_conflict is None
    )
    extended = synchronization_profile(
        east_left + (entry_pair[0],),
        east_right + (entry_pair[1],),
    )
    east_switch = (
        east_complete
        and extended.first_conflict == len(east_left)
    )
    return BridgeMetrics(
        signatures=signatures,
        triple_lcp=common_prefix_length(signatures),
        east_profile=east_profile,
        east_complete=east_complete,
        east_switch=east_switch,
    )


def observed_metrics(
    streams: Mapping[str, Sequence[int]] | None = None,
) -> BridgeMetrics:
    streams = canonical_streams() if streams is None else streams
    segments = bridge_segments(streams)
    specs = bridge_specs()
    entry_pair = tuple(
        streams[name][specs[name].late_entry_full]
        for name in EAST_PAIR
    )
    return bridge_metrics(
        segments,
        (entry_pair[0], entry_pair[1]),
    )


def late_context_profiles(
    streams: Mapping[str, Sequence[int]] | None = None,
) -> dict[str, SynchronizationProfile]:
    streams = canonical_streams() if streams is None else streams
    profiles = {}
    for name, left, left_start, right, right_start, length in CONTEXT_SPECS:
        if name not in {"last-west4", "last-east5"}:
            continue
        profiles[name] = synchronization_profile(
            streams[left][left_start : left_start + length],
            streams[right][right_start : right_start + length],
        )
    return profiles


@dataclass(frozen=True)
class BroadMetrics:
    maximum_triple_lcp: int
    any_pair_complete: bool
    any_joint: bool


def broad_metrics(
    streams: Mapping[str, Sequence[int]],
    *,
    target_lcp: int = TARGET_LCP,
) -> BroadMetrics:
    maximum_lcp = 0
    any_pair = False
    any_joint = False
    for include_endpoint, include_entry in BOUNDARY_VARIANTS:
        segments = bridge_segments(
            streams,
            include_endpoint=include_endpoint,
            include_entry=include_entry,
        )
        signatures = {
            name: equality_signature(segment)
            for name, segment in segments.items()
        }
        lcp = common_prefix_length(tuple(signatures.values()))
        pair_complete = False
        for left, right in combinations(FINAL_MESSAGES, 2):
            limit = min(len(signatures[left]), len(signatures[right]))
            if signatures[left][:limit] == signatures[right][:limit]:
                pair_complete = True
        maximum_lcp = max(maximum_lcp, lcp)
        any_pair |= pair_complete
        any_joint |= pair_complete and lcp >= target_lcp
    return BroadMetrics(maximum_lcp, any_pair, any_joint)


def _anchor_preserved(
    stream: Sequence[int],
    spec: BridgeSpec,
) -> bool:
    trimmed = tuple(stream[FULL_FRAME_OFFSET:])
    hits = clean_gap_anchors(
        trimmed,
        minimum_gap=TARGET_GAP,
        maximum_gap=TARGET_GAP,
    ).get(TARGET_GAP, ())
    return hits == (
        GapAnchor(spec.anchor_start_trimmed, spec.anchor_value),
    )


def shuffle_one_bridge(
    stream: Sequence[int],
    spec: BridgeSpec,
    rng: random.Random,
    *,
    max_attempts: int = 10000,
) -> tuple[int, ...]:
    """Shuffle only one bridge while preserving every frozen nuisance."""

    stream = tuple(stream)
    endpoint = spec.endpoint_full
    entry = spec.late_entry_full
    fixed_first = stream[endpoint]
    suffix = stream[endpoint + 1 : entry]
    for _ in range(max_attempts):
        shuffled = shuffle_without_adjacent_doubles(suffix, rng)
        if shuffled and (
            fixed_first == shuffled[0]
            or shuffled[-1] == stream[entry]
        ):
            continue
        candidate = (
            stream[:endpoint]
            + (fixed_first,)
            + shuffled
            + stream[entry:]
        )
        if any(
            left == right
            for left, right in zip(candidate, candidate[1:])
        ):
            continue
        if _anchor_preserved(candidate, spec):
            return candidate
    raise RuntimeError("failed to produce a matched bridge shuffle")


def shuffled_bridge_streams(
    streams: Mapping[str, Sequence[int]],
    rng: random.Random,
    *,
    messages: Sequence[str] = FINAL_MESSAGES,
) -> dict[str, tuple[int, ...]]:
    specs = bridge_specs()
    selected = set(messages)
    return {
        name: (
            shuffle_one_bridge(streams[name], specs[name], rng)
            if name in selected
            else tuple(streams[name])
        )
        for name in FINAL_MESSAGES
    }


@dataclass(frozen=True)
class BridgeControlAudit:
    controls: int
    seed: int
    observed: BridgeMetrics
    observed_broad: BroadMetrics
    triple_lcp_exceedances: int
    east_complete_exceedances: int
    east_switch_exceedances: int
    joint_exceedances: int
    conditioned_w4_exceedances: int
    broad_lcp_exceedances: int
    broad_pair_exceedances: int
    broad_joint_exceedances: int

    @staticmethod
    def corrected_tail(exceedances: int, controls: int) -> float:
        return (exceedances + 1) / (controls + 1)


def audit_controls(
    *,
    controls: int = 50000,
    seed: int = 0xB1236E,
) -> BridgeControlAudit:
    """Run the frozen independent and W4-conditioned matched controls."""

    if controls < 1:
        raise ValueError("at least one control is required")
    rng = random.Random(seed)
    canonical = canonical_streams()
    observed = observed_metrics(canonical)
    observed_broad = broad_metrics(canonical)
    counts = {
        "triple": 0,
        "east_complete": 0,
        "east_switch": 0,
        "joint": 0,
        "w4": 0,
        "broad_lcp": 0,
        "broad_pair": 0,
        "broad_joint": 0,
    }
    for _ in range(controls):
        shuffled = shuffled_bridge_streams(canonical, rng)
        metrics = observed_metrics(shuffled)
        broad = broad_metrics(shuffled)
        counts["triple"] += metrics.triple_lcp >= observed.triple_lcp
        counts["east_complete"] += metrics.east_complete
        counts["east_switch"] += metrics.east_switch
        counts["joint"] += metrics.joint
        counts["broad_lcp"] += (
            broad.maximum_triple_lcp
            >= observed_broad.maximum_triple_lcp
        )
        counts["broad_pair"] += broad.any_pair_complete
        counts["broad_joint"] += broad.any_joint

        conditioned = shuffled_bridge_streams(
            canonical,
            rng,
            messages=("west4",),
        )
        counts["w4"] += (
            observed_metrics(conditioned).triple_lcp
            >= observed.triple_lcp
        )
    return BridgeControlAudit(
        controls=controls,
        seed=seed,
        observed=observed,
        observed_broad=observed_broad,
        triple_lcp_exceedances=counts["triple"],
        east_complete_exceedances=counts["east_complete"],
        east_switch_exceedances=counts["east_switch"],
        joint_exceedances=counts["joint"],
        conditioned_w4_exceedances=counts["w4"],
        broad_lcp_exceedances=counts["broad_lcp"],
        broad_pair_exceedances=counts["broad_pair"],
        broad_joint_exceedances=counts["broad_joint"],
    )
