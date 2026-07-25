from __future__ import annotations

import unittest

from eye_mystery.state_table_screen import (
    audit_coordinates,
    audit_visible,
    base5_digits,
    coordinate_d4,
    from_base5,
    physical_d4,
)


class StateTableScreenTests(unittest.TestCase):
    def test_coordinate_and_direction_transforms_are_complete(self) -> None:
        coordinate_maps = tuple(
            tuple(
                coordinate_d4(row, column)[transform]
                for row in range(5)
                for column in range(5)
            )
            for transform in range(8)
        )
        self.assertEqual(len(set(coordinate_maps)), 8)
        self.assertEqual(len(physical_d4()), 8)
        for value in range(83):
            self.assertEqual(from_base5(base5_digits(value)), value)

    def test_fixed_coordinate_screen(self) -> None:
        audit = audit_coordinates(translated=False)
        self.assertEqual(
            (
                audit.models,
                audit.maximum_exact,
                len(audit.exact_witnesses),
                audit.maximum_modal_offset,
                len(audit.offset_witnesses),
            ),
            (48, 1, 6, 3, 10),
        )

    def test_translated_coordinate_screen(self) -> None:
        audit = audit_coordinates(translated=True)
        self.assertEqual(
            (
                audit.models,
                audit.maximum_exact,
                len(audit.exact_witnesses),
                audit.maximum_modal_offset,
                len(audit.offset_witnesses),
            ),
            (1200, 3, 6, 5, 2),
        )

    def test_shared_visible_geometry_is_negative(self) -> None:
        audit = audit_visible(independent_eyes=False)
        self.assertEqual(
            (
                audit.models,
                audit.maximum_exact,
                len(audit.exact_witnesses),
                audit.maximum_training,
                audit.training_cobest,
                audit.training_cobest_heldout,
            ),
            (288, 1, 12, 0, 288, 0),
        )

    def test_independent_eye_geometry_fails_heldout(self) -> None:
        audit = audit_visible(independent_eyes=True)
        self.assertEqual(
            (
                audit.models,
                audit.maximum_exact,
                len(audit.exact_witnesses),
                audit.maximum_training,
                audit.training_cobest,
                audit.training_cobest_heldout,
            ),
            (18432, 3, 4, 1, 256, 0),
        )


if __name__ == "__main__":
    unittest.main()
