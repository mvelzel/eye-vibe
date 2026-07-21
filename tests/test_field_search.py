import unittest

from eye_mystery.field_search import (
    MODULUS,
    shifted_ratio,
    tangent_difference,
    two_lag_recurrence,
)


class FieldSearchTests(unittest.TestCase):
    def test_shifted_ratio_recovers_multipliers(self) -> None:
        message = [1]
        for _ in range(20):
            message.append(3 * message[-1] % MODULUS)
        result = shifted_ratio([message])[0]
        self.assertEqual(result.parameters, (0,))
        self.assertEqual(result.unique, 1)

    def test_tangent_difference_includes_finite_difference(self) -> None:
        result = tangent_difference([[2, 5, 8, 11]])[0]
        self.assertEqual(result.parameters, (0,))
        self.assertEqual(result.unique, 1)

    def test_two_lag_recurrence_recovers_coefficients(self) -> None:
        message = [1, 4]
        for _ in range(20):
            message.append(
                (2 * message[-1] + 3 * message[-2] + 7) % MODULUS
            )
        result = two_lag_recurrence([message])[2 * MODULUS + 3]
        self.assertEqual(result.parameters, (2, 3))
        self.assertEqual(result.unique, 1)


if __name__ == "__main__":
    unittest.main()
