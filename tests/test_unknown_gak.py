import unittest

from eye_mystery.unknown_gak import (
    arbitrary_length_no_double_witness,
    minimum_operation_alphabet,
    recover_unknown_plaintext_bruteforce,
    replay_unknown_gak,
    top_changing_operation_count,
    top_changing_operation_set_count,
)


def cards(text: str) -> tuple[int, ...]:
    return tuple(ord(symbol) - ord("A") for symbol in text)


class UnknownGAKTests(unittest.TestCase):
    def test_replays_from_identity_reset_deck(self) -> None:
        operations = ((1, 2, 3, 0), (3, 1, 0, 2))
        plaintext = (0, 0, 1, 0, 1, 0, 0, 0)
        self.assertEqual(
            replay_unknown_gak(plaintext, operations, deck_size=4),
            cards("BCBDBCDA"),
        )

    def test_reproduces_community_orphan_pair(self) -> None:
        parent = recover_unknown_plaintext_bruteforce(
            cards("BCBDBCDA"),
            deck_size=4,
            operation_alphabet_size=2,
        )
        orphan = recover_unknown_plaintext_bruteforce(
            cards("BCBDBCDAC"),
            deck_size=4,
            operation_alphabet_size=2,
        )
        self.assertEqual(parent.status, "sat")
        self.assertIsNotNone(parent.witness)
        self.assertEqual(orphan.status, "unsat")
        self.assertEqual(
            orphan.operation_sets_checked,
            orphan.total_operation_sets,
        )
        self.assertEqual(orphan.total_operation_sets, 108)

    def test_truncated_enumeration_is_unknown_not_unsat(self) -> None:
        result = recover_unknown_plaintext_bruteforce(
            cards("BCBDBCDAC"),
            deck_size=4,
            operation_alphabet_size=2,
            max_operation_sets=10,
        )
        self.assertEqual(result.status, "unknown")
        self.assertEqual(result.operation_sets_checked, 10)

    def test_minimum_operation_alphabet(self) -> None:
        minimum, results = minimum_operation_alphabet(
            cards("BCBDBCDA"),
            deck_size=4,
            maximum=2,
        )
        self.assertEqual(minimum, 2)
        self.assertEqual(tuple(result.status for result in results), ("unsat", "sat"))

    def test_validates_inputs(self) -> None:
        with self.assertRaises(ValueError):
            recover_unknown_plaintext_bruteforce(
                (4,),
                deck_size=4,
                operation_alphabet_size=2,
            )

    def test_no_double_has_no_finite_capacity_bound(self) -> None:
        ciphertext, witness = arbitrary_length_no_double_witness(
            1_028,
            deck_size=83,
        )
        self.assertEqual(len(ciphertext), 1_028)
        self.assertFalse(
            any(left == right for left, right in zip(ciphertext, ciphertext[1:]))
        )
        self.assertEqual(len(witness.operations), 1)

    def test_top_changing_operation_count(self) -> None:
        self.assertEqual(top_changing_operation_count(4), 18)
        self.assertEqual(top_changing_operation_count(5), 96)
        self.assertEqual(top_changing_operation_set_count(4, 2), 108)
        self.assertEqual(top_changing_operation_set_count(5, 2), 3_456)

    def test_unique_top_count_without_top_change(self) -> None:
        result = recover_unknown_plaintext_bruteforce(
            (0,),
            deck_size=3,
            operation_alphabet_size=2,
            require_top_change=False,
        )
        self.assertEqual(result.total_operation_sets, 12)


if __name__ == "__main__":
    unittest.main()
