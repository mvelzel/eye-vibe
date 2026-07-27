from __future__ import annotations

import unittest

from eye_mystery.hidden_geometry_separators import (
    networkx_available,
    pair_separator_profile,
)


@unittest.skipUnless(
    networkx_available(),
    "optional networkx package is unavailable",
)
class HiddenGeometrySeparatorTests(unittest.TestCase):
    def test_frozen_unresolved_pair_profiles(self) -> None:
        observed = tuple(
            pair_separator_profile(*pair)
            for pair in (
                ("first-gap30", "first-cross"),
                ("last-west4", "last-east5"),
                ("last-east5", "last-east3"),
            )
        )
        self.assertEqual(
            tuple(
                (
                    item.labels,
                    item.edges,
                    item.cycle_rank,
                    item.primal_width_upper,
                    item.class_width_upper,
                )
                for item in observed
            ),
            (
                (31, 50, 20, 11, 7),
                (54, 87, 34, 13, 11),
                (54, 82, 29, 13, 16),
            ),
        )
        self.assertEqual(
            tuple(item.primal_articulations for item in observed),
            (0, 0, 0),
        )
        self.assertEqual(
            tuple(item.class_components for item in observed),
            ((16,), (29,), (29,)),
        )


if __name__ == "__main__":
    unittest.main()
