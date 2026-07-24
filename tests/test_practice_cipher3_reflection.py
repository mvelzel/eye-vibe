from __future__ import annotations

import unittest

from eye_mystery.practice_cipher3_reflection import (
    encode_reflection_messages,
    recovered_wheel_insertions,
    reciprocal_audit,
    reflection_stream,
    wheel_dihedral_match,
)
from eye_mystery.practice_cipher3_wide import load_cipher3


class PracticeCipher3ReflectionTests(unittest.TestCase):
    def test_reflection_stream_ignores_direction(self) -> None:
        coordinates = tuple(range(83))
        self.assertEqual(
            reflection_stream((0, 7, 0, 76, 0), coordinates),
            (6, 6, 6, 6),
        )

    def test_known_wheel_round_trip(self) -> None:
        wheel = tuple((17 * index + 4) % 83 for index in range(83))
        plaintexts = ((0, 1, 2, 1, 0), (2, 2, 1))
        mapping = {0: 3, 1: 11, 2: 37}
        messages = encode_reflection_messages(
            plaintexts,
            wheel,
            mapping,
            seed=9,
        )
        coordinates = [0] * 83
        for position, card in enumerate(wheel):
            coordinates[card] = position
        inverse = {magnitude - 1: value for value, magnitude in mapping.items()}
        decoded = tuple(
            tuple(inverse[magnitude] for magnitude in reflection_stream(message, coordinates))
            for message in messages
        )
        self.assertEqual(decoded, plaintexts)

    def test_wheel_dihedral_equivalence(self) -> None:
        expected = tuple(range(83))
        self.assertTrue(
            wheel_dihedral_match(
                tuple((value + 19) % 83 for value in expected),
                expected,
            )
        )
        self.assertTrue(
            wheel_dihedral_match(
                tuple((-value + 7) % 83 for value in expected),
                expected,
            )
        )

    def test_recovered_wheel_insertions_are_complete(self) -> None:
        candidates = recovered_wheel_insertions()
        self.assertEqual(len(candidates), 166)
        self.assertEqual(len({name for name, _, _ in candidates}), 166)
        self.assertTrue(
            all(
                tuple(sorted(wheel)) == tuple(range(83))
                for _name, _coordinates, wheel in candidates
            )
        )

    def test_real_reciprocal_obstruction_is_frozen(self) -> None:
        audit = reciprocal_audit(load_cipher3())
        self.assertEqual(
            (
                audit.directed_edges,
                audit.reciprocal_pairs,
                audit.maximum_reciprocal_degree,
                audit.maximum_single_direction_degree,
            ),
            (1845, 253, 14, 2),
        )


if __name__ == "__main__":
    unittest.main()
