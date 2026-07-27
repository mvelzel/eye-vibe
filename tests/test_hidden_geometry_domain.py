from __future__ import annotations

import unittest

from eye_mystery.hidden_geometry_domain import solve_hidden_geometry_domain
from eye_mystery.hidden_geometry_pairs import (
    planted_sat_pair,
    split_equidistant_star,
    split_equidistant_triangle,
)


class HiddenGeometryDomainTests(unittest.TestCase):
    def test_recovers_jointly_sat_pair(self) -> None:
        left, right = planted_sat_pair()
        result = solve_hidden_geometry_domain(
            left + right,
            modulus=7,
            timeout_ms=5_000,
        )
        self.assertEqual(result.outcome, "sat")
        self.assertEqual(
            len({coordinate for _, coordinate in result.coordinates}),
            result.labels,
        )

    def test_rejects_injection_only_star(self) -> None:
        left, right = split_equidistant_star()
        self.assertEqual(
            solve_hidden_geometry_domain(
                left,
                modulus=5,
                timeout_ms=5_000,
            ).outcome,
            "sat",
        )
        self.assertEqual(
            solve_hidden_geometry_domain(
                right,
                modulus=5,
                timeout_ms=5_000,
            ).outcome,
            "sat",
        )
        self.assertEqual(
            solve_hidden_geometry_domain(
                left + right,
                modulus=5,
                timeout_ms=5_000,
            ).outcome,
            "unsat",
        )

    def test_rejects_algebraic_triangle(self) -> None:
        left, right = split_equidistant_triangle()
        self.assertEqual(
            solve_hidden_geometry_domain(
                left + right,
                modulus=5,
                timeout_ms=5_000,
            ).outcome,
            "unsat",
        )


if __name__ == "__main__":
    unittest.main()
