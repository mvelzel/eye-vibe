"""Held-out context audit for the historical desert-glyph quotient."""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.diamond_reading import (
    COMPONENT_ORDERS,
    X_ORDER,
    Y_ORDER,
    base25_reading,
    squared_reading,
)
from eye_mystery.ninth_causal import CONTEXT_SPECS


NONLITERAL_CONTEXTS = CONTEXT_SPECS[6:]
TRAIN_CONTEXTS = NONLITERAL_CONTEXTS[:4]
HELDOUT_CONTEXTS = NONLITERAL_CONTEXTS[4:]
CONTROL_SEED = 0xD1A607


@dataclass(frozen=True)
class ContextQuotientScore:
    """Agreement for one paired-record context."""

    name: str
    agreements: int
    eligible_coordinates: int
    exact: bool


@dataclass(frozen=True)
class QuotientSplitScore:
    """Aggregate and per-context quotient agreement."""

    agreements: int
    eligible_coordinates: int
    exact_contexts: int
    contexts: tuple[ContextQuotientScore, ...]


@dataclass(frozen=True)
class DiamondContextAudit:
    """Frozen real/control result for the record-local squared quotient."""

    training: QuotientSplitScore
    heldout: QuotientSplitScore
    base25_training: QuotientSplitScore
    base25_heldout: QuotientSplitScore
    relative_order_scores: tuple[int, ...]
    document_order_rank: int
    document_order_ties: int
    controls: int
    control_hits: int
    tail: float
    control_distribution: tuple[tuple[int, int], ...]

    @property
    def passes(self) -> bool:
        return self.tail < 0.01


def accepted_streams() -> dict[str, tuple[int, ...]]:
    """Return canonical accepted ranks, including each first marker."""

    return {
        name: trigram_values(MESSAGES[name])
        for name in MESSAGE_ORDER
    }


def rank_digits(value: int) -> tuple[int, int, int]:
    """Return the natural base-five eye trigram for one accepted rank."""

    if value not in range(83):
        raise ValueError("accepted rank must lie in 0..82")
    return value // 25, value // 5 % 5, value % 5


def raw_digits(values: Sequence[int]) -> tuple[int, ...]:
    """Expand accepted ranks to the raw input expected by the transform."""

    return tuple(digit for value in values for digit in rank_digits(value))


def quotient_values(
    values: Sequence[int],
    *,
    transform: str,
    x_order: tuple[int, int, int] = X_ORDER,
    y_order: tuple[int, int, int] = Y_ORDER,
) -> tuple[int, ...]:
    """Transform one record, resetting pair phase at its first trigram."""

    raw = raw_digits(values)
    if transform == "squared":
        return squared_reading(raw, x_order=x_order, y_order=y_order)
    if transform == "base25":
        return base25_reading(raw, x_order=x_order, y_order=y_order)
    raise ValueError(f"unknown quotient transform {transform!r}")


def context_quotient_score(
    streams: Mapping[str, Sequence[int]],
    spec: tuple[str, str, int, str, int, int],
    *,
    transform: str = "squared",
    x_order: tuple[int, int, int] = X_ORDER,
    y_order: tuple[int, int, int] = Y_ORDER,
) -> ContextQuotientScore:
    """Score one aligned record after excluding completely copied pairs."""

    name, left_name, left_start, right_name, right_start, length = spec
    left = tuple(streams[left_name][left_start : left_start + length])
    right = tuple(streams[right_name][right_start : right_start + length])
    if len(left) != length or len(right) != length:
        raise ValueError("context extends beyond a supplied stream")

    left_output = quotient_values(
        left,
        transform=transform,
        x_order=x_order,
        y_order=y_order,
    )
    right_output = quotient_values(
        right,
        transform=transform,
        x_order=x_order,
        y_order=y_order,
    )

    agreements = 0
    eligible = 0
    pairs = (length + 1) // 2
    for pair_index in range(pairs):
        y_index = 2 * pair_index
        x_index = y_index + 1
        left_x = left[x_index] if x_index < length else None
        right_x = right[x_index] if x_index < length else None
        copied = left[y_index] == right[y_index] and left_x == right_x
        if copied:
            continue
        start = 3 * pair_index
        eligible += 3
        agreements += sum(
            left_value == right_value
            for left_value, right_value in zip(
                left_output[start : start + 3],
                right_output[start : start + 3],
                strict=True,
            )
        )

    return ContextQuotientScore(
        name,
        agreements,
        eligible,
        eligible > 0 and agreements == eligible,
    )


def split_score(
    streams: Mapping[str, Sequence[int]],
    specs: Sequence[tuple[str, str, int, str, int, int]],
    *,
    transform: str = "squared",
    x_order: tuple[int, int, int] = X_ORDER,
    y_order: tuple[int, int, int] = Y_ORDER,
) -> QuotientSplitScore:
    """Aggregate quotient agreement over a frozen context split."""

    contexts = tuple(
        context_quotient_score(
            streams,
            spec,
            transform=transform,
            x_order=x_order,
            y_order=y_order,
        )
        for spec in specs
    )
    return QuotientSplitScore(
        sum(context.agreements for context in contexts),
        sum(context.eligible_coordinates for context in contexts),
        sum(context.exact for context in contexts),
        contexts,
    )


def permuted_streams(
    streams: Mapping[str, Sequence[int]],
    permutation: Sequence[int],
) -> dict[str, tuple[int, ...]]:
    """Globally relabel accepted ranks while preserving every equality."""

    if sorted(permutation) != list(range(83)):
        raise ValueError("permutation must relabel exactly 0..82")
    return {
        name: tuple(permutation[value] for value in stream)
        for name, stream in streams.items()
    }


def relative_alignment_scores(
    streams: Mapping[str, Sequence[int]],
) -> tuple[int, ...]:
    """Return held-out scores for all six x orders with y fixed to 021."""

    return tuple(
        split_score(
            streams,
            HELDOUT_CONTEXTS,
            transform="squared",
            x_order=x_order,
            y_order=Y_ORDER,
        ).agreements
        for x_order in COMPONENT_ORDERS
    )


def run_diamond_context_audit(
    *,
    controls: int = 50_000,
    seed: int = CONTROL_SEED,
) -> DiamondContextAudit:
    """Run the preregistered global-label matched control."""

    if controls < 1:
        raise ValueError("controls must be positive")
    streams = accepted_streams()
    training = split_score(streams, TRAIN_CONTEXTS)
    heldout = split_score(streams, HELDOUT_CONTEXTS)
    base25_training = split_score(
        streams,
        TRAIN_CONTEXTS,
        transform="base25",
    )
    base25_heldout = split_score(
        streams,
        HELDOUT_CONTEXTS,
        transform="base25",
    )

    alignment_scores = relative_alignment_scores(streams)
    document_index = COMPONENT_ORDERS.index(X_ORDER)
    document_score = alignment_scores[document_index]
    document_order_rank = (
        1 + sum(score > document_score for score in alignment_scores)
    )
    document_order_ties = alignment_scores.count(document_score)

    rng = random.Random(seed)
    permutation = list(range(83))
    control_hits = 0
    distribution: Counter[int] = Counter()
    for _ in range(controls):
        rng.shuffle(permutation)
        control_streams = permuted_streams(streams, permutation)
        score = split_score(
            control_streams,
            HELDOUT_CONTEXTS,
        ).agreements
        distribution[score] += 1
        control_hits += int(score >= heldout.agreements)

    return DiamondContextAudit(
        training,
        heldout,
        base25_training,
        base25_heldout,
        alignment_scores,
        document_order_rank,
        document_order_ties,
        controls,
        control_hits,
        (control_hits + 1) / (controls + 1),
        tuple(sorted(distribution.items())),
    )

