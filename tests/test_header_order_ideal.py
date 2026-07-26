import unittest

from eye_mystery.header_order_ideal import (
    FULL_CUBE_SIZE,
    MESSAGE_ORDER,
    OMITTED_SIZE,
    ROUTES,
    VISIBLE_SIZE,
    affine_label_maps,
    audit_header_order_ideal,
    audit_visible_rerank,
    full_cube_rank,
    header_eye_order,
    omission_table,
    selected_route,
    selected_visible_route,
    visible_rank_table,
)


class HeaderOrderIdealTests(unittest.TestCase):
    def test_omission_is_exact_number_of_excluded_predecessors(self) -> None:
        order = (0, 3, 1, 4, 2)
        visible_ranks = visible_rank_table(order)
        omissions = omission_table(order)
        excluded = set(range(VISIBLE_SIZE, FULL_CUBE_SIZE))
        for value in range(VISIBLE_SIZE):
            rank = full_cube_rank(value, order)
            expected = sum(
                full_cube_rank(missing, order) < rank
                for missing in excluded
            )
            self.assertEqual(omissions[value], expected)
            self.assertEqual(rank - visible_ranks[value], expected)

    def test_real_headers_induce_five_eye_orders(self) -> None:
        for name in MESSAGE_ORDER:
            for route in ROUTES:
                self.assertEqual(
                    sorted(header_eye_order(name, route)),
                    list(range(5)),
                )

    def test_all_affine_maps_are_distinct_permutations(self) -> None:
        maps = affine_label_maps()
        self.assertEqual(len(maps), 82 * 83)
        self.assertEqual(len(set(maps)), len(maps))
        self.assertIn(tuple(range(VISIBLE_SIZE)), maps)
        for label_map in maps:
            self.assertEqual(sorted(label_map), list(range(VISIBLE_SIZE)))

    def test_audit_contains_the_observation_and_respects_range(self) -> None:
        audit = audit_header_order_ideal()
        self.assertEqual(audit.control_count, 82 * 83)
        self.assertGreaterEqual(audit.holdout_tail_count, 1)
        self.assertGreaterEqual(
            audit.maximum_control_holdout,
            audit.observed.holdout_agreements,
        )
        self.assertIn(audit.observed.route, ROUTES)
        self.assertLessEqual(audit.observed_support, OMITTED_SIZE + 1)
        self.assertEqual(selected_route(), audit.observed)

    def test_visible_rerank_audit_contains_the_observation(self) -> None:
        audit = audit_visible_rerank()
        self.assertEqual(audit.control_count, 82 * 83)
        self.assertGreaterEqual(audit.holdout_tail_count, 1)
        self.assertGreaterEqual(
            audit.maximum_control_holdout,
            audit.observed.holdout_agreements,
        )
        self.assertEqual(selected_visible_route(), audit.observed)


if __name__ == "__main__":
    unittest.main()
