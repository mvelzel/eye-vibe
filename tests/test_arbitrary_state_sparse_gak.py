from __future__ import annotations

import unittest

try:
    import z3  # noqa: F401
except ImportError:
    z3 = None

from eye_mystery.arbitrary_gak_sat import encrypt_messages
from eye_mystery.arbitrary_state_sparse_gak import (
    recover_arbitrary_state_gak_witness,
)
from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.isomorphs import pattern
from eye_mystery.sparse_gak_sat import encode_text
from scripts.classify_that_which_windows import WINDOWS


MATCHED_DECK = (0, 9, 8, 4, 3, 1, 6, 10, 2, 7, 5)
MATCHED_OPERATIONS = (
    (10, 3, 4, 7, 6, 2, 5, 1, 8, 0, 9),
    (6, 3, 4, 0, 7, 5, 1, 8, 2, 10, 9),
    (4, 7, 2, 0, 3, 5, 9, 1, 6, 10, 8),
    (6, 4, 0, 2, 1, 5, 9, 7, 8, 3, 10),
    (6, 4, 0, 3, 2, 5, 10, 9, 1, 8, 7),
    (1, 8, 6, 7, 5, 2, 10, 9, 0, 3, 4),
    (1, 8, 5, 7, 2, 0, 4, 10, 9, 6, 3),
)


@unittest.skipIf(z3 is None, "z3-solver is optional")
class ArbitraryStateSparseGAKTests(unittest.TestCase):
    def test_01_recovers_matched_pattern_from_independent_states(self) -> None:
        plaintext, alphabet = encode_text("THAT WHICH")
        initial_decks = tuple(
            tuple((card + shift) % 11 for card in MATCHED_DECK)
            for shift in range(6)
        )
        ciphertexts = tuple(
            encrypt_messages(
                (plaintext,),
                deck,
                MATCHED_OPERATIONS,
            )[0]
            for deck in initial_decks
        )
        self.assertEqual(
            {pattern(ciphertext) for ciphertext in ciphertexts},
            {"A.B.CB.AC."},
        )

        status, witness = recover_arbitrary_state_gak_witness(
            (plaintext,) * 6,
            ciphertexts,
            deck_size=11,
            plaintext_alphabet_size=len(alphabet),
            timeout_ms=30_000,
        )
        self.assertEqual(status, "sat")
        self.assertIsNotNone(witness)
        assert witness is not None
        self.assertEqual(
            tuple(
                encrypt_messages((plaintext,), deck, witness.operations)[0]
                for deck in witness.initial_decks
            ),
            tuple(ciphertexts),
        )

    def test_02_real_that_which_windows_have_an_exact_witness(self) -> None:
        phrase = "THAT WHICH"
        plaintext, alphabet = encode_text(phrase)
        ciphertexts = tuple(
            trigram_values(MESSAGES[window.message])[
                window.offset : window.offset + len(phrase)
            ]
            for window in WINDOWS
        )
        status, witness = recover_arbitrary_state_gak_witness(
            (plaintext,) * len(ciphertexts),
            ciphertexts,
            deck_size=83,
            plaintext_alphabet_size=len(alphabet),
            timeout_ms=60_000,
        )
        self.assertEqual(status, "sat")
        self.assertIsNotNone(witness)


if __name__ == "__main__":
    unittest.main()
