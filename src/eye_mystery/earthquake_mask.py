"""Prospective audit of the Earthquake circle's irregular 17-bit row."""

from __future__ import annotations

import itertools
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.gap_anchor import (
    FINAL_MESSAGES,
    TARGET_GAP,
    clean_gap_anchors,
    final_trimmed_bodies,
)


MASK = tuple(int(bit) for bit in "11110111011101110")
SLICE_LENGTH = len(MASK)
FINAL_STARTS = (16, 18, 17)
KNOWN_OFFSETS = frozenset((0, TARGET_GAP))
VARIANT_NAMES = (
    "forward-ones",
    "forward-zeros",
    "reverse-ones",
    "reverse-zeros",
)
METRIC_NAMES = (
    "nontrivial_exact_skeleton",
    "common_repeat_pairs",
    "consistent_bijection_support",
    "aligned_numeric_equalities",
)


@dataclass(frozen=True)
class MaskMetrics:
    nontrivial_exact_skeleton: int
    common_repeat_pairs: int
    consistent_bijection_support: int
    aligned_numeric_equalities: int

    def values(self) -> tuple[int, int, int, int]:
        return (
            self.nontrivial_exact_skeleton,
            self.common_repeat_pairs,
            self.consistent_bijection_support,
            self.aligned_numeric_equalities,
        )


@dataclass(frozen=True)
class EarthquakeMaskAudit:
    controls: int
    real_variants: tuple[MaskMetrics, ...]
    real_maxima: tuple[int, int, int, int]
    control_hits: tuple[int, int, int, int]
    metric_tails: tuple[float, float, float, float]
    corrected_tail: float
    shuffle_attempts: int

    @property
    def passes(self) -> bool:
        return (
            max(self.real_maxima) > 0
            and self.corrected_tail < 0.01
        )


def variant_offsets() -> tuple[tuple[int, ...], ...]:
    """Return the registered forward/reverse and one/zero offset family."""

    result = []
    for bits in (MASK, tuple(reversed(MASK))):
        for selected in (1, 0):
            result.append(
                tuple(
                    offset
                    for offset, bit in enumerate(bits)
                    if bit == selected and offset not in KNOWN_OFFSETS
                )
            )
    return tuple(result)


def canonical_skeleton(values: Sequence[int]) -> tuple[int, ...]:
    """Canonicalise a sequence by first occurrence."""

    labels: dict[int, int] = {}
    result = []
    for value in values:
        if value not in labels:
            labels[value] = len(labels)
        result.append(labels[value])
    return tuple(result)


def score_aligned_sequences(
    sequences: Sequence[Sequence[int]],
) -> MaskMetrics:
    """Score three aligned held-out sequences with the frozen metrics."""

    if len(sequences) != 3:
        raise ValueError("mask metrics require exactly three panels")
    lengths = {len(sequence) for sequence in sequences}
    if len(lengths) != 1:
        raise ValueError("aligned sequences must have the same length")

    skeletons = tuple(canonical_skeleton(sequence) for sequence in sequences)
    has_repeat = bool(sequences[0]) and len(set(sequences[0])) < len(sequences[0])
    exact = int(has_repeat and len(set(skeletons)) == 1)

    index_pairs = tuple(itertools.combinations(range(len(sequences[0])), 2))
    relations = tuple(
        frozenset(
            pair
            for pair in index_pairs
            if sequence[pair[0]] == sequence[pair[1]]
        )
        for sequence in sequences
    )
    common = len(set.intersection(*(set(relation) for relation in relations)))

    consistent_support = 0
    for left, right in itertools.combinations(relations, 2):
        support = left | right
        conflicts = left ^ right
        if not conflicts:
            consistent_support += len(support)

    aligned_equalities = sum(
        left == right
        for column in zip(*sequences, strict=True)
        for left, right in itertools.combinations(column, 2)
    )
    return MaskMetrics(exact, common, consistent_support, aligned_equalities)


def score_variants(
    streams: Mapping[str, Sequence[int]],
) -> tuple[MaskMetrics, ...]:
    """Score every registered mask variant on the fixed final slices."""

    if set(streams) != set(FINAL_MESSAGES):
        raise ValueError("mask test requires exactly the three final messages")
    result = []
    for offsets in variant_offsets():
        sequences = tuple(
            tuple(streams[name][start + offset] for offset in offsets)
            for name, start in zip(
                FINAL_MESSAGES,
                FINAL_STARTS,
                strict=True,
            )
        )
        result.append(score_aligned_sequences(sequences))
    return tuple(result)


def metric_maxima(
    variants: Sequence[MaskMetrics],
) -> tuple[int, int, int, int]:
    """Maximise each registered metric over the complete variant family."""

    if not variants:
        raise ValueError("at least one variant is required")
    return tuple(
        max(variant.values()[metric] for variant in variants)
        for metric in range(len(METRIC_NAMES))
    )  # type: ignore[return-value]


def _is_registered_anchor(
    stream: Sequence[int],
    *,
    start: int,
    anchor: int,
) -> bool:
    hits = clean_gap_anchors(
        stream,
        minimum_gap=TARGET_GAP,
        maximum_gap=TARGET_GAP,
    ).get(TARGET_GAP, ())
    return (
        len(hits) == 1
        and hits[0].position == start
        and hits[0].value == anchor
    )


def conditional_anchor_shuffle(
    stream: Sequence[int],
    *,
    start: int,
    rng: random.Random,
    max_attempts: int = 100_000,
) -> tuple[tuple[int, ...], int]:
    """Shuffle a body conditional on its exact promoted gap-anchor witness."""

    if start < 0 or start + TARGET_GAP >= len(stream):
        raise ValueError("registered anchor lies outside the stream")
    anchor = stream[start]
    if stream[start + TARGET_GAP] != anchor:
        raise ValueError("registered anchor endpoints are not equal")

    fixed = {start, start + TARGET_GAP}
    free_indices = tuple(index for index in range(len(stream)) if index not in fixed)
    tokens = [stream[index] for index in free_indices]
    for attempt in range(1, max_attempts + 1):
        rng.shuffle(tokens)
        candidate = [anchor if index in fixed else -1 for index in range(len(stream))]
        for index, value in zip(free_indices, tokens, strict=True):
            candidate[index] = value
        if any(left == right for left, right in zip(candidate, candidate[1:])):
            continue
        if _is_registered_anchor(candidate, start=start, anchor=anchor):
            return tuple(candidate), attempt
    raise RuntimeError("conditional anchor shuffle exhausted its attempt budget")


def planted_mask_streams() -> dict[str, tuple[int, ...]]:
    """Return a detector plant satisfying every registered positive field."""

    anchors = (75, 81, 48)
    repeats = (60, 61, 62)
    aligned = 70
    length = 40
    streams = {}
    for name, start, anchor, repeat in zip(
        FINAL_MESSAGES,
        FINAL_STARTS,
        anchors,
        repeats,
        strict=True,
    ):
        reserved = {anchor, repeat, aligned}
        fillers = iter(value for value in range(83) if value not in reserved)
        stream = [next(fillers) for _ in range(length)]
        stream[start] = anchor
        stream[start + TARGET_GAP] = anchor
        stream[start + 13] = repeat
        stream[start + 14] = aligned
        stream[start + 15] = repeat
        streams[name] = tuple(stream)
    return streams


def earthquake_mask_audit(
    *,
    controls: int = 50_000,
    seed: int = 0x21E17,
) -> EarthquakeMaskAudit:
    """Run the frozen conditional max-family mask audit."""

    if controls < 1:
        raise ValueError("at least one control is required")
    streams = final_trimmed_bodies()
    for name, start in zip(FINAL_MESSAGES, FINAL_STARTS, strict=True):
        anchor = streams[name][start]
        if not _is_registered_anchor(streams[name], start=start, anchor=anchor):
            raise AssertionError(f"{name} lacks its registered gap anchor")
        if start + SLICE_LENGTH > len(streams[name]):
            raise AssertionError(f"{name} is too short for the registered slice")

    real_variants = score_variants(streams)
    real_maxima = metric_maxima(real_variants)
    hits = [0] * len(METRIC_NAMES)
    attempts = 0
    rng = random.Random(seed)
    for _ in range(controls):
        shuffled = {}
        for name, start in zip(FINAL_MESSAGES, FINAL_STARTS, strict=True):
            shuffled[name], used = conditional_anchor_shuffle(
                streams[name],
                start=start,
                rng=rng,
            )
            attempts += used
        maxima = metric_maxima(score_variants(shuffled))
        for metric, (control, observed) in enumerate(
            zip(maxima, real_maxima, strict=True)
        ):
            hits[metric] += control >= observed

    tails = tuple((hit + 1) / (controls + 1) for hit in hits)
    corrected = min(1.0, len(METRIC_NAMES) * min(tails))
    return EarthquakeMaskAudit(
        controls,
        real_variants,
        real_maxima,
        tuple(hits),  # type: ignore[arg-type]
        tails,  # type: ignore[arg-type]
        corrected,
        attempts,
    )
