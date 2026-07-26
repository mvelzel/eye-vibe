import random
import unittest

from eye_mystery.rans_358 import (
    LOWER_BOUND,
    QuasiUniformTable,
    decode_rans,
    encode_rans,
    eye_rans_audit,
)


class Rans358Tests(unittest.TestCase):
    def test_both_quasiuniform_tables_round_trip(self) -> None:
        rng = random.Random(358)
        symbols = tuple(rng.randrange(42) for _ in range(100))
        for singleton in ("first", "last"):
            table = QuasiUniformTable(singleton)
            initial, digits = encode_rans(symbols, 100, table)
            decoded = decode_rans(
                digits,
                initial,
                table,
                maximum_symbols=len(symbols),
            )
            self.assertEqual(decoded.symbols, symbols)
            self.assertEqual(decoded.terminal_state, 100)
            self.assertEqual(decoded.consumed_digits, len(digits))

    def test_initial_states_cover_four_header_quotients(self) -> None:
        for quotient in range(1, 5):
            for header in range(83):
                state = quotient * 83 + header
                self.assertGreaterEqual(state, LOWER_BOUND)
                self.assertLess(state, 5 * LOWER_BOUND)

    def test_eye_contexts_reject_the_standard_family(self) -> None:
        results = eye_rans_audit()
        self.assertEqual(len(results), 16)
        self.assertEqual(max(result.literal_matches for result in results), 6)
        self.assertEqual(
            {result.compared for result in results},
            {185, 187, 189},
        )
        self.assertEqual(max(result.common_prefix for result in results), 0)
        self.assertEqual(
            max(result.pattern_equal_contexts for result in results),
            0,
        )


if __name__ == "__main__":
    unittest.main()
