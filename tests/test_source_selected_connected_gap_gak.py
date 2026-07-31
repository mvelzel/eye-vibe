from __future__ import annotations

import unittest

from scripts.run_source_selected_connected_gap_gak import (
    encode_shared_characters,
    source_segments,
)


class SourceSelectedConnectedGapGAKTests(unittest.TestCase):
    def test_source_gap_enumeration_ignores_other_pairs(self) -> None:
        text = (
            "THAT WHICH" + "X" * 18 + "THAT WHICH"
            + "Y" * 2
            + "THAT WHICH" + "Z" * 20 + "THAT WHICH"
        )
        segments = source_segments((("plant", text),))
        self.assertEqual(len(segments["east1"]), 1)
        self.assertEqual(segments["east1"][0].text, text[:38])
        self.assertEqual(len(segments["west1"]), 1)
        self.assertEqual(len(segments["east2"]), 0)

    def test_shared_character_encoding_is_global(self) -> None:
        text = "THAT WHICH" + "A" * 18 + "THAT WHICH"
        segment = source_segments((("plant", text),))["east1"][0]
        plaintexts, alphabet = encode_shared_characters(
            (segment, segment)
        )
        self.assertEqual(plaintexts[0], plaintexts[1])
        self.assertEqual(set(alphabet), set(text))


if __name__ == "__main__":
    unittest.main()
