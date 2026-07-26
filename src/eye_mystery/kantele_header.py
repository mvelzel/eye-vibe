"""Test factoradic Eye headers against Noita's executable Kantele songs."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import (
    header_ranks,
    inverse,
    lexicographic_unrank,
)
from eye_mystery.seventh_wide import renderer_body_tape


KANTELE_NOTES = ("a", "d", "dis", "e", "g")
KANTELE_SONGS = {
    "portal": (0, 2, 3, 4),
    "bomb": (4, 1, 3, 1),
    "worm": (1, 3, 0, 3, 2),
    # The Lua's alt_notes table converts f,g,f,a2,c to g,dis,g,e,a.
    "alchemy": (4, 2, 4, 3, 0),
}
ROUTES = ("identity", "header", "inverse-header")
NEWLINE = 5


@dataclass(frozen=True)
class SongHit:
    song: str
    start: int
    end: int
    begins_fragment: bool
    ends_fragment: bool

    @property
    def exact_fragment(self) -> bool:
        return self.begins_fragment and self.ends_fragment


def song_hits(tape: tuple[int, ...]) -> tuple[SongHit, ...]:
    """Find every Kantele secret song in one six-symbol renderer tape."""

    if any(symbol not in range(6) for symbol in tape):
        raise ValueError("renderer symbols must lie in 0..5")
    hits = []
    for song_name, song in KANTELE_SONGS.items():
        for start in range(len(tape) - len(song) + 1):
            end = start + len(song)
            if tape[start:end] != song:
                continue
            hits.append(
                SongHit(
                    song=song_name,
                    start=start,
                    end=end,
                    begins_fragment=start == 0 or tape[start - 1] == NEWLINE,
                    ends_fragment=end == len(tape) or tape[end] == NEWLINE,
                )
            )
    return tuple(hits)


def _operation(name: str, route: str) -> tuple[int, ...]:
    if route == "identity":
        return tuple(range(6))
    operation = lexicographic_unrank(header_ranks()[name])
    if route == "inverse-header":
        return inverse(operation)
    if route != "header":
        raise ValueError(f"unknown route {route!r}")
    return operation


def transformed_body_tape(
    name: str,
    *,
    route: str,
    relabel: tuple[int, ...] = tuple(range(5)),
) -> tuple[int, ...]:
    """Relabel body eyes, then apply the selected real header operation."""

    if sorted(relabel) != list(range(5)):
        raise ValueError("body relabeling must permute the five eye symbols")
    tape = renderer_body_tape(name, trigram_values(MESSAGES[name]))
    operation = _operation(name, route)
    return tuple(
        operation[relabel[symbol] if symbol != NEWLINE else NEWLINE]
        for symbol in tape
    )


@dataclass(frozen=True)
class RouteScore:
    route: str
    exact_fragments: int
    terminal_hits: int
    total_hits: int
    hits_by_message: tuple[tuple[str, tuple[SongHit, ...]], ...]

    @property
    def selection_score(self) -> tuple[int, int, int]:
        return self.exact_fragments, self.terminal_hits, self.total_hits


def score_route(
    route: str,
    *,
    relabel: tuple[int, ...] = tuple(range(5)),
) -> RouteScore:
    hits_by_message = tuple(
        (
            name,
            song_hits(
                transformed_body_tape(name, route=route, relabel=relabel)
            ),
        )
        for name in MESSAGE_ORDER
    )
    all_hits = tuple(
        hit for _, message_hits in hits_by_message for hit in message_hits
    )
    return RouteScore(
        route=route,
        exact_fragments=sum(hit.exact_fragment for hit in all_hits),
        terminal_hits=sum(hit.ends_fragment for hit in all_hits),
        total_hits=len(all_hits),
        hits_by_message=hits_by_message,
    )


def best_route(
    *, relabel: tuple[int, ...] = tuple(range(5))
) -> RouteScore:
    """Select the same frozen route family for real data and every control."""

    return max(
        (score_route(route, relabel=relabel) for route in ROUTES),
        key=lambda result: result.selection_score,
    )


@dataclass(frozen=True)
class KanteleHeaderAudit:
    observed: RouteScore
    control_count: int
    exact_tail_count: int
    maximum_control_score: tuple[int, int, int]
    score_histogram: tuple[tuple[tuple[int, int, int], int], ...]

    @property
    def exact_tail(self) -> float:
        return self.exact_tail_count / self.control_count


def kantele_header_audit() -> KanteleHeaderAudit:
    """Compare the real eye/header join with all 120 global eye relabelings."""

    observed = best_route()
    scores = tuple(
        best_route(relabel=relabel).selection_score
        for relabel in permutations(range(5))
    )
    histogram = tuple(
        (score, scores.count(score)) for score in sorted(set(scores), reverse=True)
    )
    return KanteleHeaderAudit(
        observed=observed,
        control_count=len(scores),
        exact_tail_count=sum(score >= observed.selection_score for score in scores),
        maximum_control_score=max(scores),
        score_histogram=histogram,
    )
