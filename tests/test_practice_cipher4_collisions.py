import json
from pathlib import Path
import unittest

from eye_mystery.practice_cipher4_collisions import (
    aligned_collision_profile,
    bigram_collision_profile,
    phase_shift_audit,
)


ROOT = Path(__file__).resolve().parents[1]


class PracticeCipher4CollisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.messages = json.loads(
            (ROOT / "artifacts/practice-sdlwdr/cipher4.json").read_text()
        )

    def test_profiles_recover_a_planted_relative_phase(self) -> None:
        left = (0, 1, 4, 9, 16)
        right = tuple((value + 7) % 83 for value in left)
        self.assertEqual(aligned_collision_profile(left, right)[7], len(left))
        self.assertEqual(
            bigram_collision_profile(left, right)[7],
            len(left) - 1,
        )

    def test_real_phase_shift_null_is_exact(self) -> None:
        audit = phase_shift_audit(self.messages)
        coincidences = tuple(
            (left_index, right_index, position, left_value)
            for left_index in range(3)
            for right_index in range(left_index + 1, 3)
            for position, (left_value, right_value) in enumerate(
                zip(
                    self.messages[left_index],
                    self.messages[right_index],
                )
            )
            if left_value == right_value
        )
        self.assertEqual(
            coincidences,
            ((1, 2, 340, 5), (1, 2, 369, 61)),
        )
        self.assertEqual(audit.observed.aligned_unigrams, 2)
        self.assertEqual(audit.observed.cross_message_bigrams, 183)
        self.assertEqual(audit.configurations, 83**2)
        self.assertEqual(audit.unigram_lower_or_equal, 86)
        self.assertEqual(audit.bigram_upper_or_equal, 2167)
        self.assertEqual(audit.joint_tail, 33)
        self.assertEqual(audit.cross_bigram_minimum, 116)
        self.assertEqual(audit.cross_bigram_maximum, 574)
        self.assertEqual(audit.cross_bigram_sum, 1_243_174)
        self.assertEqual(audit.within_bigram_collisions, 102)
        self.assertEqual(audit.bigram_positions, 1301)

    def test_global_translation_does_not_change_the_audit(self) -> None:
        translated = [
            [(value + 29) % 83 for value in message]
            for message in self.messages
        ]
        self.assertEqual(
            phase_shift_audit(translated),
            phase_shift_audit(self.messages),
        )


if __name__ == "__main__":
    unittest.main()
