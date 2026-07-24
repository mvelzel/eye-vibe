from __future__ import annotations

import random
import unittest

from eye_mystery.practice_cipher4_fractionation import (
    Coordinates,
    LaneSpec,
    interleave_lanes,
    lane_specs,
    reassociate_selectors,
    reassociation_specs,
    render_lanes,
    shuffle_selectors,
    split_coordinates,
)


class PracticeCipher4FractionationTests(unittest.TestCase):
    def test_split_and_interleave_round_trip(self) -> None:
        ranks = (0, 4, 8, 3, 7, 11)
        coordinates = split_coordinates(ranks, 3)
        lanes = render_lanes(
            coordinates,
            LaneSpec(3, "separate", (0, 1, 2), 0),
        )
        self.assertEqual(
            interleave_lanes(lanes, coordinates.selector),
            ranks,
        )

    def test_catalog_is_finite_and_unique(self) -> None:
        self.assertEqual(len(lane_specs(2)), 12)
        self.assertEqual(len(lane_specs(3)), 56)
        self.assertEqual(len(set(lane_specs(2) + lane_specs(3))), 68)
        self.assertEqual(len(reassociation_specs()), 186)

    def test_selector_shuffle_preserves_counts_and_width2_boundary(self) -> None:
        coordinates = Coordinates(
            (28, 1, 2, 28, 3, 4),
            (0, 1, 0, 0, 1, 0),
        )
        shuffled = shuffle_selectors(coordinates, 2, random.Random(9))
        self.assertEqual(
            sorted(shuffled.selector), sorted(coordinates.selector)
        )
        self.assertEqual((shuffled.selector[0], shuffled.selector[3]), (0, 0))

    def test_lane_reversal_and_concatenation(self) -> None:
        coordinates = Coordinates((1, 2, 3, 4), (0, 1, 0, 1))
        spec = LaneSpec(2, "concatenate", (1, 0), 0b01)
        self.assertEqual(render_lanes(coordinates, spec), ((2, 4, 3, 1),))

    def test_reassociation_shifts_only_selectors(self) -> None:
        coordinates = Coordinates((1, 2, 3, 4), (0, 1, 2, 0))
        shifted = reassociate_selectors(
            coordinates,
            next(
                spec
                for spec in reassociation_specs()
                if (spec.width, spec.period, spec.variant)
                == (3, 4, "shift-left")
            ),
        )
        self.assertEqual(shifted, (4, 8, 9, 12))


if __name__ == "__main__":
    unittest.main()
