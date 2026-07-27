from __future__ import annotations

import unittest

from eye_mystery.hidden_geometry import z3_available
from eye_mystery.hidden_geometry import solve_hidden_geometry
from eye_mystery.hidden_geometry_lazy import (
    solve_hidden_geometry_lazy_injection,
)
from eye_mystery.hidden_geometry_pairs import (
    planted_sat_pair,
    split_equidistant_star,
)


@unittest.skipUnless(z3_available(), "optional z3 package is unavailable")
class HiddenGeometryLazyInjectionTests(unittest.TestCase):
    def test_recovers_jointly_sat_pair_with_injection(self) -> None:
        left, right = planted_sat_pair()
        result = solve_hidden_geometry_lazy_injection(
            left + right,
            modulus=7,
            timeout_ms=5_000,
        )
        self.assertEqual(result.outcome, "sat")
        self.assertEqual(
            len({coordinate for _, coordinate in result.coordinates}),
            result.labels,
        )

    def test_split_star_is_unsat_only_after_injection_cuts(self) -> None:
        left, right = split_equidistant_star()
        self.assertEqual(
            solve_hidden_geometry_lazy_injection(
                left,
                modulus=5,
                timeout_ms=5_000,
            ).outcome,
            "sat",
        )
        self.assertEqual(
            solve_hidden_geometry_lazy_injection(
                right,
                modulus=5,
                timeout_ms=5_000,
            ).outcome,
            "sat",
        )
        self.assertEqual(
            solve_hidden_geometry(
                left + right,
                modulus=5,
                timeout_ms=5_000,
                injective=False,
            ).outcome,
            "sat",
        )
        result = solve_hidden_geometry_lazy_injection(
            left + right,
            modulus=5,
            timeout_ms=5_000,
        )
        self.assertEqual(result.outcome, "unsat")
        self.assertGreater(result.collision_cuts, 0)


if __name__ == "__main__":
    unittest.main()
