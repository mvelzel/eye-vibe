import unittest

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.snapshot_delta import (
    deepest_equality_geometry,
    deepest_sibling_gap_advantages,
    equality_partition,
    equality_runs,
    fixed_coordinate_cost,
    gap_advantage,
    levenshtein_distance,
    partition_tape,
)


class SnapshotDeltaTests(unittest.TestCase):
    def test_standard_edit_examples(self) -> None:
        self.assertEqual(levenshtein_distance((1, 2, 3), (1, 4, 3)), 1)
        self.assertEqual(levenshtein_distance((1, 2, 3), (1, 3)), 1)
        self.assertEqual(fixed_coordinate_cost((1, 2, 3), (1, 3)), 2)
        self.assertEqual(gap_advantage((1, 2, 3), (1, 3)), 1)

    def test_eye_deepest_sibling_advantages(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name])[1:] for name in MESSAGE_ORDER
        }
        self.assertEqual(
            deepest_sibling_gap_advantages(streams),
            (0, 7, 1, 2, 2, 0),
        )

    def test_known_aligned_runs(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name])[1:] for name in MESSAGE_ORDER
        }
        self.assertEqual(
            equality_runs(streams["east1"], streams["west1"], start=24),
            ((28, 31), (36, 48), (54, 54), (85, 85), (96, 96)),
        )

    def test_five_equality_partitions(self) -> None:
        self.assertEqual(equality_partition((7, 7, 7)), 0)
        self.assertEqual(equality_partition((7, 7, 8)), 1)
        self.assertEqual(equality_partition((7, 8, 7)), 2)
        self.assertEqual(equality_partition((8, 7, 7)), 3)
        self.assertEqual(equality_partition((6, 7, 8)), 4)

    def test_eye_partition_tape_counts(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name])[1:] for name in MESSAGE_ORDER
        }
        upper = partition_tape(
            tuple(streams[name] for name in ("east1", "west1", "east2"))
        )[24:]
        lower = partition_tape(
            tuple(streams[name] for name in ("east4", "west4", "east5"))
        )[20:]
        self.assertEqual(tuple(upper.count(value) for value in range(5)), (2, 18, 1, 1, 52))
        self.assertEqual(tuple(lower.count(value) for value in range(5)), (0, 2, 11, 6, 74))

    def test_eye_equality_geometry(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name])[1:] for name in MESSAGE_ORDER
        }
        hits, chi_square, run_ends, near_edges = deepest_equality_geometry(streams)
        self.assertEqual((hits, run_ends, near_edges), (45, 48, 2))
        self.assertAlmostEqual(chi_square, 19.133333333333333)


if __name__ == "__main__":
    unittest.main()
