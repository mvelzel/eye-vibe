import unittest

from eye_mystery.texture_sieve import (
    boundary_trimmed_masks,
    dihedral_orientations,
    lookup_bits,
)


class TextureSieveTests(unittest.TestCase):
    def test_rectangular_dihedral_orientations(self) -> None:
        rows = ((0, 1, 0), (1, 1, 0))
        orientations = dihedral_orientations(rows)
        self.assertEqual(len(orientations), 8)
        self.assertEqual({sum(map(len, item.rows)) for item in orientations}, {6})

    def test_two_boundary_bits_give_three_trims_per_orientation(self) -> None:
        rows = ((0, 1, 0), (1, 1, 0))
        masks = boundary_trimmed_masks(rows, output_rows=2, output_columns=2)
        self.assertLessEqual(len(masks), 8 * 3)
        self.assertTrue(masks)
        self.assertTrue(
            all(len(mask.rows) == 2 and len(mask.rows[0]) == 2 for mask in masks)
        )

    def test_lookup_uses_position_then_symbol(self) -> None:
        mask = ((0, 1, 0), (1, 0, 1))
        self.assertEqual(lookup_bits(mask, (0, 1, 1), (1, 0, 2)), (1, 1, 1))


if __name__ == "__main__":
    unittest.main()
