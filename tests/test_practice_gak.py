import unittest

from eye_mystery.practice_gak import (
    encrypt_mongean_cuts,
    mongean_shuffle,
    recover_mongean_cuts,
)


PRACTICE_CIPHERTEXT = (
    66, 77, 19, 15, 46, 74, 47, 52, 20, 31, 18, 65, 27, 50, 49, 12, 24,
    22, 30, 23, 15, 18, 14, 29, 23, 19, 50, 72, 22, 9, 12, 77, 46, 20,
    37, 12, 51, 39, 79, 76, 27, 70, 38, 14, 17, 35, 20, 52, 30, 53, 71,
    80, 14, 3, 50, 71, 39, 13, 18, 49, 69, 6, 81, 50, 79, 32, 75, 40, 15,
    14, 22, 0, 67, 53, 52, 36, 0, 70, 56, 40, 16, 48, 81, 80, 58, 14, 76,
    63, 16,
)
PRACTICE_PLAINTEXT = (
    "helloihopeyoufoundthiscipherinterestingletmeknowifyounoticedany"
    "weaknessesorquirksthankyou"
)


class PracticeGakTests(unittest.TestCase):
    def test_mongean_shuffle(self) -> None:
        self.assertEqual(mongean_shuffle(tuple(range(7))), (6, 4, 2, 0, 1, 3, 5))

    def test_known_practice_cipher_round_trip(self) -> None:
        cuts = tuple(ord(letter) - 96 for letter in PRACTICE_PLAINTEXT)
        self.assertEqual(encrypt_mongean_cuts(cuts), PRACTICE_CIPHERTEXT)
        recovered = recover_mongean_cuts(PRACTICE_CIPHERTEXT)
        self.assertEqual(len(recovered), len(PRACTICE_CIPHERTEXT))
        self.assertTrue(all(len(matches) == 1 for matches in recovered))
        self.assertEqual(tuple(matches[0] for matches in recovered), cuts)


if __name__ == "__main__":
    unittest.main()
