from __future__ import annotations

import random
import unittest
from collections import Counter

from eye_mystery.gap_anchor import (
    any_broad_gap_match,
    clean_gap_anchors,
    exact_reported_relation,
    final_trimmed_bodies,
    gap_anchor_audit,
    planted_gap_streams,
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


if __name__ == "__main__":
    unittest.main()
