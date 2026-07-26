"""Header-ordered conditional ranks for the no-adjacent-double Eye tape."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache

from eye_mystery.header_order_ideal import (
    HOLDOUT_CONTEXTS,
    MESSAGE_ORDER,
    ROUTES,
    TRAINING_CONTEXTS,
    VISIBLE_SIZE,
    affine_label_maps,
    canonical_streams,
    header_eye_order,
    visible_rank_table,
)


HALF_SIZE = 41


@dataclass(frozen=True)
class ConditionalRank:
    full: int
    sheet: int
    magnitude: int


def conditional_rank(
    previous: int,
    following: int,
    rank_table: tuple[int, ...],
    label_map: tuple[int, ...] = tuple(range(VISIBLE_SIZE)),
) -> ConditionalRank:
    """Rank ``following`` after deleting ``previous`` from one ordered deck."""

    if previous == following:
        raise ValueError("a self-transition has no conditional rank")
    if sorted(label_map) != list(range(VISIBLE_SIZE)):
        raise ValueError("label map must permute 0..82")
    previous_rank = rank_table[label_map[previous]]
    following_rank = rank_table[label_map[following]]
    full = following_rank - int(following_rank > previous_rank)
    if full not in range(VISIBLE_SIZE - 1):
        raise AssertionError("conditional rank lies outside 0..81")
    return ConditionalRank(
        full=full,
        sheet=full // HALF_SIZE,
        magnitude=full % HALF_SIZE,
    )


@lru_cache(maxsize=None)
def message_rank_tables(route: str) -> dict[str, tuple[int, ...]]:
    return {
        name: visible_rank_table(header_eye_order(name, route))
        for name in MESSAGE_ORDER
    }


@dataclass(frozen=True)
class ContextRankAgreement:
    name: str
    magnitude_agreements: int
    full_agreements: int
    sheet_equal: int
    transitions: int


def _score_contexts(
    specs: tuple[tuple[str, str, int, str, int, int], ...],
    streams: dict[str, tuple[int, ...]],
    tables: dict[str, tuple[int, ...]],
    label_map: tuple[int, ...],
) -> tuple[ContextRankAgreement, ...]:
    results = []
    for context_name, left, left_start, right, right_start, length in specs:
        magnitude = full = sheet_equal = 0
        for offset in range(1, length):
            left_rank = conditional_rank(
                streams[left][left_start + offset - 1],
                streams[left][left_start + offset],
                tables[left],
                label_map,
            )
            right_rank = conditional_rank(
                streams[right][right_start + offset - 1],
                streams[right][right_start + offset],
                tables[right],
                label_map,
            )
            magnitude += left_rank.magnitude == right_rank.magnitude
            full += left_rank.full == right_rank.full
            sheet_equal += left_rank.sheet == right_rank.sheet
        results.append(
            ContextRankAgreement(
                name=context_name,
                magnitude_agreements=magnitude,
                full_agreements=full,
                sheet_equal=sheet_equal,
                transitions=length - 1,
            )
        )
    return tuple(results)


@dataclass(frozen=True)
class ConditionalRouteScore:
    route: str
    training: tuple[ContextRankAgreement, ...]
    holdout: tuple[ContextRankAgreement, ...]

    @property
    def training_magnitude(self) -> int:
        return sum(item.magnitude_agreements for item in self.training)

    @property
    def holdout_magnitude(self) -> int:
        return sum(item.magnitude_agreements for item in self.holdout)

    @property
    def training_transitions(self) -> int:
        return sum(item.transitions for item in self.training)

    @property
    def holdout_transitions(self) -> int:
        return sum(item.transitions for item in self.holdout)

    @property
    def selected_sheet_xor(self) -> int:
        equal = sum(item.sheet_equal for item in self.training)
        return int(equal < self.training_transitions - equal)

    @property
    def holdout_sheet_matches(self) -> int:
        equal = sum(item.sheet_equal for item in self.holdout)
        return (
            equal
            if self.selected_sheet_xor == 0
            else self.holdout_transitions - equal
        )

    @property
    def holdout_full_agreements(self) -> int:
        return sum(item.full_agreements for item in self.holdout)


def score_route(
    route: str,
    *,
    label_map: tuple[int, ...] = tuple(range(VISIBLE_SIZE)),
    streams: dict[str, tuple[int, ...]] | None = None,
) -> ConditionalRouteScore:
    if sorted(label_map) != list(range(VISIBLE_SIZE)):
        raise ValueError("label map must permute 0..82")
    streams = canonical_streams() if streams is None else streams
    tables = message_rank_tables(route)
    return ConditionalRouteScore(
        route=route,
        training=_score_contexts(
            TRAINING_CONTEXTS,
            streams,
            tables,
            label_map,
        ),
        holdout=_score_contexts(
            HOLDOUT_CONTEXTS,
            streams,
            tables,
            label_map,
        ),
    )


def selected_route(
    *,
    label_map: tuple[int, ...] = tuple(range(VISIBLE_SIZE)),
    streams: dict[str, tuple[int, ...]] | None = None,
) -> ConditionalRouteScore:
    scores = tuple(
        score_route(route, label_map=label_map, streams=streams)
        for route in ROUTES
    )
    return max(
        scores,
        key=lambda result: (
            result.training_magnitude,
            -ROUTES.index(result.route),
        ),
    )


@dataclass(frozen=True)
class HeaderNoRepeatAudit:
    observed: ConditionalRouteScore
    control_count: int
    magnitude_tail_count: int
    full_tail_count: int
    maximum_control_magnitude: int
    magnitude_histogram: tuple[tuple[int, int], ...]

    @property
    def magnitude_tail(self) -> float:
        return self.magnitude_tail_count / self.control_count

    @property
    def full_tail(self) -> float:
        return self.full_tail_count / self.control_count


def audit_header_no_repeat() -> HeaderNoRepeatAudit:
    streams = canonical_streams()
    observed = selected_route(streams=streams)
    scores = tuple(
        selected_route(label_map=label_map, streams=streams)
        for label_map in affine_label_maps()
    )
    magnitude_values = tuple(score.holdout_magnitude for score in scores)
    full_values = tuple(score.holdout_full_agreements for score in scores)
    histogram = Counter(magnitude_values)
    return HeaderNoRepeatAudit(
        observed=observed,
        control_count=len(scores),
        magnitude_tail_count=sum(
            value >= observed.holdout_magnitude
            for value in magnitude_values
        ),
        full_tail_count=sum(
            value >= observed.holdout_full_agreements
            for value in full_values
        ),
        maximum_control_magnitude=max(magnitude_values),
        magnitude_histogram=tuple(sorted(histogram.items())),
    )
