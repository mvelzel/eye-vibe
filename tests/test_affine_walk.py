import unittest

from eye_mystery.affine_walk import _center, trace_affine_walk


class AffineWalkTests(unittest.TestCase):
    def test_center_operations_stay_in_field(self) -> None:
        self.assertEqual(_center(82, "reflection"), 2)
        self.assertTrue(all(0 <= _center(value, "reflection") < 83 for value in range(83)))

    def test_inverse_eye_pairs_cancel(self) -> None:
        # up, down, centre(identity) leaves the initial state unchanged
        self.assertEqual(trace_affine_walk([1, 3, 0], 2, (1, 3), "identity"), (0,))
        # right, left, up from state 1 yields 2 * 1 / 2 + 1 = 2
        self.assertEqual(
            trace_affine_walk([2, 4, 1], 2, (1, 3), "identity", initial=1),
            (2,),
        )


if __name__ == "__main__":
    unittest.main()
