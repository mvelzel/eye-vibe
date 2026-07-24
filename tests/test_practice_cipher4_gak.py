from __future__ import annotations

import unittest

from eye_mystery.practice_cipher4_gak import (
    CharacterModel,
    encode_nonlinear_gak,
    nonlinear_gak_beam,
    normalize_language,
    render_plaintext,
    signed_band_step,
)


class PracticeCipher4GakTests(unittest.TestCase):
    def test_packed_beam_recovers_planted_nonlinear_path(self) -> None:
        plaintext_text = "ABRACADABRA ABRACADABRA ABRACADABRA"
        training = (plaintext_text + " ") * 100
        plaintext = normalize_language(plaintext_text)
        key = tuple((17 * index + 9) % 83 for index in range(27))
        differences = encode_nonlinear_gak(
            plaintext, key, space_position=36
        )
        result = nonlinear_gak_beam(
            differences,
            CharacterModel.train(training, order=5),
            space_position=36,
            beam_width=20_000,
        )
        self.assertEqual(result.completed, len(differences))
        recovered = {
            render_plaintext(candidate.plaintext)
            for candidate in result.candidates
        }
        self.assertIn(plaintext_text, recovered)

    def test_normalization_collapses_separators(self) -> None:
        values = normalize_language("One,\n two!")
        self.assertEqual(render_plaintext(values), "ONE TWO")

    def test_zigzag_band_is_exactly_minus_28_through_plus_28(self) -> None:
        steps = tuple(
            signed_band_step(rank, "zigzag-negative-odd")
            for rank in range(57)
        )
        self.assertEqual(steps[:7], (0, -1, 1, -2, 2, -3, 3))
        self.assertEqual(set(steps), set(range(-28, 29)))


if __name__ == "__main__":
    unittest.main()
