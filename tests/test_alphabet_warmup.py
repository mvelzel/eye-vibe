import unittest

from eye_mystery.affine_gak import decode_affine_gak_from_state
from eye_mystery.alphabet_warmup import (
    LATIN_ALPHABET,
    affine_state_after_warmup,
    alphabet_warmups,
    deck_coordinates_after_warmup,
)
from eye_mystery.deck_base_generic import (
    build_base_orbit_tables,
    decode_base_top_swap_with_tables,
    encrypt_base_top_swap,
)
from eye_mystery.ninth_second import TRAILER_ALPHABET


def encode_affine_from_state(plaintext, multiplier, previous, hidden):
    ciphertext = []
    for symbol in plaintext:
        previous = (previous + symbol * pow(hidden, -1, 83)) % 83
        ciphertext.append(previous)
        hidden = hidden * multiplier(symbol) % 83
    return tuple(ciphertext)


class AlphabetWarmupTests(unittest.TestCase):
    def test_warmup_variants_are_the_two_keyed_directions(self) -> None:
        warmups = alphabet_warmups()
        self.assertEqual(tuple(item.name for item in warmups), (
            "standard-az",
            "keyed-letter-order",
            "az-in-keyed-slots",
        ))
        keyed_letters = TRAILER_ALPHABET[:26]
        self.assertEqual(
            warmups[1].plaintext,
            tuple(LATIN_ALPHABET.index(letter) for letter in keyed_letters),
        )
        self.assertEqual(
            warmups[2].plaintext,
            tuple(keyed_letters.index(letter) for letter in LATIN_ALPHABET),
        )
        self.assertEqual(
            tuple(warmups[1].plaintext[index] for index in warmups[2].plaintext),
            tuple(range(26)),
        )

    def test_deck_warmup_recovers_continuation(self) -> None:
        base = (2, 0, 4, 1, 3)
        warmup = (0, 1, 3, 2, 4)
        visible_plaintext = (2, 4, 1, 3, 0, 2)
        complete_ciphertext = encrypt_base_top_swap(
            warmup + visible_plaintext,
            base,
        )
        visible_ciphertext = complete_ciphertext[len(warmup):]
        coordinates = deck_coordinates_after_warmup(base, warmup)
        tables = build_base_orbit_tables(base, len(visible_ciphertext))
        self.assertEqual(
            decode_base_top_swap_with_tables(
                visible_ciphertext,
                tables,
                coordinates,
            ),
            visible_plaintext,
        )
        self.assertNotEqual(
            decode_base_top_swap_with_tables(visible_ciphertext, tables),
            visible_plaintext,
        )

    def test_affine_warmup_recovers_continuation(self) -> None:
        multiplier = lambda symbol: pow(2, symbol, 83)
        warmup = (0, 1, 3, 2, 4)
        visible_plaintext = (7, 2, 7, 8, 1, 8)
        state = affine_state_after_warmup(warmup, multiplier)
        self.assertIsNotNone(state)
        previous, hidden = state  # type: ignore[misc]
        ciphertext = encode_affine_from_state(
            visible_plaintext,
            multiplier,
            previous,
            hidden,
        )
        self.assertEqual(
            decode_affine_gak_from_state(
                ciphertext,
                multiplier,
                previous=previous,
                hidden=hidden,
            ),
            visible_plaintext,
        )
        self.assertNotEqual(
            decode_affine_gak_from_state(
                ciphertext,
                multiplier,
                previous=0,
                hidden=1,
            ),
            visible_plaintext,
        )

    def test_rejects_deck_instruction_outside_deck(self) -> None:
        with self.assertRaisesRegex(ValueError, "outside the deck"):
            deck_coordinates_after_warmup((1, 2, 0), (3,))


if __name__ == "__main__":
    unittest.main()
