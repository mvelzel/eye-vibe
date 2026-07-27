from __future__ import annotations

import importlib.util
import random
import unittest

from eye_mystery.sparse_xgak_sat import (
    XGAKWitness,
    check_specific_xgak_next_card,
    encrypt_xgak_messages,
    recover_sparse_xgak_witness,
)


@unittest.skipUnless(importlib.util.find_spec("z3"), "z3-solver is optional")
class SparseXGAKSolverTests(unittest.TestCase):
    def test_recovers_distinct_selectors_and_replays_exactly(self) -> None:
        rng = random.Random(270727)
        size = 8
        operations = []
        for _ in range(3):
            operation = list(range(size))
            rng.shuffle(operation)
            operations.append(tuple(operation))
        planted = XGAKWitness(tuple(operations), (1, 4, 6))
        plaintexts = ((0, 1, 2, 0, 2, 1, 0, 1, 2, 2, 0, 1),)
        ciphertexts = encrypt_xgak_messages(plaintexts, planted)

        status, witness = recover_sparse_xgak_witness(
            plaintexts,
            ciphertexts,
            deck_size=size,
            plaintext_alphabet_size=3,
            distinct_output_positions=True,
            timeout_ms=30_000,
        )
        self.assertEqual(status, "sat")
        self.assertIsNotNone(witness)
        assert witness is not None
        self.assertEqual(
            encrypt_xgak_messages(plaintexts, witness),
            ciphertexts,
        )
        self.assertEqual(len(set(witness.output_positions)), 3)

    def test_frozen_alternative_can_exhibit_non_forcing(self) -> None:
        plaintext = (0, 1, 2, 0, 2, 1, 0, 1)
        planted = XGAKWitness(
            (
                (1, 2, 3, 4, 5, 0),
                (2, 0, 4, 1, 5, 3),
                (5, 4, 3, 2, 1, 0),
            ),
            (0, 2, 4),
        )
        ciphertext = encrypt_xgak_messages((plaintext,), planted)[0]
        actual = ciphertext[5]
        alternative = (actual + 1) % 6
        result = check_specific_xgak_next_card(
            plaintext[:5],
            ciphertext[:5],
            plaintext[5],
            actual,
            alternative,
            deck_size=6,
            plaintext_alphabet_size=3,
            distinct_output_positions=True,
            timeout_ms=30_000,
        )
        self.assertEqual(result.actual_status, "sat")
        self.assertEqual(result.alternative_status, "sat")
        self.assertTrue(result.non_forcing)


if __name__ == "__main__":
    unittest.main()
