import unittest
from collections import Counter

from eye_mystery.affine_embedding import context_from_sequences
from eye_mystery.affine_linear import (
    analyze_fixed_multipliers,
    enumerate_multiplier_cases,
)
from scripts.test_affine_isomorph_embedding import last_family_contexts
from scripts.test_affine_isomorph_embedding import first_three_contexts


class AffineLinearTests(unittest.TestCase):
    def test_two_fixed_points_force_a_collision(self) -> None:
        context = context_from_sequences("impossible", (1, 2, 3), (1, 2, 4))
        case = analyze_fixed_multipliers((context,), (1,))
        self.assertEqual(case.status, "forced_collision")
        self.assertIn((3, 4), case.collisions)

    def test_c41_last_context_certificate(self) -> None:
        contexts = last_family_contexts()[:2]
        counts = Counter(
            case.status
            for case in enumerate_multiplier_cases(contexts, hidden_order=41)
        )
        self.assertEqual(
            counts,
            {"inconsistent": 1664, "forced_collision": 17},
        )

    def test_c82_combined_context_certificate(self) -> None:
        last_contexts = last_family_contexts()[:2]
        cases = tuple(
            enumerate_multiplier_cases(last_contexts, hidden_order=82)
        )
        counts = Counter(case.status for case in cases)
        self.assertEqual(
            counts,
            {"inconsistent": 6644, "forced_collision": 76, "open": 4},
        )
        first_context = first_three_contexts()[0]
        extension_counts = Counter(
            analyze_fixed_multipliers(
                last_contexts + (first_context,),
                case.multipliers + (multiplier,),
            ).status
            for case in cases
            if case.status == "open"
            for multiplier in range(1, 83)
        )
        self.assertEqual(extension_counts, {"inconsistent": 328})


if __name__ == "__main__":
    unittest.main()
