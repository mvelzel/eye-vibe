from __future__ import annotations

import unittest

try:
    import ortools  # noqa: F401
except ImportError:
    ortools = None

from eye_mystery.arbitrary_gak_sat import encrypt_messages
from eye_mystery.cp_sat_gak import recover_cp_sat_gak


@unittest.skipIf(ortools is None, "OR-Tools is optional")
class CPSATGAKTests(unittest.TestCase):
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

        status, witness = recover_cp_sat_gak(
            patterns,
            ciphertexts,
            deck_size=5,
            plaintext_alphabet_size=3,
            timeout_seconds=10,
            num_workers=2,
        )

        self.assertEqual(status, "sat")
        self.assertIsNotNone(witness)

    def test_rejects_impossible_repeated_action_orbit(self) -> None:
        status, witness = recover_cp_sat_gak(
            ((0, 0, 0),),
            ((0, 1, 1),),
            deck_size=3,
            plaintext_alphabet_size=1,
            timeout_seconds=10,
            num_workers=2,
        )
        self.assertEqual(status, "unsat")
        self.assertIsNone(witness)


if __name__ == "__main__":
    unittest.main()
