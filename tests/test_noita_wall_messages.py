from __future__ import annotations

import unittest
from pathlib import Path

from eye_mystery.noita_wall_messages import load_wall_messages
from eye_mystery.wall_steganography import decode_cover


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "artifacts" / "noita-wall-messages-en.txt"


class NoitaWallMessageTests(unittest.TestCase):
    def test_frozen_corpus_has_all_twelve_map_ids(self) -> None:
        records = load_wall_messages(CORPUS)
        self.assertEqual(
            tuple(map_id for map_id, _ in records),
            ("G9", "G7", "G6", "G10", "G8", "G11", "G12", "G1", "G2", "G3", "G4", "G5"),
        )
        self.assertEqual(len(records), 12)

    def test_editorial_sic_is_not_a_carrier_word(self) -> None:
        records = dict(load_wall_messages(CORPUS))
        self.assertNotIn("[sic]", records["G11"])
        self.assertIn("what your seeking", records["G11"])

    def test_frozen_transfer_outputs_are_stable(self) -> None:
        self.assertEqual(
            {
                map_id: decode_cover(text)
                for map_id, text in load_wall_messages(CORPUS)
            },
            {
                "G9": "?",
                "G7": "E3?",
                "G6": "?4NE",
                "G10": "33??",
                "G8": "?EA??IU",
                "G11": "X??U?U?LU",
                "G12": "????????",
                "G1": "VFG???OZ????GVF????S??WA?N3D??",
                "G2": "1?R?V?3??SF",
                "G3": "???J2UU??EP?",
                "G4": "?M?NE",
                "G5": "O???",
            },
        )


if __name__ == "__main__":
    unittest.main()
