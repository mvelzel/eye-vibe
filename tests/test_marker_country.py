from __future__ import annotations

import unittest

from eye_mystery.factoradic_headers import header_ranks
from eye_mystery.marker_country import (
    assignment_bwt_reading,
    assignment_ranks,
    column_sums,
    d4_views,
    has_country_columns,
    marker_country_audit,
    marker_grid,
)


OBSERVED = (0, 0, 1, 1, 3, 4, 2, 2, 3)
ALTERNATE_SURVIVOR = (0, 0, 1, 2, 3, 4, 2, 1, 3)


class MarkerCountryTests(unittest.TestCase):
    def test_observed_grid_has_country_code_columns(self) -> None:
        grid = marker_grid(OBSERVED)
        self.assertEqual(grid, ((0, 0, 1), (1, 3, 4), (2, 2, 3)))
        self.assertEqual(column_sums(grid), (3, 5, 8))
        self.assertEqual(len(d4_views(grid)), 8)
        self.assertTrue(has_country_columns(OBSERVED))

    def test_observed_assignment_preserves_header_ranks_and_bwt(self) -> None:
        self.assertEqual(assignment_ranks(OBSERVED), header_ranks())
        reading = assignment_bwt_reading(OBSERVED)
        self.assertTrue(reading.single_cycle)
        self.assertTrue(reading.valid_0_82)
        self.assertEqual(reading.text, "!Fi")

    def test_country_columns_resolve_the_known_factoradic_pair(self) -> None:
        self.assertEqual(
            column_sums(marker_grid(ALTERNATE_SURVIVOR)),
            (4, 4, 8),
        )
        self.assertFalse(has_country_columns(ALTERNATE_SURVIVOR, d4=True))

    def test_frozen_conditional_enumeration(self) -> None:
        audit = marker_country_audit()
        self.assertEqual(
            (
                audit.all_assignments,
                audit.in_range,
                audit.distinct_ranks,
                audit.exact_country,
                audit.d4_country,
                audit.bwt_single_cycle,
                audit.bwt_valid_0_82,
                audit.bwt_fi_suffix,
                audit.bwt_exact_bang_fi,
                audit.exact_country_and_fi_suffix,
                audit.exact_country_and_exact_bang_fi,
                audit.d4_country_and_fi_suffix,
                audit.d4_country_and_exact_bang_fi,
                audit.full_factoradic,
                audit.full_exact_country,
                audit.full_d4_country,
            ),
            (
                22_680,
                15_120,
                12_096,
                224,
                855,
                1_137,
                404,
                2,
                1,
                1,
                1,
                1,
                1,
                2,
                1,
                1,
            ),
        )
        self.assertEqual(
            tuple(survivor.assignment for survivor in audit.survivors),
            (OBSERVED, ALTERNATE_SURVIVOR),
        )
        self.assertEqual(
            tuple(survivor.bwt_text for survivor in audit.survivors),
            ("!Fi", None),
        )


if __name__ == "__main__":
    unittest.main()
