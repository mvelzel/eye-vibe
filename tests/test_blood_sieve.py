import unittest

from eye_mystery.blood_sieve import (
    BLOOD_ROW_RUNS,
    pack_bits,
    pack_chunks,
    sieve_row_pair,
    split_row_pair_values,
)
from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, ROW_PAIR_TRIGRAM_LENGTHS


class BloodSieveTests(unittest.TestCase):
    def test_mask_dimensions_and_area(self) -> None:
        self.assertEqual(len(BLOOD_ROW_RUNS), 26)
        self.assertEqual(BLOOD_ROW_RUNS[0], ((0, 83),))
        self.assertEqual(
            sum(end - start for runs in BLOOD_ROW_RUNS for start, end in runs),
            1114,
        )
        self.assertEqual(sieve_row_pair((0, 0, 0, 0, 0, 13)), (1, 1, 1, 1, 1, 0))

    def test_all_messages_split_exactly(self) -> None:
        for name in MESSAGE_ORDER:
            with self.subTest(name=name):
                rows = split_row_pair_values(
                    MESSAGES[name], ROW_PAIR_TRIGRAM_LENGTHS[name]
                )
                self.assertEqual(tuple(map(len, rows)), ROW_PAIR_TRIGRAM_LENGTHS[name])

    def test_mask_reflections(self) -> None:
        self.assertEqual(sieve_row_pair((82, 77, 75)), (1, 1, 1))
        self.assertEqual(sieve_row_pair((82, 77, 75), mirror_values=True), (1, 1, 1))
        self.assertEqual(sieve_row_pair((7,), reverse_positions=True), (1,))
        self.assertEqual(sieve_row_pair((8,), reverse_positions=True), (0,))

    def test_pack_bits(self) -> None:
        bits = (0, 1, 0, 0, 0, 0, 0, 1)
        self.assertEqual(pack_bits(bits), b"A")
        self.assertEqual(pack_bits(bits, least_significant_first=True), b"\x82")
        self.assertEqual(pack_chunks((1, 0, 0, 0, 0, 0, 1), width=7), (65,))


if __name__ == "__main__":
    unittest.main()
