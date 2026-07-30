import unittest

from eye_mystery.corpus import MESSAGES
from eye_mystery.public_automaton import GRAPH_SEED, SEED, decode


class PublicAutomatonTests(unittest.TestCase):
    def test_seed_and_literal_replay_vector(self) -> None:
        self.assertEqual(len(SEED), 25)
        self.assertEqual(
            decode(MESSAGES["east1"]),
            "rutiezfv frk dlj jeoyzlohlxzfmdf vbpiqqttskrioghqcxxqakkzuztjiisxmmojjyfyrzlptxxpzohtgorcdmogjchrrz",
        )

    def test_rejects_incomplete_or_invalid_input(self) -> None:
        with self.assertRaises(ValueError):
            decode((0, 1))
        with self.assertRaises(ValueError):
            decode((0, 1, 5))

    def test_authored_graph_seed_variant_is_replayable(self) -> None:
        self.assertEqual(len(GRAPH_SEED), 25)
        self.assertTrue(
            decode(MESSAGES["east1"], seed=GRAPH_SEED).startswith(
                "rutiezfv frk dlw weoyzlohlxzfmdf"
            )
        )


if __name__ == "__main__":
    unittest.main()
