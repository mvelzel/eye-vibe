"""Header-ordered ranks in the visible 83-word base-five order ideal."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import (
    header_ranks,
    inverse,
    lexicographic_unrank,
)
from eye_mystery.ninth_causal import CONTEXT_SPECS


VISIBLE_SIZE = 83
FULL_CUBE_SIZE = 125
OMITTED_SIZE = FULL_CUBE_SIZE - VISIBLE_SIZE
NEWLINE = 5
ROUTES = ("header", "inverse-header")
NONLITERAL_CONTEXT_SPECS = CONTEXT_SPECS[6:]
TRAINING_CONTEXTS = NONLITERAL_CONTEXT_SPECS[:4]
HOLDOUT_CONTEXTS = NONLITERAL_CONTEXT_SPECS[4:]


def base5_digits(value: int) -> tuple[int, int, int]:
    if value not in range(FULL_CUBE_SIZE):
        raise ValueError("value must lie in the complete base-five cube")
    return value // 25, value // 5 % 5, value % 5


@lru_cache(maxsize=None)
def header_eye_order(name: str, route: str) -> tuple[int, ...]:
    """Return the marker-selected collation of the five visible eye digits."""

    operation = lexicographic_unrank(header_ranks()[name])
    if route == "inverse-header":
        operation = inverse(operation)
    elif route != "header":
        raise ValueError(f"unknown route {route!r}")
    order = tuple(symbol for symbol in operation if symbol != NEWLINE)
    if sorted(order) != list(range(5)):
        raise AssertionError("header does not induce a five-eye order")
    return order


def full_cube_rank(value: int, order: tuple[int, ...]) -> int:
    """Rank one trigram among all 125 words under a digit collation."""

    if sorted(order) != list(range(5)):
        raise ValueError("order must permute the five eye digits")
    digit_rank = {digit: rank for rank, digit in enumerate(order)}
    high, middle, low = base5_digits(value)
    return (
        25 * digit_rank[high]
        + 5 * digit_rank[middle]
        + digit_rank[low]
    )


@lru_cache(maxsize=None)
def visible_rank_table(order: tuple[int, ...]) -> tuple[int, ...]:
    """Map canonical visible values to their rank in the ordered 83-set."""

    ordered = sorted(
        range(VISIBLE_SIZE),
        key=lambda value: full_cube_rank(value, order),
    )
    ranks = [0] * VISIBLE_SIZE
    for rank, value in enumerate(ordered):
        ranks[value] = rank
    return tuple(ranks)


@lru_cache(maxsize=None)
def omission_table(order: tuple[int, ...]) -> tuple[int, ...]:
    """Count excluded cube words preceding every visible glyph."""

    visible_ranks = visible_rank_table(order)
    table = tuple(
        full_cube_rank(value, order) - visible_ranks[value]
        for value in range(VISIBLE_SIZE)
    )
    if any(value not in range(OMITTED_SIZE + 1) for value in table):
        raise AssertionError("omission count lies outside 0..42")
    return table


@lru_cache(maxsize=None)
def message_omission_tables(route: str) -> dict[str, tuple[int, ...]]:
    return {
        name: omission_table(header_eye_order(name, route))
        for name in MESSAGE_ORDER
    }


@lru_cache(maxsize=None)
def message_visible_rank_tables(route: str) -> dict[str, tuple[int, ...]]:
    return {
        name: visible_rank_table(header_eye_order(name, route))
        for name in MESSAGE_ORDER
    }


def affine_label_map(multiplier: int, intercept: int) -> tuple[int, ...]:
    if multiplier not in range(1, VISIBLE_SIZE):
        raise ValueError("multiplier must be nonzero modulo 83")
    if intercept not in range(VISIBLE_SIZE):
        raise ValueError("intercept must lie in 0..82")
    return tuple(
        (multiplier * value + intercept) % VISIBLE_SIZE
        for value in range(VISIBLE_SIZE)
    )


@lru_cache(maxsize=1)
def affine_label_maps() -> tuple[tuple[int, ...], ...]:
    return tuple(
        affine_label_map(multiplier, intercept)
        for multiplier in range(1, VISIBLE_SIZE)
        for intercept in range(VISIBLE_SIZE)
    )


@lru_cache(maxsize=1)
def canonical_streams() -> dict[str, tuple[int, ...]]:
    return {
        name: tuple(trigram_values(MESSAGES[name]))
        for name in MESSAGE_ORDER
    }


@dataclass(frozen=True)
class ContextAgreement:
    name: str
    agreements: int
    length: int


@dataclass(frozen=True)
class RouteScore:
    route: str
    training: tuple[ContextAgreement, ...]
    holdout: tuple[ContextAgreement, ...]

    @property
    def training_agreements(self) -> int:
        return sum(result.agreements for result in self.training)

    @property
    def training_length(self) -> int:
        return sum(result.length for result in self.training)

    @property
    def holdout_agreements(self) -> int:
        return sum(result.agreements for result in self.holdout)

    @property
    def holdout_length(self) -> int:
        return sum(result.length for result in self.holdout)


def _score_contexts(
    specs: tuple[tuple[str, str, int, str, int, int], ...],
    streams: dict[str, tuple[int, ...]],
    tables: dict[str, tuple[int, ...]],
    label_map: tuple[int, ...],
) -> tuple[ContextAgreement, ...]:
    results = []
    for context_name, left, left_start, right, right_start, length in specs:
        left_table = tables[left]
        right_table = tables[right]
        agreements = sum(
            left_table[label_map[streams[left][left_start + offset]]]
            == right_table[label_map[streams[right][right_start + offset]]]
            for offset in range(length)
        )
        results.append(ContextAgreement(context_name, agreements, length))
    return tuple(results)


def _score_route(
    route: str,
    tables: dict[str, tuple[int, ...]],
    label_map: tuple[int, ...],
    streams: dict[str, tuple[int, ...]],
) -> RouteScore:
    return RouteScore(
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


def score_route(
    route: str,
    *,
    label_map: tuple[int, ...] = tuple(range(VISIBLE_SIZE)),
    streams: dict[str, tuple[int, ...]] | None = None,
) -> RouteScore:
    """Score the omission-count channel for one frozen route."""

    if sorted(label_map) != list(range(VISIBLE_SIZE)):
        raise ValueError("label map must permute 0..82")
    streams = canonical_streams() if streams is None else streams
    return _score_route(
        route,
        message_omission_tables(route),
        label_map,
        streams,
    )


def score_visible_route(
    route: str,
    *,
    label_map: tuple[int, ...] = tuple(range(VISIBLE_SIZE)),
    streams: dict[str, tuple[int, ...]] | None = None,
) -> RouteScore:
    """Score bijective visible-codebook reranking for one frozen route."""

    if sorted(label_map) != list(range(VISIBLE_SIZE)):
        raise ValueError("label map must permute 0..82")
    streams = canonical_streams() if streams is None else streams
    return _score_route(
        route,
        message_visible_rank_tables(route),
        label_map,
        streams,
    )


def selected_route(
    *,
    label_map: tuple[int, ...] = tuple(range(VISIBLE_SIZE)),
    streams: dict[str, tuple[int, ...]] | None = None,
) -> RouteScore:
    """Select only on training; the declared tie rule favors header."""

    scores = tuple(
        score_route(route, label_map=label_map, streams=streams)
        for route in ROUTES
    )
    return max(
        scores,
        key=lambda result: (
            result.training_agreements,
            -ROUTES.index(result.route),
        ),
    )


def selected_visible_route(
    *,
    label_map: tuple[int, ...] = tuple(range(VISIBLE_SIZE)),
    streams: dict[str, tuple[int, ...]] | None = None,
) -> RouteScore:
    """Select a visible-rerank route on training only."""

    scores = tuple(
        score_visible_route(route, label_map=label_map, streams=streams)
        for route in ROUTES
    )
    return max(
        scores,
        key=lambda result: (
            result.training_agreements,
            -ROUTES.index(result.route),
        ),
    )


def output_support(
    route: str,
    label_map: tuple[int, ...],
    streams: dict[str, tuple[int, ...]],
) -> tuple[int, bool]:
    tables = message_omission_tables(route)
    outputs = {
        tables[name][label_map[value]]
        for name in MESSAGE_ORDER
        for value in streams[name][1:]
    }
    return len(outputs), OMITTED_SIZE in outputs


@dataclass(frozen=True)
class HeaderOrderIdealAudit:
    observed: RouteScore
    observed_support: int
    observed_uses_42: bool
    control_count: int
    holdout_tail_count: int
    support_lower_tail_count: int
    maximum_control_holdout: int
    holdout_histogram: tuple[tuple[int, int], ...]

    @property
    def holdout_tail(self) -> float:
        return self.holdout_tail_count / self.control_count

    @property
    def support_lower_tail(self) -> float:
        return self.support_lower_tail_count / self.control_count


def audit_header_order_ideal() -> HeaderOrderIdealAudit:
    streams = canonical_streams()
    identity = tuple(range(VISIBLE_SIZE))
    observed = selected_route(label_map=identity, streams=streams)
    observed_support, observed_uses_42 = output_support(
        observed.route,
        identity,
        streams,
    )

    holdout_scores = []
    supports = []
    for label_map in affine_label_maps():
        score = selected_route(label_map=label_map, streams=streams)
        support, _uses_42 = output_support(score.route, label_map, streams)
        holdout_scores.append(score.holdout_agreements)
        supports.append(support)

    histogram = Counter(holdout_scores)
    return HeaderOrderIdealAudit(
        observed=observed,
        observed_support=observed_support,
        observed_uses_42=observed_uses_42,
        control_count=len(holdout_scores),
        holdout_tail_count=sum(
            score >= observed.holdout_agreements
            for score in holdout_scores
        ),
        support_lower_tail_count=sum(
            support <= observed_support for support in supports
        ),
        maximum_control_holdout=max(holdout_scores),
        holdout_histogram=tuple(sorted(histogram.items())),
    )


@dataclass(frozen=True)
class VisibleRerankAudit:
    observed: RouteScore
    control_count: int
    holdout_tail_count: int
    maximum_control_holdout: int
    holdout_histogram: tuple[tuple[int, int], ...]

    @property
    def holdout_tail(self) -> float:
        return self.holdout_tail_count / self.control_count


def audit_visible_rerank() -> VisibleRerankAudit:
    streams = canonical_streams()
    identity = tuple(range(VISIBLE_SIZE))
    observed = selected_visible_route(label_map=identity, streams=streams)
    holdout_scores = tuple(
        selected_visible_route(label_map=label_map, streams=streams)
        .holdout_agreements
        for label_map in affine_label_maps()
    )
    histogram = Counter(holdout_scores)
    return VisibleRerankAudit(
        observed=observed,
        control_count=len(holdout_scores),
        holdout_tail_count=sum(
            score >= observed.holdout_agreements
            for score in holdout_scores
        ),
        maximum_control_holdout=max(holdout_scores),
        holdout_histogram=tuple(sorted(histogram.items())),
    )
