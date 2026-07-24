from __future__ import annotations

import random
import unittest
from collections import Counter

from eye_mystery.seventeenth_state import (
    FibrationAudit,
    coarsest_equitable_partition,
    eye_bodies,
    evaluate_hankel_split,
    fibration_audit,
    hankel_control_audit,
    modular_rank,
    partition_is_equitable,
    periodic_hankel_plant,
    planted_regular_cover,
    shuffle_without_adjacent_doubles,
)


class SeventeenthFibrationTests(unittest.TestCase):
    def test_planted_cover_is_recovered_exactly(self) -> None:
        matrix, expected = planted_regular_cover()
        recovered = coarsest_equitable_partition(matrix)
        self.assertEqual(recovered, expected)
        self.assertTrue(partition_is_equitable(matrix, recovered))

    def test_eye_audit_matches_frozen_result(self) -> None:
        expected = (
            FibrationAudit(True, False, 77, 76, 7, 83, 83, 1, False),
            FibrationAudit(False, False, 77, 76, 7, 83, 83, 1, False),
            FibrationAudit(True, True, 75, 74, 9, 83, 83, 1, False),
            FibrationAudit(False, True, 75, 74, 9, 83, 83, 1, False),
        )
        self.assertEqual(fibration_audit(), expected)


class SeventeenthHankelTests(unittest.TestCase):
    def test_modular_rank_is_exact(self) -> None:
        matrix = ((1, 2, 3), (2, 4, 6), (1, 1, 0))
        self.assertEqual(modular_rank(matrix, 83), 2)
        self.assertEqual(modular_rank(((83, 0), (0, 1)), 83), 1)

    def test_shuffle_preserves_registered_nuisances(self) -> None:
        source = (0, 1, 0, 2, 1, 2, 0)
        shuffled = shuffle_without_adjacent_doubles(
            source,
            random.Random(917),
        )
        self.assertEqual(Counter(shuffled), Counter(source))
        self.assertEqual(len(shuffled), len(source))
        self.assertTrue(
            all(left != right for left, right in zip(shuffled, shuffled[1:]))
        )

    def test_algebraic_selector_always_chooses_shallow_block(self) -> None:
        plant = periodic_hankel_plant()
        split = evaluate_hankel_split(plant, ("east1", "west1", "east2"))
        self.assertEqual(split.selected_depth, (1, 1))
        self.assertGreaterEqual(split.blocks[0].score, split.blocks[1].score)
        self.assertGreaterEqual(split.blocks[0].score, split.blocks[2].score)

    def test_periodic_positive_control_passes_small_audit(self) -> None:
        audit = hankel_control_audit(
            periodic_hankel_plant(),
            controls=19,
        )
        self.assertTrue(audit.training.selected.all_fields_deficient)
        self.assertTrue(audit.heldout.selected.all_fields_deficient)
        self.assertEqual(audit.exceedances, 0)
        self.assertEqual(audit.heldout_rank_excess, 0)

    def test_eye_hankel_splits_match_frozen_result(self) -> None:
        streams = eye_bodies(prefix_trimmed=True)
        training = evaluate_hankel_split(
            streams,
            ("east1", "west1", "east2"),
        )
        heldout = evaluate_hankel_split(
            streams,
            ("west2", "east3", "west3", "east4", "west4", "east5"),
        )
        self.assertEqual(
            [
                (block.depth, block.rows, block.columns, block.ranks)
                for block in training.blocks
            ],
            [
                ((1, 1), 75, 75, (72, 72, 72)),
                ((2, 1), 298, 75, (75, 75, 75)),
                ((1, 2), 75, 298, (75, 75, 75)),
            ],
        )
        self.assertEqual(
            [
                (block.depth, block.rows, block.columns, block.ranks)
                for block in heldout.blocks
            ],
            [
                ((1, 1), 84, 84, (84, 84, 84)),
                ((2, 1), 679, 84, (84, 84, 84)),
                ((1, 2), 84, 679, (84, 84, 84)),
            ],
        )


if __name__ == "__main__":
    unittest.main()
