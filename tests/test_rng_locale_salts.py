from __future__ import annotations

import unittest

from eye_mystery.rng_locale_salts import scan_rng_locale_salts


class RngLocaleSaltTests(unittest.TestCase):
    def test_direct_and_traced_salts(self) -> None:
        source = """
-- SetRandomSeed(x + 683.1, y + 34.2)
function example(x, y, a, b)
  SetRandomSeed(x+2617.941, y-1229.3581)
  a = a + 509.7
  b = b + 683.1
  SetRandomSeed(a, b)
end
"""
        hits = scan_rng_locale_salts((("example.lua", source),))
        self.assertEqual(len(hits), 2)
        self.assertEqual(
            tuple(tuple(str(value) for value in arg) for arg in hits[0].salts),
            (("2617.941",), ("-1229.3581",)),
        )
        self.assertEqual(hits[1].integer_parts, ((509,), (683,)))
        self.assertEqual(hits[1].marker_codes, (683,))
        self.assertTrue(hits[1].is_geographic_pair)
        self.assertEqual(hits[1].eye_ascii_pair(), "+3")
        self.assertTrue(hits[1].is_compact_arithmetic_instruction())

    def test_trace_stops_at_other_assignment(self) -> None:
        source = """
x = x + 683.1
x = position()
SetRandomSeed(x, y)
"""
        hit = scan_rng_locale_salts((("example.lua", source),))[0]
        self.assertEqual(hit.salts, ((), ()))

    def test_multiple_or_bare_literals_are_not_geographic_pair(self) -> None:
        source = """
SetRandomSeed(x + 34 + 7, 683)
"""
        hit = scan_rng_locale_salts((("example.lua", source),))[0]
        self.assertEqual(hit.integer_parts, ((34, 7), ()))
        self.assertIsNone(hit.eye_ascii_pair())
        self.assertFalse(hit.is_geographic_pair)

    def test_multiline_call_and_nested_comma(self) -> None:
        source = """
SetRandomSeed(
  x + fn(x + 683, 2) + 358.9,
  y + 34
)
"""
        hit = scan_rng_locale_salts((("example.lua", source),))[0]
        self.assertEqual(hit.integer_parts, ((358,), (34,)))

    def test_signed_and_reversed_eye_ascii_pair(self) -> None:
        source = "SetRandomSeed(x - 509.7, y + 683.1)"
        hit = scan_rng_locale_salts((("example.lua", source),))[0]
        self.assertNotEqual(hit.eye_ascii_pair(), "+3")
        self.assertEqual(hit.eye_ascii_pair(absolute=True), "+3")
        self.assertEqual(hit.eye_ascii_pair(absolute=True, reverse=True), "3+")


if __name__ == "__main__":
    unittest.main()
