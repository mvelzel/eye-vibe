from __future__ import annotations

import random
import unittest
from collections import Counter

from eye_mystery.earthquake_mask import (
    FINAL_STARTS,
    conditional_anchor_shuffle,
    metric_maxima,
    planted_mask_streams,
    score_variants,
    variant_offsets,
)
from eye_mystery.gap_anchor import FINAL_MESSAGES, TARGET_GAP, clean_gap_anchors


class EarthquakeMaskTests(unittest.TestCase):
    def test_registered_offsets_remove_known_anchor_pair(self) -> None:
        self.assertEqual(
            (
                (1, 2, 3, 5, 6, 7, 9, 10, 13, 14, 15),
                (4, 8, 12, 16),
                (1, 2, 3, 5, 6, 7, 9, 10, 13, 14, 15, 16),
                (4, 8, 12),
            ),
            variant_offsets(),
        )

    def test_positive_plant_exercises_every_metric(self) -> None:
        variants = score_variants(planted_mask_streams())
        self.assertEqual((1, 1, 3, 3), variants[0].values())
        self.assertEqual((1, 1, 3, 3), metric_maxima(variants))

    def test_conditional_shuffle_preserves_registered_structure(self) -> None:
        streams = planted_mask_streams()
        rng = random.Random(0x21A17)
        for name, start in zip(FINAL_MESSAGES, FINAL_STARTS, strict=True):
            shuffled, attempts = conditional_anchor_shuffle(
                streams[name],
                start=start,
                rng=rng,
            )
            self.assertGreaterEqual(attempts, 1)
            self.assertEqual(Counter(streams[name]), Counter(shuffled))
            self.assertFalse(
                any(left == right for left, right in zip(shuffled, shuffled[1:]))
            )
            hits = clean_gap_anchors(
                shuffled,
                minimum_gap=TARGET_GAP,
                maximum_gap=TARGET_GAP,
            ).get(TARGET_GAP, ())
            self.assertEqual(1, len(hits))
            self.assertEqual(start, hits[0].position)
            self.assertEqual(streams[name][start], hits[0].value)


if __name__ == "__main__":
    unittest.main()
