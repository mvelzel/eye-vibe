"""Cheap diagnostics for the frozen tenth wide Eye-cipher horizon."""

from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations, permutations

from eye_mystery.ninth_causal import CONTEXT_SPECS, gf2_rank
from eye_mystery.ninth_second import base5_digits
from eye_mystery.prefix_hierarchy import prefix_clusters


NONLITERAL_CONTEXTS = CONTEXT_SPECS[6:]
FIRST_CONTEXTS = NONLITERAL_CONTEXTS[:4]
LAST_CONTEXTS = NONLITERAL_CONTEXTS[4:]
DIGIT_ORDERS = tuple(permutations(range(3)))
ORDER_CONVENTIONS = tuple(
    (order, reverse) for order in DIGIT_ORDERS for reverse in (False, True)
)
ORDINAL_PROJECTIONS = tuple(
    [("full", order) for order in DIGIT_ORDERS]
    + [("pair", pair) for pair in permutations(range(3), 2)]
)
DIFFERENTIAL_VARIANTS = ("mod83", "mod101", "outer", "middle")


def reordered_value(value: int, order: Sequence[int]) -> int:
    digits = base5_digits(value)
    result = 0
    for digit in order:
        result = 5 * result + digits[digit]
    return result


def projected_value(value: int, projection: tuple[str, tuple[int, ...]]) -> int:
    kind, order = projection
    if kind not in {"full", "pair"}:
        raise ValueError(f"unknown ordinal projection: {kind}")
    expected = 3 if kind == "full" else 2
    if len(order) != expected or len(set(order)) != expected:
        raise ValueError("projection contains the wrong number of distinct digits")
    return reordered_value(value, order)


def ordinal_pattern(values: Sequence[int]) -> tuple[int, ...]:
    """Return a tie-aware rank pattern."""

    ranks = {value: rank for rank, value in enumerate(sorted(set(values)))}
    return tuple(ranks[value] for value in values)


def ordinal_cross_collisions(
    streams: Mapping[str, Sequence[int]],
    *,
    length: int,
    projection: tuple[str, tuple[int, ...]],
) -> int:
    """Count equal ordinal windows belonging to different messages."""

    if length < 2:
        raise ValueError("ordinal windows must contain at least two values")
    counts: dict[tuple[int, ...], Counter[str]] = defaultdict(Counter)
    for name, stream in streams.items():
        projected = tuple(projected_value(value, projection) for value in stream)
        for start in range(len(projected) - length + 1):
            counts[ordinal_pattern(projected[start : start + length])][name] += 1
    collisions = 0
    for by_message in counts.values():
        total = sum(by_message.values())
        collisions += (
            total * total - sum(count * count for count in by_message.values())
        ) // 2
    return collisions


def ordinal_score_family(
    streams: Mapping[str, Sequence[int]],
    *,
    lengths: Iterable[int] = range(3, 9),
) -> dict[tuple[int, str, tuple[int, ...]], int]:
    return {
        (length, projection[0], projection[1]): ordinal_cross_collisions(
            streams,
            length=length,
            projection=projection,
        )
        for length in lengths
        for projection in ORDINAL_PROJECTIONS
    }


def context_mappings(
    streams: Mapping[str, Sequence[int]], specs=NONLITERAL_CONTEXTS
) -> tuple[dict[int, int], ...]:
    result = []
    for _, left, left_start, right, right_start, length in specs:
        mapping: dict[int, int] = {}
        reverse: dict[int, int] = {}
        for source, target in zip(
            streams[left][left_start : left_start + length],
            streams[right][right_start : right_start + length],
            strict=True,
        ):
            if source in mapping and mapping[source] != target:
                raise ValueError("context is not a function")
            if target in reverse and reverse[target] != source:
                raise ValueError("context is not injective")
            mapping[source] = target
            reverse[target] = source
        result.append(mapping)
    return tuple(result)


def fixed_points(mapping: Mapping[int, int]) -> int:
    return sum(source == target for source, target in mapping.items())


def shuffled_context_mappings_fixed_points(
    mappings: Sequence[Mapping[int, int]], rng: random.Random
) -> tuple[dict[int, int], ...]:
    """Shuffle fixed domain/image pairs while retaining fixed-point counts."""

    output = []
    for mapping in mappings:
        sources = tuple(sorted(mapping))
        targets = list(mapping.values())
        target_fixed = fixed_points(mapping)
        for _ in range(10_000):
            rng.shuffle(targets)
            candidate = dict(zip(sources, targets, strict=True))
            if fixed_points(candidate) == target_fixed:
                output.append(candidate)
                break
        else:
            raise RuntimeError("fixed-point-conditioned shuffle failed")
    return tuple(output)


def rising_sequences(
    mapping: Mapping[int, int],
    convention: tuple[tuple[int, int, int], bool],
) -> int:
    """Count increasing runs in one partial permutation restriction."""

    order, reverse = convention

    def key(value: int) -> int:
        transformed = reordered_value(value, order)
        return -transformed if reverse else transformed

    targets = tuple(mapping[source] for source in sorted(mapping, key=key))
    if not targets:
        return 0
    target_keys = tuple(key(target) for target in targets)
    return 1 + sum(
        right < left for left, right in zip(target_keys, target_keys[1:])
    )


@dataclass(frozen=True)
class RiffleScore:
    rising_sequences: int
    edges: int
    convention: tuple[tuple[int, int, int], bool]


def riffle_score(
    mappings: Sequence[Mapping[int, int]], *, convention=None
) -> RiffleScore:
    conventions = ORDER_CONVENTIONS if convention is None else (convention,)
    best = None
    edges = sum(map(len, mappings))
    for candidate in conventions:
        score = RiffleScore(
            sum(rising_sequences(mapping, candidate) for mapping in mappings),
            edges,
            candidate,
        )
        if best is None or score.rising_sequences < best.rising_sequences:
            best = score
    assert best is not None
    return best


@dataclass(frozen=True)
class RiffleHeldOutScore:
    train: RiffleScore
    test: RiffleScore


def riffle_held_out_score(
    train_mappings: Sequence[Mapping[int, int]],
    test_mappings: Sequence[Mapping[int, int]],
) -> RiffleHeldOutScore:
    train = riffle_score(train_mappings)
    return RiffleHeldOutScore(
        train,
        riffle_score(test_mappings, convention=train.convention),
    )


def out_faro_position(position: int, *, size: int = 84) -> int:
    if size % 2 or size < 2:
        raise ValueError("a perfect Faro requires a positive even deck size")
    if position not in range(size):
        raise ValueError("card position is outside the deck")
    half = size // 2
    return 2 * position if position < half else 2 * (position - half) + 1


def in_faro_position(position: int, *, size: int = 84) -> int:
    if size % 2 or size < 2:
        raise ValueError("a perfect Faro requires a positive even deck size")
    if position not in range(size):
        raise ValueError("card position is outside the deck")
    half = size // 2
    return 2 * position + 1 if position < half else 2 * (position - half)


def multiplicative_order(value: int, modulus: int) -> int:
    if math.gcd(value, modulus) != 1:
        raise ValueError("multiplicative order requires a unit")
    current = 1
    for exponent in range(1, modulus + 1):
        current = current * value % modulus
        if current == 1:
            return exponent
    raise AssertionError("Euler's theorem guarantees an order")


@dataclass(frozen=True)
class ColorRefinementScore:
    classes: int
    singleton_classes: int
    largest_class: int
    iterations: int
    colors: tuple[int, ...]


def directed_color_refinement(
    edges: Iterable[tuple[int, int]], *, alphabet_size: int = 83
) -> ColorRefinementScore:
    """Return the coarsest directed equitable refinement from one color."""

    outgoing = [set() for _ in range(alphabet_size)]
    incoming = [set() for _ in range(alphabet_size)]
    for source, target in set(edges):
        if source not in range(alphabet_size) or target not in range(alphabet_size):
            raise ValueError("transition edge outside alphabet")
        outgoing[source].add(target)
        incoming[target].add(source)
    colors = (0,) * alphabet_size
    iterations = 0
    while True:
        signatures = tuple(
            (
                colors[value],
                tuple(sorted(Counter(colors[target] for target in outgoing[value]).items())),
                tuple(sorted(Counter(colors[source] for source in incoming[value]).items())),
            )
            for value in range(alphabet_size)
        )
        palette = {signature: index for index, signature in enumerate(sorted(set(signatures)))}
        refined = tuple(palette[signature] for signature in signatures)
        if refined == colors:
            break
        colors = refined
        iterations += 1
    sizes = Counter(colors)
    return ColorRefinementScore(
        len(sizes),
        sum(size == 1 for size in sizes.values()),
        max(sizes.values(), default=0),
        iterations,
        colors,
    )


def differential_state(left: int, right: int, variant: str) -> int:
    if variant == "mod83":
        return (right - left) % 83
    if variant == "mod101":
        return (right - left) % 101
    left_digits = base5_digits(left)
    right_digits = base5_digits(right)
    if variant == "outer":
        return (
            (right_digits[0] - left_digits[0]) % 5 * 5
            + (right_digits[2] - left_digits[2]) % 5
        )
    if variant == "middle":
        return (right_digits[1] - left_digits[1]) % 5
    raise ValueError(f"unknown differential variant: {variant}")


def _immediate_children(
    members: Sequence[str], depth: int, bodies: Mapping[str, Sequence[int]]
) -> tuple[tuple[str, ...], ...]:
    groups: dict[int | None, list[str]] = {}
    for name in members:
        value = bodies[name][depth] if depth < len(bodies[name]) else None
        groups.setdefault(value, []).append(name)
    return tuple(tuple(group) for group in groups.values())


@dataclass(frozen=True)
class DifferentialScore:
    repeated_mass: int
    observations: int
    union_support: int
    summed_support: int
    support_rank: int
    branches: int


def branch_differential_score(
    bodies: Mapping[str, Sequence[int]], variant: str
) -> DifferentialScore:
    if variant not in DIFFERENTIAL_VARIANTS:
        raise ValueError(f"unknown differential variant: {variant}")
    counters = []
    for cluster in prefix_clusters(bodies):
        children = _immediate_children(cluster.members, cluster.length, bodies)
        counter: Counter[int] = Counter()
        for first_index, first in enumerate(children):
            for second in children[first_index + 1 :]:
                for left in first:
                    for right in second:
                        stop = min(len(bodies[left]), len(bodies[right]))
                        for position in range(cluster.length, stop):
                            counter[
                                differential_state(
                                    bodies[left][position],
                                    bodies[right][position],
                                    variant,
                                )
                            ] += 1
        counters.append(counter)
    supports = tuple(set(counter) for counter in counters)
    universe = set().union(*supports) if supports else set()
    rows = tuple(
        sum(1 << value for value in support)
        for support in supports
    )
    observations = sum(sum(counter.values()) for counter in counters)
    summed_support = sum(len(counter) for counter in counters)
    return DifferentialScore(
        observations - summed_support,
        observations,
        len(universe),
        summed_support,
        gf2_rank(rows),
        len(counters),
    )


@dataclass(frozen=True)
class ContextGraphScore:
    vertices: int
    edges: int
    components: int
    cycle_rank: int


def context_graph_score(specs=NONLITERAL_CONTEXTS) -> ContextGraphScore:
    """Audit whether observed context windows define any semantic loop."""

    edges = []
    vertices = set()
    for _, left, left_start, right, right_start, length in specs:
        first = (left, left_start, length)
        second = (right, right_start, length)
        vertices.update((first, second))
        edges.append((first, second))
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    components = 0
    remaining = set(vertices)
    while remaining:
        components += 1
        frontier = [remaining.pop()]
        while frontier:
            current = frontier.pop()
            for neighbour in adjacency[current] & remaining:
                remaining.remove(neighbour)
                frontier.append(neighbour)
    return ContextGraphScore(
        len(vertices),
        len(edges),
        components,
        len(edges) - len(vertices) + components,
    )
