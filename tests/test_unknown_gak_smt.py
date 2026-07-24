import shutil
import unittest

from eye_mystery.unknown_gak import recover_unknown_plaintext_bruteforce
from eye_mystery.unknown_gak_smt import (
    build_unknown_gak_messages_smt2,
    build_unknown_gak_smt2,
    solve_unknown_gak_messages_with_z3,
    solve_unknown_gak_with_z3,
)


def cards(text: str) -> tuple[int, ...]:
    return tuple(ord(symbol) - ord("A") for symbol in text)


class UnknownGAKSMTEncodingTests(unittest.TestCase):
    def test_formula_contains_ordinary_gak_constraints(self) -> None:
        formula = build_unknown_gak_smt2(
            cards("BCB"),
            deck_size=4,
            operation_alphabet_size=2,
        )
        self.assertIn("(assert (not (= p_0_0 0)))", formula)
        self.assertIn("(assert (distinct p_0_0 p_1_0))", formula)
        self.assertIn("(assert (< p_0_0 p_1_0))", formula)
        self.assertIn("(assert (= s_2_0 1))", formula)

    def test_formula_validates_inputs(self) -> None:
        with self.assertRaises(ValueError):
            build_unknown_gak_smt2(
                (0,),
                deck_size=4,
                operation_alphabet_size=4,
            )

    def test_multi_message_formula_shares_operations_and_resets_states(self) -> None:
        formula = build_unknown_gak_messages_smt2(
            ((1, 2), (2, 1)),
            deck_size=4,
            operation_alphabet_size=2,
        )
        self.assertEqual(
            formula.count("(declare-fun p_0 (Int) Int)"),
            1,
        )
        self.assertIn("(assert (= e_0_0_0", formula)
        self.assertIn("(assert (= e_1_0_0", formula)
        self.assertIn("(assert (= (p_0 0) 1))", formula)
        self.assertIn("(assert (= (p_1 0) 2))", formula)
        self.assertIn("(assert (= q_0_0 0))", formula)
        self.assertIn("(assert (= q_1_0 1))", formula)


@unittest.skipUnless(shutil.which("z3"), "z3 command-line solver is optional")
class UnknownGAKSMTSolverTests(unittest.TestCase):
    def test_matches_complete_enumerator_on_parent_and_orphan(self) -> None:
        for ciphertext in (cards("BCBDBCDA"), cards("BCBDBCDAC")):
            enumerated = recover_unknown_plaintext_bruteforce(
                ciphertext,
                deck_size=4,
                operation_alphabet_size=2,
            )
            symbolic = solve_unknown_gak_with_z3(
                ciphertext,
                deck_size=4,
                operation_alphabet_size=2,
                timeout_ms=5_000,
            )
            self.assertEqual(symbolic.status, enumerated.status)
            self.assertEqual(symbolic.witness is not None, symbolic.status == "sat")

    def test_recovers_shared_operations_across_reset_messages(self) -> None:
        operations = ((1, 2, 3, 0), (3, 1, 0, 2))
        from eye_mystery.unknown_gak import replay_unknown_gak

        plaintexts = ((0, 0, 1, 0), (1, 0, 1, 1))
        ciphertexts = tuple(
            replay_unknown_gak(plaintext, operations, deck_size=4)
            for plaintext in plaintexts
        )
        result = solve_unknown_gak_messages_with_z3(
            ciphertexts,
            deck_size=4,
            operation_alphabet_size=2,
            timeout_ms=5_000,
        )
        self.assertEqual(result.status, "sat")
        self.assertIsNotNone(result.witness)

    def test_lazy_multi_message_encoding_preserves_parent_orphan_decision(
        self,
    ) -> None:
        for ciphertext, expected in (
            (cards("BCBDBCDA"), "sat"),
            (cards("BCBDBCDAC"), "unsat"),
        ):
            result = solve_unknown_gak_messages_with_z3(
                (ciphertext,),
                deck_size=4,
                operation_alphabet_size=2,
                timeout_ms=5_000,
            )
            self.assertEqual(result.status, expected)
            self.assertEqual(result.witness is not None, expected == "sat")


if __name__ == "__main__":
    unittest.main()
