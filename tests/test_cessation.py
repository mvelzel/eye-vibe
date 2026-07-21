import unittest

from eye_mystery.cessation import (
    CESSATION_KEY,
    bits_to_bytes,
    skip_key_bits,
    text_likeness,
    trace_trigram_skip_states,
)


class CessationTests(unittest.TestCase):
    def test_key_has_documented_calendar_length(self) -> None:
        self.assertEqual(len(CESSATION_KEY), 31)

    def test_skip_and_reset_semantics(self) -> None:
        self.assertEqual(skip_key_bits((1, 2, 1), (1, 0, 1, 1)), (1, 1, 1))
        self.assertEqual(
            skip_key_bits((1, 0, 1), (1, 0, 1, 1), reset_value=0),
            (1, 1),
        )

    def test_bit_packing_and_text_score(self) -> None:
        bits = tuple(map(int, "01000001"))
        self.assertEqual(bits_to_bytes(bits), b"A")
        self.assertEqual(text_likeness(b"A \x00"), (2, 2, -1))

    def test_three_skips_emit_one_cyclic_state(self) -> None:
        directions = (0, 1, 2, 4, 4, 3)
        self.assertEqual(
            trace_trigram_skip_states(directions, (1, 2, 3, 4, 5), 11),
            (6, 9),
        )
        self.assertEqual(
            trace_trigram_skip_states(
                directions, (-1, -2, -3, -4, -5), 11
            ),
            (5, 2),
        )

    def test_trigram_state_validation(self) -> None:
        with self.assertRaises(ValueError):
            trace_trigram_skip_states((0, 1), (1, 2, 3, 4, 5), 26)
        with self.assertRaises(ValueError):
            trace_trigram_skip_states((0, 1, 5), (1, 2, 3, 4, 5), 26)


if __name__ == "__main__":
    unittest.main()
