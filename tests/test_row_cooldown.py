from __future__ import annotations

import random
import unittest

from eye_mystery.fifteenth_second import trimmed_eye_words
from eye_mystery.row_cooldown import (
    PANEL_ORDER,
    TARGET_VECTOR,
    audit_cooldowns,
    minimum_recurrence_distance,
    planted_cooldown_words,
    registered_context_fixed_positions,
    shuffled_words,
)


class RowCooldownTests(unittest.TestCase):
    def test_minimum_recurrence_distance(self) -> None:
        self.assertEqual(minimum_recurrence_distance((0, 1, 2, 0)), 3)
        self.assertEqual(minimum_recurrence_distance((0, 1, 0, 2)), 2)
        self.assertEqual(minimum_recurrence_distance((0, 1, 2)), 4)

    def test_canonical_vector_and_split(self) -> None:
        audit = audit_cooldowns()
        self.assertEqual(audit.minima, TARGET_VECTOR)
        self.assertTrue(audit.row_uniform)
        self.assertTrue(audit.row_uniform_distinct)
        self.assertEqual(audit.split_prediction.thresholds, (3, 2, 4))
        self.assertTrue(audit.split_prediction.passes)

    def test_positive_control_recovers_row_thresholds(self) -> None:
        audit = audit_cooldowns(planted_cooldown_words())
        self.assertEqual(audit.minima, TARGET_VECTOR)

    def test_context_fixed_shuffle_preserves_cells_and_multisets(self) -> None:
        words = trimmed_eye_words()
        fixed = registered_context_fixed_positions(words)
        shuffled = shuffled_words(
            words,
            random.Random(270727),
            fixed_positions=fixed,
        )
        for name in PANEL_ORDER:
            self.assertEqual(sorted(shuffled[name]), sorted(words[name]))
            self.assertTrue(
                all(
                    shuffled[name][index] == words[name][index]
                    for index in fixed[name]
                )
            )
            self.assertTrue(
                all(
                    left != right
                    for left, right in zip(
                        shuffled[name],
                        shuffled[name][1:],
                    )
                )
            )


if __name__ == "__main__":
    unittest.main()
