import random
import unittest

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.sparse_deck import (
    decode_sparse_deck,
    decode_sparse_deck_hidden_sequences,
    encrypt_sparse_deck,
    encrypt_sparse_deck_hidden_sequences,
    no_swap_rules,
)


class SparseDeckTests(unittest.TestCase):
    def test_round_trip_random_rules(self) -> None:
        rng = random.Random(20260721)
        size = 17
        rules = tuple(
            tuple(rng.sample(range(1, size), 2)) for _ in range(size)
        )
        plaintext = tuple(rng.randrange(size) for _ in range(200))
        self.assertEqual(
            decode_sparse_deck(encrypt_sparse_deck(plaintext, rules), rules),
            plaintext,
        )

    def test_round_trip_hidden_swap_sequences(self) -> None:
        rng = random.Random(20260722)
        size = 13
        rules = tuple(
            tuple(
                tuple(rng.sample(range(1, size), 2))
                for _ in range(3)
            )
            for _ in range(size)
        )
        plaintext = tuple(rng.randrange(size) for _ in range(100))
        ciphertext = encrypt_sparse_deck_hidden_sequences(plaintext, rules)
        self.assertEqual(
            decode_sparse_deck_hidden_sequences(ciphertext, rules),
            plaintext,
        )

    def test_no_swap_matches_top_swap_model(self) -> None:
        plaintext = (4, 1, 3, 4, 2, 1)
        rules = no_swap_rules(7)
        ciphertext = encrypt_sparse_deck(plaintext, rules)
        self.assertEqual(ciphertext, (4, 1, 3, 0, 2, 4))
        self.assertEqual(decode_sparse_deck(ciphertext, rules), plaintext)

    def test_rejects_top_hidden_swap(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-top"):
            decode_sparse_deck((1,), ((1, 1), (0, 1)))

    def test_concrete_lower_hermetic_crib_witness(self) -> None:
        plaintext = "THEREISNOGOODTHATCAN"
        ranks = {
            "T": 66,
            "H": 18,
            "E": 49,
            "R": 75,
            "I": 2,
            "S": 60,
            "N": 29,
            "O": 40,
            "G": 59,
            "D": 15,
            "A": 68,
            "C": 36,
        }
        hidden = {
            "T": (5, 18),
            "H": (18, 55),
            "E": (18, 54),
            "R": (18, 49),
            "I": (9, 18),
            "S": (59, 66),
            "N": (59, 60),
            "O": (9, 40),
            "G": (9, 18),
            "D": (29, 47),
            "A": (3, 66),
            "C": (54, 68),
        }
        rules = list(no_swap_rules(83))
        for letter, swap in hidden.items():
            rules[ranks[letter]] = swap
        ciphertext = encrypt_sparse_deck(
            tuple(ranks[letter] for letter in plaintext), tuple(rules)
        )
        self.assertEqual(
            ciphertext,
            trigram_values(MESSAGES["east4"])[1:21],
        )

    def test_concrete_shared_hermetic_crib_witness(self) -> None:
        ranks = {
            "T": 66,
            "H": 18,
            "A": 68,
            "W": 13,
            "I": 2,
            "C": 36,
            "E": 49,
            "R": 75,
            "S": 60,
            "N": 29,
            "O": 40,
            "G": 59,
            "D": 15,
        }
        hidden = {
            "T": ((5, 18), (3, 62)),
            "H": ((18, 55), (48, 68)),
            "A": ((3, 66), (9, 61)),
            "W": ((2, 29), (18, 75)),
            "I": ((9, 18), (24, 36)),
            "C": ((54, 68), (2, 42)),
            "E": ((18, 54), (1, 9)),
            "R": ((18, 49), (1, 24)),
            "S": ((59, 66), (17, 24)),
            "N": ((59, 60), (17, 18)),
            "O": ((9, 40), (18, 36)),
            "G": ((9, 18), (18, 18)),
            "D": ((29, 47), (2, 2)),
        }
        rules = [((1, 1), (1, 1)) for _ in range(83)]
        for letter, swaps in hidden.items():
            rules[ranks[letter]] = swaps

        for name, plaintext in (
            ("east1", "THATWHICHI"),
            ("east4", "THEREISNOGOODTHATCAN"),
        ):
            ciphertext = encrypt_sparse_deck_hidden_sequences(
                tuple(ranks[letter] for letter in plaintext), rules
            )
            self.assertEqual(
                ciphertext,
                trigram_values(MESSAGES[name])[1 : 1 + len(plaintext)],
            )

    def test_concrete_four_transposition_crib_witness(self) -> None:
        ranks = {
            "T": 66,
            "H": 18,
            "A": 68,
            "W": 13,
            "I": 2,
            "C": 36,
            "S": 60,
            "B": 61,
            "O": 40,
            "E": 49,
            "R": 75,
            "N": 29,
            "G": 59,
            "D": 15,
        }
        hidden = {
            "T": ((5, 18), (3, 62), (48, 60)),
            "H": ((18, 55), (48, 68), (60, 68)),
            "A": ((3, 66), (9, 61), (55, 60)),
            "W": ((2, 29), (18, 75), (36, 48)),
            "I": ((9, 18), (24, 36), (24, 60)),
            "C": ((54, 68), (2, 42), (36, 70)),
            "S": ((59, 66), (17, 24), (9, 13)),
            "B": ((40, 61), (10, 40), (32, 40)),
            "O": ((9, 40), (18, 36), (7, 64)),
            "E": ((18, 54), (1, 9), (9, 36)),
            "R": ((18, 49), (1, 24), (1, 60)),
            "N": ((59, 60), (17, 18), (7, 13)),
            "G": ((9, 18), (18, 18), (40, 64)),
            "D": ((29, 47), (2, 2), (1, 36)),
        }
        rules = [((1, 1), (1, 1), (1, 1)) for _ in range(83)]
        for letter, swaps in hidden.items():
            rules[ranks[letter]] = swaps

        for name, plaintext in (
            ("east1", "THATWHICHISABO"),
            ("east4", "THEREISNOGOODTHATCAN"),
        ):
            ciphertext = encrypt_sparse_deck_hidden_sequences(
                tuple(ranks[letter] for letter in plaintext), rules
            )
            self.assertEqual(
                ciphertext,
                trigram_values(MESSAGES[name])[1 : 1 + len(plaintext)],
            )

    def test_concrete_full_shared_hermetic_crib_witness(self) -> None:
        ranks = {
            "T": 66,
            "H": 18,
            "A": 68,
            "W": 13,
            "I": 2,
            "C": 36,
            "S": 60,
            "B": 61,
            "O": 40,
            "E": 49,
            "R": 75,
            "N": 29,
            "G": 59,
            "D": 15,
            "V": 14,
            "L": 78,
            "K": 70,
        }
        hidden = {
            "T": ((5, 18), (3, 62), (48, 60)),
            "H": ((18, 55), (48, 68), (60, 68)),
            "A": ((3, 66), (9, 61), (55, 60)),
            "W": ((2, 29), (18, 75), (36, 48)),
            "I": ((9, 18), (24, 36), (24, 60)),
            "C": ((54, 68), (2, 42), (36, 70)),
            "S": ((59, 66), (2, 8), (9, 13)),
            "B": ((1, 9), (1, 15), (32, 40)),
            "O": ((9, 40), (18, 36), (7, 64)),
            "E": ((18, 54), (1, 9), (9, 36)),
            "R": ((18, 49), (1, 24), (1, 60)),
            "N": ((59, 60), (17, 18), (7, 13)),
            "G": ((9, 18), (18, 18), (40, 64)),
            "D": ((29, 47), (2, 2), (1, 36)),
            "V": ((8, 29), (49, 59), (49, 81)),
            "L": ((9, 49), (1, 1), (1, 1)),
            "K": ((1, 1), (1, 1), (1, 1)),
        }
        rules = [((1, 1), (1, 1), (1, 1)) for _ in range(83)]
        for letter, swaps in hidden.items():
            rules[ranks[letter]] = swaps

        for name, plaintext in (
            ("east1", "THATWHICHISABOVEISLIKETO"),
            ("east4", "THEREISNOGOODTHATCAN"),
        ):
            ciphertext = encrypt_sparse_deck_hidden_sequences(
                tuple(ranks[letter] for letter in plaintext), rules
            )
            self.assertEqual(
                ciphertext,
                trigram_values(MESSAGES[name])[1 : 1 + len(plaintext)],
            )


if __name__ == "__main__":
    unittest.main()
