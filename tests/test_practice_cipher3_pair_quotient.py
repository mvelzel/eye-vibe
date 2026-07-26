import random
import unittest

from eye_mystery.practice_cipher3_pair_quotient import (
    PROJECTIVE_SLOPES,
    ROUTES,
    EqualityPatternModel,
    PairArchitecture,
    decode_with_key,
    encode_pair_streams,
    equality_pattern,
    pair_positions,
    quotient_pair_streams,
)


class PracticeCipher3PairQuotientTests(unittest.TestCase):
    def test_frozen_catalog_has_34860_architectures(self) -> None:
        self.assertEqual(len(ROUTES), 5)
        self.assertEqual(len(PROJECTIVE_SLOPES), 84)
        self.assertEqual(len(ROUTES) * len(PROJECTIVE_SLOPES) * 83, 34_860)

    def test_equality_pattern_is_substitution_invariant(self) -> None:
        values = (9, 4, 9, 7, 4, 4)
        substituted = (81, 12, 81, 2, 12, 12)
        self.assertEqual(
            equality_pattern(values),
            (0, 1, 0, 2, 1, 1),
        )
        self.assertEqual(
            equality_pattern(values),
            equality_pattern(substituted),
        )
        model = EqualityPatternModel.train(
            "ABACABADABACABA " * 20,
            width=6,
        )
        self.assertEqual(
            model.score((values,)),
            model.score((substituted,)),
        )

    def test_likelihood_ratio_prefers_planted_equality_grammar(self) -> None:
        model = EqualityPatternModel.train(
            "ABRACADABRA ABRACADABRA " * 100,
            width=6,
        )
        planted = tuple(
            (0, 1, 2, 0, 3, 0, 4, 0, 1, 2, 0, 5) * 20
        )
        all_distinct = tuple(index % 42 for index in range(len(planted)))
        planted_score, _ = model.score((planted,))
        random_score, _ = model.score((all_distinct,))
        self.assertGreater(planted_score, random_score)

    def test_every_route_encodes_and_decodes_exactly(self) -> None:
        rng = random.Random(19)
        key = list(range(42))
        rng.shuffle(key)
        for route_index, route in enumerate(ROUTES):
            with self.subTest(route=route):
                architecture = PairArchitecture(
                    route,
                    37,
                    (11 + route_index) % 83,
                )
                raw_lengths = (17, 18, 21)
                plaintexts = tuple(
                    tuple(
                        (7 * index + message_index) % 42
                        for index in range(len(pair_positions(length, route)))
                    )
                    for message_index, length in enumerate(raw_lengths)
                )
                ciphertexts = encode_pair_streams(
                    plaintexts,
                    raw_lengths,
                    architecture,
                    key,
                    seed=100 + route_index,
                )
                decoded = decode_with_key(
                    quotient_pair_streams(ciphertexts, architecture),
                    key,
                )
                self.assertEqual(decoded, plaintexts)

    def test_zero_and_infinite_slopes_round_trip(self) -> None:
        route = ROUTES[0]
        key = tuple((17 * value + 3) % 42 for value in range(42))
        plaintexts = (tuple(range(20)),)
        raw_lengths = (21,)
        for slope in (0, None):
            with self.subTest(slope=slope):
                architecture = PairArchitecture(route, slope, 52)
                ciphertexts = encode_pair_streams(
                    plaintexts,
                    raw_lengths,
                    architecture,
                    key,
                    seed=91,
                )
                self.assertEqual(
                    decode_with_key(
                        quotient_pair_streams(ciphertexts, architecture),
                        key,
                    ),
                    plaintexts,
                )


if __name__ == "__main__":
    unittest.main()
