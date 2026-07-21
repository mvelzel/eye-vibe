import unittest

from eye_mystery.deck_shuffles import (
    affine_with_fixed_card,
    affine_with_removed_dummy,
    interleave,
    josephus,
    mongean,
    standard_base_candidates,
)


class DeckShuffleTests(unittest.TestCase):
    def test_generators_are_permutations(self) -> None:
        examples = (
            interleave(11, 6),
            interleave(11, 5, right_first=True),
            mongean(11),
            mongean(11, first_to_top=True, reverse_source=True),
            josephus(11, 3),
            affine_with_fixed_card(11, 10, 3, 4),
            affine_with_removed_dummy(11, 5, 7),
        )
        for example in examples:
            self.assertEqual(tuple(sorted(example)), tuple(range(11)))

    def test_candidate_names_and_permutations_are_unique(self) -> None:
        candidates = tuple(standard_base_candidates(11))
        self.assertEqual(len({name for name, _ in candidates}), len(candidates))
        self.assertEqual(
            len({permutation for _, permutation in candidates}), len(candidates)
        )


if __name__ == "__main__":
    unittest.main()
