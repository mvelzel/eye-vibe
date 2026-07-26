import unittest

from eye_mystery.binary_initializer import (
    HIGH_HALF_STORE,
    LOW_HALF_STORE,
    expected_initializer_halves,
    matches_eye_initializer,
    stack_immediates,
)


def compiled_fixture(words: tuple[int, ...]) -> bytes:
    result = bytearray()
    for word in words:
        result.extend(LOW_HALF_STORE)
        result.extend((word & 0xFFFFFFFF).to_bytes(4, "little"))
        result.extend(b"\x90")
        high = word >> 32
        if high:
            result.extend(HIGH_HALF_STORE)
            result.extend(high.to_bytes(4, "little"))
        result.extend(b"\x90")
    return bytes(result)


class BinaryInitializerTests(unittest.TestCase):
    def test_planted_initializer_is_recovered(self) -> None:
        words = (0x1122334455667788, 0x00000000AABBCCDD, 0xFFEEDDCCBBAA0099)
        code = compiled_fixture(words)
        lows, highs = expected_initializer_halves(words)
        self.assertEqual(stack_immediates(code, LOW_HALF_STORE), lows)
        self.assertEqual(stack_immediates(code, HIGH_HALF_STORE), highs)
        self.assertTrue(matches_eye_initializer(code, words))

    def test_one_changed_half_rejects_the_plant(self) -> None:
        words = (0x1122334455667788, 0xFFEEDDCCBBAA0099)
        code = bytearray(compiled_fixture(words))
        code[3] ^= 1
        self.assertFalse(matches_eye_initializer(bytes(code), words))

    def test_prefix_length_is_checked(self) -> None:
        with self.assertRaises(ValueError):
            stack_immediates(b"", b"\xc7")


if __name__ == "__main__":
    unittest.main()
