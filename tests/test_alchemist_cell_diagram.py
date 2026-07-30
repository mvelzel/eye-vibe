import unittest
from pathlib import Path

from eye_mystery.alchemist_cell_diagram import (
    DiagramVariant,
    decimal_text,
    hexadecimal_text,
    lower_tape,
    orient_records,
    parse_alchemist_diagram,
    sorted_direction_table,
    upper_permutation,
)


ASSET = (
    Path(__file__).parents[1]
    / "artifacts"
    / "alchemist-cell-diagram"
    / "raw"
    / "alchemist_secret_background.png"
)


class AlchemistCellDiagramTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.diagram = parse_alchemist_diagram(ASSET)

    def test_exact_authored_records(self) -> None:
        self.assertEqual(
            upper_permutation(self.diagram, DiagramVariant(False, False)),
            (4, 2, 1, 6, 5, 7, 0, 3),
        )
        self.assertEqual(
            lower_tape(self.diagram, DiagramVariant(False, False)),
            (4, 2, 4, 3, 0, 2, 4, 1),
        )
        self.assertEqual(
            sorted_direction_table(self.diagram, DiagramVariant(False, False)),
            (4, 4, 2, 1, 4, 0, 3, 2),
        )

    def test_rows_alternate_in_opposite_phases(self) -> None:
        records = orient_records(self.diagram, DiagramVariant(False, False))
        self.assertEqual(tuple(record.top_row for record in records), (0, 1) * 4)
        self.assertEqual(tuple(record.bottom_row for record in records), (1, 0) * 4)

    def test_complete_cell_indices_have_hex_and_decimal_readings(self) -> None:
        variant = DiagramVariant(False, False)
        self.assertEqual(hexadecimal_text(self.diagram, variant), "4A1E5F0B")
        self.assertEqual(decimal_text(self.diagram, variant), "92935291")
        self.assertEqual(
            hexadecimal_text(
                self.diagram, variant, linearization="column-major"
            ),
            "852DAF07",
        )
        self.assertEqual(
            decimal_text(self.diagram, variant, linearization="column-major"),
            "94961492",
        )

    def test_frozen_global_reflections(self) -> None:
        reflected = DiagramVariant(reverse_groups=True, reverse_columns=True)
        self.assertEqual(
            upper_permutation(self.diagram, reflected),
            (4, 7, 0, 2, 1, 6, 5, 3),
        )
        self.assertEqual(
            lower_tape(self.diagram, reflected),
            (3, 0, 2, 4, 1, 0, 2, 0),
        )
        self.assertEqual(
            sorted_direction_table(self.diagram, reflected),
            (2, 1, 4, 0, 3, 2, 0, 0),
        )

    def test_row_complement_changes_no_numeric_output(self) -> None:
        plain = DiagramVariant(False, False, False)
        complemented = DiagramVariant(False, False, True)
        self.assertEqual(lower_tape(self.diagram, plain), lower_tape(self.diagram, complemented))
        self.assertEqual(
            upper_permutation(self.diagram, plain),
            upper_permutation(self.diagram, complemented),
        )
        self.assertEqual(
            sorted_direction_table(self.diagram, plain),
            sorted_direction_table(self.diagram, complemented),
        )


if __name__ == "__main__":
    unittest.main()
