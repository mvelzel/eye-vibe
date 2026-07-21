import unittest

from eye_mystery.marker_orders import (
    MARKER_TRIE_ORDER,
    clusters_are_contiguous,
    eye_prefix_clusters,
    marker_lexicographic_order,
    marker_order_composition_counts,
    marker_order_summary,
)


class MarkerOrderTests(unittest.TestCase):
    def test_third_then_first_digit_orders_prefix_trie(self) -> None:
        self.assertEqual(marker_lexicographic_order(), MARKER_TRIE_ORDER)
        self.assertTrue(
            clusters_are_contiguous(
                MARKER_TRIE_ORDER, eye_prefix_clusters()
            )
        )
        self.assertEqual(
            marker_order_summary()["third_digit_multiset"],
            (0, 0, 1, 1, 2, 2, 3, 3, 4),
        )

    def test_exact_observed_marker_assignment_composition_counts(self) -> None:
        self.assertEqual(
            marker_order_composition_counts(),
            {
                "fixed_chain": 168,
                "any_chain": 1_512,
                "fixed_sort": 864,
                "any_sort": 11_592,
                "both_fixed": 1,
                "fixed_chain_any_sort": 1,
                "any_chain_fixed_sort": 8,
                "both_any": 22,
            },
        )


if __name__ == "__main__":
    unittest.main()
