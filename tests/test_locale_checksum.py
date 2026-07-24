from __future__ import annotations

import unittest

from eye_mystery.calling_codes import CALLING_CODE_REGIONS, geographic_regions
from eye_mystery.locale_checksum import (
    calling_code_views,
    decimal_column_code,
    locale_checksum_audit,
    observed_plane_summaries,
    region_matches_code,
)
from eye_mystery.marker_country import BwtReading, marker_grid


OBSERVED = (0, 0, 1, 1, 3, 4, 2, 2, 3)


class LocaleChecksumTests(unittest.TestCase):
    def test_pinned_calling_code_regions(self) -> None:
        self.assertEqual(len(CALLING_CODE_REGIONS), 215)
        self.assertEqual(geographic_regions(34), ("ES",))
        self.assertEqual(geographic_regions(358), ("FI", "AX"))
        self.assertEqual(geographic_regions(683), ("NU",))
        self.assertEqual(geographic_regions(800), ())
        self.assertEqual(geographic_regions(457), ())

    def test_decimal_parser_and_d4_broadening(self) -> None:
        self.assertEqual(
            decimal_column_code(marker_grid((0, 0, 0, 0, 1, 1, 0, 2, 3))),
            34,
        )
        self.assertIsNone(
            decimal_column_code(marker_grid((4, 0, 0, 4, 0, 0, 4, 0, 0)))
        )
        reflected = (1, 0, 0, 4, 3, 1, 3, 2, 2)
        self.assertEqual(
            tuple(view[0] for view in calling_code_views(reflected, d4=False)),
            (853,),
        )
        self.assertIn(358, tuple(view[0] for view in calling_code_views(reflected, d4=True)))

    def test_region_suffix_is_case_insensitive_and_multi_region(self) -> None:
        self.assertTrue(region_matches_code(BwtReading(True, True, "!Fi"), 358))
        self.assertTrue(region_matches_code(BwtReading(True, True, "?ax"), 358))
        self.assertFalse(region_matches_code(BwtReading(True, True, "!ES"), 358))

    def test_observed_three_plane_codes(self) -> None:
        summaries = observed_plane_summaries()
        self.assertEqual(
            tuple((item.digits, item.code, item.regions) for item in summaries),
            (
                ((6, 8, 3), 683, ("NU",)),
                ((0, 3, 4), 34, ("ES",)),
                ((3, 5, 8), 358, ("FI", "AX")),
            ),
        )

    def test_frozen_universe_and_factoradic_baseline(self) -> None:
        audit = locale_checksum_audit()
        self.assertEqual(
            (
                audit.all_assignments,
                audit.in_range,
                audit.distinct_ranks,
                audit.natural_geographic_code,
                audit.d4_geographic_code,
                audit.bwt_letter_suffix,
                audit.natural_semantic_match,
                audit.natural_bang_match,
                audit.d4_semantic_match,
                audit.d4_bang_match,
                audit.full_factoradic,
                audit.full_natural_semantic_match,
                audit.full_d4_semantic_match,
            ),
            (
                22_680,
                15_120,
                12_096,
                1_282,
                3_914,
                173,
                1,
                1,
                1,
                1,
                2,
                1,
                1,
            ),
        )
        self.assertEqual(len(audit.matches), 1)
        match = audit.matches[0]
        self.assertEqual(match.assignment, OBSERVED)
        self.assertTrue(match.natural)
        self.assertEqual((match.code, match.regions, match.text), (358, ("FI", "AX"), "!Fi"))
        self.assertTrue(match.factoradic)


if __name__ == "__main__":
    unittest.main()
