import unittest

from eye_mystery.binary_initializer import (
    HIGH_HALF_STORE,
    LOW_HALF_STORE,
    audit_eye_callsite,
    expected_initializer_halves,
    matches_eye_initializer,
    relative_call_sites,
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

    def test_relative_call_target_is_resolved(self) -> None:
        code_va = 0x1000
        target_va = 0x1800
        call_offset = 0x40
        code = bytearray(b"\x90" * 0x100)
        displacement = target_va - (code_va + call_offset + 5)
        code[call_offset] = 0xE8
        code[call_offset + 1 : call_offset + 5] = displacement.to_bytes(
            4,
            "little",
            signed=True,
        )
        self.assertEqual(
            relative_call_sites(bytes(code), code_va, target_va),
            (code_va + call_offset,),
        )

    def test_planted_caller_interface_is_recovered(self) -> None:
        text_va = 0x1000
        initializer_va = 0x1800
        call = 0x1C00
        text = bytearray(b"\x90" * 0x1000)

        def plant(address: int, value: bytes) -> None:
            offset = address - text_va
            text[offset : offset + len(value)] = value

        displacement = initializer_va - (call + 5)
        plant(call, b"\xe8" + displacement.to_bytes(4, "little", signed=True))
        plant(
            initializer_va + 0x2B,
            b"\x89\x55\x9c\x89\x4d\x98",
        )
        plant(
            initializer_va + 0x46,
            b"\x8b\x45\x08\xc7\x45\xfc\x00\x00\x00\x00\x85\xc0",
        )
        plant(call - 0x1CB, b"\x89\x45\xec")
        plant(call - 0x9E, b"\x40\x89\x45\xec\x83\xf8\x09")
        plant(call - 0x74, b"\xff\x75\xec")
        plant(call - 0x281, b"\x8b\xd9\x89\x5d\xe4")
        plant(
            call - 0x1C8,
            bytes.fromhex(
                "83 e0 01 75 09 83 fb ff 0f 84 11 01 00 00 "
                "83 f8 01 75 08 3b d8 0f 84 04 01 00 00"
            ),
        )
        plant(call - 0x18, b"\xf3\x0f\x2c\xd3")
        plant(call - 0x04, b"\xf3\x0f\x2c\xca")

        audit = audit_eye_callsite(bytes(text), text_va, initializer_va)
        self.assertEqual(audit.callsite_va, call)
        self.assertTrue(audit.exact_interface)


if __name__ == "__main__":
    unittest.main()
