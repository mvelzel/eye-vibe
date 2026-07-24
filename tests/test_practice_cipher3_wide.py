from __future__ import annotations

import unittest

from eye_mystery.deck_selected import decode_base_selected_action
from eye_mystery.practice_cipher3_wide import (
    EXCEPTIONAL_RAW,
    RECOVERED_WHEEL_CARDS,
    WheelControlSemantics,
    decode_recovered_wheel,
    decode_fixed_base_selected_action,
    drift_values,
    initial_deck_candidates,
    load_cipher3,
    recursive_transfer_scores,
    render_wheel_coordinates,
    select_fixed_drift,
    select_physical_transfer,
    select_recursive_transfer,
)
from eye_mystery.practice_sdlwdr import (
    PUZZLE1_SHIFTS,
    decode_puzzle1_section,
)


class PracticeCipher3WidePrimitiveTests(unittest.TestCase):
    def test_recovered_wheel_contains_every_nonexceptional_card(self) -> None:
        self.assertEqual(len(RECOVERED_WHEEL_CARDS), 82)
        self.assertEqual(
            set(RECOVERED_WHEEL_CARDS),
            set(range(83)) - {EXCEPTIONAL_RAW},
        )

    def test_fixed_drift_recovers_a_planted_progression(self) -> None:
        message = tuple((7 + 3 * position) % 83 for position in range(20))
        self.assertEqual(
            set(
                drift_values(
                    message,
                    coordinate_system="standard83",
                    direction=1,
                    step=3,
                )
            ),
            {7},
        )

    def test_initial_decks_are_distinct_permutations(self) -> None:
        candidates = initial_deck_candidates()
        self.assertEqual(len(candidates), len({deck for _, deck in candidates}))
        self.assertTrue(
            all(tuple(sorted(deck)) == tuple(range(83)) for _, deck in candidates)
        )

    def test_fixed_base_decoder_matches_existing_implementation(self) -> None:
        base = (1, 2, 3, 4, 0)
        ciphertext = (0, 3, 1, 4)
        self.assertEqual(
            decode_fixed_base_selected_action(
                ciphertext,
                base,
                "move-to-front",
            ),
            decode_base_selected_action(
                ciphertext,
                base,
                "move-to-front",
            ),
        )

    def test_wheel_control_family_contains_solved_cipher1_semantics(self) -> None:
        from json import loads
        from pathlib import Path

        messages = loads(
            (
                Path(__file__).resolve().parents[1]
                / "artifacts/practice-sdlwdr/cipher1.json"
            ).read_text()
        )
        semantics = WheelControlSemantics(
            emit=True,
            toggle_parity=True,
            toggle_direction=False,
            reset_accumulator=False,
            reset_anchor=False,
        )
        index = next(
            index
            for index, message in enumerate(messages)
            if EXCEPTIONAL_RAW in message
        )
        coordinates = decode_recovered_wheel(
            messages[index],
            semantics,
            initial_direction=1,
            initial_parity=0,
        )
        self.assertEqual(
            render_wheel_coordinates(
                coordinates,
                PUZZLE1_SHIFTS[index],
                1,
            ),
            decode_puzzle1_section(
                messages[index],
                PUZZLE1_SHIFTS[index],
            ),
        )


class PracticeCipher3WideCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.streams = load_cipher3()

    def test_fixed_drift_selection_is_frozen(self) -> None:
        score = select_fixed_drift(self.streams)
        self.assertEqual(
            (
                score.coordinate_system,
                score.direction,
                score.step,
                score.training_unique,
                score.heldout_b_unique,
                score.heldout_c_unique,
            ),
            ("recovered82", -1, 9, 78, 82, 82),
        )

    def test_recursive_transfer_family_replays_every_emit_after_candidate(self) -> None:
        scores = recursive_transfer_scores(self.streams)
        self.assertTrue(
            all(
                score.replay_exact
                for score in scores
                if score.valid and score.update_timing == "after"
            )
        )

    def test_recursive_transfer_selection_is_frozen(self) -> None:
        score = select_recursive_transfer(self.streams)
        self.assertEqual(
            (
                score.initial_deck,
                score.marker_mode,
                score.update_timing,
                score.training_outside_42,
                score.training_unique,
                score.heldout_b_outside_42,
                score.heldout_c_outside_42,
            ),
            (
                "wheel-J-first-forward",
                "body",
                "after",
                159,
                82,
                351,
                581,
            ),
        )

    def test_physical_transfer_selection_is_frozen(self) -> None:
        score = select_physical_transfer(self.streams)
        self.assertEqual(
            (
                score.base,
                score.action,
                score.marker_mode,
                score.training_outside_42,
                score.training_unique,
                score.heldout_b_outside_42,
                score.heldout_c_outside_42,
            ),
            (
                "affine-82-fixed0-13-16",
                "move-to-front",
                "body",
                136,
                75,
                364,
                582,
            ),
        )


if __name__ == "__main__":
    unittest.main()
