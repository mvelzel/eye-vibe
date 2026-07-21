import unittest

from eye_mystery.cipher_clock import (
    AKI_DISK_INPUT_RING,
    affine_output_positions,
    reciprocal_digram_witnesses,
    reciprocal_plaintext_ring_lower_bound,
    wadsworth_decode,
)
from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values


class CipherClockTests(unittest.TestCase):
    def test_finds_reciprocal_digrams(self) -> None:
        messages = {"one": (3, 7, 4), "two": (7, 3, 9)}
        witnesses = reciprocal_digram_witnesses(messages)
        self.assertEqual(len(witnesses), 1)
        self.assertEqual((witnesses[0].first, witnesses[0].second), (3, 7))
        self.assertEqual(
            reciprocal_plaintext_ring_lower_bound(messages, 11), 6
        )

    def test_no_reciprocal_digram_has_trivial_bound(self) -> None:
        self.assertEqual(
            reciprocal_plaintext_ring_lower_bound({"one": (1, 2, 3)}, 83),
            1,
        )

    def test_eye_bodies_exclude_a_finnish_wadsworth_ring(self) -> None:
        bodies = {
            name: trigram_values(MESSAGES[name])[1:]
            for name in MESSAGE_ORDER
        }
        witnesses = reciprocal_digram_witnesses(bodies)
        self.assertEqual(len(witnesses), 59)
        self.assertEqual(
            (witnesses[0].first, witnesses[0].second), (0, 37)
        )
        self.assertEqual(
            reciprocal_plaintext_ring_lower_bound(bodies, 83), 42
        )

    def test_next_occurrence_cipher_clock_semantics(self) -> None:
        positions = affine_output_positions(5, 1, 0)
        self.assertEqual(
            wadsworth_decode((0, 1, 1, 4), "abcdef", positions),
            "fafc",
        )
        self.assertEqual(len(AKI_DISK_INPUT_RING), 114)
        self.assertEqual(len(set(AKI_DISK_INPUT_RING)), 37)

    def test_affine_output_order_must_be_a_permutation(self) -> None:
        with self.assertRaises(ValueError):
            affine_output_positions(6, 2, 0)


if __name__ == "__main__":
    unittest.main()
