from unittest import TestCase

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.edit_diamond import (
    AdditiveDiamond,
    literal_edit_diamonds,
)


class AdditiveDiamondTests(TestCase):
    def test_cipher4_insertion_selects_band_midpoint(self) -> None:
        diamond = AdditiveDiamond((18, 22), (12,))
        self.assertEqual(diamond.neutral_solutions(57), (28,))
        self.assertEqual(diamond.residual(28, 57), 0)
        self.assertNotEqual(diamond.residual(27, 57), 0)

    def test_noninvertible_length_difference_returns_all_solutions(self) -> None:
        diamond = AdditiveDiamond((4, 4, 4), (2,))
        self.assertEqual(diamond.neutral_solutions(10), (0, 5))

    def test_literal_search_recovers_planted_one_symbol_edit(self) -> None:
        streams = {
            "long": (1, 2, 3, 18, 22, 4, 5, 6),
            "short": (1, 2, 3, 12, 4, 5, 6),
        }
        events = literal_edit_diamonds(
            streams,
            context_length=3,
            maximum_gap=2,
        )
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].left_path, (18, 22))
        self.assertEqual(events[0].right_path, (12,))
        self.assertEqual(events[0].additive.neutral_solutions(57), (28,))

    def test_eyes_have_no_literal_short_edit_diamond(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name])
            for name in MESSAGE_ORDER
        }
        events = literal_edit_diamonds(
            streams,
            context_length=4,
            maximum_gap=8,
        )
        self.assertEqual(events, ())
