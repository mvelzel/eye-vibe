from __future__ import annotations

import unittest

from eye_mystery.paley_projection import (
    RepeatContext,
    best_binary_text_fit,
    complement_fit,
    grouped_values,
    legendre_bit,
    transition_bits,
)


class PaleyProjectionTests(unittest.TestCase):
    def test_negation_flips_character_modulo_83(self) -> None:
        for value in range(1, 83):
            self.assertEqual(legendre_bit(value) ^ legendre_bit(-value), 1)

    def test_transition_projection_rejects_doubles(self) -> None:
        with self.assertRaises(ValueError):
            transition_bits((4, 4))
        self.assertEqual(transition_bits((0, 1, 0)), (0, 1))

    def test_drop_header_omits_only_first_edge(self) -> None:
        values = (7, 0, 1, 2)
        self.assertEqual(transition_bits(values, drop_header=True), (0, 0))
        self.assertEqual(transition_bits(values)[1:], (0, 0))

    def test_complement_fit_accepts_reversed_differences(self) -> None:
        streams = {"a": (0, 1, 3, 7), "b": (10, 9, 7, 3)}
        result = complement_fit(
            streams,
            (RepeatContext("reverse", 4, (("a", 0), ("b", 0))),),
        )
        self.assertEqual((result.matches, result.comparisons), (3, 3))
        self.assertEqual(result.exact_occurrences, 1)

    def test_fixed_width_groups_support_bit_endianness(self) -> None:
        bits = (1, 0, 0, 0, 0, 0, 1)
        self.assertEqual(grouped_values(bits, 7), (65,))
        self.assertEqual(grouped_values(bits, 7, least_significant_first=True), (65,))

    def test_binary_text_scan_finds_plain_ascii_fixture(self) -> None:
        # Squares encode zero and non-squares encode one.  Prefixing a zero
        # vertex realizes the requested bit differences cumulatively.
        target = tuple(int(bit) for char in b"ABC" for bit in f"{char:08b}")
        square = 1
        nonsquare = next(value for value in range(1, 83) if legendre_bit(value) == 1)
        stream = [0]
        for bit in target:
            stream.append((stream[-1] + (nonsquare if bit else square)) % 83)
        fit = best_binary_text_fit({"x": tuple(stream)}, {"only": ("x",)})
        self.assertEqual(fit.rate, 1.0)


if __name__ == "__main__":
    unittest.main()
