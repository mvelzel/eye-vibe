import unittest

from eye_mystery.partial_group import (
    compose_partial,
    conflict_witness,
    distinctness_clique,
    generate_partial_words,
    inverse_partial,
    verify_distinctness_clique,
)


class PartialGroupTests(unittest.TestCase):
    def test_inverse_and_composition_keep_only_forced_edges(self) -> None:
        first = {0: 1, 1: 2, 3: 4}
        second = {1: 5, 2: 6, 7: 8}
        self.assertEqual(inverse_partial(first), {1: 0, 2: 1, 4: 3})
        self.assertEqual(compose_partial(first, second), {0: 5, 1: 6})

    def test_conflict_is_a_distinctness_witness(self) -> None:
        self.assertEqual(conflict_witness({0: 1}, {0: 2}), (0, 1, 2))
        self.assertIsNone(conflict_witness({0: 1}, {1: 2}))
        self.assertIsNone(conflict_witness({0: 1}, {0: 1, 1: 2}))

    def test_short_word_closure_and_clique_are_exact_witnesses(self) -> None:
        words = generate_partial_words(
            {
                "a": {0: 1, 1: 2, 2: 0},
                "b": {0: 2, 1: 0, 2: 1},
            },
            3,
            max_depth=3,
        )
        by_name = {word.name: word.mapping for word in words}
        self.assertEqual(by_name["identity"], {0: 0, 1: 1, 2: 2})
        self.assertIn({0: 2, 1: 0, 2: 1}, by_name.values())
        clique = distinctness_clique(words)
        self.assertTrue(verify_distinctness_clique(clique))
        self.assertEqual(len(clique), 3)


if __name__ == "__main__":
    unittest.main()
