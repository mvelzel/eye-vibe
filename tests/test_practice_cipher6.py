from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

from eye_mystery.practice_cipher6 import (
    ALTAR_LETTERS,
    EXPECTED_PREFIXES,
    TRAILER_PHRASE,
    asset_tape,
    asset_tape_base_audit,
    asset_tape_base_permutations,
    candidate_decks,
    circle_base_permutation_audit,
    circle_base_permutations,
    keyed_deck,
    paired_deck_audit,
    read_ciphertext,
    stable_partition_permutation,
)


ROOT = Path(__file__).resolve().parents[1]
CIPHERTEXT = ROOT / "artifacts/practice-sdlwdr/cipher6-revised.txt"


class PracticeCipher6Tests(unittest.TestCase):
    def test_exact_revised_attachment_and_observables(self) -> None:
        raw = CIPHERTEXT.read_bytes()
        self.assertEqual(
            hashlib.sha256(raw).hexdigest(),
            "0b5e0a73e1cb8efc6090fa893fc4604195d2d85e884bfe2d39f35952974654c2",
        )
        lines = read_ciphertext(CIPHERTEXT)
        self.assertEqual(tuple(map(len, lines)), (57, 53, 77, 99, 108, 72, 111, 110, 74))
        self.assertEqual(tuple(line[0] for line in lines), EXPECTED_PREFIXES)
        self.assertEqual(set(value for line in lines for value in line), set(range(83)))

    def test_source_fixed_decks_are_permutations(self) -> None:
        decks = candidate_decks()
        self.assertEqual(len(decks), 9)
        for deck in decks.values():
            self.assertEqual(set(deck), set(range(83)))
        self.assertEqual(keyed_deck(ALTAR_LETTERS)[:26], tuple(ord(c) - 65 for c in ALTAR_LETTERS))

    def test_frozen_audit_size_and_prefix_oracle(self) -> None:
        results = paired_deck_audit(read_ciphertext(CIPHERTEXT))
        self.assertEqual(len(results), 9 * 9 * 6)
        self.assertEqual(results[0].total, 761)
        self.assertTrue(any(result.prefix_matches == 9 for result in results))

    def test_circle_base_permutations_are_valid_and_deduplicated(self) -> None:
        bases = circle_base_permutations()
        self.assertEqual(len(bases), len(set(bases.values())))
        for permutation in bases.values():
            self.assertEqual(set(permutation), set(range(83)))
        irregular = stable_partition_permutation(
            "11110111011101110", reverse=False, ones_first=True
        )
        self.assertEqual(irregular[:4], (0, 1, 2, 3))
        self.assertEqual(irregular[-4:], (67, 72, 76, 80))

    def test_circle_base_audit_keeps_numbered_prefixes(self) -> None:
        results = circle_base_permutation_audit(read_ciphertext(CIPHERTEXT))
        self.assertEqual(len(results), len(circle_base_permutations()) * 3)
        self.assertTrue(all(result.prefix_matches == 9 for result in results))
        self.assertTrue(all(result.total == 761 for result in results))

    def test_joint_asset_tape_and_permutations(self) -> None:
        self.assertEqual(len(TRAILER_PHRASE), 22)
        self.assertEqual(len(asset_tape(reverse_binary=False)), 83)
        self.assertEqual(len(asset_tape(reverse_binary=True)), 83)
        bases = asset_tape_base_permutations()
        self.assertEqual(len(bases), len(set(bases.values())))
        for permutation in bases.values():
            self.assertEqual(set(permutation), set(range(83)))

    def test_joint_asset_tape_audit_keeps_numbered_prefixes(self) -> None:
        results = asset_tape_base_audit(read_ciphertext(CIPHERTEXT))
        self.assertEqual(len(results), len(asset_tape_base_permutations()) * 3)
        self.assertTrue(all(result.prefix_matches == 9 for result in results))
        self.assertTrue(all(result.total == 761 for result in results))


if __name__ == "__main__":
    unittest.main()
