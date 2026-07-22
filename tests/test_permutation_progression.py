import unittest

from eye_mystery.permutation_progression import (
    CycleLayout,
    decode_progression,
    decoded_alphabet_size,
    encrypt_progression,
    inverse_permutation,
)


class PermutationProgressionTests(unittest.TestCase):
    def test_cycle_layout_uses_each_cycles_own_modulus(self) -> None:
        layout = CycleLayout((4, 1))
        self.assertEqual(layout.slot_metadata(), (
            (0, 0, 4),
            (0, 1, 4),
            (0, 2, 4),
            (0, 3, 4),
            (4, 0, 1),
        ))
        self.assertEqual(layout.decode_slot(1, 5), 0)
        self.assertEqual(layout.decode_slot(4, 99), 4)

    def test_inverse(self) -> None:
        permutation = (2, 0, 3, 1)
        inverse = inverse_permutation(permutation)
        self.assertEqual(inverse, (1, 3, 0, 2))

    def test_round_trip(self) -> None:
        permutation = (2, 0, 3, 1)
        plaintext = (0, 1, 1, 2, 3, 0, 2)
        ciphertext = encrypt_progression(plaintext, permutation)
        self.assertEqual(
            decode_progression(ciphertext, permutation), plaintext
        )
        self.assertEqual(decoded_alphabet_size((ciphertext,), permutation), 4)

    def test_skip_resets_position(self) -> None:
        permutation = (1, 2, 3, 0)
        plaintext = (3, 2, 1, 0)
        ciphertext = encrypt_progression(plaintext, permutation)
        with_marker = (2,) + ciphertext
        self.assertEqual(
            decode_progression(with_marker, permutation, skip=1), plaintext
        )


if __name__ == "__main__":
    unittest.main()
