"""Key-free necessities for breadth-first Eye-cipher architectures."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import permutations

from .conformance_grid import determinant_three


TRIGRAM_ORDERS = tuple(permutations(range(3)))


def base_five_digits(value: int) -> tuple[int, int, int]:
    if not 0 <= value < 125:
        raise ValueError("value is not a base-five trigram")
    return value // 25, (value // 5) % 5, value % 5


@dataclass(frozen=True)
class PathScore:
    matches: int
    transitions: int
    component_order: tuple[int, int, int]
    reversed_streams: bool


def debruijn_overlap_score(
    streams: Sequence[Sequence[int]],
    component_order: Sequence[int],
    *,
    reversed_streams: bool = False,
) -> tuple[int, int]:
    """Count order-two overlaps between adjacent base-five trigrams."""

    order = tuple(component_order)
    if order not in TRIGRAM_ORDERS:
        raise ValueError("component_order must permute the three digits")
    matches = 0
    transitions = 0
    for stream in streams:
        values = tuple(reversed(stream)) if reversed_streams else tuple(stream)
        digits = tuple(
            tuple(base_five_digits(value)[index] for index in order)
            for value in values
        )
        for left, right in zip(digits, digits[1:]):
            transitions += 1
            matches += left[1:] == right[:2]
    return matches, transitions


def best_debruijn_overlap(streams: Sequence[Sequence[int]]) -> PathScore:
    candidates = []
    for order in TRIGRAM_ORDERS:
        for reversed_streams in (False, True):
            matches, transitions = debruijn_overlap_score(
                streams, order, reversed_streams=reversed_streams
            )
            candidates.append(
                PathScore(matches, transitions, order, reversed_streams)
            )
    return max(
        candidates,
        key=lambda result: (
            result.matches,
            tuple(-value for value in result.component_order),
            not result.reversed_streams,
        ),
    )


@dataclass(frozen=True)
class AffineRecurrenceScore:
    matches: int
    transitions: int
    multiplier: int
    translation: int


def best_affine_recurrence(
    streams: Sequence[Sequence[int]], *, modulus: int = 83
) -> AffineRecurrenceScore:
    """Exhaust ``next = a*current+b`` over one shared finite field."""

    if modulus < 2:
        raise ValueError("modulus must be at least two")
    transitions = Counter(
        (left % modulus, right % modulus)
        for stream in streams
        for left, right in zip(stream, stream[1:])
    )
    return best_affine_recurrence_from_counts(transitions, modulus=modulus)


def best_affine_recurrence_from_counts(
    transitions: Mapping[tuple[int, int], int], *, modulus: int = 83
) -> AffineRecurrenceScore:
    """Exhaust the shared affine recurrence on a transition multiset."""

    if modulus < 2:
        raise ValueError("modulus must be at least two")
    if any(
        count < 0
        or current not in range(modulus)
        or following not in range(modulus)
        for (current, following), count in transitions.items()
    ):
        raise ValueError("invalid transition count")
    total = sum(transitions.values())
    best = AffineRecurrenceScore(-1, total, 0, 0)
    for multiplier in range(modulus):
        for translation in range(modulus):
            matches = sum(
                transitions[current, (multiplier * current + translation) % modulus]
                for current in range(modulus)
            )
            candidate = AffineRecurrenceScore(
                matches, total, multiplier, translation
            )
            if (candidate.matches, -multiplier, -translation) > (
                best.matches,
                -best.multiplier,
                -best.translation,
            ):
                best = candidate
    return best


def trie_transition_counts(
    streams: Sequence[Sequence[int]],
) -> Counter[tuple[int, int]]:
    """Count parent-to-child label transitions once per merged trie node."""

    root: dict[int, dict] = {}
    for stream in streams:
        node = root
        for value in stream:
            node = node.setdefault(value, {})

    transitions: Counter[tuple[int, int]] = Counter()

    def visit(node: dict[int, dict], parent: int | None) -> None:
        for value, child in node.items():
            if parent is not None:
                transitions[parent, value] += 1
            visit(child, value)

    visit(root, None)
    return transitions


def aligned_determinant_zero_count(
    streams: Mapping[str, Sequence[int]],
    order: Sequence[str],
    *,
    modulus: int,
    start: int,
    rotations: Mapping[str, int] | None = None,
) -> tuple[int, int]:
    """Count rank-at-most-two slices in a fixed row-major 3×3 message grid."""

    if len(order) != 9 or set(order) != set(streams):
        raise ValueError("order must name all nine streams exactly once")
    if start < 0:
        raise ValueError("start must be nonnegative")
    available = min(len(streams[name]) for name in order) - start
    if available < 0:
        raise ValueError("start lies beyond the shortest stream")
    offsets = rotations or {}
    zeros = 0
    for relative in range(available):
        values = []
        for name in order:
            stream = streams[name]
            index = (start + relative + offsets.get(name, 0)) % len(stream)
            values.append(stream[index])
        matrix = tuple(tuple(values[3 * row : 3 * row + 3]) for row in range(3))
        zeros += determinant_three(matrix, modulus) == 0
    return zeros, available


@dataclass(frozen=True)
class HeaderMomentScore:
    matches: int
    modulus: int
    degree: int
    sign: int
    matched_names: tuple[str, ...]


def header_moment_scores(
    streams: Mapping[str, Sequence[int]],
    *,
    moduli: Sequence[int] = (83, 101),
    degrees: Sequence[int] = tuple(range(5)),
) -> tuple[HeaderMomentScore, ...]:
    """Test fixed polynomial body moments as systematic first-symbol checks."""

    results = []
    for modulus in moduli:
        for degree in degrees:
            moments = {
                name: sum(
                    pow(position, degree, modulus) * value
                    for position, value in enumerate(stream[1:], start=1)
                )
                % modulus
                for name, stream in streams.items()
            }
            for sign in (-1, 1):
                matched = tuple(
                    name
                    for name, stream in streams.items()
                    if stream[0] % modulus == sign * moments[name] % modulus
                )
                results.append(
                    HeaderMomentScore(
                        len(matched), modulus, degree, sign, matched
                    )
                )
    return tuple(results)
