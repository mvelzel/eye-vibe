from __future__ import annotations

import random
import unittest

from eye_mystery.arbitrary_gak_sat import encrypt_messages
from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.free_group_gak import (
    _fold_words,
    _walk,
    audit_free_group_gak,
    construct_free_group_gak_witness,
    recover_fixed_schedule_gak_with_z3,
)
from eye_mystery.sparse_gak_sat import encode_text
from scripts.check_waite_m3_suffix import EAST2_RAW_OFFSET, WAITE_M3_SUFFIX
from scripts.classify_that_which_windows import WINDOWS

try:
    import z3  # noqa: F401
except ImportError:
    z3 = None


class FreeGroupGAKTests(unittest.TestCase):
    def test_stallings_fold_closes_generated_subgroup(self) -> None:
        _, rows = _fold_words(((1, 1), (1, 1, 1)))
        transitions = {
            (source, letter): target for source, letter, target in rows
        }
        self.assertEqual(_walk(transitions, (1,)), 0)

    def test_rejects_impossible_repeated_action_orbit(self) -> None:
        audit = audit_free_group_gak(((0, 0, 0),), ((0, 1, 1),))
        self.assertTrue(audit.forced_nonfix_words)

    def test_rejects_waite_suffix_and_accepts_local_that_which(self) -> None:
        waite, _ = encode_text(WAITE_M3_SUFFIX)
        waite_audit = audit_free_group_gak(
            (waite,),
            (trigram_values(MESSAGES["east2"])[EAST2_RAW_OFFSET:],),
        )
        self.assertTrue(waite_audit.forced_nonfix_words)

        phrase, _ = encode_text("THAT WHICH")
        ciphertexts = tuple(
            trigram_values(MESSAGES[window.message])[
                window.offset : window.offset + len(phrase)
            ]
            for window in WINDOWS
        )
        phrase_audit = audit_free_group_gak(
            (phrase,) * len(ciphertexts),
            ciphertexts,
        )
        self.assertFalse(phrase_audit.forced_nonfix_words)

    def test_constructs_and_replays_valid_random_fixture(self) -> None:
        rng = random.Random(27072026)
        deck_size = 17
        operation_count = 4
        operations = []
        for _ in range(operation_count):
            operation = list(range(deck_size))
            rng.shuffle(operation)
            operations.append(tuple(operation))
        plaintexts = tuple(
            tuple(rng.randrange(operation_count) for _ in range(length))
            for length in (18, 20, 23)
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

        audit, witness = construct_free_group_gak_witness(
            plaintexts,
            ciphertexts,
            deck_size=83,
            plaintext_alphabet_size=operation_count,
            completion_trials=2_000,
            seed=27072026,
        )
        self.assertFalse(audit.forced_nonfix_words)
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

    @unittest.skipIf(z3 is None, "z3-solver is optional")
    def test_origin_solver_recovers_valid_fixed_schedules(self) -> None:
        plaintexts = ((0, 1, 0, 1), (1, 0, 1, 1))
        operations = (
            (1, 2, 3, 0),
            (2, 0, 3, 1),
        )
        decks = ((0, 1, 2, 3), (3, 1, 0, 2))
        ciphertexts = tuple(
            encrypt_messages((plaintext,), deck, operations)[0]
            for plaintext, deck in zip(plaintexts, decks, strict=True)
        )
        status, witness = recover_fixed_schedule_gak_with_z3(
            plaintexts,
            ciphertexts,
            deck_size=4,
            plaintext_alphabet_size=2,
            timeout_ms=10_000,
        )
        self.assertEqual(status, "sat")
        self.assertIsNotNone(witness)


if __name__ == "__main__":
    unittest.main()
