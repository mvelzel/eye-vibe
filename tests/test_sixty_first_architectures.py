import random
import unittest

from eye_mystery.sixty_first_architectures import (
    INCIDENCE_VARIANTS,
    PACKET_SPECS,
    TREE_LAYOUTS,
    audit_incidence_tape,
    audit_packet_family,
    audit_tree_geometry,
    decode_packet_message,
    encode_packet_message,
    incidence_rank,
    incidence_table,
    root_swap_label_map,
    tree_distance_table,
)


class SixtyFirstArchitecturesTests(unittest.TestCase):
    def test_incidence_pairings_have_41_pairs_and_one_singleton(self) -> None:
        for endpoint in ("end-singleton", "start-singleton"):
            fibers = {}
            for value in range(83):
                fibers.setdefault(incidence_rank(value, endpoint), []).append(value)
            self.assertEqual(sorted(fibers), list(range(42)))
            self.assertEqual(sum(len(fiber) == 1 for fiber in fibers.values()), 1)
            self.assertEqual(sum(len(fiber) == 2 for fiber in fibers.values()), 41)
        for endpoint, route in INCIDENCE_VARIANTS:
            for name in ("east1", "west2", "east5"):
                table = incidence_table(name, endpoint, route)
                self.assertEqual(len(table), 83)
                self.assertEqual(set(table), set(range(42)))

    def test_balanced_tree_layouts_have_83_nodes_and_root_swap_is_isometry(self) -> None:
        rng = random.Random(123)
        for layout in TREE_LAYOUTS:
            distances = tree_distance_table(layout)
            self.assertEqual(len(distances), 83)
            self.assertTrue(all(len(row) == 83 for row in distances))
            mapping = root_swap_label_map(layout)
            self.assertEqual(sorted(mapping), list(range(83)))
            for _ in range(500):
                left = rng.randrange(83)
                right = rng.randrange(83)
                self.assertEqual(
                    distances[left][right],
                    distances[mapping[left]][mapping[right]],
                )

    def test_every_packet_spec_round_trips_boundary_ranks(self) -> None:
        for spec in PACKET_SPECS:
            plaintext = tuple(
                value
                for _ in range(4)
                for value in (0, spec.size - 1, spec.size // 2)
            )
            ciphertext = encode_packet_message(plaintext, spec)
            self.assertEqual(
                decode_packet_message(ciphertext, spec),
                plaintext,
            )

    def test_real_batch_results_are_reproducible(self) -> None:
        incidence = audit_incidence_tape()
        self.assertEqual(
            (
                incidence.observed.endpoint,
                incidence.observed.route,
                incidence.observed.training_matches,
                incidence.observed.holdout_matches,
                incidence.holdout_tail_count,
                incidence.controls,
            ),
            ("end-singleton", "header", 0, 2, 3073, 6806),
        )
        tree = audit_tree_geometry()
        self.assertEqual(
            (
                tree.observed.layout,
                tree.observed.training_matches,
                tree.observed.holdout_matches,
                tree.holdout_tail_count,
                tree.controls,
            ),
            ("breadth-first", 8, 12, 944, 6806),
        )
        packets = audit_packet_family()
        self.assertEqual(packets[0].total_valid, 30)
        self.assertFalse(any(score.complete for score in packets))


if __name__ == "__main__":
    unittest.main()
