import unittest
from fractions import Fraction

from eye_mystery.checksum_self_pointer import (
    canonical_profiles,
    exact_typed_probability,
    field_assignment_probability,
    header_residual_assignment_probability,
    ledger_containment_probability,
    observed_field_event,
    observed_typed_coordinate_event,
    packet_sum_permutation_probability,
    packet_sum_probability,
    permutation_probability,
    target_mask_distribution,
    typed_coordinate_probability,
)


class ChecksumSelfPointerTests(unittest.TestCase):
    def test_canonical_profiles_reproduce_all_self_occurrences(self) -> None:
        profiles = canonical_profiles()
        self.assertEqual(
            tuple(
                (
                    item.name,
                    item.total,
                    item.quotient,
                    item.remainder,
                    item.positions,
                    item.distances,
                )
                for item in profiles
            ),
            (
                ("east1", 4040, 40, 0, (27, 33), (13, 7)),
                ("east3", 5656, 56, 0, (45, 69, 118), (11, 13, 62)),
                ("east5", 4545, 45, 0, (75,), (30,)),
            ),
        )

    def test_mask_distributions_cover_every_conditioned_subset(self) -> None:
        for item in canonical_profiles():
            distribution = target_mask_distribution(item)
            expected = __import__("math").comb(
                item.length - 1,
                item.body_occurrences,
            )
            self.assertEqual(sum(distribution.values()), expected)

    def test_exact_probabilities_are_reproducible(self) -> None:
        self.assertEqual(
            exact_typed_probability(),
            Fraction(12931, 410873085),
        )
        numerator, denominator, probability = permutation_probability()
        self.assertEqual((numerator, denominator), (41573328, 220227973560))
        self.assertEqual(probability, Fraction(1732222, 9176165565))

    def test_coordinate_graph_probabilities_are_reproducible(self) -> None:
        self.assertEqual(
            typed_coordinate_probability(),
            Fraction(13367, 12234887420),
        )
        self.assertEqual(
            field_assignment_probability(require_all=False),
            Fraction(3847023, 6117443710),
        )
        self.assertEqual(
            field_assignment_probability(require_all=True),
            Fraction(3, 12234887420),
        )
        self.assertTrue(observed_typed_coordinate_event())
        self.assertTrue(observed_field_event(require_all=False))
        self.assertFalse(observed_field_event(require_all=True))

    def test_all_occurrence_packet_probabilities_are_reproducible(self) -> None:
        self.assertEqual(
            ledger_containment_probability(),
            Fraction(4277, 2203161),
        )
        self.assertEqual(
            packet_sum_probability(),
            Fraction(5837, 2446977484),
        )
        self.assertEqual(
            packet_sum_permutation_probability(),
            Fraction(367453, 36704662260),
        )
        self.assertEqual(
            header_residual_assignment_probability(),
            Fraction(74201, 3670466226),
        )


if __name__ == "__main__":
    unittest.main()
