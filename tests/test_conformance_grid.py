from __future__ import annotations

import unittest

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


class ConformanceGridTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }
        cls.markers = tuple(cls.streams[name][0] for name in MESSAGE_ORDER)
        cls.bodies = tuple(cls.streams[name][1:] for name in MESSAGE_ORDER)

    def test_first_six_edges_are_opposite_cycles(self) -> None:
        edges = tuple(map(marker_control_edge, self.markers))
        self.assertEqual(
            edges[:6],
            ((0, 1), (1, 2), (2, 0), (0, 2), (2, 1), (1, 0)),
        )
        self.assertTrue(are_opposite_three_cycles(edges[:3], edges[3:6]))
        self.assertTrue(edges_enumerate_component_orders(edges[:6]))
        self.assertEqual(
            tuple(map(edge_component_order, edges[:6])),
            (
                (0, 1, 2),
                (1, 2, 0),
                (2, 0, 1),
                (0, 2, 1),
                (2, 1, 0),
                (1, 0, 2),
            ),
        )
        self.assertEqual(count_opposite_cycle_assignments(edges), (108, 90_720))

    def test_each_natural_row_has_a_common_body_prefix(self) -> None:
        self.assertEqual(
            tuple(
                common_prefix_length(self.bodies[start : start + 3])
                for start in (0, 3, 6)
            ),
            (24, 5, 20),
        )

    def test_checksum_matrix_is_full_rank(self) -> None:
        sums = tuple(sum(self.streams[name]) % 101 for name in MESSAGE_ORDER)
        matrix = tuple(sums[start : start + 3] for start in (0, 3, 6))
        self.assertEqual(matrix, ((0, 84, 7), (53, 0, 1), (32, 88, 0)))
        self.assertEqual(determinant_three(matrix, 101), 87)

    def test_headers_are_not_affine_grid_coordinates(self) -> None:
        features = tuple(
            (first - 1, middle, third)
            for first, middle, third in map(marker_digits, self.markers)
        )
        self.assertEqual(affine_grid_projection_count(features), 0)

    def test_direct_per_panel_component_unscramble_loses_structure(self) -> None:
        edges = tuple(map(marker_control_edge, self.markers))
        for self_order in ((0, 1, 2), (0, 2, 1)):
            for invert in (False, True):
                transformed = []
                for edge, body in zip(edges, self.bodies):
                    order = (
                        self_order
                        if edge[0] == edge[1]
                        else edge_component_order(edge)
                    )
                    if invert:
                        order = tuple(order.index(index) for index in range(3))
                    transformed.append(
                        tuple(permute_trigram(value, order) for value in body)
                    )
                flat = tuple(value for body in transformed for value in body)
                self.assertEqual(len(set(flat)), 117)
                self.assertGreaterEqual(sum(value > 82 for value in flat), 176)
                self.assertEqual(
                    tuple(
                        common_prefix_length(transformed[start : start + 3])
                        for start in (0, 3, 6)
                    ),
                    (0, 0, 0),
                )

    def test_parity_boundary_echo_matches_marker_bwt_digits(self) -> None:
        from eye_mystery.marker_bwt import marker_bwt_summary

        echo = parity_boundary_echo(self.streams, "east2", "west2")
        self.assertEqual(echo, (1, 38, 73))
        self.assertEqual("".join(chr(value + 32) for value in echo), "!Fi")
        self.assertEqual(echo, marker_bwt_summary()["values"])
        self.assertEqual(
            tuple(digit for value in echo for digit in marker_digits(value)),
            marker_bwt_summary()["restored_digits"],
        )

        echoes = {
            parity_boundary_echo(self.streams, even, odd)
            for even in ("east1", "west1", "east2")
            for odd in ("west2", "east3", "west3")
        }
        self.assertEqual(len(echoes), 9)
        self.assertEqual(sum(value == echo for value in echoes), 1)


if __name__ == "__main__":
    unittest.main()
