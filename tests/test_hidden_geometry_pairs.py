from __future__ import annotations

import unittest

from eye_mystery.hidden_geometry import chord_constraints, z3_available
from eye_mystery.hidden_geometry_pairs import (
    CONTEXT_NAMES,
    canonical_context_pairs,
    pair_constraints,
    planted_sat_pair,
    solve_control_fragments,
    split_equidistant_triangle,
)


class HiddenGeometryPairInventoryTests(unittest.TestCase):
    def test_canonical_census_contains_every_unordered_pair_once(self) -> None:
        pairs = canonical_context_pairs()
        self.assertEqual(len(pairs), 21)
        self.assertEqual(len(set(pairs)), 21)
        self.assertEqual(
            {frozenset(pair) for pair in pairs},
            {
                frozenset((left, right))
                for index, left in enumerate(CONTEXT_NAMES)
                for right in CONTEXT_NAMES[index + 1 :]
            },
        )

    def test_pair_constraints_are_exact_union_of_named_contexts(self) -> None:
        left, right = canonical_context_pairs()[0]
        constraints = pair_constraints(left, right)
        self.assertEqual({item.context for item in constraints}, {left, right})
        self.assertEqual(
            len(constraints),
            len(chord_constraints(names=(left,)))
            + len(chord_constraints(names=(right,))),
        )

    def test_rejects_duplicate_or_unknown_names(self) -> None:
        with self.assertRaisesRegex(ValueError, "different"):
            pair_constraints(CONTEXT_NAMES[0], CONTEXT_NAMES[0])
        with self.assertRaisesRegex(ValueError, "unknown"):
            pair_constraints(CONTEXT_NAMES[0], "not-a-context")


@unittest.skipUnless(z3_available(), "optional z3 package is unavailable")
class HiddenGeometryPairControlTests(unittest.TestCase):
    def test_planted_pair_is_jointly_sat_in_both_encodings(self) -> None:
        outcomes = solve_control_fragments(planted_sat_pair(), modulus=7)
        self.assertEqual(
            tuple(
                (integer.outcome, bitvector.outcome)
                for integer, bitvector in outcomes
            ),
            (("sat", "sat"), ("sat", "sat"), ("sat", "sat")),
        )

    def test_split_triangle_is_only_jointly_unsat(self) -> None:
        outcomes = solve_control_fragments(
            split_equidistant_triangle(),
            modulus=5,
        )
        self.assertEqual(
            tuple(
                (integer.outcome, bitvector.outcome)
                for integer, bitvector in outcomes
            ),
            (("sat", "sat"), ("sat", "sat"), ("unsat", "unsat")),
        )


if __name__ == "__main__":
    unittest.main()
