import unittest

from eye_mystery.practice_cipher3_signed_path import (
    decode_signed_path,
    make_signed_path_plant,
    solve_signed_path,
)


LENGTHS = (
    57,
    65,
    57,
    66,
    66,
    67,
    115,
    117,
    126,
    111,
    115,
    120,
    188,
    191,
    192,
    185,
    215,
    194,
)


class PracticeCipher3SignedPathTests(unittest.TestCase):
    def test_full_plant_is_satisfiable_and_replays(self) -> None:
        messages, _, _ = make_signed_path_plant(LENGTHS, "full")
        result = solve_signed_path(messages, "full")
        self.assertEqual(result.status, "sat")
        self.assertIsNotNone(result.mapping)
        self.assertIsNotNone(result.plaintexts)
        self.assertIsNotNone(
            decode_signed_path(messages, result.mapping or (), "full")
        )

    def test_primer_plant_is_satisfiable_and_replays(self) -> None:
        messages, _, _ = make_signed_path_plant(LENGTHS, "primer")
        result = solve_signed_path(messages, "primer")
        self.assertEqual(result.status, "sat")
        self.assertIsNotNone(result.mapping)
        self.assertIsNotNone(result.starts)
        self.assertIsNotNone(result.plaintexts)
        self.assertIsNotNone(
            decode_signed_path(
                messages,
                result.mapping or (),
                "primer",
                starts=result.starts,
            )
        )


if __name__ == "__main__":
    unittest.main()
