import unittest

from eye_mystery.blood_deck import (
    blood_cut_vectors,
    cut_letter_map,
    decode_base_then_blood_cut,
    decode_blood_cut_then_base,
)


class BloodDeckTests(unittest.TestCase):
    def test_natural_vectors(self) -> None:
        vectors = blood_cut_vectors()
        self.assertEqual(len(vectors["end"]), 26)
        self.assertEqual(vectors["end"][:3], (83, 78, 76))
        self.assertEqual(vectors["count"][5], 66)
        self.assertEqual(vectors["span"][5], 67)
        for name in ("end", "span", "count"):
            with self.subTest(name=name):
                self.assertEqual(len(cut_letter_map(vectors[name])), 26)
        with self.assertRaises(ValueError):
            cut_letter_map(vectors["start"])

    def test_both_composition_orders_round_trip(self) -> None:
        size = 11
        base = tuple((3 * position + 2) % size for position in range(size))
        cuts = (1, 4, 7)
        plaintext = (0, 2, 1, 1, 0, 2)
        for base_first in (True, False):
            deck = tuple(range(size))
            ciphertext = []
            for letter in plaintext:
                cut = cuts[letter]
                if base_first:
                    deck = tuple(deck[position] for position in base)
                    deck = deck[cut:] + deck[:cut]
                else:
                    deck = deck[cut:] + deck[:cut]
                    deck = tuple(deck[position] for position in base)
                ciphertext.append(deck[0])
            decoder = (
                decode_base_then_blood_cut
                if base_first
                else decode_blood_cut_then_base
            )
            self.assertEqual(decoder(ciphertext, base, cuts), plaintext)


if __name__ == "__main__":
    unittest.main()
