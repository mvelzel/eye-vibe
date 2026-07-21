from __future__ import annotations

import unittest

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.suffix_rows import (
    complete_bwt_rows_pass_first_column_test,
    count_realisable_orders,
    lcp_divergence,
    natural_trigram_sort_orders,
    order_constraints,
    order_is_realisable,
)


TRIE_ORDER = (
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


class SuffixRowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        values = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }
        cls.markers = {name: stream[0] for name, stream in values.items()}
        cls.bodies = {name: stream[1:] for name, stream in values.items()}

    def test_marker_order_lcp_and_inequalities(self) -> None:
        self.assertEqual(
            tuple(
                lcp_divergence(self.bodies[left], self.bodies[right])[0]
                for left, right in zip(TRIE_ORDER, TRIE_ORDER[1:])
            ),
            (24, 24, 2, 5, 20, 20, 9, 5),
        )
        self.assertEqual(
            order_constraints(TRIE_ORDER, self.bodies),
            (
                (80, 29),
                (29, 69),
                (48, 49),
                (69, 2),
                (77, 60),
                (60, 33),
                (2, 78),
                (2, 23),
            ),
        )
        self.assertTrue(order_is_realisable(TRIE_ORDER, self.bodies))

    def test_all_realisable_orders_are_the_864_trie_leaf_orders(self) -> None:
        self.assertEqual(count_realisable_orders(self.bodies), 864)

    def test_no_shared_natural_trigram_order_selects_marker_order(self) -> None:
        orders = natural_trigram_sort_orders(self.bodies)
        self.assertEqual(len(orders), 182)
        self.assertNotIn(TRIE_ORDER, orders)
        self.assertNotIn(TRIE_ORDER[::-1], orders)

    def test_distinct_markers_cannot_be_complete_bwt_last_column(self) -> None:
        self.assertFalse(
            complete_bwt_rows_pass_first_column_test(self.bodies, self.markers)
        )


if __name__ == "__main__":
    unittest.main()
