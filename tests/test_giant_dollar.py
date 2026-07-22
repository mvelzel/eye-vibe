from pathlib import Path
import unittest

from eye_mystery.giant_dollar import (
    always_opaque_columns,
    best_comparisons,
    centre_run_widths,
    compare_windows,
    dimensions,
    file_sha256,
    load_alpha_mask,
    scan_windows,
)


ASSET = Path(
    "/private/tmp/noita-history.kgAkGA/current/entities/animals/"
    "boss_centipede/rewards/giant_dollar.png"
)
EARLY_ASSET = Path(
    "/private/tmp/noita-history.kgAkGA/early-access/data/entities/animals/"
    "boss_centipede/rewards/giant_dollar.png"
)


class GiantDollarUnitTests(unittest.TestCase):
    def test_centre_widths_are_derived_from_invariant_stem(self) -> None:
        mask = (
            (False, True, True, True, False),
            (True, True, True, True, True),
            (False, False, True, False, False),
        )

        self.assertEqual(dimensions(mask), (5, 3))
        self.assertEqual(always_opaque_columns(mask), (2,))
        self.assertEqual(centre_run_widths(mask), ((2, 3, 1), (2, 3, 1)))

    def test_window_scan_retains_selection_multiplicity(self) -> None:
        left = (1, 2, 3, 4, 5)
        right = (5, 4, 9, 2, 1)

        selected = compare_windows(
            left,
            right,
            left_start=0,
            right_start=0,
            length=5,
            right_reversed=True,
        )
        self.assertEqual(selected.equal_rows, 4)
        self.assertEqual(selected.absolute_difference, 6)
        self.assertEqual(selected.mismatches, ((2, 3, 9),))
        self.assertEqual(len(scan_windows(left, right, length=3)), 18)
        self.assertTrue(best_comparisons(scan_windows(left, left, length=5)))


@unittest.skipUnless(ASSET.exists(), "unpacked Noita history asset not present")
class GiantDollarAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mask = load_alpha_mask(ASSET)
        cls.left, cls.right = centre_run_widths(cls.mask)

    def test_raw_asset_facts(self) -> None:
        self.assertEqual(dimensions(self.mask), (41, 75))
        self.assertEqual(always_opaque_columns(self.mask), (19, 20, 21))
        self.assertEqual(sum(map(sum, self.mask)), 1311)
        self.assertEqual(
            file_sha256(ASSET),
            "0bc8284f0b915d73e350343faa4be2ff3d36f4e73e0edea59267a3d55a69e9c1",
        )

    def test_43_row_claim_and_selection_scan(self) -> None:
        comparisons = scan_windows(self.left, self.right, length=43)
        best = best_comparisons(comparisons)

        self.assertEqual(len(comparisons), 2178)
        self.assertEqual(len(best), 18)
        self.assertTrue(
            all(
                comparison.equal_rows == 42
                and comparison.absolute_difference == 1
                and comparison.right_reversed
                for comparison in best
            )
        )
        advertised = compare_windows(
            self.left,
            self.right,
            left_start=12,
            right_start=15,
            length=43,
            right_reversed=True,
        )
        self.assertEqual(advertised.mismatches, ((22, 11, 12),))

    def test_same_defect_is_embedded_in_a_60_row_relation(self) -> None:
        comparison = compare_windows(
            self.left,
            self.right,
            left_start=5,
            right_start=5,
            length=60,
            right_reversed=True,
        )

        self.assertEqual(comparison.equal_rows, 59)
        self.assertEqual(comparison.mismatches, ((29, 11, 12),))

    @unittest.skipUnless(EARLY_ASSET.exists(), "early-access asset not present")
    def test_current_and_archived_assets_are_byte_identical(self) -> None:
        self.assertEqual(ASSET.read_bytes(), EARLY_ASSET.read_bytes())


if __name__ == "__main__":
    unittest.main()
