import unittest

from eye_mystery.gaussian_walk import (
    EYE_VECTORS,
    MODULUS,
    add,
    inverse,
    multiply,
    norm,
    trace_gaussian_walk,
)


class GaussianWalkTests(unittest.TestCase):
    def test_i_is_a_square_root_of_minus_one(self) -> None:
        self.assertEqual(multiply((0, 1), (0, 1)), (MODULUS - 1, 0))

    def test_nonzero_elements_have_inverses(self) -> None:
        for value in ((1, 0), (0, 1), (7, 19), (82, 82)):
            self.assertNotEqual(norm(value), 0)
            self.assertEqual(multiply(value, inverse(value)), (1, 0))

    def test_cardinal_eye_vectors_cancel(self) -> None:
        opposite_sums = tuple(
            add(EYE_VECTORS[left], EYE_VECTORS[right])
            for left, right in ((1, 3), (2, 4))
        )
        self.assertEqual(opposite_sums, ((0, 0), (0, 0)))

    def test_simple_additive_walk(self) -> None:
        # right, up, left leaves the state at i, whose norm is one.
        self.assertEqual(
            trace_gaussian_walk(
                (2, 1, 4), center_mode="identity", observation="norm"
            ),
            (1,),
        )


if __name__ == "__main__":
    unittest.main()
