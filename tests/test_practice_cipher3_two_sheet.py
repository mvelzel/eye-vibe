import unittest

from eye_mystery.practice_cipher3_two_sheet import (
    decode_with_key,
    encode_two_sheet,
    involution_orbits,
    involution_quotient_table,
    quotient_streams,
)


class PracticeCipher3TwoSheetTests(unittest.TestCase):
    def test_every_affine_reflection_has_41_pairs_and_one_fixed_point(self) -> None:
        for reflection in range(83):
            orbits = involution_orbits(reflection)
            self.assertEqual(len(orbits), 42)
            self.assertEqual(sum(len(orbit) == 1 for orbit in orbits), 1)
            self.assertEqual(sum(len(orbit) == 2 for orbit in orbits), 41)
            self.assertEqual(
                sorted(value for orbit in orbits for value in orbit),
                list(range(83)),
            )

    def test_true_quotient_and_key_decode_exactly(self) -> None:
        key = tuple((17 * value + 3) % 42 for value in range(42))
        plaintexts = (
            tuple(range(42)),
            (3, 1, 4, 1, 5, 9, 2, 6),
        )
        ciphertexts = encode_two_sheet(
            plaintexts,
            37,
            key,
            seed=12345,
        )
        quotient = quotient_streams(ciphertexts, 37)
        self.assertEqual(decode_with_key(quotient, key), plaintexts)
        table = involution_quotient_table(37)
        self.assertTrue(
            all(
                table[orbit[0]] == table[orbit[1]]
                for orbit in involution_orbits(37)
                if len(orbit) == 2
            )
        )


if __name__ == "__main__":
    unittest.main()
