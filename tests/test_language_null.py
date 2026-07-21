import random
import unittest

from eye_mystery.language_null import prefix_tree_parity_shuffle


class LanguageNullTests(unittest.TestCase):
    def test_preserves_tree_edges_and_parity_frequencies(self) -> None:
        reference = {
            "a": (9, 1, 2, 3, 4, 5, 6, 7),
            "b": (8, 1, 2, 3, 4, 8, 9, 0),
            "c": (7, 1, 2, 6, 7, 8, 9, 0),
        }
        streams = {
            name: tuple(100 * index + position for position in range(len(values)))
            for index, (name, values) in enumerate(reference.items())
        }
        shuffled = prefix_tree_parity_shuffle(
            streams, reference, random.Random(17)
        )
        for name in streams:
            self.assertEqual(shuffled[name][0], streams[name][0])
            for parity in (0, 1):
                self.assertCountEqual(
                    shuffled[name][parity::2], streams[name][parity::2]
                )
        # All three share the root edge at positions 1..2, so they use the
        # same source position there after shuffling.
        for position in (1, 2):
            origins = {
                shuffled[name][position] % 100 for name in reference
            }
            self.assertEqual(len(origins), 1)
        # a/b share the child edge at positions 3..4 and still use matching
        # source positions, independently of c's suffix shuffle.
        for position in (3, 4):
            self.assertEqual(
                shuffled["a"][position] % 100,
                shuffled["b"][position] % 100,
            )


if __name__ == "__main__":
    unittest.main()
