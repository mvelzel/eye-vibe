import unittest

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.walk_mask import (
    chunk_values,
    direction_bits,
    walk_violations,
    xor_periodic_mask,
)


PRACTICE_ONE = tuple(
    map(
        int,
        "432121232123404043401210401212104323234010401010404012321234043432121212"
        "343404323232104340121012343432323434043212321040401040401043232101043432"
        "101210101212104340432123234040404323212343434010123212321040401040404321"
        "23210401012323404343404043212321040101232323210104",
    )
)


class WalkMaskTests(unittest.TestCase):
    def test_solved_practice_puzzle_readout(self) -> None:
        directions = direction_bits(PRACTICE_ONE, modulus=5)
        self.assertIsNotNone(directions)
        unmasked = xor_periodic_mask(directions or (), (0, 1))
        decoded = bytes(chunk_values(unmasked, width=7, offset=6)).decode("ascii")
        self.assertEqual(decoded, "ermutation Representation Destination")

    def test_eye_streams_are_not_constant_step_walks(self) -> None:
        for name in MESSAGE_ORDER:
            with self.subTest(name=name):
                values = trigram_values(MESSAGES[name])
                self.assertTrue(walk_violations(values, modulus=83, step=1))

    def test_rejects_non_walk(self) -> None:
        self.assertIsNone(direction_bits((0, 1, 3), modulus=5))


if __name__ == "__main__":
    unittest.main()
