import unittest

from eye_mystery.progression_certificate import (
    CommutationContradiction,
    ProgressionContradiction,
    context_mapping,
    last_family_commutation_contradiction,
    last_family_progression_contradictions,
)


class ProgressionCertificateTests(unittest.TestCase):
    def test_one_step_context_is_a_partial_permutation(self) -> None:
        mapping = context_mapping("east4", 68, "east5", 69, 30)
        self.assertEqual(len(mapping), 25)
        self.assertEqual(len(set(mapping.values())), 25)

    def test_last_family_contains_two_direct_contradictions(self) -> None:
        contradictions = last_family_progression_contradictions()
        self.assertEqual(
            contradictions,
            (
                # P(31)=33, P(33)=62, P(62)=8, but P^3(31)=69.
                ProgressionContradiction(31, (31, 33, 62, 8), 69),
                # P(69)=31, P(31)=33, P(33)=62, but P^3(69)=17.
                ProgressionContradiction(69, (69, 31, 33, 62), 17),
            ),
        )

    def test_last_family_context_maps_cannot_commute(self) -> None:
        self.assertEqual(
            last_family_commutation_contradiction(),
            CommutationContradiction(
                start=3,
                first_then_second=(3, 44, 23),
                second_then_first=(3, 22, 23),
                colliding_source=59,
            ),
        )


if __name__ == "__main__":
    unittest.main()
