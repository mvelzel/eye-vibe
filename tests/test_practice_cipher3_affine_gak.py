from __future__ import annotations

import random
import unittest

from eye_mystery.affine_gak import decode_affine_gak
from eye_mystery.practice_cipher3_affine_gak import (
    StructuredCandidate,
    candidate_multiplier,
    discrete_log_table,
    encrypt_affine_gak,
    named_group,
    replay_exact_model,
    solve_exact_affine_gak,
    structured_search,
)


class AffineGakPrimitiveTests(unittest.TestCase):
    def test_two_is_primitive_modulo_83(self) -> None:
        self.assertEqual(len(discrete_log_table()), 82)

    def test_every_mode_round_trips(self) -> None:
        plaintext = tuple((7 * index) % 41 + 1 for index in range(80))
        multiplier = lambda value: pow(2, value, 83)
        for mode in (
            "full",
            "primer",
            "skip",
            "indicator-hidden",
            "indicator-both",
        ):
            with self.subTest(mode=mode):
                ciphertext = encrypt_affine_gak(
                    plaintext,
                    multiplier,
                    mode,
                    header=17,
                )
                self.assertEqual(
                    decode_affine_gak(ciphertext, multiplier, mode),
                    plaintext,
                )

    def test_structured_multiplier_families(self) -> None:
        self.assertEqual(
            candidate_multiplier(
                StructuredCandidate("full", "linear", (7, 11)),
                5,
            ),
            46,
        )
        self.assertEqual(
            candidate_multiplier(
                StructuredCandidate("full", "power-base", (2,)),
                5,
            ),
            32,
        )


class AffineGakPositiveControlTests(unittest.TestCase):
    @staticmethod
    def planted_streams() -> dict[str, tuple[tuple[int, ...], ...]]:
        rng = random.Random(0xA661)
        streams = {}
        for group_index, group in enumerate(("A", "B", "C")):
            messages = []
            for message_index in range(6):
                plaintext = list(range(1, 43))
                plaintext.extend(
                    rng.randrange(1, 43)
                    for _ in range(55 + 20 * group_index)
                )
                rng.shuffle(plaintext)
                messages.append(
                    encrypt_affine_gak(
                        plaintext,
                        lambda value: pow(2, value, 83),
                        "indicator-both",
                        header=1 + group_index * 6 + message_index,
                    )
                )
            streams[group] = tuple(messages)
        return streams

    def test_structured_catalog_retains_true_planted_family(self) -> None:
        result = structured_search(self.planted_streams())
        planted = StructuredCandidate(
            "indicator-both",
            "power-base",
            (2,),
        )
        self.assertIn(planted, result.minimizers)
        self.assertIsNotNone(result.complete_unique)
        self.assertLessEqual(result.complete_unique, 42)

    def test_exact_model_is_sat_and_replays(self) -> None:
        update_table = {
            value: (7 * value + 3) % 82
            for value in range(1, 5)
        }
        plaintext = (1, 2, 3, 4) * 3
        messages = (
            (
                "plant0",
                encrypt_affine_gak(
                    plaintext,
                    lambda value: pow(2, update_table[value], 83),
                    "indicator-both",
                    header=17,
                ),
            ),
        )
        result = solve_exact_affine_gak(
            messages,
            mode="indicator-both",
            max_symbols=4,
            timeout_ms=10_000,
        )
        self.assertEqual(result.status, "sat")
        self.assertEqual(len(result.realized_states), 4)
        self.assertTrue(
            replay_exact_model(result, messages, mode="indicator-both")
        )


if __name__ == "__main__":
    unittest.main()
