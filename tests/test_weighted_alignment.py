from __future__ import annotations

import unittest

from eye_mystery.weighted_alignment import (
    PANEL_ROWS,
    convolve_many,
    cyclic_alignment_histogram,
    real_rows,
    rotate,
    weighted_alignment_audit,
    weighted_plant,
    weighted_score,
)


class WeightedAlignmentTests(unittest.TestCase):
    def test_real_row_lengths_are_frozen(self) -> None:
        self.assertEqual(tuple(map(len, (row[0] for row in real_rows()))), (74, 96, 93))

    def test_perfect_plant_and_simultaneous_rotation(self) -> None:
        second = tuple((7 * index + 3) % 83 for index in range(17))
        third = tuple((11 * index + 9) % 83 for index in range(17))
        plant = weighted_plant(second, third)
        self.assertEqual(weighted_score(plant), 17)
        for offset in range(17):
            self.assertEqual(
                weighted_score(tuple(rotate(column, offset) for column in plant)),
                17,
            )

    def test_each_exact_null_has_l_squared_mass(self) -> None:
        histograms = tuple(cyclic_alignment_histogram(row) for row in real_rows())
        self.assertEqual(
            tuple(sum(histogram.values()) for histogram in histograms),
            (74**2, 96**2, 93**2),
        )
        combined = convolve_many(histograms)
        self.assertEqual(
            sum(combined.values()),
            (74**2) * (96**2) * (93**2),
        )

    def test_frozen_audit_uses_natural_rows(self) -> None:
        audit = weighted_alignment_audit()
        self.assertEqual(tuple(row.names for row in audit.rows), PANEL_ROWS)
        self.assertEqual(tuple(row.length for row in audit.rows), (74, 96, 93))
        self.assertEqual(
            tuple(
                (
                    row.real_score,
                    row.null_upper,
                    row.null_total,
                    row.null_min,
                    row.null_max,
                )
                for row in audit.rows
            ),
            (
                (2, 1_253, 5_476, 0, 6),
                (1, 6_252, 9_216, 0, 7),
                (1, 5_851, 8_649, 0, 6),
            ),
        )
        self.assertEqual(audit.real_total, 4)
        self.assertEqual(audit.null_total, (74**2) * (96**2) * (93**2))
        self.assertEqual(audit.null_upper, 171_017_439_974)
        self.assertEqual((audit.null_min, audit.null_max), (0, 19))


if __name__ == "__main__":
    unittest.main()
