import unittest

from eye_mystery.alternating_substitution import solve
from eye_mystery.ngram import TetragramModel


class AlternatingSubstitutionTests(unittest.TestCase):
    def test_homophonic_mode_can_merge_states_on_both_sides(self) -> None:
        model = TetragramModel.train("A" * 1_000)
        result = solve(
            ((0, 1, 2, 0, 1, 2, 0, 1, 2),),
            model,
            restarts=4,
            iterations=10_000,
            seed=19,
            injective=False,
        )
        self.assertEqual(result.plaintexts, ("A" * 9,))


if __name__ == "__main__":
    unittest.main()
