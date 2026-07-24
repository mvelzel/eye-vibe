import math
import unittest

from eye_mystery.cessation_wheel import (
    ContextAgreement,
    HELDOUT_CONTEXTS,
    OrientationResult,
    TRAIN_CONTEXTS,
    changed_label_agreement,
    evaluate_orientation,
    fixed_composition_tapes,
    sample_visual_row,
    sampled_message_values,
    select_orientation,
)
from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.earthquake_mask import MASK


class CessationWheelTests(unittest.TestCase):
    def test_terminal_aware_sampling_moves_one_position_past_endpoint(self) -> None:
        tape = (0, 1, 0, 1, 1, 0, 1)
        row = (0, 1, 2)
        self.assertEqual(sample_visual_row(row, tape), (0, 0, 1))
        self.assertEqual(
            sample_visual_row(row, tape, terminal_aware=False),
            (0, 0, 0),
        )

    def test_visual_sampling_restores_every_trigram_boundary(self) -> None:
        for name in MESSAGE_ORDER:
            with self.subTest(name=name):
                sampled = sampled_message_values(name, MASK)
                self.assertEqual(sampled_message_values(name, MASK), sampled)
                self.assertEqual(
                    len(sampled),
                    len(trigram_values(MESSAGES[name])),
                )
                self.assertTrue(all(value in range(8) for value in sampled))

    def test_changed_label_score_omits_literal_positions(self) -> None:
        original = {
            "a": (1, 2, 3, 4),
            "b": (1, 5, 6, 4),
        }
        sampled = {
            "a": (7, 1, 2, 3),
            "b": (0, 1, 2, 5),
        }
        score = changed_label_agreement(
            sampled,
            (("fixture", "a", 0, "b", 0, 4),),
            original=original,
        )
        self.assertEqual(score.agreements, 2)
        self.assertEqual(score.changed_positions, 2)
        self.assertEqual(score.exact_contexts, 1)

    def test_orientation_selector_uses_training_only_and_forward_ties(self) -> None:
        weak = ContextAgreement(1, 4, 0, 1)
        strong = ContextAgreement(2, 4, 0, 1)
        perfect_heldout = ContextAgreement(4, 4, 1, 1)
        empty_heldout = ContextAgreement(0, 4, 0, 1)
        forward = OrientationResult("forward", weak, perfect_heldout)
        reverse = OrientationResult("reverse", strong, empty_heldout)
        self.assertEqual(
            select_orientation((forward, reverse)).orientation,
            "reverse",
        )
        self.assertEqual(
            select_orientation(
                (
                    OrientationResult("forward", strong, empty_heldout),
                    OrientationResult("reverse", strong, perfect_heldout),
                )
            ).orientation,
            "forward",
        )

    def test_fixed_composition_null_is_exact(self) -> None:
        tapes = fixed_composition_tapes()
        self.assertEqual(len(tapes), math.comb(17, 4))
        self.assertIn(MASK, tapes)
        self.assertEqual(len(set(tapes)), len(tapes))
        self.assertTrue(
            all(len(tape) == 17 and tape.count(0) == 4 for tape in tapes)
        )

    def test_real_orientation_selection_is_deterministic(self) -> None:
        first = evaluate_orientation(MASK)
        second = evaluate_orientation(MASK)
        self.assertEqual(first, second)
        self.assertEqual(first.training.contexts, len(TRAIN_CONTEXTS))
        self.assertEqual(first.heldout.contexts, len(HELDOUT_CONTEXTS))


if __name__ == "__main__":
    unittest.main()
