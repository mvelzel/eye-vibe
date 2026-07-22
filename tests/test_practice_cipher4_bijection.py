import random
import unittest

from eye_mystery.practice_cipher4_bijection import (
    BijectionAnnealer,
    CaseNgrams,
    encode_substitution,
    normalize_case_text,
)


class PracticeCipher4BijectionTests(unittest.TestCase):
    def test_normalization_preserves_case_and_supported_punctuation(self) -> None:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,'-"
        self.assertEqual(
            normalize_case_text("  One—two… ‘Three’.\n", alphabet),
            "One-two 'Three'.",
        )

    def test_encoder_and_annealer_recover_small_planted_substitution(self) -> None:
        alphabet = "ABCDE abcde.,"
        plaintext = ("A bad cab. A bad cab. A bad cab.",)
        shuffled = list(range(len(alphabet)))
        random.Random(83).shuffle(shuffled)
        mapping = {
            character: shuffled[index]
            for index, character in enumerate(alphabet)
        }
        streams = encode_substitution(plaintext, mapping)
        model = CaseNgrams.train(" ".join(plaintext) * 30, alphabet, order=3)
        candidate = BijectionAnnealer(
            streams,
            model,
            alphabet,
            random.Random(101),
        ).run(80_000, 8.0)
        self.assertEqual(candidate.plaintexts, plaintext)


if __name__ == "__main__":
    unittest.main()
