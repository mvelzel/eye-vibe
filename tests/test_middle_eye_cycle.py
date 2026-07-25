from __future__ import annotations

import unittest

from eye_mystery.middle_eye_cycle import (
    COUNTERCLOCKWISE_FROM_UP,
    audit_order,
    axis_audits,
    boundary_audit,
    direction_repeats,
    middle_axis_audit,
)


class MiddleEyeCycleTests(unittest.TestCase):
    def test_axis_inventories(self) -> None:
        first, middle, third = axis_audits()
        self.assertEqual(
            (first.multiplier, first.present, first.repeated, first.repeat_order),
            (25, 1, 0, ()),
        )
        self.assertEqual(
            (
                middle.multiplier,
                middle.present,
                middle.repeated,
                middle.repeat_order,
            ),
            (5, 4, 4, (1, 4, 3, 2)),
        )
        self.assertTrue(middle.complete)
        self.assertEqual(
            (third.multiplier, third.present, third.repeated, third.repeat_order),
            (1, 4, 2, (1, 2)),
        )
        self.assertFalse(first.complete)
        self.assertFalse(third.complete)

    def test_middle_direction_records(self) -> None:
        self.assertEqual(
            tuple(
                (
                    record.direction,
                    record.class_id,
                    record.first_position,
                    record.repeat_position,
                    record.distance,
                )
                for record in middle_axis_audit().records
            ),
            (
                (1, 5, 5, 9, 4),
                (2, 10, 11, 34, 23),
                (3, 15, 16, 29, 13),
                (4, 20, 22, 26, 4),
            ),
        )

    def test_physical_order_counts(self) -> None:
        audit = audit_order()
        self.assertEqual(audit.observed_order, COUNTERCLOCKWISE_FROM_UP)
        self.assertEqual(
            (
                audit.permutations,
                audit.exact_counterclockwise_from_up,
                audit.either_orientation_from_up,
                audit.any_rotated_physical_cycle,
            ),
            (24, 1, 2, 8),
        )

    def test_class10_is_boundary_conflict_and_marker_return(self) -> None:
        audit = boundary_audit()
        self.assertEqual(
            (
                audit.boundary,
                audit.loop_class,
                audit.mate_class,
                audit.first_conflict,
                audit.loop_positions,
            ),
            (34, 10, 27, True, (11, 34)),
        )
        self.assertEqual(
            (
                audit.loop_value,
                audit.mate_class_value,
                audit.loop_to_mate_difference,
                audit.mate_to_loop_difference,
                audit.loop_to_mate_markers,
                audit.mate_to_loop_markers,
            ),
            (67, 73, 6, 77, (), ("west4",)),
        )

    def test_synthetic_counterclockwise_cycle(self) -> None:
        signature = (5, 20, 15, 10, 5, 20, 15, 10)
        records = direction_repeats(signature, 5)
        order = tuple(
            record.direction
            for record in sorted(
                records,
                key=lambda record: int(record.repeat_position),
            )
        )
        self.assertEqual(order, COUNTERCLOCKWISE_FROM_UP)


if __name__ == "__main__":
    unittest.main()
