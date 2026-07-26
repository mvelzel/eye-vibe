import random
import unittest

from eye_mystery.practice_cipher3_arbitrary_two_sheet import (
    decode_streams,
    encode_streams,
    event_accuracy,
    random_key,
    validate_key,
)


class PracticeCipher3ArbitraryTwoSheetTests(unittest.TestCase):
    def test_random_key_has_exact_two_sheet_capacities(self) -> None:
        key = random_key(random.Random(7))
        validate_key(key)
        multiplicities = sorted(key.count(value) for value in set(key))
        self.assertEqual(multiplicities, [1] + [2] * 41)

    def test_balanced_encoding_round_trips(self) -> None:
        key = random_key(random.Random(11))
        plaintexts = (
            tuple(range(42)),
            tuple(reversed(range(42))),
            (0, 0, 1, 1, 41, 41),
        )
        ciphertexts = encode_streams(plaintexts, key, seed=13)
        decoded = decode_streams(ciphertexts, key)
        self.assertEqual(decoded, plaintexts)
        self.assertEqual(event_accuracy(decoded, plaintexts), 1.0)

    def test_invalid_capacity_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_key(tuple(range(42)) + tuple(range(40)) + (0,))


if __name__ == "__main__":
    unittest.main()
