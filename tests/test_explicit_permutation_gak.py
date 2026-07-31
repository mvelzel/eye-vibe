from __future__ import annotations

import unittest

try:
    import z3  # noqa: F401
except ImportError:
    z3 = None

from eye_mystery.arbitrary_gak_sat import encrypt_messages
from eye_mystery.explicit_permutation_gak import (
    recover_explicit_permutation_gak,
)


@unittest.skipIf(z3 is None, "z3-solver is optional")
class ExplicitPermutationGAKTests(unittest.TestCase):
    def test_recovers_partially_known_plant(self) -> None:
        operations = (
            (1, 2, 3, 4, 0),
            (2, 0, 4, 1, 3),
            (4, 3, 2, 1, 0),
        )
        decks = (
            (0, 1, 2, 3, 4),
            (4, 2, 0, 3, 1),
        )
        plaintexts = (
            (0, 1, 0, 2, 1, 2),
            (1, 0, 1, 2, 0, 2),
        )
        patterns = (
            (0, None, 0, None, None, None),
            (1, None, 1, None, None, None),
        )
        ciphertexts = tuple(
            encrypt_messages((plaintext,), deck, operations)[0]
            for plaintext, deck in zip(plaintexts, decks, strict=True)
        )

        status, witness = recover_explicit_permutation_gak(
            patterns,
            ciphertexts,
            deck_size=5,
            plaintext_alphabet_size=3,
            pinned_action_count=2,
            timeout_ms=10_000,
        )

        self.assertEqual(status, "sat")
        self.assertIsNotNone(witness)
        assert witness is not None
        self.assertEqual(
            tuple(
                encrypt_messages(
                    (plaintext,), deck, witness.operations
                )[0]
                for plaintext, deck in zip(
                    witness.plaintexts,
                    witness.initial_decks,
                    strict=True,
                )
            ),
            ciphertexts,
        )

    def test_rejects_impossible_repeated_action_orbit(self) -> None:
        status, witness = recover_explicit_permutation_gak(
            ((0, 0, 0),),
            ((0, 1, 1),),
            deck_size=3,
            plaintext_alphabet_size=1,
            pinned_action_count=1,
            timeout_ms=10_000,
        )
        self.assertEqual(status, "unsat")
        self.assertIsNone(witness)

    def test_validates_inputs(self) -> None:
        with self.assertRaises(ValueError):
            recover_explicit_permutation_gak(
                ((1,),),
                ((0,),),
                deck_size=3,
                plaintext_alphabet_size=1,
            )


if __name__ == "__main__":
    unittest.main()
