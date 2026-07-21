"""Key-free checks for a suffix-array interpretation of the Eye bodies."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from itertools import permutations


def lcp_divergence(
    left: Sequence[int], right: Sequence[int]
) -> tuple[int, int | None, int | None]:
    """Return common-prefix length and the first two differing labels."""

    length = 0
    limit = min(len(left), len(right))
    while length < limit and left[length] == right[length]:
        length += 1
    left_value = left[length] if length < len(left) else None
    right_value = right[length] if length < len(right) else None
    return length, left_value, right_value


def order_constraints(
    order: Sequence[str], streams: Mapping[str, Sequence[int]]
) -> tuple[tuple[int, int], ...] | None:
    """Return alphabet inequalities needed to sort streams in ``order``.

    ``None`` means a longer stream precedes one of its own exact prefixes, so
    no symbol ordering can realize the requested lexicographic order.
    """

    edges: list[tuple[int, int]] = []
    for left_name, right_name in zip(order, order[1:]):
        _, left, right = lcp_divergence(streams[left_name], streams[right_name])
        if left is None:
            continue
        if right is None:
            return None
        edges.append((left, right))
    return tuple(edges)


def constraints_are_acyclic(edges: Sequence[tuple[int, int]]) -> bool:
    """Whether the strict alphabet inequalities admit a total extension."""

    successors: dict[int, set[int]] = {}
    for left, right in edges:
        if left == right:
            return False
        successors.setdefault(left, set()).add(right)

    visited: set[int] = set()
    active: set[int] = set()

    def visit(node: int) -> bool:
        if node in active:
            return False
        if node in visited:
            return True
        active.add(node)
        if any(not visit(target) for target in successors.get(node, ())):
            return False
        active.remove(node)
        visited.add(node)
        return True

    return all(visit(node) for node in tuple(successors))


def order_is_realisable(
    order: Sequence[str], streams: Mapping[str, Sequence[int]]
) -> bool:
    edges = order_constraints(order, streams)
    return edges is not None and constraints_are_acyclic(edges)


def count_realisable_orders(streams: Mapping[str, Sequence[int]]) -> int:
    """Exhaust every panel order under an otherwise arbitrary alphabet."""

    names = tuple(streams)
    return sum(order_is_realisable(order, streams) for order in permutations(names))


def trigram_digits(value: int) -> tuple[int, int, int]:
    if not 0 <= value < 125:
        raise ValueError("value is not a base-five trigram")
    return value // 25, (value // 5) % 5, value % 5


def natural_trigram_sort_orders(
    streams: Mapping[str, Sequence[int]],
) -> set[tuple[str, ...]]:
    """Sort under 6 eye priorities × 120 shared direction orders."""

    names = tuple(streams)
    results: set[tuple[str, ...]] = set()
    for eye_order in permutations(range(3)):
        for direction_order in permutations(range(5)):
            direction_rank = {
                value: rank for rank, value in enumerate(direction_order)
            }

            def label_key(value: int) -> tuple[int, int, int]:
                digits = trigram_digits(value)
                return tuple(direction_rank[digits[index]] for index in eye_order)

            results.add(
                tuple(
                    sorted(
                        names,
                        key=lambda name: tuple(
                            label_key(value) for value in streams[name]
                        ),
                    )
                )
            )
    return results


def complete_bwt_rows_pass_first_column_test(
    bodies: Mapping[str, Sequence[int]], markers: Mapping[str, int]
) -> bool:
    """Necessary multiset test for bodies as all rows of one BWT matrix.

    A complete sorted-rotation matrix has the same symbol multiset in its first
    and last columns.  Here the proposed last column is the distinct marker
    set and the proposed first column is the first body symbol of every row.
    """

    if set(bodies) != set(markers):
        raise ValueError("body and marker names differ")
    if any(not body for body in bodies.values()):
        raise ValueError("BWT rows cannot be empty")
    return sorted(body[0] for body in bodies.values()) == sorted(markers.values())
