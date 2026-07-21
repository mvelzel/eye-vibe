from __future__ import annotations

import importlib.util
import random
import unittest

from eye_mystery.arbitrary_gak_sat import (
    apply_operation,
    encrypt_messages,
    recover_known_plaintext_witness,
)


class ArbitraryGAKCoreTests(unittest.TestCase):
    def test_apply_operation_uses_right_action_convention(self) -> None:
        self.assertEqual(apply_operation((10, 11, 12), (2, 0, 1)), (12, 10, 11))

    def test_messages_reset_to_the_same_deck(self) -> None:
        initial = (0, 1, 2, 3)
        operations = ((1, 2, 3, 0), (3, 0, 1, 2))
        plaintexts = ((0, 1, 0), (0, 1, 0))
        first, second = encrypt_messages(plaintexts, initial, operations)
        self.assertEqual(first, second)


@unittest.skipUnless(importlib.util.find_spec("z3"), "z3-solver is optional")
class ArbitraryGAKSolverTests(unittest.TestCase):
    def test_recovers_an_exact_toy_witness(self) -> None:
        rng = random.Random(260721)
        size = 5
        initial = tuple(range(size))
        operations = []
        for _ in range(2):
            operation = list(range(size))
            rng.shuffle(operation)
            operations.append(tuple(operation))
        plaintexts = tuple(
            tuple(rng.randrange(2) for _ in range(14)) for _ in range(3)
        )
        ciphertexts = encrypt_messages(plaintexts, initial, operations)
        status, witness = recover_known_plaintext_witness(
            plaintexts,
            ciphertexts,
            deck_size=size,
            plaintext_alphabet_size=2,
            initial_top_card=0,
            timeout_ms=30_000,
        )
        self.assertEqual(status, "sat")
        self.assertIsNotNone(witness)
        assert witness is not None
        self.assertEqual(
            encrypt_messages(plaintexts, witness.initial_deck, witness.operations),
            ciphertexts,
        )


if __name__ == "__main__":
    unittest.main()
