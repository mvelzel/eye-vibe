from __future__ import annotations

import unittest

try:
    import z3  # noqa: F401
except ImportError:
    z3 = None

from eye_mystery.arbitrary_gak_sat import encrypt_messages
from eye_mystery.partially_known_arbitrary_state_gak import (
    recover_partially_known_arbitrary_state_gak,
)


@unittest.skipIf(z3 is None, "z3-solver is optional")
class PartiallyKnownArbitraryStateGAKTests(unittest.TestCase):
    def test_01_recovers_small_partially_known_plant(self) -> None:
        deck_size = 5
        operation_count = 2
        operations = (
            (1, 2, 3, 4, 0),
            (2, 0, 4, 1, 3),
        )
        decks = (
            (0, 1, 2, 3, 4),
            (4, 2, 0, 3, 1),
        )
        schedules = (
            (0, 1, 0, 1, 1),
            (1, 0, 1, 0, 0),
        )
        patterns = (
            (0, None, 0, None, None),
            (1, None, 1, None, None),
        )
        ciphertexts = tuple(
            encrypt_messages((schedule,), deck, operations)[0]
            for schedule, deck in zip(schedules, decks, strict=True)
        )

        status, witness = recover_partially_known_arbitrary_state_gak(
            patterns,
            ciphertexts,
            deck_size=deck_size,
            plaintext_alphabet_size=operation_count,
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
                    witness.plaintexts, witness.initial_decks, strict=True
                )
            ),
            ciphertexts,
        )
        for pattern, plaintext in zip(patterns, witness.plaintexts, strict=True):
            self.assertTrue(
                all(
                    pinned is None or pinned == recovered
                    for pinned, recovered in zip(pattern, plaintext, strict=True)
                )
            )

    def test_02_rejects_impossible_repeated_action_orbit(self) -> None:
        status, witness = recover_partially_known_arbitrary_state_gak(
            ((0, 0, 0),),
            ((0, 1, 1),),
            deck_size=3,
            plaintext_alphabet_size=1,
            timeout_ms=10_000,
        )
        self.assertEqual(status, "unsat")
        self.assertIsNone(witness)

    def test_validates_inputs(self) -> None:
        with self.assertRaises(ValueError):
            recover_partially_known_arbitrary_state_gak(
                ((1,),),
                ((0,),),
                deck_size=3,
                plaintext_alphabet_size=1,
            )


if __name__ == "__main__":
    unittest.main()
