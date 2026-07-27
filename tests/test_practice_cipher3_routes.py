import random
import unittest

from eye_mystery.practice_cipher3_routes import (
    SixStreamRoute,
    apply_route,
    coordinate_equivalence_class,
    equivalent_coordinate_order,
    generate_action_control,
    globally_equivalent_coordinate_order,
    route_catalog,
    route_coordinates,
    scatter_path,
    score_route,
)


class PracticeCipher3RoutesTests(unittest.TestCase):
    def test_frozen_catalog_has_17280_routes(self) -> None:
        catalog = route_catalog()
        self.assertEqual(len(catalog), 17_280)
        self.assertEqual(sum(route.kind == "row" for route in catalog), 5_760)
        self.assertEqual(
            sum(route.kind == "column" for route in catalog),
            11_520,
        )

    def test_scatter_and_route_round_trip(self) -> None:
        lengths = (7, 9, 8, 6, 10, 5)
        routes = (
            SixStreamRoute(
                "row",
                True,
                (2, 5, 1, 4, 0, 3),
                "snake-reverse",
            ),
            SixStreamRoute(
                "column",
                True,
                (4, 1, 5, 0, 3, 2),
                "snake",
                True,
                True,
            ),
        )
        for route_index, route in enumerate(routes):
            with self.subTest(route=route):
                path = tuple(
                    index % 83
                    for index in range(len(route_coordinates(lengths, route)))
                )
                rows = scatter_path(
                    path,
                    lengths,
                    route,
                    seed=route_index,
                )
                self.assertEqual(apply_route(rows, route), path)

    def test_action_control_uses_at_most_42_steps_and_has_no_doubles(self) -> None:
        lengths = (19, 21, 23, 18, 22, 20)
        route = SixStreamRoute(
            "column",
            False,
            (4, 1, 5, 0, 3, 2),
            "snake",
            True,
            True,
        )
        shifts = random.Random(7).sample(range(1, 83), 42)
        rows = generate_action_control(
            lengths,
            route,
            shifts,
            tuple(43 - index for index in range(42)),
            seed=11,
        )
        audit = score_route(rows, route)
        self.assertLessEqual(audit.difference_support, 42)
        self.assertTrue(
            all(
                left != right
                for row in rows
                for left, right in zip(row, row[1:])
            )
        )

    def test_global_reversal_is_an_equivalent_coordinate_order(self) -> None:
        lengths = (5, 6, 7, 8, 9, 10)
        forward = SixStreamRoute(
            "row",
            False,
            (0, 1, 2, 3, 4, 5),
            "forward",
        )
        reverse = SixStreamRoute(
            "row",
            False,
            (5, 4, 3, 2, 1, 0),
            "reverse",
        )
        self.assertTrue(
            equivalent_coordinate_order(lengths, forward, reverse)
        )

    def test_a_equivalence_can_break_when_ragged_width_changes(self) -> None:
        selected = SixStreamRoute(
            "column",
            True,
            (4, 1, 5, 0, 3, 2),
            "snake",
            True,
            False,
        )
        counterpart = SixStreamRoute(
            "column",
            True,
            (4, 1, 5, 0, 3, 2),
            "snake",
            True,
            True,
        )
        lengths_a = (57, 65, 57, 66, 66, 67)
        lengths_b = (115, 117, 126, 111, 115, 120)
        catalog = (selected, counterpart)
        a_class = coordinate_equivalence_class(
            lengths_a,
            catalog,
            selected,
        )
        self.assertEqual(a_class, catalog)
        self.assertFalse(
            globally_equivalent_coordinate_order(
                (lengths_a, lengths_b),
                selected,
                counterpart,
            )
        )


if __name__ == "__main__":
    unittest.main()
