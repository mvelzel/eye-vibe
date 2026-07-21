import random
import unittest

from eye_mystery.deck_base import decode_affine_base_swap
from eye_mystery.deck_base_generic import (
    build_base_orbit_tables,
    compose,
    decode_base_top_swap,
    decode_base_top_swap_with_cycles,
    decode_base_top_swap_hidden_sequence_with_tables,
    decode_base_top_swap_hidden_with_tables,
    decode_base_top_swap_with_tables,
    encrypt_base_top_swap,
    permutation_power,
)


def materialized_decode(ciphertext, base):
    deck = list(range(len(base)))
    result = []
    for card in ciphertext:
        deck = [deck[base[position]] for position in range(len(base))]
        position = deck.index(card)
        result.append(position)
        deck[0], deck[position] = deck[position], deck[0]
    return tuple(result)


class GenericDeckBaseTests(unittest.TestCase):
    def test_matches_materialized_random_permutations(self) -> None:
        rng = random.Random(1234)
        for _ in range(20):
            base = list(range(11))
            rng.shuffle(base)
            ciphertext = tuple(rng.randrange(11) for _ in range(40))
            self.assertEqual(
                decode_base_top_swap(ciphertext, base),
                materialized_decode(ciphertext, base),
            )
            self.assertEqual(
                decode_base_top_swap_with_cycles(ciphertext, base),
                materialized_decode(ciphertext, base),
            )

    def test_matches_specialized_affine_decoder(self) -> None:
        ciphertext = (2, 5, 1, 2, 6, 0, 4)
        modulus = 7
        for multiplier in range(1, modulus):
            for offset in range(modulus):
                base = tuple(
                    (multiplier * position + offset) % modulus
                    for position in range(modulus)
                )
                self.assertEqual(
                    decode_base_top_swap(ciphertext, base),
                    decode_affine_base_swap(
                        ciphertext, multiplier, offset, modulus
                    ),
                )

    def test_arbitrary_initial_card_order(self) -> None:
        base = (2, 0, 4, 1, 3)
        initial_coordinates = (3, 1, 4, 0, 2)
        initial_deck = [0] * 5
        for card, coordinate in enumerate(initial_coordinates):
            initial_deck[coordinate] = card
        ciphertext = (3, 0, 4, 3, 2, 1)

        deck = initial_deck
        expected = []
        for card in ciphertext:
            deck = [deck[base[position]] for position in range(5)]
            position = deck.index(card)
            expected.append(position)
            deck[0], deck[position] = deck[position], deck[0]
        tables = build_base_orbit_tables(base, len(ciphertext))
        self.assertEqual(
            decode_base_top_swap_with_tables(
                ciphertext, tables, initial_coordinates
            ),
            tuple(expected),
        )

    def test_composition_and_power(self) -> None:
        permutation = (1, 2, 3, 4, 0)
        self.assertEqual(compose(permutation, permutation), (2, 3, 4, 0, 1))
        self.assertEqual(permutation_power(permutation, 3), (3, 4, 0, 1, 2))

    def test_generic_round_trip(self) -> None:
        base = (2, 0, 4, 1, 3)
        plaintext = (2, 4, 1, 3, 2, 0, 4)
        ciphertext = encrypt_base_top_swap(plaintext, base)
        self.assertEqual(decode_base_top_swap(ciphertext, base), plaintext)

    def test_plaintext_selected_hidden_swap(self) -> None:
        base = (2, 0, 4, 1, 3)
        plaintext = (2, 4, 1, 3, 2, 0, 4)

        def hidden(position, size):
            return 1 + position % (size - 1), 1 + (position + 1) % (size - 1)

        deck = list(range(5))
        ciphertext = []
        for position in plaintext:
            deck = [deck[base[index]] for index in range(5)]
            deck[0], deck[position] = deck[position], deck[0]
            ciphertext.append(deck[0])
            left, right = hidden(position, 5)
            deck[left], deck[right] = deck[right], deck[left]
        tables = build_base_orbit_tables(base, len(ciphertext))
        self.assertEqual(
            decode_base_top_swap_hidden_with_tables(
                ciphertext, tables, hidden
            ),
            plaintext,
        )

    def test_single_hidden_sequence_matches_wrapper(self) -> None:
        base = (2, 0, 4, 1, 3)
        ciphertext = (4, 1, 3, 0)
        tables = build_base_orbit_tables(base, len(ciphertext))

        def rule(position, size):
            return (
                1 + position % (size - 1),
                1 + (position + 2) % (size - 1),
            )

        self.assertEqual(
            decode_base_top_swap_hidden_sequence_with_tables(
                ciphertext, tables, (rule,)
            ),
            decode_base_top_swap_hidden_with_tables(
                ciphertext, tables, rule
            ),
        )


if __name__ == "__main__":
    unittest.main()
