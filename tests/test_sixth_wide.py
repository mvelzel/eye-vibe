import unittest

from eye_mystery.affine_embedding import Context
from eye_mystery.sixth_wide import (
    best_missing_completion,
    best_polynomial_header_rule,
    cancel_direction_word,
    column_collision_score,
    column_label_mutual_information,
    erase_neutral_word,
    fixed_width_digits,
    linear_system_consistent,
    literal_affine_context_fit,
    polynomial_hash,
    word_inventory,
)


class SixthWideTests(unittest.TestCase):
    def test_literal_affine_context(self) -> None:
        context = Context("translation", ((0, 1), (1, 2), (2, 0)))
        fit = literal_affine_context_fit(context, modulus=3, dimension=1)
        self.assertTrue(fit.consistent)
        self.assertEqual(fit.pairs, 3)

    def test_inconsistent_linear_system(self) -> None:
        self.assertFalse(linear_system_consistent(((1,), (1,)), (0, 1), 5))

    def test_polynomial_hash_and_header_rule(self) -> None:
        self.assertEqual(polynomial_hash((1, 2, 3), 2, 101), 17)
        streams = ((-17 % 101, 1, 2, 3), (-17 % 101, 1, 2, 3))
        rule = best_polynomial_header_rule(streams)
        self.assertEqual(rule.matches, 2)

    def test_missing_completion_finds_planted_constant(self) -> None:
        # For x=y=0, the first selected constant producing a missing word is
        # k=3: 333_base5=93.
        fit = best_missing_completion(((0, 0),))
        self.assertEqual(fit.missing, 1)
        self.assertEqual(fit.constant, 3)

    def test_word_reductions(self) -> None:
        self.assertEqual(fixed_width_digits(7, 5, 3), (0, 1, 2))
        self.assertEqual(erase_neutral_word(7), (1, 2))
        self.assertEqual(cancel_direction_word(40), ())  # 130_base5
        self.assertEqual(word_inventory(erase_neutral_word).full_classes, 85)

    def test_column_information(self) -> None:
        associated = ((0, 1), (0, 1), (0, 1))
        unassociated = ((0, 1), (1, 0), (0, 1), (1, 0))
        self.assertGreater(
            column_label_mutual_information(associated),
            column_label_mutual_information(unassociated),
        )
        self.assertEqual(column_collision_score(((0, 1),), ((0, 1),)), 2)
        self.assertEqual(column_collision_score(((0, 1),), ((1, 0),)), 0)


if __name__ == "__main__":
    unittest.main()
