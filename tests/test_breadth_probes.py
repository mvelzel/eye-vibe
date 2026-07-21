from __future__ import annotations

import unittest
from collections import Counter

from eye_mystery.blood_sieve import split_row_pair_values
from eye_mystery.breadth_probes import (
    best_affine_step_translation,
    reuse_stack_distances,
)
from eye_mystery.conformance_grid import marker_control_edge
from eye_mystery.corpus import (
    MESSAGES,
    MESSAGE_ORDER,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)


class BreadthProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }
        cls.bodies = {name: stream[1:] for name, stream in cls.streams.items()}

    def test_complete_rows_are_not_substitution_permutations(self) -> None:
        rows = tuple(
            row
            for name in MESSAGE_ORDER
            for row in split_row_pair_values(
                MESSAGES[name], ROW_PAIR_TRIGRAM_LENGTHS[name]
            )
            if len(row) == 26
        )
        counts = Counter(len(set(row)) for row in rows)
        self.assertEqual(len(rows), 34)
        self.assertEqual(
            counts,
            Counter({22: 11, 21: 9, 23: 6, 24: 3, 20: 2, 25: 2, 19: 1}),
        )
        self.assertEqual(counts[26], 0)

    def test_small_cache_does_not_cover_most_repeats(self) -> None:
        distances = tuple(
            distance
            for name in MESSAGE_ORDER
            for distance in reuse_stack_distances(self.bodies[name])
        )
        self.assertEqual(len(distances), 469)
        self.assertEqual(sum(value <= 8 for value in distances), 105)
        self.assertEqual(max(distances), 66)

    def test_simple_affine_z101_walk_does_not_collapse(self) -> None:
        self.assertEqual(
            best_affine_step_translation(tuple(self.bodies.values()), modulus=101),
            (582, 80, (60, 61, 66, 63, 76, 64, 67, 64, 61)),
        )

    def test_repeated_control_edges_do_not_have_fixed_residue(self) -> None:
        residues: dict[tuple[int, int], list[int]] = {}
        for name in MESSAGE_ORDER:
            stream = self.streams[name]
            residues.setdefault(marker_control_edge(stream[0]), []).append(
                sum(stream) % 101
            )
        self.assertEqual(residues[(0, 2)], [53, 88])
        self.assertEqual(residues[(1, 0)], [1, 0])


if __name__ == "__main__":
    unittest.main()
