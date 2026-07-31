from __future__ import annotations

import unittest
from pathlib import Path

from eye_mystery.noita_wall_messages import load_wall_message_lines
from eye_mystery.wall_context_deck import (
    UPDATE_FAMILIES,
    decode_labels,
    encode_ranks,
    wall_parameter_tables,
)


ROOT = Path(__file__).resolve().parents[1]


class WallContextDeckTests(unittest.TestCase):
    def test_parameter_tables_cover_all_eighty_three_labels(self) -> None:
        lines = dict(
            load_wall_message_lines(
                ROOT / "artifacts" / "noita-wall-messages-en.txt"
            )
        )
        tables = wall_parameter_tables(lines)
        self.assertEqual(len(tables), 10)
        self.assertTrue(all(len(values) == 83 for _, values in tables))

    def test_every_update_round_trips_both_parameter_indices(self) -> None:
        deck = tuple(range(11))
        parameters = tuple((index * 3 + 2) % 11 for index in range(11))
        plaintext = (3, 1, 9, 0, 4, 7, 2, 10, 5, 6, 8)
        for family in UPDATE_FAMILIES:
            for parameter_index in ("label", "rank"):
                with self.subTest(
                    family=family,
                    parameter_index=parameter_index,
                ):
                    ciphertext = encode_ranks(
                        plaintext,
                        deck,
                        parameters,
                        family=family,
                        parameter_index=parameter_index,
                    )
                    self.assertEqual(
                        decode_labels(
                            ciphertext,
                            deck,
                            parameters,
                            family=family,
                            parameter_index=parameter_index,
                        ),
                        plaintext,
                    )


if __name__ == "__main__":
    unittest.main()
