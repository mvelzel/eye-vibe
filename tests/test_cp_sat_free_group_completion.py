from __future__ import annotations

import random
import unittest

try:
    import ortools  # noqa: F401
except ImportError:
    ortools = None

from eye_mystery.arbitrary_gak_sat import encrypt_messages
from eye_mystery.cp_sat_free_group_completion import (
    recover_cp_sat_free_group_completion,
)


@unittest.skipIf(ortools is None, "OR-Tools is optional")
class CPSATFreeGroupCompletionTests(unittest.TestCase):
    def test_recovers_fixed_random_fixture(self) -> None:
        rng = random.Random(31072026)
        deck_size = 7
        action_count = 3
        operations = []
        for _ in range(action_count):
            operation = list(range(deck_size))
            rng.shuffle(operation)
            operations.append(tuple(operation))
        plaintexts = (
            (0, 1, 2, 1, 0, 2, 2, 1),
            (2, 0, 1, 1, 2, 0, 2, 1),
        )
        decks = []
        for _ in plaintexts:
            deck = list(range(deck_size))
            rng.shuffle(deck)
            decks.append(tuple(deck))
        ciphertexts = tuple(
            encrypt_messages((plaintext,), deck, operations)[0]
            for plaintext, deck in zip(plaintexts, decks, strict=True)
        )

        status, witness = recover_cp_sat_free_group_completion(
            plaintexts,
            ciphertexts,
            deck_size=deck_size,
            plaintext_alphabet_size=action_count,
            timeout_seconds=10,
            num_workers=2,
        )

        self.assertEqual(status, "sat")
        self.assertIsNotNone(witness)

    def test_rejects_impossible_repeated_action_orbit(self) -> None:
        status, witness = recover_cp_sat_free_group_completion(
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
