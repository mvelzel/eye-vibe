import unittest
from fractions import Fraction

from eye_mystery.header_packet_cardinality import (
    CHECKSUM_FAMILY,
    all_triple_hits,
    audit_count_assignments,
    exact_cardinality_ledger,
    full_slot_probability,
    natural_diagonal_probability,
    observed_rows,
    sparse_packet_matrix,
)


class HeaderPacketCardinalityTests(unittest.TestCase):
    def test_observed_ledger_closes(self) -> None:
        rows = observed_rows()
        self.assertEqual(
            tuple(
                (
                    row.name,
                    row.edge,
                    row.source_indegree,
                    row.packet_count,
                    row.closes,
                )
                for row in rows
            ),
            (
                ("east1", (0, 1), 1, 2, True),
                ("east3", (2, 1), 0, 3, True),
                ("east5", (1, 0), 2, 1, True),
            ),
        )
        self.assertTrue(exact_cardinality_ledger(CHECKSUM_FAMILY))

    def test_count_assignment_audit_is_reproducible(self) -> None:
        audit = audit_count_assignments()
        self.assertEqual(
            (
                audit.assignments,
                audit.exact_hits,
                audit.broad_hits,
                audit.exact_assignments,
                audit.broad_assignments,
            ),
            (6, 1, 2, ((2, 3, 1),), ((2, 3, 1), (2, 1, 3))),
        )
        self.assertEqual(
            tuple(
                (
                    hit.endpoint,
                    hit.degree_direction,
                    hit.orientation,
                )
                for hit in audit.observed_formula_hits
            ),
            (("source", "in", "three-minus"),),
        )

    def test_all_triple_calibration_is_reproducible(self) -> None:
        hits = all_triple_hits()
        self.assertEqual(
            tuple(
                (hit.names, hit.counts, hit.remainders, hit.all_close)
                for hit in hits
            ),
            (
                (
                    ("east1", "west2", "west3"),
                    (2, 2, 2),
                    (0, 53, 1),
                    False,
                ),
                (
                    ("east1", "east3", "east5"),
                    (2, 3, 1),
                    (0, 0, 0),
                    True,
                ),
            ),
        )

    def test_sparse_matrix_uses_every_packet_value_once(self) -> None:
        self.assertEqual(
            sparse_packet_matrix(),
            (
                (13, 7, None),
                (11, 13, 21),
                (None, None, 30),
            ),
        )

    def test_diagonal_position_controls_are_reproducible(self) -> None:
        self.assertEqual(
            natural_diagonal_probability(frozenset((56,))),
            Fraction(187280803, 11011398678),
        )
        self.assertEqual(
            natural_diagonal_probability(frozenset((40, 56, 45))),
            Fraction(1077567439, 27528496695),
        )
        self.assertEqual(
            full_slot_probability(),
            Fraction(4447356527, 24469774840),
        )


if __name__ == "__main__":
    unittest.main()
