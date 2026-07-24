from __future__ import annotations

import unittest

from eye_mystery.corpus import MESSAGES
from eye_mystery.diamond_reading import (
    X_ORDER,
    Y_ORDER,
    base25_reading,
    component_pairs,
    pair_trigrams,
    squared_reading,
    uniform_pair_baseline,
)


class DiamondReadingTests(unittest.TestCase):
    def test_document_orders_reproduce_opening(self) -> None:
        self.assertEqual((0, 2, 1), Y_ORDER)
        self.assertEqual((1, 2, 0), X_ORDER)
        self.assertEqual(
            ((3, 2), (1, 0), (2, 0), (4, 0), (3, 0), (1, 1)),
            component_pairs(MESSAGES["east1"])[:6],
        )
        self.assertEqual(
            (17, 5, 10, 20, 15, 6, 12, 17, 2, 3),
            base25_reading(MESSAGES["east1"])[:10],
        )
        self.assertEqual(
            (11, 1, 4, 16, 9, 2, 6, 11, 2, 3),
            squared_reading(MESSAGES["east1"])[:10],
        )

    def test_odd_message_receives_one_zero_trigram(self) -> None:
        pairs = pair_trigrams(MESSAGES["east1"])
        self.assertEqual(50, len(pairs))
        self.assertEqual((0, 0, 0), pairs[-1][1])
        self.assertEqual(150, len(squared_reading(MESSAGES["east1"])))

    def test_uniform_baseline_accounts_for_collisions(self) -> None:
        self.assertAlmostEqual(0.04, uniform_pair_baseline("base25"))
        self.assertAlmostEqual(0.0624, uniform_pair_baseline("squared"))


if __name__ == "__main__":
    unittest.main()
