from __future__ import annotations

import unittest
from pathlib import Path

from eye_mystery.wall_steganography import (
    carrier_groups,
    decode_cover,
    mismatches_against_plaintext,
)


ROOT = Path(__file__).resolve().parents[1]
COVER = (ROOT / "artifacts" / "practice-wall-steganography.txt").read_text(
    encoding="utf-8"
).strip()
RAW_DECODE = (
    "VISIONSOFETERNIEYLIEAHEAD?ULLOFHOPELESSNESS"
    "RUBEDOJUSTOUTOFREACH"
)
SOLUTION = (
    "VISIONSOFETERNITYLIEAHEADFULLOFHOPELESSNESS"
    "RUBEDOJUSTOUTOFREACH"
)


class WallSteganographyTests(unittest.TestCase):
    def test_visible_rule_decodes_all_sixty_three_groups(self) -> None:
        groups = carrier_groups(COVER)
        self.assertEqual(len(groups), 63)
        self.assertEqual(sum(len(group.words) for group in groups), 170)
        self.assertEqual(decode_cover(COVER), RAW_DECODE)

    def test_internal_capitals_create_the_expected_group_boundaries(self) -> None:
        group_texts = tuple(group.text for group in carrier_groups(COVER))
        self.assertIn("Who is", group_texts)
        self.assertIn("The one god", group_texts)
        self.assertIn("you do not", group_texts)
        self.assertIn("Truly understand anything", group_texts)
        self.assertIn("even you are of", group_texts)
        self.assertIn("Our", group_texts)
        self.assertIn("Vision and eye", group_texts)

    def test_two_complementary_carrier_repairs_restore_full_plaintext(self) -> None:
        groups = carrier_groups(COVER)
        words = {
            word.index: word
            for group in groups
            for word in group.words
        }
        self.assertEqual((words[37].text, words[37].bit), ("yet", "."))
        self.assertEqual((words[64].text, words[64].bit), ("this", "-"))
        self.assertEqual(37 + 64, 101)
        self.assertEqual(
            decode_cover(COVER, bit_overrides={37: "-", 64: "."}),
            SOLUTION,
        )
        mismatches = mismatches_against_plaintext(COVER, SOLUTION)
        self.assertEqual(
            tuple(
                (
                    mismatch.group_index,
                    mismatch.plaintext,
                    mismatch.word.index,
                    mismatch.word.text,
                    mismatch.word.bit,
                    mismatch.expected_bit,
                )
                for mismatch in mismatches
            ),
            (
                (16, "T", 37, "yet", ".", "-"),
                (26, "F", 64, "this", "-", "."),
            ),
        )

    def test_small_planted_cover_decodes_without_language_scoring(self) -> None:
        # ...- / .. then an internal capital split to ... / .. / --- / -.
        cover = (
            "One two six worship? One two The god you, One two, "
            "four four four, four one."
        )
        self.assertEqual(decode_cover(cover), "VISION")


if __name__ == "__main__":
    unittest.main()
