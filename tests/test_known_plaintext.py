import unittest

from eye_mystery.known_plaintext import first_isomorphism_conflict


class KnownPlaintextTests(unittest.TestCase):
    def test_finds_key_independent_pattern_conflict(self) -> None:
        conflict = first_isomorphism_conflict(
            {"one": "thex", "two": "thez"},
            {"one": (1, 2, 1, 3), "two": (4, 5, 6, 7)},
            min_length=3,
        )
        self.assertIsNotNone(conflict)
        assert conflict is not None
        self.assertEqual("".join(conflict.plaintext), "the")
        self.assertEqual(
            {item.ciphertext_pattern for item in conflict.occurrences},
            {"A.A", "..."},
        )

    def test_accepts_consistent_relabelled_patterns(self) -> None:
        conflict = first_isomorphism_conflict(
            {"one": "the", "two": "the"},
            {"one": (1, 2, 1), "two": (4, 5, 4)},
        )
        self.assertIsNone(conflict)

    def test_rejects_length_mismatch(self) -> None:
        with self.assertRaises(ValueError):
            first_isomorphism_conflict(
                {"one": "abc"}, {"one": (1, 2)}
            )


if __name__ == "__main__":
    unittest.main()
