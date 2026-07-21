"""Two complementary message orders encoded by the initial trigrams."""

from __future__ import annotations

from collections.abc import Sequence
from itertools import permutations, product

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.initials import initial_digits, perfect_successor_rotation
from eye_mystery.prefix_hierarchy import PrefixCluster, prefix_clusters


MARKER_TRIE_ORDER = (
    "east1",
    "west1",
    "east2",
    "west2",
    "east4",
    "west4",
    "east5",
    "east3",
    "west3",
)


def marker_lexicographic_order(
    digit_order: tuple[int, int, int] = (2, 0, 1),
    signs: tuple[int, int, int] = (1, 1, 1),
) -> tuple[str, ...]:
    """Sort messages by signed marker digits, with the third as tie-breaker."""

    if tuple(sorted(digit_order)) != (0, 1, 2):
        raise ValueError("digit_order must be a permutation of (0, 1, 2)")
    if any(sign not in (-1, 1) for sign in signs):
        raise ValueError("signs must contain only -1 or 1")
    digits = dict(zip(MESSAGE_ORDER, initial_digits(), strict=True))
    return tuple(
        sorted(
            MESSAGE_ORDER,
            key=lambda name: tuple(
                sign * digits[name][digit]
                for sign, digit in zip(signs, digit_order, strict=True)
            ),
        )
    )


def eye_prefix_clusters() -> tuple[PrefixCluster, ...]:
    streams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    return prefix_clusters(streams, start=1)


def clusters_are_contiguous(
    order: Sequence[str], clusters: Sequence[PrefixCluster]
) -> bool:
    """Return whether every non-root prefix cluster is an interval."""

    positions = {name: index for index, name in enumerate(order)}
    if set(positions) != set(MESSAGE_ORDER):
        raise ValueError("order must contain every message exactly once")
    return all(
        max(positions[name] for name in cluster.members)
        - min(positions[name] for name in cluster.members)
        + 1
        == len(cluster.members)
        for cluster in clusters
        if len(cluster.members) < len(MESSAGE_ORDER)
    )


def marker_order_composition_counts() -> dict[str, int]:
    """Enumerate observed-marker assignments for the two ordering rules.

    ``fixed_chain`` requires all eight links in the East-5-first order.
    ``fixed_sort`` uses ascending digits ``(third, first, middle)`` and asks
    that every ciphertext-prefix cluster be contiguous.  The ``any`` variants
    allow any cyclic trail start and any signed choice of two sorting digits.
    The denominator for every count is ``9!``.
    """

    markers = initial_digits()
    cluster_indices = tuple(
        tuple(MESSAGE_ORDER.index(name) for name in cluster.members)
        for cluster in eye_prefix_clusters()
        if len(cluster.members) < len(MESSAGE_ORDER)
    )
    trail = (8, 0, 1, 2, 3, 4, 5, 6, 7)

    sort_keys = tuple(
        (digits, signs)
        for digits in permutations(range(3), 2)
        for signs in product((1, -1), repeat=2)
    )
    marker_sort_orders = []
    for digits, signs in sort_keys:
        remaining = 3 - digits[0] - digits[1]
        marker_sort_orders.append(
            tuple(
                sorted(
                    range(9),
                    key=lambda marker: (
                        signs[0] * markers[marker][digits[0]],
                        signs[1] * markers[marker][digits[1]],
                        markers[marker][remaining],
                    ),
                )
            )
        )
    fixed_marker_sort = tuple(
        sorted(
            range(9),
            key=lambda marker: (
                markers[marker][2],
                markers[marker][0],
                markers[marker][1],
            ),
        )
    )

    def compatible(order: tuple[int, ...]) -> bool:
        positions = [0] * 9
        for index, message in enumerate(order):
            positions[message] = index
        return all(
            max(positions[message] for message in cluster)
            - min(positions[message] for message in cluster)
            + 1
            == len(cluster)
            for cluster in cluster_indices
        )

    counts = {
        "fixed_chain": 0,
        "any_chain": 0,
        "fixed_sort": 0,
        "any_sort": 0,
        "both_fixed": 0,
        "fixed_chain_any_sort": 0,
        "any_chain_fixed_sort": 0,
        "both_any": 0,
    }
    for assignment in permutations(range(9)):
        fixed_chain = all(
            markers[assignment[trail[index]]][0] - 1
            == markers[assignment[trail[index + 1]]][1]
            for index in range(8)
        )
        circular_links = sum(
            markers[assignment[index]][0] - 1
            == markers[assignment[(index + 1) % 9]][1]
            for index in range(9)
        )
        any_chain = circular_links >= 8

        inverse = [0] * 9
        for message, marker in enumerate(assignment):
            inverse[marker] = message
        fixed_sort = compatible(
            tuple(inverse[marker] for marker in fixed_marker_sort)
        )
        any_sort = any(
            compatible(tuple(inverse[marker] for marker in marker_order))
            for marker_order in marker_sort_orders
        )

        events = {
            "fixed_chain": fixed_chain,
            "any_chain": any_chain,
            "fixed_sort": fixed_sort,
            "any_sort": any_sort,
            "both_fixed": fixed_chain and fixed_sort,
            "fixed_chain_any_sort": fixed_chain and any_sort,
            "any_chain_fixed_sort": any_chain and fixed_sort,
            "both_any": any_chain and any_sort,
        }
        for name, event in events.items():
            counts[name] += event
    return counts


def marker_order_summary() -> dict[str, object]:
    order = marker_lexicographic_order()
    clusters = eye_prefix_clusters()
    return {
        "trail_order": perfect_successor_rotation(),
        "trie_order": order,
        "trie_order_is_contiguous": clusters_are_contiguous(order, clusters),
        "third_digit_multiset": tuple(
            sorted(digits[2] for digits in initial_digits())
        ),
    }
