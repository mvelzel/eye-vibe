import random
import unittest

from eye_mystery.wide_complements import (
    best_header_feature_rule,
    best_tape_dependence,
    context_determinism,
    exclusion_rank,
    exclusion_ranks,
    primitive_roots_f83,
    reflection_log_orbit,
    reflection_log_quotient,
    reflection_orbit,
    reflection_quotient,
    rolling_reflection_quotient,
)


class WideComplementTests(unittest.TestCase):
    def test_reflection_quotient_has_42_classes_on_z83(self) -> None:
        values = reflection_quotient(tuple(range(83)), 17)
        self.assertEqual(set(values), set(range(42)))
        self.assertEqual(reflection_orbit(18, 17), 1)
        self.assertEqual(reflection_orbit(16, 17), 1)
        self.assertEqual(rolling_reflection_quotient((17, 18, 16)), (1, 2))

    def test_multiplicative_reflection_quotient_has_42_classes(self) -> None:
        generator = primitive_roots_f83()[0]
        values = reflection_log_quotient(tuple(range(83)), 17, generator)
        self.assertEqual(set(values), set(range(42)))
        self.assertEqual(
            reflection_log_orbit(18, 17, generator),
            reflection_log_orbit(16, 17, generator),
        )

    def test_exclusion_rank_is_a_bijection_after_removing_current(self) -> None:
        ranks = [exclusion_rank(23, value) for value in range(83) if value != 23]
        self.assertEqual(ranks, list(range(82)))
        self.assertEqual(exclusion_ranks((23, 22, 24)), (22, 23))

    def test_context_determinism_recovers_a_second_order_rule(self) -> None:
        stream = (0, 1, 1, 2, 3, 5, 8, 13)
        result = context_determinism((stream,), 2)
        self.assertEqual(result.conflicting_contexts, 0)
        self.assertEqual(result.accuracy, 1.0)

    def test_delayed_tape_probe_finds_a_planted_copy(self) -> None:
        rng = random.Random(7)
        first = tuple(rng.randrange(5) for _ in range(200))
        second = (4, 4) + first[:-2]
        third = (1,) * len(first)
        stream = tuple(25 * a + 5 * b + c for a, b, c in zip(first, second, third))
        result = best_tape_dependence((stream,), maximum_lag=3)
        self.assertGreater(result.information, 2.2)
        self.assertEqual(abs(result.lag), 2)

    def test_header_feature_search_recovers_a_signed_offset(self) -> None:
        streams = {"a": (8, 1), "b": (10, 2), "c": (12, 3)}
        features = {
            "a": {"length": 3},
            "b": {"length": 5},
            "c": {"length": 7},
        }
        result = best_header_feature_rule(streams, features, moduli=(83,))
        self.assertEqual(result.matches, 3)
        self.assertEqual((result.sign, result.offset), (1, 5))


if __name__ == "__main__":
    unittest.main()
