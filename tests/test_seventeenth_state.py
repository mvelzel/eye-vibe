from __future__ import annotations

import unittest

from eye_mystery.seventeenth_state import (
    FibrationAudit,
    coarsest_equitable_partition,
    fibration_audit,
    partition_is_equitable,
    planted_regular_cover,
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


if __name__ == "__main__":
    unittest.main()
