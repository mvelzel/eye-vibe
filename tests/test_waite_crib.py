import unittest

from eye_mystery.corpus import MESSAGES, trigram_values
from scripts.check_waite_m3_suffix import (
    EAST2_RAW_OFFSET,
    WAITE_M3_SUFFIX,
    repeated_substring_checks,
)


class WaiteCribTests(unittest.TestCase):
    def test_suffix_fills_east2_exactly(self) -> None:
        east2 = trigram_values(MESSAGES["east2"])
        self.assertEqual(len(WAITE_M3_SUFFIX), 81)
        self.assertEqual(EAST2_RAW_OFFSET + len(WAITE_M3_SUFFIX), len(east2))

    def test_repeated_substrings_are_isomorph_compatible(self) -> None:
        east2 = trigram_values(MESSAGES["east2"])[EAST2_RAW_OFFSET:]
        checks = repeated_substring_checks(WAITE_M3_SUFFIX, east2)
        self.assertTrue(checks)
        self.assertTrue(all(item.compatible for item in checks))

        longest = max(checks, key=lambda item: item.length)
        self.assertEqual(longest.text, "E THAT WHICH IS THE ")
        self.assertEqual(longest.length, 20)
        self.assertEqual((longest.first, longest.second), (6, 41))


if __name__ == "__main__":
    unittest.main()
