import unittest

from eye_mystery.gap_anchor import ordinal_ranks
from eye_mystery.row_record_transfer import (
    FINAL_ANCHORS,
    FINAL_HEADERS,
    FINAL_ORDERS,
    FINAL_TARGET_RANKS,
    audit_all_rows,
    slot_headers,
)


class RowRecordTransferTests(unittest.TestCase):
    def test_known_final_record_is_positive_calibration(self) -> None:
        self.assertEqual(
            slot_headers(FINAL_ANCHORS, FINAL_ORDERS),
            FINAL_HEADERS,
        )
        self.assertEqual(ordinal_ranks(FINAL_ANCHORS), FINAL_TARGET_RANKS)

    def test_earlier_rows_fail_before_body_selection(self) -> None:
        row1, row2, final = audit_all_rows()
        self.assertEqual(row1.feasible_count, 83)
        self.assertEqual(
            row1.attainable_rank_patterns,
            ((0, 2, 1), (1, 0, 2), (2, 1, 0)),
        )
        self.assertEqual(row1.target_rank_count, 0)
        self.assertFalse(row1.complete_grammar_feasible)

        self.assertEqual(row2.feasible_count, 0)
        self.assertFalse(row2.numeric_feasible)
        self.assertFalse(row2.complete_grammar_feasible)

        self.assertEqual(final.feasible_count, 83)
        self.assertGreater(final.target_rank_count, 0)
        self.assertTrue(final.complete_grammar_feasible)


if __name__ == "__main__":
    unittest.main()
