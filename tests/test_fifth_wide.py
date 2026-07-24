import unittest

from eye_mystery.fifth_wide import (
    best_cellular_fit,
    best_grid_fit,
    best_radix_fit,
    best_stable_sort_fit,
    cellular_leave_one_pair_out,
    directed_edge_reuse,
    radix_values,
    transition_occupancy,
    turtle_bounding_area,
)


class FifthWideTests(unittest.TestCase):
    def test_directed_edge_reuse(self) -> None:
        self.assertEqual(directed_edge_reuse(((1, 2, 1, 2), (2, 3))), (1, 4, 3))

    def test_transition_occupancy(self) -> None:
        score = transition_occupancy(((0, 1, 2), (0, 2, 1)))
        self.assertEqual(
            (
                score.events,
                score.distinct_edges,
                score.maximum_outdegree,
                score.maximum_indegree,
            ),
            (4, 4, 2, 2),
        )

    def test_cellular_fit_recovers_shifted_center_rule(self) -> None:
        pairs = (
            ((0, 1, 2, 3, 4), (4, 0, 1, 2, 3)),
            ((4, 3, 2, 1, 0), (0, 4, 3, 2, 1)),
        )
        fit = best_cellular_fit(pairs, maximum_radius=0, maximum_shift=1)
        self.assertEqual((fit.correct, fit.samples, fit.shift), (8, 8, 1))
        cross_validation = cellular_leave_one_pair_out(
            pairs, radius=fit.radius, shift=fit.shift
        )
        self.assertEqual(
            (cross_validation.correct, cross_validation.covered), (6, 6)
        )

    def test_radix_conversion_and_selection(self) -> None:
        self.assertEqual(radix_values((1, 0), 10, 2), (1, 0, 1, 0))
        fit = best_radix_fit(((65, 66, 67),))
        self.assertGreater(fit.length, 0)

    def test_stable_sort_fit_finds_component_order(self) -> None:
        rows = ((0, 25, 50, 75), (1, 26, 51, 76))
        fit = best_stable_sort_fit(rows)
        self.assertEqual(fit.fraction, 1.0)
        self.assertEqual(fit.component_order[0], 0)

    def test_grid_fit_recovers_digitwise_sum(self) -> None:
        records = ((31, 6, 25), (62, 31, 31))
        fit = best_grid_fit(records)
        self.assertEqual((fit.matches, fit.operation), (2, "sum"))

    def test_turtle_bounding_area(self) -> None:
        self.assertEqual(turtle_bounding_area((2, 3, 4, 1)), 4)


if __name__ == "__main__":
    unittest.main()
