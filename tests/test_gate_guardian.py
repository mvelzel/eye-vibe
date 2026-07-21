from fractions import Fraction
import unittest

from PIL import Image

from scripts.analyze_gate_guardian import (
    AXES,
    checksum_grid,
    circular_magnitude,
    connected_components,
    fixed_axis_probability,
    natural_assembly,
    reflection_total,
)


class GateGuardianTests(unittest.TestCase):
    def test_checksum_reflections_reproduce_gate_theory_numbers(self) -> None:
        grid = checksum_grid()

        self.assertEqual(grid, (0, 84, 7, 53, 0, 1, 32, 88, 0))
        self.assertEqual(
            reflection_total(grid, AXES["main-diagonal"]),
            ((31, 25, 14), 70),
        )
        self.assertEqual(reflection_total(grid, AXES["anti-diagonal"])[1], 53)
        self.assertEqual(reflection_total(grid, AXES["horizontal"])[1], 43)
        self.assertEqual(reflection_total(grid, AXES["vertical"])[1], 88)

    def test_circular_magnitude_wraps_mod_101(self) -> None:
        self.assertEqual(circular_magnitude(84, 53), 31)
        self.assertEqual(circular_magnitude(1, 88), 14)

    def test_fixed_axis_probability_is_exact(self) -> None:
        self.assertEqual(fixed_axis_probability(70), Fraction(15036, 101**3))

    def test_connected_components_respects_diagonal_choice(self) -> None:
        points = {(0, 0), (1, 1), (4, 4)}

        self.assertEqual(sorted(map(len, connected_components(points))), [1, 2])
        self.assertEqual(
            sorted(map(len, connected_components(points, diagonals=False))),
            [1, 1, 1],
        )

    def test_natural_assembly_uses_authored_dimensions(self) -> None:
        images = {
            "Veska": Image.new("RGBA", (52, 66)),
            "Molari": Image.new("RGBA", (37, 71)),
            "Mokke": Image.new("RGBA", (37, 71)),
            "Seula": Image.new("RGBA", (57, 55)),
        }

        assembly, positions = natural_assembly(images)

        self.assertEqual(assembly.size, (126, 121))
        self.assertEqual(
            positions,
            {
                "Molari": (0, 50),
                "Veska": (37, 55),
                "Mokke": (89, 50),
                "Seula": (34, 0),
            },
        )


if __name__ == "__main__":
    unittest.main()
