import unittest

from eye_mystery.partial_permutation import (
    complete_partial_permutation,
    completion_stats,
    permutation_is_even,
    validate_partial_permutation,
)


class PartialPermutationTests(unittest.TestCase):
    def test_path_and_cycle_bounds_are_sharp(self) -> None:
        # 0->1->2 is closed as (0 1 2), while (3 4) is already a cycle.
        stats = completion_stats({0: 1, 1: 2, 3: 4, 4: 3, 5: 5}, 8)
        self.assertEqual(stats.path_lengths, (2,))
        self.assertEqual(stats.cycle_lengths, (2, 1))
        self.assertEqual(stats.minimum_transpositions, 3)
        self.assertEqual(stats.minimum_even_transpositions, 4)
        self.assertEqual(stats.minimum_odd_transpositions, 3)
        self.assertEqual(stats.minimum_support, 5)

    def test_two_missing_edges_allow_both_signs(self) -> None:
        stats = completion_stats({0: 1, 1: 0}, 4)
        self.assertTrue(stats.even_completion)
        self.assertTrue(stats.odd_completion)

    def test_unique_completion_has_forced_sign(self) -> None:
        even = completion_stats({0: 1, 1: 0, 2: 2}, 3)
        self.assertFalse(even.even_completion)
        self.assertTrue(even.odd_completion)
        self.assertIsNone(even.minimum_even_transpositions)
        self.assertEqual(even.minimum_odd_transpositions, 1)

    def test_rejects_non_injective_mapping(self) -> None:
        with self.assertRaises(ValueError):
            validate_partial_permutation({0: 2, 1: 2}, 3)

    def test_constructs_both_completion_signs(self) -> None:
        mapping = {0: 1, 1: 2, 4: 4}
        even = complete_partial_permutation(mapping, 6, even=True)
        odd = complete_partial_permutation(mapping, 6, even=False)
        self.assertTrue(permutation_is_even(even))
        self.assertFalse(permutation_is_even(odd))
        for source, target in mapping.items():
            self.assertEqual(even[source], target)
            self.assertEqual(odd[source], target)


if __name__ == "__main__":
    unittest.main()
