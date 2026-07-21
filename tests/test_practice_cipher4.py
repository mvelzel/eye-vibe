import json
from pathlib import Path
import unittest

from eye_mystery.practice_cipher4 import (
    AffineSchedule,
    affine_schedule_survivors,
    consistent_recurrence_prefix,
    consistent_recurrence_prefix_at,
    cyclic_differences,
    decode_affine_schedule,
)


ROOT = Path(__file__).resolve().parents[1]


class PracticeCipher4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.messages = json.loads(
            (ROOT / "artifacts/practice-sdlwdr/cipher4.json").read_text()
        )
        cls.second_differences = cyclic_differences(cls.messages[1])

    def test_source_consistency_recovers_a_planted_arbitrary_function(self) -> None:
        plaintext = (1, 2, 1, 3, 2, 1)
        function = {1: 7, 2: 11, 3: 19}
        differences = tuple(
            (following - function[current]) % 83
            for current, following in zip(plaintext, plaintext[1:])
        )
        self.assertEqual(
            consistent_recurrence_prefix(plaintext, differences),
            len(differences),
        )
        self.assertEqual(
            consistent_recurrence_prefix_at(
                (80,) + plaintext + (81,),
                1,
                differences,
            ),
            len(differences),
        )
        corrupted = differences[:2] + ((differences[2] + 1) % 83,) + differences[3:]
        self.assertEqual(
            consistent_recurrence_prefix(plaintext, corrupted),
            2,
        )

    def test_affine_decoder_round_trip_shape(self) -> None:
        decoded = decode_affine_schedule(
            (5, 6, 7),
            4,
            ciphertext_sign=1,
            multiplier=2,
            translation=3,
        )
        self.assertEqual(decoded, (4, 16, 41, 9))

    def test_natural_alphabets_exclude_every_affine_rotation_schedule(self) -> None:
        self.assertEqual(
            affine_schedule_survivors(
                self.second_differences,
                tuple(range(26)) + (36,),
            ),
            (),
        )
        self.assertEqual(
            affine_schedule_survivors(
                self.second_differences,
                range(42),
            ),
            (),
        )

    def test_57_state_affine_survivors_are_only_the_direct_rank_reading(self) -> None:
        survivors = affine_schedule_survivors(
            self.second_differences,
            range(57),
        )
        self.assertEqual(
            survivors,
            (
                # p[i+1] = delta[i] - 22
                AffineSchedule(1, 0, 61, tuple(range(57))),
                # The reflected equivalent p[i+1] = -delta[i] - 5.
                AffineSchedule(-1, 0, 78, tuple(range(57))),
            ),
        )


if __name__ == "__main__":
    unittest.main()
