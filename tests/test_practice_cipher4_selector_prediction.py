import random
import unittest

from eye_mystery.practice_cipher4_selector_prediction import (
    ContextSpec,
    attribute_prediction,
    audit_selector_prediction,
    context_specs,
    cross_validated_prediction,
)


class PracticeCipher4SelectorPredictionTests(unittest.TestCase):
    def test_context_catalog_is_unique(self) -> None:
        specs = context_specs()
        identities = {(spec.name, spec.phase) for spec in specs}
        self.assertEqual(len(specs), len(identities))

    def test_current_payload_predicts_planted_selector(self) -> None:
        rng = random.Random(4)
        quotient = tuple(
            tuple(rng.randrange(9) for _ in range(250)) for _ in range(3)
        )
        selector = tuple(
            tuple(value % 2 for value in stream) for stream in quotient
        )
        score = cross_validated_prediction(
            quotient,
            selector,
            spec=ContextSpec("q"),
            selector_size=2,
            payload_modulus=9,
            radius=2,
        )
        self.assertGreater(score.gain_bits_per_symbol, 0.5)
        self.assertEqual(score.accuracy, 1.0)

    def test_selection_calibration_is_reproducible(self) -> None:
        rng = random.Random(7)
        quotient = tuple(
            tuple(rng.randrange(8) for _ in range(100)) for _ in range(3)
        )
        selector = tuple(
            tuple(rng.randrange(2) for _ in stream) for stream in quotient
        )
        left = audit_selector_prediction(
            quotient,
            selector,
            selector_size=2,
            payload_modulus=8,
            controls=10,
            seed=5,
        )
        right = audit_selector_prediction(
            quotient,
            selector,
            selector_size=2,
            payload_modulus=8,
            controls=10,
            seed=5,
        )
        self.assertEqual(left, right)

    def test_declared_null_modes_are_reproducible(self) -> None:
        quotient = ((0, 1, 2, 0, 1, 2) * 4,) * 3
        selector = (
            (0, 1, 0, 1, 0, 1) * 4,
            (1, 0, 1, 0, 1, 0) * 4,
            (0, 0, 1, 1, 0, 1) * 4,
        )
        for null_mode in (
            "within-q",
            "circular-selector",
            "paired-rank",
        ):
            left = audit_selector_prediction(
                quotient,
                selector,
                selector_size=2,
                payload_modulus=3,
                controls=3,
                seed=17,
                null_mode=null_mode,
            )
            right = audit_selector_prediction(
                quotient,
                selector,
                selector_size=2,
                payload_modulus=3,
                controls=3,
                seed=17,
                null_mode=null_mode,
            )
            self.assertEqual(left, right)

    def test_attribution_separates_exact_rank_bigram_reuse(self) -> None:
        quotient = (
            (9, 0, 1, 2, 8),
            (7, 0, 1, 3, 6),
            (5, 4, 3, 2, 1),
        )
        selector = (
            (1, 0, 1, 0, 1),
            (0, 0, 1, 1, 0),
            (1, 0, 1, 0, 1),
        )
        result = attribute_prediction(
            quotient,
            selector,
            spec=ContextSpec("previous-q+q+previous-r"),
            selector_size=2,
            payload_modulus=10,
            width=2,
            radius=1,
        )
        self.assertGreater(result.seen_context_exact_bigram, 0)
        self.assertEqual(
            result.correct_seen_context_exact_bigram,
            result.seen_context_exact_bigram,
        )


if __name__ == "__main__":
    unittest.main()
