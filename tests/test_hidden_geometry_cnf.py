from __future__ import annotations

import unittest

from eye_mystery.hidden_geometry_cnf import (
    pysat_available,
    solve_hidden_geometry_cnf,
)
from eye_mystery.hidden_geometry_pairs import (
    planted_sat_pair,
    split_equidistant_triangle,
)


@unittest.skipUnless(
    pysat_available(),
    "optional python-sat package is unavailable",
)
class HiddenGeometryCNFTests(unittest.TestCase):
    def test_recovers_each_fragment_and_union_of_sat_pair(self) -> None:
        left, right = planted_sat_pair()
        for constraints in (left, right, left + right):
            with self.subTest(constraints=len(constraints)):
                result = solve_hidden_geometry_cnf(constraints, modulus=7)
                self.assertEqual(result.outcome, "sat")
                self.assertEqual(
                    len({coordinate for _, coordinate in result.coordinates}),
                    result.labels,
                )

    def test_split_triangle_is_only_jointly_unsat(self) -> None:
        left, right = split_equidistant_triangle()
        self.assertEqual(
            solve_hidden_geometry_cnf(left, modulus=5).outcome,
            "sat",
        )
        self.assertEqual(
            solve_hidden_geometry_cnf(right, modulus=5).outcome,
            "sat",
        )
        self.assertEqual(
            solve_hidden_geometry_cnf(left + right, modulus=5).outcome,
            "unsat",
        )

    def test_injection_rejects_forced_duplicate_coordinates(self) -> None:
        constraints = planted_sat_pair()[0]
        result = solve_hidden_geometry_cnf(
            constraints,
            modulus=7,
            fixed_coordinates={2: 0},
        )
        self.assertEqual(result.outcome, "unsat")


if __name__ == "__main__":
    unittest.main()
