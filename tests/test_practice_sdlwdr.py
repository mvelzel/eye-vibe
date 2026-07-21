import hashlib
import json
import unittest
from pathlib import Path

from eye_mystery.practice_sdlwdr import (
    COMBINED82,
    PLAINTEXT_ALPHABET,
    PLAINTEXT_WHEEL,
    decode_puzzle1_sections,
    decode_puzzle2_sections,
)


ROOT = Path(__file__).resolve().parents[1]


class PracticeSdlwdrTests(unittest.TestCase):
    def test_recovered_wheels_are_complete(self) -> None:
        self.assertEqual(len(COMBINED82), 82)
        self.assertEqual(len(set(COMBINED82)), 82)
        self.assertEqual(len(PLAINTEXT_ALPHABET), 42)
        self.assertEqual(set(PLAINTEXT_WHEEL), set(PLAINTEXT_ALPHABET))

    def test_cipher1_decodes_confirmed_source(self) -> None:
        messages = json.loads(
            (ROOT / "artifacts/practice-sdlwdr/cipher1.json").read_text()
        )
        plaintexts = decode_puzzle1_sections(messages)
        self.assertEqual(
            tuple(map(len, plaintexts)),
            tuple(len(message) - 1 for message in messages),
        )
        self.assertTrue(
            plaintexts[0].startswith("WAINAMOINEN OLD AND TRUTHFUL")
        )
        self.assertIn("ON THE SEA’S SMOOTH PLAIN", plaintexts[0])
        self.assertTrue(
            plaintexts[-1].endswith("LISTEN TO MY WONDROUS SINGING")
        )

    def test_cipher1_plaintext_fingerprints(self) -> None:
        messages = json.loads(
            (ROOT / "artifacts/practice-sdlwdr/cipher1.json").read_text()
        )
        observed = tuple(
            hashlib.sha256(text.encode()).hexdigest()
            for text in decode_puzzle1_sections(messages)
        )
        expected = (
            "0442bd0da97cc29cdb3c60b8f3fada0659b9a583e748a6620f85161410b8ecb3",
            "11b73724879dfb5620d8dc76a5d879f95bba80211a3e7ee968bfd60236b4855c",
            "81221396f2e82e072f729fd725258e133557926139fb5af44ac760851396f275",
            "6f6815c511621dd87333b64fd6d1d9f2875478bb4e61338eb35790b9c8a34e86",
            "c77136e5d843c7321e9aca4d09bbc2cdc69558a6a1095712109e1411eab8b415",
            "f66a1e3954fa241135f4bbc3cdf5c6cde7da49eb8c8db76d4d269972d221ffb8",
            "abd58bf773946a92c64236e0b430d191fdacf6326565ca3a30b4bb1e50469776",
            "5fdd7122baabd6b8dcba4048cabed2e83daa6ea46c6bae7f0309add60ebf180e",
            "ded5975dba310e1a8b8822bc82fb010d4d645140a7b29f677b08b7265d37cde6",
            "286629742c81d1a755d9ba394e1143f0f0e012442d2999e698fedbeca9966fa8",
            "ffb0d5dd447c4c9c5b76f9a5d3170396e0c6d85c6aae71ce69c1bb280b6610aa",
            "3b348e0fe060f2f99e89b0cc0e15d384a5e581a1eb0a0ab85a42a9783b9eb004",
            "ac6e4935dbabdd5ae495fc4bcfd1d2c312f1a02f40fe267666fce126f9250e26",
            "413d5eda1df8a320ebcf3dde45bcdf94aa25c413b224d68c4394f608708bf034",
            "065a2e8a1751342448b9fbd2d179f897efccf739438e7f2a8e34fcad6086fefd",
            "fa14a70cde5af455fcba48d126041de35984b6f8a0da6f006d84ba8bec4e61d4",
            "4922b4f1b7c39a667aa8c45e5de154c6a690804d73a01d483fee04247089c101",
        )
        self.assertEqual(observed, expected)

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
