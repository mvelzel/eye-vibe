"""Matched-control audit of the final-row gap-anchor/header relation."""

from __future__ import annotations

import itertools
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.fifteenth_second import NATURAL_OPENING_TRIMS
from eye_mystery.seventeenth_state import shuffle_without_adjacent_doubles


MODULUS = 83
FINAL_MESSAGES = ("east4", "west4", "east5")
FINAL_HEADERS = (27, 77, 33)
TARGET_GAP = 11
BROAD_GAPS = tuple(range(2, 31))


def final_trimmed_bodies() -> dict[str, tuple[int, ...]]:
    """Return final-row bodies after marker and copied-opening removal."""

    return {
        name: tuple(trigram_values(MESSAGES[name]))[
            1 + NATURAL_OPENING_TRIMS[name] :
        ]
        for name in FINAL_MESSAGES
    }


@dataclass(frozen=True)
class GapAnchor:
    position: int
    value: int


def clean_gap_anchors(
    stream: Sequence[int],
    *,
    minimum_gap: int = min(BROAD_GAPS),
    maximum_gap: int = max(BROAD_GAPS),
) -> dict[int, tuple[GapAnchor, ...]]:
    """Find endpoint repeats whose intervening window has no other equality."""

    if minimum_gap < 1 or maximum_gap < minimum_gap:
        raise ValueError("invalid gap range")
    positions: dict[int, list[int]] = {}
    for index, value in enumerate(stream):
        positions.setdefault(value, []).append(index)

    hits: dict[int, list[GapAnchor]] = {}
    for value, value_positions in positions.items():
        for left_index, left in enumerate(value_positions):
            for right in value_positions[left_index + 1 :]:
                gap = right - left
                if gap > maximum_gap:
                    break
                if gap < minimum_gap:
                    continue
                window = stream[left : right + 1]
                if len(set(window)) == gap:
                    hits.setdefault(gap, []).append(GapAnchor(left, value))
    return {
        gap: tuple(sorted(anchors, key=lambda anchor: anchor.position))
        for gap, anchors in hits.items()
    }


def unique_anchor_values(
    streams: Mapping[str, Sequence[int]],
    gap: int,
) -> tuple[int, int, int] | None:
    """Return final-row anchor values when every stream has exactly one hit."""

    values = []
    for name in FINAL_MESSAGES:
        hits = clean_gap_anchors(
            streams[name],
            minimum_gap=gap,
            maximum_gap=gap,
        ).get(gap, ())
        if len(hits) != 1:
            return None
        values.append(hits[0].value)
    return tuple(values)  # type: ignore[return-value]


def exact_reported_relation(
    anchors: Sequence[int],
    headers: Sequence[int] = FINAL_HEADERS,
) -> bool:
    """Check the exact message-ordered relation reported in Discord."""

    if len(anchors) != 3 or len(headers) != 3:
        raise ValueError("relation requires three anchors and three headers")
    east4, west4, east5 = anchors
    return tuple(headers) == (
        (east4 - east5) % MODULUS,
        (east4 - west4) % MODULUS,
        (west4 - east5) % MODULUS,
    )


def broad_difference_relation(
    anchors: Sequence[int],
    headers: Sequence[int] = FINAL_HEADERS,
) -> bool:
    """Allow every anchor ordering and header-to-edge assignment."""

    if len(anchors) != 3 or len(headers) != 3:
        raise ValueError("relation requires three anchors and three headers")
    target = sorted(headers)
    return any(
        sorted(
            (
                (first - second) % MODULUS,
                (first - third) % MODULUS,
                (second - third) % MODULUS,
            )
        )
        == target
        for first, second, third in itertools.permutations(anchors)
    )


def any_broad_gap_match(
    streams: Mapping[str, Sequence[int]],
) -> tuple[int, tuple[int, int, int]] | None:
    """Search the complete preregistered gap and anchor-order family."""

    by_message = {
        name: clean_gap_anchors(streams[name])
        for name in FINAL_MESSAGES
    }
    for gap in BROAD_GAPS:
        hits = tuple(by_message[name].get(gap, ()) for name in FINAL_MESSAGES)
        if not all(len(message_hits) == 1 for message_hits in hits):
            continue
        anchors = tuple(message_hits[0].value for message_hits in hits)
        if broad_difference_relation(anchors):
            return gap, anchors  # type: ignore[return-value]
    return None


def planted_gap_streams() -> dict[str, tuple[int, ...]]:
    """Return a short exact detector plant with the real anchor relation."""

    anchors = (75, 81, 48)
    streams = {}
    for name, anchor in zip(FINAL_MESSAGES, anchors, strict=True):
        interior = tuple(range(10))
        trailing = tuple(range(10, 18))
        streams[name] = (anchor,) + interior + (anchor,) + trailing
    return streams


@dataclass(frozen=True)
class GapAnchorAudit:
    real_positions: tuple[int, int, int]
    real_anchors: tuple[int, int, int]
    predicted_nonreference: tuple[int, int]
    controls: int
    targeted_structure_controls: int
    targeted_relation_controls: int
    broad_relation_controls: int
    targeted_corrected_tail: float
    broad_corrected_tail: float

    @property
    def passes(self) -> bool:
        return (
            self.predicted_nonreference == self.real_anchors[1:]
            and self.targeted_corrected_tail < 0.01
            and self.broad_corrected_tail < 0.01
        )


def gap_anchor_audit(
    *,
    controls: int = 50_000,
    seed: int = 0x18A11,
) -> GapAnchorAudit:
    """Run targeted and fully selection-corrected matched controls."""

    if controls < 1:
        raise ValueError("at least one control is required")
    streams = final_trimmed_bodies()
    real_hits = tuple(
        clean_gap_anchors(
            streams[name],
            minimum_gap=TARGET_GAP,
            maximum_gap=TARGET_GAP,
        ).get(TARGET_GAP, ())
        for name in FINAL_MESSAGES
    )
    if not all(len(hits) == 1 for hits in real_hits):
        raise AssertionError("real target gap is not uniquely selected")
    positions = tuple(hits[0].position for hits in real_hits)
    anchors = tuple(hits[0].value for hits in real_hits)
    if not exact_reported_relation(anchors):
        raise AssertionError("real exact relation does not reproduce")
    if any_broad_gap_match(streams) is None:
        raise AssertionError("real broad relation does not reproduce")

    predicted = (
        (anchors[0] - FINAL_HEADERS[1]) % MODULUS,
        (anchors[0] - FINAL_HEADERS[0]) % MODULUS,
    )

    rng = random.Random(seed)
    targeted_structure = 0
    targeted_relation = 0
    broad_relation = 0
    for _ in range(controls):
        shuffled = {
            name: shuffle_without_adjacent_doubles(streams[name], rng)
            for name in FINAL_MESSAGES
        }
        control_anchors = unique_anchor_values(shuffled, TARGET_GAP)
        if control_anchors is not None:
            targeted_structure += 1
            targeted_relation += exact_reported_relation(control_anchors)
        broad_relation += any_broad_gap_match(shuffled) is not None

    return GapAnchorAudit(
        positions,  # type: ignore[arg-type]
        anchors,  # type: ignore[arg-type]
        predicted,
        controls,
        targeted_structure,
        targeted_relation,
        broad_relation,
        (1 + targeted_relation) / (1 + controls),
        (1 + broad_relation) / (1 + controls),
    )


@dataclass(frozen=True)
class GapAnchorLabelAudit:
    controls: int
    body_only_exact_matches: int
    body_only_broad_matches: int
    joint_exact_matches: int
    joint_broad_matches: int
    body_only_exact_tail: float
    body_only_broad_tail: float
    joint_exact_tail: float
    joint_broad_tail: float

    @property
    def natural_coordinate_passes(self) -> bool:
        return (
            self.body_only_broad_tail < 0.01
            and self.joint_broad_tail < 0.01
        )


def gap_anchor_label_audit(
    *,
    controls: int = 50_000,
    seed: int = 0x18B0D,
) -> GapAnchorLabelAudit:
    """Run the frozen body-only and joint global-label nulls."""

    if controls < 1:
        raise ValueError("at least one control is required")
    anchors = (75, 81, 48)
    headers = FINAL_HEADERS
    rng = random.Random(seed)
    body_exact = 0
    body_broad = 0
    joint_exact = 0
    joint_broad = 0
    permutation = list(range(MODULUS))
    for _ in range(controls):
        rng.shuffle(permutation)
        mapped_anchors = tuple(permutation[value] for value in anchors)
        mapped_headers = tuple(permutation[value] for value in headers)
        body_exact += exact_reported_relation(mapped_anchors, headers)
        body_broad += broad_difference_relation(mapped_anchors, headers)
        joint_exact += exact_reported_relation(
            mapped_anchors,
            mapped_headers,
        )
        joint_broad += broad_difference_relation(
            mapped_anchors,
            mapped_headers,
        )

    denominator = controls + 1
    return GapAnchorLabelAudit(
        controls,
        body_exact,
        body_broad,
        joint_exact,
        joint_broad,
        (1 + body_exact) / denominator,
        (1 + body_broad) / denominator,
        (1 + joint_exact) / denominator,
        (1 + joint_broad) / denominator,
    )
