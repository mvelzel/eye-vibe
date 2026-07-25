from __future__ import annotations

import unittest

from eye_mystery.factoradic_headers import header_ranks
from eye_mystery.gate_plus3_transfer import assignment_ranks
from eye_mystery.phase_ledger import (
    audit_phase_ledger,
    exact_ledger_match,
    phase_suffix_lengths,
    phase_sums,
    row2_circulation,
)


class PhaseLedgerTests(unittest.TestCase):
    def test_suffixes_are_derived_from_promoted_bridge(self) -> None:
        self.assertEqual(phase_suffix_lengths(), (3, 4, 3))

    def test_observed_ledger_is_exact(self) -> None:
        ranks = header_ranks()
        self.assertEqual(row2_circulation(ranks), 7)
        self.assertEqual(phase_sums(ranks), (7, 7, 7))
        self.assertTrue(exact_ledger_match(ranks))

    def test_duplicate_edge_factoradic_survivor_breaks_ledger(self) -> None:
        alternate = assignment_ranks((0, 0, 1, 2, 3, 4, 2, 1, 3))
        self.assertFalse(exact_ledger_match(alternate))

    def test_conditional_audit_is_stable(self) -> None:
        audit = audit_phase_ledger()
        self.assertEqual(
            (
                audit.assignments,
                audit.exact_matches,
                audit.exact_and_final_scalar_matches,
                audit.any_symbol_matches,
                audit.any_suffix_matches,
                audit.any_symbol_and_suffix_matches,
                audit.constant_only_matches,
                audit.constant_and_suffix_matches,
                audit.fixed_suffix_symbols,
                audit.factoradic_survivors,
            ),
            (12096, 159, 12, 159, 273, 694, 1413, 4803, (5,), 2),
        )
        self.assertEqual(
            audit.matching_factoradic_survivors,
            ((0, 0, 1, 1, 3, 4, 2, 2, 3),),
        )


if __name__ == "__main__":
    unittest.main()
