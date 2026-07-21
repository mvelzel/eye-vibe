"""Alternative parity-aware orders for the three eyes in each triangle."""

from __future__ import annotations

from collections.abc import Sequence
from itertools import permutations


TRIANGLE_ORDERS = tuple(permutations(range(3)))


def values_for_orders(
    message: Sequence[int],
    even_order: tuple[int, int, int],
    odd_order: tuple[int, int, int],
) -> tuple[int, ...]:
    """Read grouped eyes using separate orders for alternating triangles."""

    if len(message) % 3:
        raise ValueError("eye stream length must be divisible by three")
    result = []
    for symbol_index, start in enumerate(range(0, len(message), 3)):
        triangle = message[start : start + 3]
        order = even_order if symbol_index % 2 == 0 else odd_order
        result.append(
            25 * triangle[order[0]]
            + 5 * triangle[order[1]]
            + triangle[order[2]]
        )
    return tuple(result)


def is_canonical_range(values: Sequence[int]) -> bool:
    return set(values) == set(range(83))
