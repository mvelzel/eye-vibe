import unittest

from eye_mystery.context_checksum_transfer import (
    audit_registered_contexts,
    checksum_plant,
)


class ContextChecksumTransferTests(unittest.TestCase):
    def test_synthetic_two_record_plant_passes(self) -> None:
        plant = checksum_plant()
        self.assertEqual(plant.prediction, (3, 2))
        self.assertEqual(plant.observed_checks, (3, 2))
        self.assertEqual(
            tuple((window.start, window.end) for window in plant.windows),
            ((11, 12), (13, 14)),
        )
        self.assertTrue(plant.complete_two_field_match)

    def test_last_east5_is_the_calibration_context(self) -> None:
        calibration = audit_registered_contexts().calibration
        self.assertEqual(calibration.name, "last-east5")
        self.assertEqual(calibration.registered_length, 30)
        self.assertEqual(calibration.actual_common_length, 30)
        self.assertEqual(calibration.prediction, (3, 2))
        self.assertEqual(calibration.observed_checks, (3, 2))
        self.assertTrue(calibration.complete_two_field_match)
        self.assertEqual(calibration.broad_ordered_pair_matches, 4)
        self.assertEqual(calibration.broad_ordered_pairs, 81)

    def test_all_registered_external_transfers_fail(self) -> None:
        result = audit_registered_contexts()
        self.assertEqual(
            tuple(
                (
                    audit.name,
                    audit.registered_length,
                    audit.actual_common_length,
                    audit.prediction,
                    audit.observed_checks,
                )
                for audit in result.transfers
            ),
            (
                ("first-gap30", 18, 32, (0, 0), ()),
                ("first-cross", 18, 23, (1, 0), (2, 81, 51)),
                ("first-cross-late", 18, 23, (1, 0), (2,)),
                ("first-gap28", 9, 19, (0, 0), ()),
                ("last-west4", 30, 34, (2, 2), ()),
                ("last-east3", 25, 27, (3, 2), (11,)),
            ),
        )
        self.assertEqual(result.testable_contexts, 3)
        self.assertEqual(result.tested_fields, 4)
        self.assertEqual(result.matching_fields, 0)
        self.assertEqual(result.complete_two_field_matches, 0)
        self.assertEqual(result.reversed_matching_fields, 0)

    def test_no_failed_complete_record_can_be_rescued_by_panel_pair(self) -> None:
        result = audit_registered_contexts()
        first_cross = next(
            audit for audit in result.transfers
            if audit.name == "first-cross"
        )
        self.assertEqual(first_cross.broad_ordered_pair_matches, 0)
        last_east3 = next(
            audit for audit in result.transfers
            if audit.name == "last-east3"
        )
        self.assertEqual(last_east3.broad_ordered_pair_matches, 0)


if __name__ == "__main__":
    unittest.main()
