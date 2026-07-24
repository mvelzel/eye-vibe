import unittest
from itertools import combinations

from eye_mystery.fifteenth_novel import (
    GRAY_WORDS,
    MULTISETS,
    PREFIX_SHAPES,
    GraySpec,
    PackingSpec,
    PrefixCodeSpec,
    gray_position,
    gray_score,
    default_gray_audit,
    default_tree_isometry_audit,
    lcp_depth,
    multiset_order,
    multiset_stream,
    order_stream,
    pack_complete_bits,
    prefix_bits,
    prefix_code_specs,
    reflected_gray_words,
    symbols_from_plain_bits,
    tree_isometry_score,
)
from eye_mystery.hidden_geometry import ChordConstraint


class FifteenthNovelTests(unittest.TestCase):
    def test_catalan_prefix_catalog_has_42_six_leaf_shapes(self) -> None:
        self.assertEqual(42, len(PREFIX_SHAPES))
        self.assertEqual(84, len(prefix_code_specs()))
        self.assertEqual(len(PREFIX_SHAPES), len(set(PREFIX_SHAPES)))
        for shape in PREFIX_SHAPES:
            self.assertEqual(6, len(shape))
            for left, right in combinations(shape, 2):
                self.assertFalse(
                    left == right[: len(left)]
                    or right == left[: len(right)]
                )

    def test_prefix_tree_round_trips_plain_bits(self) -> None:
        bits = tuple(
            (byte >> shift) & 1
            for byte in b"THE EYE MESSAGE "
            for shift in reversed(range(8))
        )
        spec = PrefixCodeSpec(17, "header")
        symbols = symbols_from_plain_bits(
            bits,
            40,
            spec,
            maximum_symbols=40,
        )
        decoded = prefix_bits(symbols, 40, spec)
        self.assertEqual(bits[: len(decoded)], decoded)
        packed = pack_complete_bits(
            decoded,
            PackingSpec(8, 0, False),
        )
        self.assertEqual(tuple(b"THE EYE MESSAGE ")[: len(packed)], packed)

    def test_multiset_and_order_factor_complete_cube(self) -> None:
        self.assertEqual(35, len(MULTISETS))
        observed = {multiset_order(value)[0] for value in range(125)}
        accepted = {multiset_order(value)[0] for value in range(83)}
        self.assertEqual(set(range(35)), observed)
        self.assertEqual(31, len(accepted))
        values = (0, 1, 5, 7, 25, 31, 51, 82)
        self.assertEqual(len(values), len(multiset_stream(values)))
        self.assertEqual(len(values), len(order_stream(values)))
        self.assertTrue(all(value in range(6) for value in order_stream(values)))

    def test_lcp_depth_uses_the_selected_component_order(self) -> None:
        left = 25 * 1 + 5 * 2 + 3
        right = 25 * 1 + 5 * 4 + 3
        self.assertEqual(1, lcp_depth(left, right, (0, 1, 2)))
        self.assertEqual(2, lcp_depth(left, right, (2, 0, 1)))

    def test_conditional_tree_automorphism_preserves_target_ultrametric(self) -> None:
        order = (2, 0, 1)

        def transform(value: int) -> int:
            source = value // 25, value // 5 % 5, value % 5
            target = [0, 0, 0]
            prefix = ()
            for level, component in enumerate(order):
                target[component] = (
                    source[component] + sum(prefix) + level + 1
                ) % 5
                prefix = (*prefix, source[component])
            return 25 * target[0] + 5 * target[1] + target[2]

        source = tuple(range(125))
        target = tuple(transform(value) for value in source)
        score = tree_isometry_score((("plant", source, target),), order)
        self.assertTrue(score.exact)
        damaged = (*target[:-1], target[-2])
        with self.assertRaises(ValueError):
            tree_isometry_score((("damaged", source, damaged),), order)

    def test_reflected_gray_words_form_a_hamiltonian_grid_path(self) -> None:
        self.assertEqual(125, len(GRAY_WORDS))
        self.assertEqual(125, len(set(GRAY_WORDS)))
        self.assertEqual(GRAY_WORDS, reflected_gray_words(3, 5))
        for left, right in zip(GRAY_WORDS, GRAY_WORDS[1:]):
            differences = [
                abs(a - b) for a, b in zip(left, right, strict=True)
            ]
            self.assertEqual(1, differences.count(1))
            self.assertEqual(2, differences.count(0))

    def test_circular_gray_translation_preserves_adjacent_chords(self) -> None:
        spec = GraySpec((2, 0, 1), 0b101, "circular")
        by_position = {
            gray_position(value, spec): value for value in range(125)
        }
        positions = (2, 7, 18, 33, 61, 93, 121)
        source = tuple(by_position[position] for position in positions)
        target = tuple(by_position[(position + 17) % 125] for position in positions)
        constraints = tuple(
            ChordConstraint(
                "plant",
                1,
                index,
                source[index],
                source[index + 1],
                target[index],
                target[index + 1],
            )
            for index in range(len(source) - 1)
        )
        self.assertTrue(gray_score(constraints, spec).exact)

    def test_eye_tree_isometry_result_is_frozen(self) -> None:
        audit = default_tree_isometry_audit()
        self.assertEqual((1, 2, 0), audit.selected_order)
        self.assertEqual((171, 249), (
            audit.train.agreements,
            audit.train.comparisons,
        ))
        self.assertEqual((573, 831), (
            audit.heldout.agreements,
            audit.heldout.comparisons,
        ))
        self.assertFalse(audit.train.exact)
        self.assertFalse(audit.heldout.exact)

    def test_eye_gray_result_is_frozen(self) -> None:
        audit = default_gray_audit()
        self.assertEqual(
            GraySpec((2, 1, 0), 0, "circular"),
            audit.selected,
        )
        self.assertEqual((3, 59), (
            audit.train.agreements,
            audit.train.comparisons,
        ))
        self.assertEqual((3, 82), (
            audit.heldout.agreements,
            audit.heldout.comparisons,
        ))
        self.assertFalse(audit.train.exact)
        self.assertFalse(audit.heldout.exact)


if __name__ == "__main__":
    unittest.main()
