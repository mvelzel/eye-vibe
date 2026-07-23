import unittest

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.finnish_syllables import (
    aligned_equality_runs,
    equality_signature,
    syllabify_word,
    syllable_tokens,
)


CRAFTED_FIRST = """
Paukkovalla paaterella. Mitä itket, impi rukka, Impi rukka, neito nuori;
Maammoko pahon pitävi? Maammoni hyvin pitävi. Immikkö aholla itki,
"""

CRAFTED_SECOND = """
Paukkovalla paaterella. Mitä itket, impi rukka, Impi rukka, neito nuori;
Sikkoko pahon pitävi? Sikkoni hyvin pitävi. Immikkö aholla itki,
"""


class FinnishSyllableTests(unittest.TestCase):
    def test_kielitoimisto_general_examples(self) -> None:
        self.assertEqual(syllabify_word("kala"), ("ka", "la"))
        self.assertEqual(syllabify_word("luita"), ("lui", "ta"))
        self.assertEqual(syllabify_word("metsä"), ("met", "sä"))
        self.assertEqual(syllabify_word("ainoa"), ("ai", "no", "a"))
        self.assertEqual(syllabify_word("herttuaa"), ("hert", "tu", "aa"))
        self.assertEqual(syllabify_word("puolueita"), ("puo", "lu", "ei", "ta"))
        self.assertEqual(syllabify_word("paperien"), ("pa", "pe", "ri", "en"))
        self.assertEqual(syllabify_word("pieni"), ("pie", "ni"))

    def test_crafted_discord_pair_has_only_the_shared_opening(self) -> None:
        first = syllable_tokens(CRAFTED_FIRST)
        second = syllable_tokens(CRAFTED_SECOND)
        self.assertEqual(len(first), 48)
        self.assertEqual(len(second), 48)
        self.assertEqual(
            aligned_equality_runs(first, second),
            ((True, 24), (False, 2), (True, 6), (False, 2), (True, 14)),
        )

    def test_eye_pair_has_a_different_post_prefix_run_pattern(self) -> None:
        east = trigram_values(MESSAGES["east1"])[1:]
        west = trigram_values(MESSAGES["west1"])[1:]
        self.assertEqual(
            aligned_equality_runs(east, west)[:5],
            ((True, 24), (False, 4), (True, 4), (False, 4), (True, 13)),
        )

    def test_equality_signature(self) -> None:
        self.assertEqual(equality_signature(("a", "b", "a", "c")), (0, 1, 0, 2))

    def test_rejects_nonword_input(self) -> None:
        with self.assertRaises(ValueError):
            syllabify_word("two words")


if __name__ == "__main__":
    unittest.main()
