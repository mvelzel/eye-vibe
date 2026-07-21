import unittest

from eye_mystery.initials import (
    circular_chain_event_counts,
    circular_successor_links,
    marker_grid_exit_signatures,
    marker_grid_permutation_null_counts,
    marker_summary,
    perfect_successor_rotation,
    trace_marker_digit,
)


class InitialMarkerTests(unittest.TestCase):
    def test_published_initial_relations(self) -> None:
        result = marker_summary()
        self.assertTrue(result["all_above_26"])
        self.assertEqual(result["seven_link_chain"], (True,) * 7)
        self.assertFalse(result["last_link"])
        self.assertEqual(
            result["sums_divisible_by_101"], ("east1", "east3", "east5")
        )
        self.assertEqual(result["largest_triple_gcd"], 101)
        self.assertEqual(
            result["largest_triple_gcd_groups"],
            (("east1", "east3", "east5"),),
        )
        self.assertEqual(
            tuple(result["marker_checksum_offsets_mod_101"])[::4],
            (0, 0, 0),
        )

    def test_east5_first_is_the_unique_perfect_rotation(self) -> None:
        self.assertEqual(
            circular_successor_links(),
            (True, True, True, True, True, True, True, False, True),
        )
        self.assertEqual(
            perfect_successor_rotation(),
            (
                "east5",
                "east1",
                "west1",
                "east2",
                "west2",
                "east3",
                "west3",
                "east4",
                "west4",
            ),
        )

    def test_exact_circular_chain_null_count(self) -> None:
        favorable, total = circular_chain_event_counts()
        self.assertEqual(favorable, 236_930_178_600)
        self.assertEqual(total, 119_276_318_345_184_000)

    def test_east5_marker_directions_all_exit_grid(self) -> None:
        self.assertEqual(trace_marker_digit("east5", 0), (("east5", "west3", "east2"), 1))
        self.assertEqual(trace_marker_digit("east5", 1), (("east5", "west3", "east2"), 2))
        self.assertEqual(trace_marker_digit("east5", 2), (("east5",), 3))

    def test_three_starts_have_north_east_south_exits(self) -> None:
        signatures = marker_grid_exit_signatures()
        self.assertEqual(
            tuple(
                name
                for name, signature in zip(
                    (
                        "east1",
                        "west1",
                        "east2",
                        "west2",
                        "east3",
                        "west3",
                        "east4",
                        "west4",
                        "east5",
                    ),
                    signatures,
                    strict=True,
                )
                if signature == (1, 2, 3)
            ),
            ("east3", "west3", "east5"),
        )

    def test_exact_marker_grid_shuffle_nulls(self) -> None:
        fixed, histogram, total = marker_grid_permutation_null_counts()
        self.assertEqual((fixed, total), (2_688, 362_880))
        self.assertEqual(histogram[:4], (357_552, 4_080, 936, 312))
        fixed, histogram, total = marker_grid_permutation_null_counts(
            hold_east5_marker=True
        )
        self.assertEqual((fixed, total), (2_160, 40_320))
        self.assertEqual(histogram[:4], (38_130, 1_710, 432, 48))


if __name__ == "__main__":
    unittest.main()
