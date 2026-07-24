import unittest

from eye_mystery.fourteenth_reassociation import (
    TrackReassociationSpec,
    reassociate_track,
    reassociation_specs,
)
from eye_mystery.fourteenth_selector import base5_digits


class FourteenthReassociationTests(unittest.TestCase):
    def test_catalog_is_complete_and_unique(self) -> None:
        specs = reassociation_specs()
        self.assertEqual(3 * 25 * 3, len(specs))
        self.assertEqual(len(specs), len(set(specs)))

    def test_opposite_shifts_round_trip_on_complete_blocks(self) -> None:
        values = tuple(range(21))
        encrypted = reassociate_track(
            values,
            TrackReassociationSpec(2, 7, "shift-right"),
        )
        self.assertIsNotNone(encrypted)
        decrypted = reassociate_track(
            encrypted,
            TrackReassociationSpec(2, 7, "shift-left"),
        )
        self.assertEqual(values, decrypted)

    def test_only_selected_component_moves(self) -> None:
        values = (1, 7, 13, 19, 20, 21)
        rendered = reassociate_track(
            values,
            TrackReassociationSpec(1, 3, "reverse"),
        )
        self.assertIsNotNone(rendered)
        for before, after in zip(values, rendered, strict=True):
            before_digits = base5_digits(before)
            after_digits = base5_digits(after)
            self.assertEqual(before_digits[0], after_digits[0])
            self.assertEqual(before_digits[2], after_digits[2])

    def test_out_of_range_reconstruction_is_rejected(self) -> None:
        self.assertIsNone(
            reassociate_track(
                (75, 20),
                TrackReassociationSpec(0, 2, "shift-left"),
            )
        )

    def test_partial_final_block_is_routed_with_its_actual_length(self) -> None:
        values = (0, 1, 2, 3, 4)
        encrypted = reassociate_track(
            values,
            TrackReassociationSpec(2, 3, "shift-right"),
        )
        self.assertEqual((2, 0, 1, 4, 3), encrypted)


if __name__ == "__main__":
    unittest.main()
