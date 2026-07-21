import unittest

from eye_mystery.chaocipher import decrypt, encrypt


class ChaocipherTests(unittest.TestCase):
    def test_historical_example(self) -> None:
        left_text = "HXUCZVAMDSLKPEFJRIGTWOBNYQ"
        right_text = "PTLNBQDEOYSFAVZKGJRIHWXUMC"
        plaintext = "WELLDONEISBETTERTHANWELLSAID"
        ciphertext = "OAHQHCNYNXTSZJRRHJBYHQKSOUJY"
        symbols = {character: index for index, character in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
        inverse = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        def encode(text: str) -> tuple[int, ...]:
            return tuple(symbols[character] for character in text)

        encrypted = encrypt(encode(plaintext), encode(left_text), encode(right_text))
        self.assertEqual("".join(inverse[value] for value in encrypted), ciphertext)
        self.assertEqual(
            decrypt(encode(ciphertext), encode(left_text), encode(right_text)),
            encode(plaintext),
        )

    def test_generalized_odd_alphabet_round_trip(self) -> None:
        left = tuple(range(7))
        right = (3, 1, 4, 0, 6, 2, 5)
        plaintext = (0, 6, 6, 1, 2, 5, 0, 3, 4)
        for nadir in (3, 4):
            ciphertext = encrypt(plaintext, left, right, nadir=nadir)
            self.assertEqual(decrypt(ciphertext, left, right, nadir=nadir), plaintext)


if __name__ == "__main__":
    unittest.main()
