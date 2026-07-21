"""Cheap necessities for several breadth-first Eye mechanism families."""

from __future__ import annotations

from collections.abc import Sequence


def reuse_stack_distances(stream: Sequence[int]) -> tuple[int, ...]:
    """Count distinct intervening labels at every repeated occurrence."""

    previous: dict[int, int] = {}
    distances: list[int] = []
    for index, value in enumerate(stream):
        if value in previous:
            distances.append(len(set(stream[previous[value] + 1 : index])))
        previous[value] = index
    return tuple(distances)


def cumulative_state_count(
    stream: Sequence[int], *, translation: int, modulus: int
) -> int:
    """Unique states in the walk with steps ``value + translation``."""

    state = 0
    visited: set[int] = set()
    for value in stream:
        state = (state + value + translation) % modulus
        visited.add(state)
    return len(visited)


def best_affine_step_translation(
    streams: Sequence[Sequence[int]], *, modulus: int
) -> tuple[int, int, tuple[int, ...]]:
    """Minimize total unique states over nonzero affine step scalings.

    Any step rule ``a*value+b`` with nonzero ``a`` has the same collision
    structure, after scaling states, as ``value+t`` for ``t=b/a``.  Exhausting
    ``t`` therefore covers the complete affine family for this statistic.
    """

    candidates = []
    for translation in range(modulus):
        counts = tuple(
            cumulative_state_count(
                stream, translation=translation, modulus=modulus
            )
            for stream in streams
        )
        candidates.append((sum(counts), translation, counts))
    return min(candidates)
