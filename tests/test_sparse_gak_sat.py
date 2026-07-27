from __future__ import annotations

import importlib.util
import random
import unittest

from eye_mystery.arbitrary_gak_sat import encrypt_messages
from eye_mystery.sparse_gak_sat import (
    canonical_initial_deck,
    check_next_card_forcing,
    encode_text,
    find_sparse_unsat_core,
    recover_sparse_known_plaintext_witness,
)


class SparseGAKCoreTests(unittest.TestCase):
    def test_canonical_deck_and_literal_text_encoding(self) -> None:
        self.assertEqual(canonical_initial_deck(5, 2), (2, 0, 1, 3, 4))
        encoded, alphabet = encode_text("ABACA")
        self.assertEqual(alphabet, ("A", "B", "C"))
        self.assertEqual(encoded, (0, 1, 0, 2, 0))


@unittest.skipUnless(importlib.util.find_spec("z3"), "z3-solver is optional")
class SparseGAKSolverTests(unittest.TestCase):
    def test_recovers_symbolic_top_and_replays_exactly(self) -> None:
        rng = random.Random(270727)
        size = 7
        initial = canonical_initial_deck(size, 4)
        operations = []
        for _ in range(3):
            operation = list(range(size))
            rng.shuffle(operation)
            operations.append(tuple(operation))
        plaintexts = ((0, 1, 2, 0, 2, 1, 0, 1, 2, 2, 0, 1),)
        ciphertexts = encrypt_messages(plaintexts, initial, operations)

        status, witness = recover_sparse_known_plaintext_witness(
            plaintexts,
            ciphertexts,
            deck_size=size,
            plaintext_alphabet_size=3,
            timeout_ms=30_000,
        )
        self.assertEqual(status, "sat")
        self.assertIsNotNone(witness)
        assert witness is not None
        self.assertEqual(
            encrypt_messages(plaintexts, witness.initial_deck, witness.operations),
            ciphertexts,
        )

    def test_heldout_check_can_exhibit_non_forcing(self) -> None:
        plaintext = (0, 1, 0, 1, 0, 1)
        initial = canonical_initial_deck(6, 3)
        operations = (
            (1, 2, 3, 4, 5, 0),
            (2, 0, 4, 1, 5, 3),
        )
        ciphertext = encrypt_messages((plaintext,), initial, operations)[0]
        result = check_next_card_forcing(
            plaintext[:3],
            ciphertext[:3],
            plaintext[3],
            ciphertext[3],
            deck_size=6,
            plaintext_alphabet_size=2,
            timeout_ms=30_000,
        )
        self.assertEqual(result.actual_status, "sat")
        self.assertEqual(result.alternative_status, "sat")
        self.assertIsNotNone(result.alternative_card)
        self.assertNotEqual(result.alternative_card, ciphertext[3])

    def test_unsat_core_reports_observation_locations(self) -> None:
        # Repeating one permutation cannot emit A,A,B: after the first repeat,
        # the emitted card is at a fixed point and must remain on top.
        result = find_sparse_unsat_core(
            ((0, 0, 0),),
            ((0, 0, 1),),
            deck_size=3,
            plaintext_alphabet_size=1,
            timeout_ms=30_000,
        )
        self.assertEqual(result.status, "unsat")
        self.assertEqual(set(result.observations), {(0, 0), (0, 1), (0, 2)})


if __name__ == "__main__":
    unittest.main()
