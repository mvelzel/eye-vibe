import random
import unittest

from eye_mystery.practice_cipher4 import project_action_band
from eye_mystery.practice_cipher4_factor import (
    contiguous_width_screen,
    difference_ladder,
    label_shuffle_audit,
    mutual_information,
    serial_mutual_information,
)


class PracticeCipher4FactorTests(unittest.TestCase):
    def test_action_band_projections(self) -> None:
        actions = (22, 23, 24, 25, 78)
        self.assertEqual(project_action_band(actions, "rank-div2"), (0, 0, 1, 1, 28))
        self.assertEqual(project_action_band(actions, "rank-mod2"), (0, 1, 0, 1, 0))
        self.assertEqual(project_action_band(actions, "rank-div3"), (0, 0, 0, 1, 18))
        self.assertEqual(project_action_band(actions, "rank-mod3"), (0, 1, 2, 0, 2))
        self.assertEqual(project_action_band(actions, "rank-div19"), (0, 0, 0, 0, 2))
        self.assertEqual(project_action_band(actions, "rank-mod19"), (0, 1, 2, 3, 18))

    def test_mutual_information_detects_exact_dependence(self) -> None:
        left = (0, 0, 1, 1) * 10
        independent = (0, 1, 0, 1) * 10
        self.assertAlmostEqual(mutual_information(left, independent), 0.0)
        self.assertAlmostEqual(mutual_information(left, left), 1.0)
        self.assertGreater(serial_mutual_information((left,)), 0.0)

    def test_difference_ladder_keeps_boundaries_separate(self) -> None:
        layers = difference_ladder(((1, 3, 6), (8, 2)), modulus=10, orders=2)
        self.assertEqual(layers[0], ((1, 3, 6), (8, 2)))
        self.assertEqual(layers[1], ((2, 3), (4,)))

    def test_label_shuffle_audit_is_reproducible(self) -> None:
        ranks = tuple(random.Random(4).randrange(57) for _ in range(200))
        left = label_shuffle_audit(ranks, divisor=3, controls=20, seed=9)
        right = label_shuffle_audit(ranks, divisor=3, controls=20, seed=9)
        self.assertEqual(left, right)

    def test_width_screen_is_reproducible(self) -> None:
        ranks = ((0, 1, 2, 3, 4, 5) * 10,)
        left = contiguous_width_screen(ranks, widths=(2, 3), controls=10, seed=4)
        right = contiguous_width_screen(ranks, widths=(2, 3), controls=10, seed=4)
        self.assertEqual(left, right)
        self.assertEqual(tuple(row.width for row in left), (2, 3))


if __name__ == "__main__":
    unittest.main()
