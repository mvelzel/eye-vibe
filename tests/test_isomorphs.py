import unittest

from eye_mystery.isomorphs import pattern, score


class IsomorphTests(unittest.TestCase):
    def test_pattern(self) -> None:
        self.assertEqual(pattern((7, 1, 8, 2, 9, 8, 3, 7, 9)), "A.B.CB.AC")

    def test_score_increases_with_repeats(self) -> None:
        self.assertGreater(score("A.B.CB.AC", 6), score("A.B.CB.AC", 2))


if __name__ == "__main__":
    unittest.main()
