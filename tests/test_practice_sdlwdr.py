import hashlib
import json
import unittest
from pathlib import Path

from eye_mystery.practice_sdlwdr import (
    COMBINED82,
    PLAINTEXT_ALPHABET,
    PLAINTEXT_WHEEL,
    decode_puzzle2_sections,
)


ROOT = Path(__file__).resolve().parents[1]


class PracticeSdlwdrTests(unittest.TestCase):
    def test_recovered_wheels_are_complete(self) -> None:
        self.assertEqual(len(COMBINED82), 82)
        self.assertEqual(len(set(COMBINED82)), 82)
        self.assertEqual(len(PLAINTEXT_ALPHABET), 42)
        self.assertEqual(set(PLAINTEXT_WHEEL), set(PLAINTEXT_ALPHABET))

    def test_cipher2_decodes_confirmed_source(self) -> None:
        messages = json.loads(
            (ROOT / "artifacts/practice-sdlwdr/cipher2.json").read_text()
        )
        plaintexts = decode_puzzle2_sections(messages)
        self.assertEqual(
            tuple(map(len, plaintexts)),
            tuple(len(message) - 1 for message in messages),
        )
        self.assertTrue(
            plaintexts[0].startswith("THUS HAS FIRE RETURNED TO NORTHLAND")
        )
        self.assertIn("WILL ASSUME A SECOND BODY", plaintexts[10])
        self.assertTrue(
            plaintexts[12].startswith("WAINAMOINEN OLD AND TRUTHFUL")
        )

    def test_cipher2_plaintext_fingerprints(self) -> None:
        messages = json.loads(
            (ROOT / "artifacts/practice-sdlwdr/cipher2.json").read_text()
        )
        observed = tuple(
            hashlib.sha256(text.encode()).hexdigest()
            for text in decode_puzzle2_sections(messages)
        )
        expected = (
            "39d36ef34525caffc0439ff98ae14bbde9c1e6d8e3774f9366aab1ebe25ec01c",
            "8629f72c57f308a596ea3122cf91b39a11bbea66bca3bcd34be2791a35f67d3b",
            "8b0c28e71dff5fa35d8fd783ed65ae4a15699d0da2b680cd0c36d87eb0bfcc27",
            "17ca9e1aad1f0fe0eb64a58b22a79c47249b94502f2fd2120a3653dd802fddd8",
            "7c0687ce925fec5c3f0e7dab68294257963f31a226f4225ffe8424d9fefab98d",
            "b3060fca1c563a5f45c6cef9c59d429bda895b9e048b69da41254a197a815513",
            "341a9f5e0f3f26466cb9d84dccc97dce6ee0686aba362dac31f6cda28da9897c",
            "b9e1286ac48317afe2d1dc623afead5a635dcb53d46775a937d1a48943992fe2",
            "45161df9166939ec921df0ed88e7e0f3492f78de5dd19a939ed6de05b71a19a7",
            "15fb6492e782264c24123b82b182ac86da93a7f7e431e1e070f749213982afb1",
            "35cc06cf8d9e03bc7d4f7015b04aba60557ae862bdad9b0682da0f80a06525e9",
            "8c2072f71f39c128dc379d1b53c0ff03de3aa756cea2b5fb2eeebe004a1984e9",
            "47a4616b2eec0362ddb9e90e3f62032f461891c1deb0a99b763547702afc0e03",
        )
        self.assertEqual(observed, expected)


if __name__ == "__main__":
    unittest.main()
