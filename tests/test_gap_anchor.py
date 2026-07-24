from __future__ import annotations

import random
import unittest
from collections import Counter

from eye_mystery.gap_anchor import (
    any_broad_gap_match,
    broad_position_match,
    clean_gap_anchors,
    exact_reported_relation,
    final_trimmed_bodies,
    gap_anchor_audit,
    gap_anchor_label_audit,
    gap_anchor_position_audit,
    planted_gap_streams,
    planted_position_streams,
    relative_position_order,
    unique_anchor_values,
)
from eye_mystery.seventeenth_state import shuffle_without_adjacent_doubles


class GapAnchorTests(unittest.TestCase):
    def test_positive_detector_plant(self) -> None:
        streams = planted_gap_streams()
        anchors = unique_anchor_values(streams, 11)
        self.assertEqual(anchors, (75, 81, 48))
        self.assertTrue(exact_reported_relation(anchors))
        self.assertEqual(any_broad_gap_match(streams), (11, anchors))

    def test_real_gap_selector_is_unique(self) -> None:
        streams = final_trimmed_bodies()
        expected = {
            "east4": (16, 75),
            "west4": (18, 81),
            "east5": (17, 48),
        }
        for name, pair in expected.items():
            hits = clean_gap_anchors(
                streams[name],
                minimum_gap=11,
                maximum_gap=11,
            )
            self.assertEqual(
                tuple((hit.position, hit.value) for hit in hits[11]),
                (pair,),
            )

    def test_no_double_shuffle_preserves_multiset(self) -> None:
        source = final_trimmed_bodies()["east4"]
        shuffled = shuffle_without_adjacent_doubles(
            source,
            random.Random(0x18A11),
        )
        self.assertEqual(Counter(source), Counter(shuffled))
        self.assertTrue(
            all(left != right for left, right in zip(shuffled, shuffled[1:]))
        )

    def test_small_real_audit_reproduces_relation(self) -> None:
        audit = gap_anchor_audit(controls=19)
        self.assertEqual(audit.real_positions, (16, 18, 17))
        self.assertEqual(audit.real_anchors, (75, 81, 48))
        self.assertEqual(audit.predicted_nonreference, (81, 48))

    def test_label_control_is_deterministic(self) -> None:
        audit = gap_anchor_label_audit(controls=19)
        self.assertEqual(audit, gap_anchor_label_audit(controls=19))

    def test_position_plant_and_order(self) -> None:
        plant = planted_position_streams()
        self.assertEqual(
            broad_position_match(plant),
            (11, (75, 81, 48), (0, 2, 1)),
        )
        self.assertEqual(relative_position_order((16, 18, 17)), (0, 2, 1))
        self.assertIsNone(relative_position_order((16, 19, 17)))

    def test_position_control_is_deterministic(self) -> None:
        audit = gap_anchor_position_audit(controls=19)
        self.assertEqual(audit, gap_anchor_position_audit(controls=19))


if __name__ == "__main__":
    unittest.main()
