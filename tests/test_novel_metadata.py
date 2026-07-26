import unittest

from eye_mystery.novel_metadata import (
    descriptor_permutation_matches,
    q_headers_are_noncenter_derangements,
    range_descriptor,
    row_staggers,
)


class NovelMetadataTests(unittest.TestCase):
    def test_358_describes_the_visible_alphabet_cut(self) -> None:
        descriptor = range_descriptor()
        self.assertEqual(
            (descriptor.quotient, descriptor.radix, descriptor.remainder),
            (3, 5, 8),
        )
        self.assertEqual(descriptor.size, 83)
        self.assertEqual(descriptor.maximum_digits, (3, 1, 2))
        self.assertEqual(descriptor_permutation_matches(), ((3, 5, 8),))

    def test_q_headers_are_derangements_after_removing_center(self) -> None:
        self.assertTrue(q_headers_are_noncenter_derangements())

    def test_literal_middle_header_stagger_only_occurs_in_final_row(self) -> None:
        first, second, final = row_staggers()
        self.assertEqual(first.unique_gap_records, ())
        self.assertEqual(
            second.unique_gap_records,
            ((3, (90, 97, 113), None, (63, 17, 54)),),
        )
        self.assertEqual(final.middle_order, (0, 2, 1))
        self.assertEqual(
            final.unique_gap_records,
            ((11, (16, 18, 17), (0, 2, 1), (75, 81, 48)),),
        )


if __name__ == "__main__":
    unittest.main()
