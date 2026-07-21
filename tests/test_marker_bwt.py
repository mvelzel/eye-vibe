import unittest

from eye_mystery.marker_bwt import (
    cyclic_bwt,
    inverse_cyclic_bwt,
    marker_bwt_multiset_null_counts,
    marker_bwt_lf_order,
    marker_bwt_plaintext_order,
    marker_bwt_summary,
    marker_bwt_trail_assignment_counts,
    stable_lf_mapping,
)


class MarkerBwtTests(unittest.TestCase):
    def test_marker_payload_decodes_to_bang_fi(self) -> None:
        summary = marker_bwt_summary()
        self.assertEqual(summary["last_column"], tuple(map(int, "300113422")))
        self.assertEqual(summary["first_column"], tuple(map(int, "001122334")))
        self.assertEqual(summary["lf_mapping"], (6, 0, 1, 2, 3, 7, 8, 4, 5))
        self.assertEqual(summary["restored_digits"], tuple(map(int, "001123243")))
        self.assertEqual(summary["values"], (1, 38, 73))
        self.assertEqual(summary["ascii32"], "!Fi")
        self.assertTrue(summary["round_trip"])
        self.assertEqual(
            marker_bwt_lf_order(),
            (
                "east5",
                "west3",
                "west4",
                "east3",
                "east4",
                "west2",
                "east2",
                "west1",
                "east1",
            ),
        )
        self.assertEqual(
            marker_bwt_plaintext_order(),
            (
                "east1",
                "west1",
                "east2",
                "west2",
                "east4",
                "east3",
                "west4",
                "west3",
                "east5",
            ),
        )

    def test_bwt_round_trip(self) -> None:
        plaintext = tuple(map(int, "001123243"))
        last_column, primary = cyclic_bwt(plaintext)
        self.assertEqual((last_column, primary), (tuple(map(int, "300113422")), 0))
        self.assertEqual(inverse_cyclic_bwt(last_column, primary), plaintext)
        self.assertEqual(stable_lf_mapping(last_column), (6, 0, 1, 2, 3, 7, 8, 4, 5))

    def test_exact_observed_payload_multiset_null(self) -> None:
        self.assertEqual(
            marker_bwt_multiset_null_counts(),
            {
                "permutations": 22_680,
                "single_cycle": 2_520,
                "valid_0_82": 1_031,
                "punct_upper_lower": 15,
                "case_insensitive_fi_suffix": 2,
                "exact_bang_fi": 1,
            },
        )

    def test_exact_fixed_trail_assignment_null(self) -> None:
        self.assertEqual(
            marker_bwt_trail_assignment_counts(),
            {
                "fixed_trail": 168,
                "single_cycle": 37,
                "valid_0_82": 14,
                "exact_bang_fi": 1,
            },
        )


if __name__ == "__main__":
    unittest.main()
