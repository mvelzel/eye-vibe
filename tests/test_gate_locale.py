from __future__ import annotations

import unittest

from eye_mystery.gate_locale import (
    gate_locale_reading,
    increment_residue_census,
    permutation_texts,
)


class GateLocaleTests(unittest.TestCase):
    def test_direct_fi_reading(self) -> None:
        upper = (
            frozenset({(0, 0)}),
            frozenset({(10, 2), (11, 1), (12, 0), (12, -1), (13, -2)}),
            frozenset({(20, 0), (21, 1), (21, 2)}),
        )
        lower = (
            frozenset({(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)}),
            frozenset({(10, 3)}),
            frozenset({(12, -4)}),
            frozenset({(15, 0)}),
        )
        reading = gate_locale_reading(upper, lower)
        self.assertIsNotNone(reading)
        assert reading is not None
        self.assertEqual(reading.component_sizes, (1, 5, 3))
        self.assertEqual(reading.number, 153)
        self.assertEqual(reading.increment, 3)
        self.assertEqual(reading.text, "fi")

    def test_singletons_must_follow_plus(self) -> None:
        upper = (frozenset({(0, 0)}),)
        lower = (
            frozenset({(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)}),
            frozenset({(-5, 0)}),
        )
        self.assertIsNone(gate_locale_reading(upper, lower))

    def test_permutation_and_residue_comparators(self) -> None:
        readings = dict(permutation_texts((1, 5, 3), 3))
        self.assertEqual(readings[(1, 5, 3)], "fi")
        self.assertEqual(readings[(3, 5, 1)], "36")
        lowercase, regions = increment_residue_census(3)
        self.assertEqual(lowercase, 15)
        self.assertEqual(len(regions), 24)
        self.assertIn((70, "fi"), regions)


if __name__ == "__main__":
    unittest.main()
