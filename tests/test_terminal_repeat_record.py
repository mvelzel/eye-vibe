from __future__ import annotations

import unittest

from eye_mystery.factoradic_headers import header_ranks
from eye_mystery.terminal_repeat_record import (
    RECORD_ORDER,
    RepeatEvent,
    audit_terminal_record,
    common_late_signature,
    observed_event_hits,
    ordered_event_match,
    record_values,
    repeat_events,
    terminal_event,
    terminal_record_matches,
)


class TerminalRepeatRecordTests(unittest.TestCase):
    def test_common_signature_and_repeat_events(self) -> None:
        self.assertEqual(len(common_late_signature()), 30)
        self.assertEqual(
            tuple(
                (
                    event.position,
                    event.previous_position,
                    event.distance,
                    event.class_id,
                )
                for event in repeat_events()
            ),
            (
                (9, 5, 4, 5),
                (18, 0, 18, 0),
                (26, 22, 4, 20),
                (27, 1, 26, 1),
                (29, 16, 13, 15),
            ),
        )
        self.assertEqual(terminal_event(), repeat_events()[-1])

    def test_observed_terminal_record(self) -> None:
        self.assertEqual(RECORD_ORDER, ("west3", "east3", "west2"))
        self.assertEqual(record_values(), (34, 63, 76))
        self.assertTrue(terminal_record_matches(header_ranks()))

    def test_synthetic_event_plant_and_broken_record(self) -> None:
        planted = dict(header_ranks())
        planted.update({"west3": 10, "east3": 19, "west2": 23})
        event = RepeatEvent(9, 5, 4, 5)
        self.assertTrue(
            ordered_event_match(planted, RECORD_ORDER, event)
        )
        broken = dict(header_ranks())
        broken["west2"] = 75
        self.assertFalse(terminal_record_matches(broken))

    def test_observed_broad_inventory_is_unique(self) -> None:
        unsigned = observed_event_hits(signed=False)
        signed = observed_event_hits(signed=True)
        self.assertEqual(len(unsigned), 1)
        self.assertEqual(len(signed), 1)
        hit = unsigned[0]
        self.assertEqual(hit.row, 2)
        self.assertEqual(hit.order, RECORD_ORDER)
        self.assertEqual(hit.event, terminal_event())
        self.assertEqual(hit.signs, (1, 1))
        self.assertEqual(signed[0], hit)

    def test_conditional_counts_and_joint_selection(self) -> None:
        audit = audit_terminal_record()
        self.assertEqual(
            (
                audit.assignments,
                audit.boundary,
                audit.position,
                audit.record,
                audit.record_and_full_closure,
                audit.record_and_source_delta,
                audit.record_and_topology,
                audit.broad_row2,
                audit.broad_any_row,
                audit.broad_signed,
                audit.factoradic_survivors,
                audit.record_factoradic_survivors,
                audit.record_and_closure_factoradic_survivors,
            ),
            (
                12096,
                1620,
                468,
                126,
                2,
                1,
                1,
                291,
                291,
                727,
                2,
                ((0, 0, 1, 1, 3, 4, 2, 2, 3),),
                ((0, 0, 1, 1, 3, 4, 2, 2, 3),),
            ),
        )


if __name__ == "__main__":
    unittest.main()
