import unittest

from eye_mystery.deck_base import decode_affine_base_swap


def materialized_decode(ciphertext, multiplier, offset, modulus, secondary="none"):
    deck = list(range(modulus))
    result = []
    for card in ciphertext:
        deck = [deck[(multiplier * index + offset) % modulus] for index in range(modulus)]
        position = deck.index(card)
        result.append(position)
        deck[0], deck[position] = deck[position], deck[0]
        if secondary == "one-k" and position not in (0, 1):
            deck[1], deck[position] = deck[position], deck[1]
    return tuple(result)


class DeckBaseTests(unittest.TestCase):
    def test_lazy_affine_state_matches_materialized_deck(self) -> None:
        ciphertext = (3, 1, 6, 4, 2, 0, 5, 3)
        expected = materialized_decode(ciphertext, 3, 2, 7)
        self.assertEqual(decode_affine_base_swap(ciphertext, 3, 2, 7), expected)

    def test_secondary_swap_matches_materialized_deck(self) -> None:
        ciphertext = (3, 1, 6, 4, 2, 0, 5, 3)
        expected = materialized_decode(ciphertext, 3, 2, 7, "one-k")
        self.assertEqual(
            decode_affine_base_swap(ciphertext, 3, 2, 7, "one-k"),
            expected,
        )


if __name__ == "__main__":
    unittest.main()
