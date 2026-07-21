"""Structural probes for the nine messages as a 3×3 conformance grid."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Iterator, Sequence
from itertools import product
from itertools import permutations


Edge = tuple[int, int]


def marker_digits(value: int) -> tuple[int, int, int]:
    if not 0 <= value < 125:
        raise ValueError("marker is not a base-five trigram")
    return value // 25, (value // 5) % 5, value % 5


def marker_control_edge(value: int) -> Edge:
    """Decode the established ``middle -> first-1`` three-state edge."""

    first, middle, _ = marker_digits(value)
    if first not in (1, 2, 3) or middle not in (0, 1, 2):
        raise ValueError("marker does not encode a three-state control edge")
    return middle, first - 1


def is_directed_three_cycle(edges: Sequence[Edge]) -> bool:
    """Whether three ordered edges form one loop through all three states."""

    if len(edges) != 3:
        return False
    return (
        all(target == edges[(index + 1) % 3][0] for index, (_, target) in enumerate(edges))
        and {source for source, _ in edges} == {0, 1, 2}
        and all(source != target for source, target in edges)
    )


def are_opposite_three_cycles(first: Sequence[Edge], second: Sequence[Edge]) -> bool:
    """Whether two rows are the two orientations of the loop on three states."""

    return (
        is_directed_three_cycle(first)
        and is_directed_three_cycle(second)
        and set(first).isdisjoint(second)
        and set(first) | set(second)
        == {(source, target) for source in range(3) for target in range(3) if source != target}
    )


def edge_component_order(edge: Edge) -> tuple[int, int, int]:
    """Name an eye-component permutation by source, target, then remainder."""

    source, target = edge
    if source == target or source not in range(3) or target not in range(3):
        raise ValueError("a non-self three-state edge is required")
    return source, target, 3 - source - target


def edges_enumerate_component_orders(edges: Sequence[Edge]) -> bool:
    """Whether the edges name every element of S3 exactly once."""

    if any(source == target for source, target in edges):
        return False
    return set(map(edge_component_order, edges)) == set(permutations(range(3)))


def permute_trigram(value: int, order: Sequence[int]) -> int:
    if sorted(order) != [0, 1, 2]:
        raise ValueError("order is not a permutation of three components")
    digits = marker_digits(value)
    return 25 * digits[order[0]] + 5 * digits[order[1]] + digits[order[2]]


def parity_boundary_echo(
    streams: dict[str, Sequence[int]],
    even_name: str,
    odd_name: str,
    *,
    odd_row_prefix_length: int = 5,
) -> tuple[int, int, int]:
    """Apply header S3 orders to a frozen root/frame/exit construction.

    Streams include their marker at offset zero.  The two-symbol universal
    body root is reversed, as in a backwards/BWT-style reconstruction, and
    transformed by one even-row header.  The first symbol after the odd row's
    shared body prefix is transformed by its own header and appended.
    """

    even_stream = streams[even_name]
    odd_stream = streams[odd_name]
    if len(even_stream) < 3 or len(odd_stream) <= odd_row_prefix_length + 1:
        raise ValueError("streams are too short for the boundary construction")
    even_edge = marker_control_edge(even_stream[0])
    odd_edge = marker_control_edge(odd_stream[0])
    even_order = edge_component_order(even_edge)
    odd_order = edge_component_order(odd_edge)
    return (
        permute_trigram(even_stream[2], even_order),
        permute_trigram(even_stream[1], even_order),
        permute_trigram(odd_stream[1 + odd_row_prefix_length], odd_order),
    )


def distinct_multiset_permutations(values: Iterable[Edge]) -> Iterator[tuple[Edge, ...]]:
    """Yield every distinct ordering without materializing duplicate tuples."""

    counts = Counter(values)
    length = sum(counts.values())
    current: list[Edge] = []

    def visit() -> Iterator[tuple[Edge, ...]]:
        if len(current) == length:
            yield tuple(current)
            return
        for value in tuple(counts):
            if not counts[value]:
                continue
            counts[value] -= 1
            current.append(value)
            yield from visit()
            current.pop()
            counts[value] += 1

    yield from visit()


def count_opposite_cycle_assignments(edges: Sequence[Edge]) -> tuple[int, int]:
    """Count multiset assignments whose first two rows are opposite cycles."""

    total = 0
    matches = 0
    for assignment in distinct_multiset_permutations(edges):
        total += 1
        matches += are_opposite_three_cycles(assignment[:3], assignment[3:6])
    return matches, total


def common_prefix_length(streams: Sequence[Sequence[int]]) -> int:
    if not streams:
        return 0
    length = 0
    for values in zip(*streams):
        if len(set(values)) != 1:
            break
        length += 1
    return length


def determinant_three(matrix: Sequence[Sequence[int]], modulus: int) -> int:
    if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
        raise ValueError("expected a 3×3 matrix")
    a = matrix
    return (
        a[0][0] * a[1][1] * a[2][2]
        + a[0][1] * a[1][2] * a[2][0]
        + a[0][2] * a[1][0] * a[2][1]
        - a[0][2] * a[1][1] * a[2][0]
        - a[0][1] * a[1][0] * a[2][2]
        - a[0][0] * a[1][2] * a[2][1]
    ) % modulus


def affine_grid_projection_count(features: Sequence[Sequence[int]]) -> int:
    """Count affine F3 maps of marker features to the fixed nine grid cells."""

    if len(features) != 9 or any(len(row) != 3 for row in features):
        raise ValueError("expected nine three-component marker features")
    augmented = tuple(tuple(value % 3 for value in row) + (1,) for row in features)
    forms = tuple(
        tuple(sum(weight * value for weight, value in zip(weights, row)) % 3 for row in augmented)
        for weights in product(range(3), repeat=4)
    )
    target_rows = tuple(index // 3 for index in range(9))
    target_columns = tuple(index % 3 for index in range(9))
    return sum(
        row_form == target_rows and column_form == target_columns
        for row_form in forms
        for column_form in forms
    )
