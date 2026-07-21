import unittest

from eye_mystery.affine_gak import decode_affine_gak


def encrypt(plaintext, multiplier_for_plaintext):
    hidden = 1
    visible = 0
    result = []
    for symbol in plaintext:
        # Rearrangement of t=(x'-x)*a.
        visible = (visible + symbol * pow(hidden, -1, 83)) % 83
        result.append(visible)
        hidden = hidden * multiplier_for_plaintext(symbol) % 83
    return tuple(result)


class AffineGakTests(unittest.TestCase):
    def test_round_trip(self) -> None:
        plaintext = (1, 2, 3, 5, 8, 13, 21)
        multiplier = lambda value: value + 1
        ciphertext = encrypt(plaintext, multiplier)
        self.assertEqual(decode_affine_gak(ciphertext, multiplier), plaintext)


if __name__ == "__main__":
    unittest.main()
