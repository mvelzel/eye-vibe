import unittest

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, ROW_PAIR_TRIGRAM_LENGTHS
from eye_mystery.visual_rows import (
    direction_mask_rows,
    interleave_visual_rows,
    visual_rows,
)


class VisualRowsTests(unittest.TestCase):
    def test_known_first_row_pair(self) -> None:
        rows = visual_rows(MESSAGES["east1"], ROW_PAIR_TRIGRAM_LENGTHS["east1"])
        self.assertEqual(
            "".join(map(str, rows[0])),
            "201013223304041130232114313033004024000",
        )
        self.assertEqual(
            "".join(map(str, rows[1])),
            "032041220001422242122220110003201341113",
        )

    def test_round_trip_all_messages(self) -> None:
        for name in MESSAGE_ORDER:
            with self.subTest(name=name):
                rows = visual_rows(MESSAGES[name], ROW_PAIR_TRIGRAM_LENGTHS[name])
                self.assertEqual(interleave_visual_rows(rows), MESSAGES[name])

    def test_complete_visual_row_width_is_39(self) -> None:
        for name in MESSAGE_ORDER:
            rows = visual_rows(MESSAGES[name], ROW_PAIR_TRIGRAM_LENGTHS[name])
            for row in rows[:-2]:
                self.assertEqual(len(row), 39)

    def test_direction_masks_align_at_top_left(self) -> None:
        masks = direction_mask_rows((((0, 1), (2,)), ((1,), (3, 4))))
        self.assertEqual(masks, ((3, 2), (12, 16)))


if __name__ == "__main__":
    unittest.main()
