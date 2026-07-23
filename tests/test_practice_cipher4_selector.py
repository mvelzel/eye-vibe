import random
import unittest

from eye_mystery.practice_cipher4_bijection import CaseNgrams
from eye_mystery.practice_cipher4_selector import (
    SelectorLaw,
    best_affine_render,
    decode_selector_walk,
    encode_unsigned_walk,
    selector_laws,
)


class PracticeCipher4SelectorTests(unittest.TestCase):
    def test_unsigned_planted_walk_round_trip(self) -> None:
        plaintext = (2, 8, 1, 28, 0, 14)
        selectors = (0, 1, 0, 0, 1, 0)
        ranks = encode_unsigned_walk(
            plaintext,
            width=2,
            modulus=29,
            selectors=selectors,
        )
        self.assertEqual(
            decode_selector_walk(ranks, 29, SelectorLaw("unsigned", 2, 0)),
            plaintext,
        )

    def test_selector_families_are_finite_and_named(self) -> None:
        laws = selector_laws(2)
        self.assertGreater(len(laws), 20)
        self.assertEqual(len({law.name for law in laws}), len(laws))
        self.assertIn(SelectorLaw("lanes", 2, 0), laws)

    def test_toggle_timing_and_lane_state_are_explicit(self) -> None:
        ranks = (2, 3, 4, 5)
        before = SelectorLaw("toggle", 2, 0, (0, 1), 1, True)
        after = SelectorLaw("toggle", 2, 0, (0, 1), 1, False)
        self.assertNotEqual(
            decode_selector_walk(ranks, 11, before),
            decode_selector_walk(ranks, 11, after),
        )
        lanes = decode_selector_walk(
            ranks, 11, SelectorLaw("lanes", 2, 0)
        )
        self.assertEqual(len(lanes), len(ranks))

    def test_best_render_recovers_a_ring_rotation(self) -> None:
        alphabet = "ABCD "
        training = "ABCD ABCD " * 100
        model = CaseNgrams.train(training, alphabet, order=3)
        text = "ABCD ABCD "
        shifted = tuple((alphabet.index(character) + 2) % len(alphabet) for character in text)
        rendered = best_affine_render(
            (shifted,),
            alphabet,
            model,
            independent_portion_shifts=True,
        )
        self.assertEqual(rendered.texts, (text,))

    def test_random_walk_stays_in_ring(self) -> None:
        rng = random.Random(8)
        ranks = tuple(rng.randrange(57) for _ in range(200))
        for law in selector_laws(3):
            values = decode_selector_walk(ranks, 31, law)
            self.assertTrue(all(value in range(31) for value in values))


if __name__ == "__main__":
    unittest.main()
