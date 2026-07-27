import unittest
from itertools import combinations, permutations

from eye_mystery.partial_permutation import (
    complete_partial_permutation,
    completion_stats,
    finite_order_completion,
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

    def test_finite_order_completion_uses_one_planted_cycle(self) -> None:
        result = finite_order_completion(
            {0: 1, 1: 2, 3: 4, 4: 5},
            6,
            6,
        )
        self.assertTrue(result.feasible)
        self.assertEqual(result.path_vertex_lengths, (3, 3))
        self.assertEqual(result.minimum_extra_vertices, 0)

    def test_finite_order_completion_can_add_filler(self) -> None:
        result = finite_order_completion({0: 1, 1: 2, 2: 3}, 6, 6)
        self.assertTrue(result.feasible)
        self.assertEqual(result.minimum_extra_vertices, 2)

    def test_finite_order_completion_rejects_long_path(self) -> None:
        result = finite_order_completion(
            {index: index + 1 for index in range(6)},
            9,
            5,
        )
        self.assertFalse(result.feasible)
        self.assertIsNone(result.minimum_extra_vertices)

    def test_finite_order_completion_rejects_bad_cycle(self) -> None:
        result = finite_order_completion(
            {0: 1, 1: 2, 2: 3, 3: 0},
            6,
            6,
        )
        self.assertFalse(result.feasible)
        self.assertEqual(result.incompatible_cycle_lengths, (4,))

    def test_finite_order_completion_matches_small_bruteforce(self) -> None:
        for size in range(1, 5):
            full_permutations = tuple(permutations(range(size)))
            for domain_size in range(size + 1):
                for domain in combinations(range(size), domain_size):
                    for image in permutations(range(size), domain_size):
                        mapping = dict(zip(domain, image, strict=True))
                        for exponent in range(1, 7):
                            expected = any(
                                all(
                                    candidate[source] == target
                                    for source, target in mapping.items()
                                )
                                and all(
                                    self._permutation_power(candidate, value, exponent)
                                    == value
                                    for value in range(size)
                                )
                                for candidate in full_permutations
                            )
                            self.assertEqual(
                                finite_order_completion(
                                    mapping, size, exponent
                                ).feasible,
                                expected,
                            )

    @staticmethod
    def _permutation_power(
        permutation: tuple[int, ...], value: int, exponent: int
    ) -> int:
        for _ in range(exponent):
            value = permutation[value]
        return value


if __name__ == "__main__":
    unittest.main()
