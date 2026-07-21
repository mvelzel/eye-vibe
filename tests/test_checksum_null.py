import unittest

from eye_mystery.checksum_null import (
    TWO_DIGIT_PRIMES,
    all_sums_avoid_divisors_probability,
    avoids_divisors,
    gcd_at_least_probability,
    marker_permutation_divisor_counts,
    marker_permutation_event_counts,
    simulate_partition_gcd_events,
    uniform_sum_counts,
)
from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.initials import body_sums, initial_values


class ChecksumNullTests(unittest.TestCase):
    def test_uniform_sum_counts(self) -> None:
        self.assertEqual(uniform_sum_counts(1, 2), (1, 1, 1))
        self.assertEqual(uniform_sum_counts(2, 2), (1, 2, 3, 2, 1))

    def test_exact_probability_excludes_all_zero_tuple(self) -> None:
        probability = gcd_at_least_probability((1, 1, 1), threshold=2, high=2)
        self.assertAlmostEqual(probability, 7 / 27)

    def test_divisor_avoidance_probability(self) -> None:
        self.assertTrue(avoids_divisors(7, (2, 3)))
        self.assertFalse(avoids_divisors(8, (2, 3)))
        self.assertAlmostEqual(
            all_sums_avoid_divisors_probability(
                (1, 1), divisors=(2,), high=2
            ),
            1 / 9,
        )

    def test_partition_simulation_validates_lengths(self) -> None:
        with self.assertRaises(ValueError):
            simulate_partition_gcd_events(
                (1, 2, 3), (2, 2), fixed_indices=(0, 0, 1), trials=1
            )

    def test_marker_assignment_counts(self) -> None:
        counts = marker_permutation_event_counts(
            (0, 1, 2),
            (0, 2, 1),
            modulus=3,
            fixed_indices=(0, 1, 2),
            families=((0,), (1,), (2,)),
        )
        self.assertEqual(counts["total"], 6)
        self.assertEqual(counts["fixed"], 1)
        self.assertEqual(counts["any_three"], 1)
        self.assertEqual(counts["family_cover"], 1)

    def test_marker_assignment_divisor_counts(self) -> None:
        counts = marker_permutation_divisor_counts(
            (0, 1, 2),
            (0, 2, 1),
            divisors=(2,),
            modulus=3,
            fixed_indices=(0,),
        )
        self.assertEqual(
            counts,
            {"total": 6, "avoid": 0, "checksum": 2, "both": 0},
        )

    def test_eye_two_digit_prime_observation_and_conditional_counts(self) -> None:
        messages = tuple(
            trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        )
        self.assertTrue(
            all(
                avoids_divisors(sum(message), TWO_DIGIT_PRIMES)
                for message in messages
            )
        )
        probability = all_sums_avoid_divisors_probability(
            tuple(map(len, messages))
        )
        self.assertAlmostEqual(probability, 0.004699414767, places=12)
        self.assertEqual(
            marker_permutation_divisor_counts(
                body_sums(),
                initial_values(),
                modulus=101,
                fixed_indices=(0, 4, 8),
            ),
            {
                "total": 362880,
                "avoid": 938,
                "checksum": 720,
                "both": 18,
            },
        )


if __name__ == "__main__":
    unittest.main()
