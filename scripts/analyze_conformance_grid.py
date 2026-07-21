#!/usr/bin/env python3
"""Probe the Eye headers and bodies as a 3×3 conformance suite."""

from eye_mystery.conformance_grid import (
    affine_grid_projection_count,
    are_opposite_three_cycles,
    common_prefix_length,
    count_opposite_cycle_assignments,
    determinant_three,
    edge_component_order,
    edges_enumerate_component_orders,
    marker_control_edge,
    marker_digits,
    parity_boundary_echo,
    permute_trigram,
)
from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values


def main() -> None:
    streams = {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}
    markers = tuple(streams[name][0] for name in MESSAGE_ORDER)
    bodies = tuple(streams[name][1:] for name in MESSAGE_ORDER)
    edges = tuple(map(marker_control_edge, markers))
    prefix_depths = tuple(
        common_prefix_length(bodies[start : start + 3]) for start in (0, 3, 6)
    )
    sums = tuple(sum(streams[name]) % 101 for name in MESSAGE_ORDER)
    matrix = tuple(sums[start : start + 3] for start in (0, 3, 6))
    matches, total = count_opposite_cycle_assignments(edges)
    features = tuple(
        (first - 1, middle, third)
        for first, middle, third in map(marker_digits, markers)
    )

    print("control edges:", edges)
    print("first two rows are opposite cycles:", are_opposite_three_cycles(edges[:3], edges[3:6]))
    print("first six enumerate S3:", edges_enumerate_component_orders(edges[:6]))
    print("component orders:", tuple(map(edge_component_order, edges[:6])))
    print("conditional assignments:", matches, "/", total)
    print("body common-prefix depths by row:", prefix_depths)
    print("mod-101 matrix:", matrix)
    print("determinant mod 101:", determinant_three(matrix, 101))
    print("affine marker-to-grid projections over F3:", affine_grid_projection_count(features))

    even_row = ("east1", "west1", "east2")
    odd_row = ("west2", "east3", "west3")
    echoes = {
        (even, odd): parity_boundary_echo(streams, even, odd)
        for even in even_row
        for odd in odd_row
    }
    target_echo = parity_boundary_echo(streams, "east2", "west2")
    print("parity-boundary body echo values:", target_echo)
    print("parity-boundary body echo digits:", tuple(digit for value in target_echo for digit in marker_digits(value)))
    print("parity-boundary body echo ASCII+32:", "".join(chr(value + 32) for value in target_echo))
    print("exact !Fi echoes in 3x3 family:", sum(value == (1, 38, 73) for value in echoes.values()), "/", len(echoes))

    for self_order in ((0, 1, 2), (0, 2, 1)):
        for invert in (False, True):
            transformed = []
            for edge, body in zip(edges, bodies):
                order = self_order if edge[0] == edge[1] else edge_component_order(edge)
                if invert:
                    order = tuple(order.index(index) for index in range(3))
                transformed.append(tuple(permute_trigram(value, order) for value in body))
            flat = tuple(value for body in transformed for value in body)
            row_prefixes = tuple(
                common_prefix_length(transformed[start : start + 3])
                for start in (0, 3, 6)
            )
            print(
                "per-panel reorder",
                f"self={self_order}",
                f"inverse={invert}",
                f"alphabet={len(set(flat))}",
                f"above82={sum(value > 82 for value in flat)}",
                f"row-prefixes={row_prefixes}",
            )


if __name__ == "__main__":
    main()
