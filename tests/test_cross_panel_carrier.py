import unittest

from eye_mystery.cross_panel_carrier import (
    HOLDOUT_CLASSES,
    TRAINING_CLASSES,
    _eye_prediction,
    base5_digits,
    common_tables,
)


class CrossPanelCarrierTests(unittest.TestCase):
    def test_common_tables_have_25_distinct_labels(self) -> None:
        tables = common_tables()
        self.assertEqual(set(tables), {"east4", "west4", "east5"})
        for table in tables.values():
            self.assertEqual(len(table), 25)
            self.assertEqual(len(set(table)), 25)

    def test_holdouts_partition_classes(self) -> None:
        self.assertEqual(HOLDOUT_CLASSES, (10, 24))
        self.assertEqual(len(TRAINING_CLASSES), 23)
        self.assertFalse(set(HOLDOUT_CLASSES) & set(TRAINING_CLASSES))

    def test_base5_round_trip(self) -> None:
        for value in range(83):
            digits = base5_digits(value)
            self.assertEqual(25 * digits[0] + 5 * digits[1] + digits[2], value)

    def test_eye_prediction_identity_from_left(self) -> None:
        order = (0, 1, 2)
        for value in range(83):
            self.assertEqual(
                _eye_prediction(
                    base5_digits(value),
                    (0, 0, 0),
                    left_order=order,
                    right_order=order,
                    target_order=order,
                    a=1,
                    b=0,
                    offsets=(0, 0, 0),
                ),
                value,
            )


if __name__ == "__main__":
    unittest.main()

