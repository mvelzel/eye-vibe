import unittest

from eye_mystery.header_no_repeat import (
    HALF_SIZE,
    audit_header_no_repeat,
    conditional_rank,
    selected_route,
)
from eye_mystery.header_order_ideal import VISIBLE_SIZE


class HeaderNoRepeatTests(unittest.TestCase):
    def test_conditional_rank_deletes_previous_position(self) -> None:
        table = tuple(range(VISIBLE_SIZE))
        lower = conditional_rank(20, 10, table)
        upper = conditional_rank(20, 21, table)
        self.assertEqual(lower.full, 10)
        self.assertEqual(upper.full, 20)
        for result in (lower, upper):
            self.assertEqual(
                result.full,
                HALF_SIZE * result.sheet + result.magnitude,
            )
            self.assertIn(result.sheet, (0, 1))
            self.assertIn(result.magnitude, range(HALF_SIZE))

    def test_conditional_rank_rejects_a_double(self) -> None:
        with self.assertRaises(ValueError):
            conditional_rank(4, 4, tuple(range(VISIBLE_SIZE)))

    def test_exact_audit_contains_observation(self) -> None:
        audit = audit_header_no_repeat()
        self.assertEqual(audit.control_count, 82 * 83)
        self.assertGreaterEqual(audit.magnitude_tail_count, 1)
        self.assertGreaterEqual(
            audit.maximum_control_magnitude,
            audit.observed.holdout_magnitude,
        )
        self.assertEqual(selected_route(), audit.observed)


if __name__ == "__main__":
    unittest.main()
