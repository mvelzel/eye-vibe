import unittest

from eye_mystery.mono_substitution import solve_mono_substitution
from eye_mystery.ngram import TetragramModel


class MonoSubstitutionTests(unittest.TestCase):
    def test_returns_injective_key_and_plaintexts(self) -> None:
        corpus = ("THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG" * 20)
        model = TetragramModel.train(corpus)
        result = solve_mono_substitution(
            ((0, 1, 2, 0, 1, 2),), model, restarts=1, iterations=100
        )
        self.assertEqual(len(set(result.key)), 26)
        self.assertEqual(len(result.plaintexts[0]), 6)

    def test_homophonic_mode_can_merge_states(self) -> None:
        model = TetragramModel.train("A" * 1_000)
        result = solve_mono_substitution(
            ((0, 1, 2, 0, 1, 2, 0, 1, 2),),
            model,
            restarts=2,
            iterations=3_000,
            seed=17,
            injective=False,
        )
        self.assertEqual(result.plaintexts, ("A" * 9,))
        self.assertEqual(result.key[:3], (0, 0, 0))


if __name__ == "__main__":
    unittest.main()
