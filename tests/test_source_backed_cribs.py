import unittest

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.known_plaintext import first_isomorphism_conflict
from scripts.check_source_backed_cribs import EAST1_WALL_CRIB, occurrences


class SourceBackedCribTests(unittest.TestCase):
    def test_east1_wall_crib_is_exact_length_and_compatible(self) -> None:
        body = trigram_values(MESSAGES["east1"])[1:]
        self.assertEqual(len(EAST1_WALL_CRIB), len(body))
        self.assertIsNone(
            first_isomorphism_conflict(
                {"east1": EAST1_WALL_CRIB},
                {"east1": body},
                min_length=2,
                max_length=40,
            )
        )

    def test_repeated_phrase_positions(self) -> None:
        self.assertEqual(
            occurrences(EAST1_WALL_CRIB, "WHY ELSE WOULD YOU BE"),
            (35, 63),
        )


if __name__ == "__main__":
    unittest.main()
