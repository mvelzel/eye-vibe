"""Finite six-stream row and ragged-column routes for practice Cipher 3."""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from functools import lru_cache
from itertools import permutations


SIZE = 83
ROW_MODES = ("forward", "reverse", "snake-forward", "snake-reverse")


@dataclass(frozen=True)
class SixStreamRoute:
    kind: str
    trim_body: bool
    row_order: tuple[int, ...]
    mode: str
    align_right: bool = False
    reverse_columns: bool = False

    def __post_init__(self) -> None:
        if self.kind not in {"row", "column"}:
            raise ValueError("route kind must be row or column")
        if sorted(self.row_order) != list(range(6)):
            raise ValueError("row order must permute 0..5")
        if self.kind == "row":
            if self.mode not in ROW_MODES:
                raise ValueError("invalid row direction mode")
            if self.align_right or self.reverse_columns:
                raise ValueError("row routes do not use column fields")
        elif self.mode not in {"fixed", "snake"}:
            raise ValueError("invalid column vertical mode")


def route_sort_key(route: SixStreamRoute) -> tuple[object, ...]:
    return (
        0 if route.kind == "row" else 1,
        int(route.trim_body),
        route.row_order,
        route.mode,
        int(route.align_right),
        int(route.reverse_columns),
    )


def route_catalog() -> tuple[SixStreamRoute, ...]:
    routes = []
    for trim_body in (False, True):
        for row_order in permutations(range(6)):
            for mode in ROW_MODES:
                routes.append(
                    SixStreamRoute(
                        "row",
                        trim_body,
                        tuple(row_order),
                        mode,
                    )
                )
            for align_right in (False, True):
                for reverse_columns in (False, True):
                    for mode in ("fixed", "snake"):
                        routes.append(
                            SixStreamRoute(
                                "column",
                                trim_body,
                                tuple(row_order),
                                mode,
                                align_right,
                                reverse_columns,
                            )
                        )
    return tuple(routes)


def route_coordinates(
    lengths: Sequence[int],
    route: SixStreamRoute,
) -> tuple[tuple[int, int], ...]:
    """Return supplied-row coordinates in routed path order."""
    if len(lengths) != 6:
        raise ValueError("a route requires six row lengths")
    start = int(route.trim_body)
    if any(length < start for length in lengths):
        raise ValueError("trim exceeds a supplied row")

    if route.kind == "row":
        output = []
        for order_index, row in enumerate(route.row_order):
            reverse = (
                route.mode == "reverse"
                or (route.mode == "snake-forward" and order_index % 2 == 1)
                or (route.mode == "snake-reverse" and order_index % 2 == 0)
            )
            indices = list(range(start, lengths[row]))
            if reverse:
                indices.reverse()
            output.extend((row, index) for index in indices)
        return tuple(output)

    effective_lengths = tuple(length - start for length in lengths)
    width = max(effective_lengths, default=0)
    columns = list(range(width))
    if route.reverse_columns:
        columns.reverse()
    output = []
    for traversal_index, column in enumerate(columns):
        rows = list(route.row_order)
        if route.mode == "snake" and traversal_index % 2 == 1:
            rows.reverse()
        for row in rows:
            offset = width - effective_lengths[row] if route.align_right else 0
            local_index = column - offset
            if local_index in range(effective_lengths[row]):
                output.append((row, start + local_index))
    return tuple(output)


def apply_route(
    rows: Sequence[Sequence[int]],
    route: SixStreamRoute,
) -> tuple[int, ...]:
    if len(rows) != 6:
        raise ValueError("a route requires six rows")
    coordinates = route_coordinates(tuple(map(len, rows)), route)
    return tuple(rows[row][index] for row, index in coordinates)


@dataclass(frozen=True)
class RouteScore:
    route: SixStreamRoute
    events: int
    distinct_edges: int
    repeated_events: int
    maximum_outdegree: int
    maximum_indegree: int
    effective_uniform_choices: float
    difference_support: int


@lru_cache(maxsize=None)
def _effective_choices(
    visits: tuple[int, ...],
    distinct_edges: int,
) -> float:
    lower = 1.0
    upper = 10_000.0
    for _ in range(60):
        choices = (lower + upper) / 2
        expected = sum(
            choices * (1 - (1 - 1 / choices) ** count)
            for count in visits
        )
        if expected < distinct_edges:
            lower = choices
        else:
            upper = choices
    return (lower + upper) / 2


def score_path(path: Sequence[int], route: SixStreamRoute) -> RouteScore:
    if any(value not in range(SIZE) for value in path):
        raise ValueError("path value lies outside 0..82")
    edges = tuple(zip(path, path[1:]))
    multiplicities = Counter(edges)
    outgoing: dict[int, set[int]] = {}
    incoming: dict[int, set[int]] = {}
    visits = Counter()
    for left, right in edges:
        outgoing.setdefault(left, set()).add(right)
        incoming.setdefault(right, set()).add(left)
        visits[left] += 1
    distinct = len(multiplicities)
    return RouteScore(
        route,
        len(edges),
        distinct,
        len(edges) - distinct,
        max(map(len, outgoing.values()), default=0),
        max(map(len, incoming.values()), default=0),
        _effective_choices(
            tuple(visits[value] for value in range(SIZE)),
            distinct,
        ),
        len({(right - left) % SIZE for left, right in edges}),
    )


def score_route(
    rows: Sequence[Sequence[int]],
    route: SixStreamRoute,
) -> RouteScore:
    return score_path(apply_route(rows, route), route)


@dataclass(frozen=True)
class RouteSearch:
    broad: tuple[RouteScore, ...]
    additive: tuple[RouteScore, ...]


def search_routes(
    rows: Sequence[Sequence[int]],
    *,
    catalog: Sequence[SixStreamRoute] | None = None,
) -> RouteSearch:
    if catalog is None:
        catalog = route_catalog()
    scores = tuple(score_route(rows, route) for route in catalog)
    broad = tuple(
        sorted(
            scores,
            key=lambda result: (
                result.distinct_edges,
                result.effective_uniform_choices,
                route_sort_key(result.route),
            ),
        )
    )
    additive = tuple(
        sorted(
            scores,
            key=lambda result: (
                result.difference_support,
                result.distinct_edges,
                result.effective_uniform_choices,
                route_sort_key(result.route),
            ),
        )
    )
    return RouteSearch(broad, additive)


def equivalent_coordinate_order(
    lengths: Sequence[int],
    left: SixStreamRoute,
    right: SixStreamRoute,
) -> bool:
    left_coordinates = route_coordinates(lengths, left)
    right_coordinates = route_coordinates(lengths, right)
    return (
        left_coordinates == right_coordinates
        or left_coordinates == tuple(reversed(right_coordinates))
    )


def coordinate_equivalence_class(
    lengths: Sequence[int],
    catalog: Sequence[SixStreamRoute],
    selected: SixStreamRoute,
) -> tuple[SixStreamRoute, ...]:
    """Return every declared route with the selected A path or its reversal."""
    return tuple(
        route
        for route in catalog
        if equivalent_coordinate_order(lengths, route, selected)
    )


def globally_equivalent_coordinate_order(
    length_sets: Sequence[Sequence[int]],
    left: SixStreamRoute,
    right: SixStreamRoute,
) -> bool:
    """Test coordinate-order equivalence across every supplied length set."""
    return all(
        equivalent_coordinate_order(lengths, left, right)
        for lengths in length_sets
    )


def scatter_path(
    path: Sequence[int],
    lengths: Sequence[int],
    route: SixStreamRoute,
    *,
    seed: int,
) -> tuple[tuple[int, ...], ...]:
    coordinates = route_coordinates(lengths, route)
    if len(path) != len(coordinates):
        raise ValueError("path length does not match route")
    rng = random.Random(seed)
    rows: list[list[int | None]] = [
        [None] * length for length in lengths
    ]
    for value, (row, index) in zip(path, coordinates, strict=True):
        rows[row][index] = value
    for row in rows:
        for index, value in enumerate(row):
            if value is not None:
                continue
            forbidden = {
                neighbor
                for neighbor in (
                    row[index - 1] if index > 0 else None,
                    row[index + 1] if index + 1 < len(row) else None,
                )
                if neighbor is not None
            }
            choices = [
                candidate
                for candidate in range(SIZE)
                if candidate not in forbidden
            ]
            row[index] = rng.choice(choices)
    result = tuple(tuple(int(value) for value in row) for row in rows)
    if any(
        left == right
        for row in result
        for left, right in zip(row, row[1:])
    ):
        raise AssertionError("scatter created an adjacent double")
    return result


def generate_action_control(
    lengths: Sequence[int],
    route: SixStreamRoute,
    shifts: Sequence[int],
    weights: Sequence[float],
    *,
    seed: int,
) -> tuple[tuple[int, ...], ...]:
    """Generate a no-double routed path using at most 42 visible translations."""
    if len(shifts) != 42 or len(set(shifts)) != 42:
        raise ValueError("control requires 42 distinct shifts")
    if any(shift not in range(1, SIZE) for shift in shifts):
        raise ValueError("control shifts must be nonzero modulo 83")
    if len(weights) != 42 or any(weight <= 0 for weight in weights):
        raise ValueError("control requires 42 positive action weights")
    coordinates = route_coordinates(lengths, route)
    if not coordinates:
        return scatter_path((), lengths, route, seed=seed)

    rng = random.Random(seed)
    path = [rng.randrange(SIZE)]
    assigned = {coordinates[0]: path[0]}
    action_indices = tuple(range(42))
    for coordinate in coordinates[1:]:
        row, index = coordinate
        forbidden = {
            assigned[neighbor]
            for neighbor in ((row, index - 1), (row, index + 1))
            if neighbor in assigned
        }
        previous = path[-1]
        next_value: int | None = None
        for _attempt in range(100):
            action = rng.choices(action_indices, weights=weights, k=1)[0]
            candidate = (previous + shifts[action]) % SIZE
            if candidate not in forbidden:
                next_value = candidate
                break
        if next_value is None:
            allowed = [
                (previous + shift) % SIZE
                for shift in shifts
                if (previous + shift) % SIZE not in forbidden
            ]
            if not allowed:
                raise RuntimeError("no action avoids a supplied-row double")
            next_value = rng.choice(allowed)
        path.append(next_value)
        assigned[coordinate] = next_value

    return scatter_path(path, lengths, route, seed=seed ^ 0x5CA77E2)
