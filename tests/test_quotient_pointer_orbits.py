import random
import unittest
from collections import Counter

from eye_mystery.corpus import MESSAGE_ORDER
from eye_mystery.quotient_pointer_orbits import (
    CHECKSUM_FAMILY,
    TABLE_SIZE,
    FunctionalOrbit,
    PanelOrbit,
    canonical_signature,
    common_window_signatures,
    conditioned_table_spec,
    functional_orbit,
    panel_orbit,
    sample_conditioned_table,
    signature,
)


class QuotientPointerOrbitTests(unittest.TestCase):
    @staticmethod
    def _planted_orbit(
        path: tuple[int, ...],
        split: int,
    ) -> FunctionalOrbit:
        table = list(range(TABLE_SIZE))
        for left, right in zip(path, path[1:]):
            table[left] = right
        table[path[-1]] = path[split]
        return functional_orbit(table, path[0])

    def test_functional_orbit_splits_tail_and_cycle(self) -> None:
        orbit = functional_orbit((1, 2, 2), 0)
        self.assertEqual(orbit.path, (0, 1, 2))
        self.assertEqual(orbit.tail, (0, 1))
        self.assertEqual(orbit.cycle, (2,))
        self.assertEqual(orbit.repeated_state, 2)

    def test_canonical_paths_and_partition(self) -> None:
        item = canonical_signature()
        profiles = {
            panel.name: (
                panel.orbit.path,
                len(panel.orbit.tail),
                len(panel.orbit.cycle),
            )
            for panel in item.panels
        }
        self.assertEqual(
            profiles,
            {
                "east1": ((40, 47), 1, 1),
                "west1": ((40, 47), 1, 1),
                "east2": ((47, 64, 81, 72, 66, 34, 57, 10, 42), 0, 9),
                "west2": (
                    (42, 53, 78, 35, 62, 52, 47, 43, 82, 1, 66),
                    4,
                    7,
                ),
                "east3": ((56, 60, 22, 45), 0, 4),
                "west3": ((47, 32, 62, 8, 11, 26, 19, 28), 6, 2),
                "east4": ((53, 58, 38, 48, 75), 4, 1),
                "west4": (
                    (
                        48,
                        64,
                        71,
                        63,
                        50,
                        81,
                        23,
                        80,
                        66,
                        14,
                        59,
                        68,
                        8,
                        29,
                        35,
                        27,
                        16,
                    ),
                    11,
                    6,
                ),
                "east5": (
                    (45, 10, 2, 5, 54, 32, 79, 12, 9, 40, 55, 30, 60, 34),
                    7,
                    7,
                ),
            },
        )
        self.assertEqual(item.all_orbit_total, 72)
        self.assertEqual(item.all_union_size, 51)
        self.assertEqual(item.omitted_label_count, 32)
        self.assertEqual(item.closing_tail_total, 8)
        self.assertEqual(item.closing_cycle_total, 12)
        self.assertEqual(item.pure_nonclosing_orbit_sizes, (9,))
        self.assertEqual(item.other_nonclosing_orbit_total, 43)
        self.assertEqual(item.closing_orbit_total, 20)
        self.assertEqual(item.closing_union_size, 17)
        self.assertEqual(item.closing_cycle_lengths, (1, 4, 7))
        self.assertEqual(item.closing_intersection_sizes, (0, 1, 2))
        self.assertTrue(item.objective_gate_event)
        self.assertTrue(item.broad_objective_gate_event)
        self.assertTrue(item.predicted_full_partition_event)
        self.assertTrue(item.broad_full_partition_event)
        self.assertTrue(item.phase_event)
        self.assertTrue(item.ordered_cycle_event)
        self.assertTrue(item.header_overlap_event)
        self.assertTrue(item.typed_sieve_remainder_event)
        self.assertTrue(item.any_checksum_remainder_event)

    def test_planted_gate_phase_signature_is_detected(self) -> None:
        paths = {
            "east1": ((0, 1), 1),
            "west1": ((20, 21), 1),
            "east2": (tuple(range(22, 31)), 0),
            "west2": (tuple(range(31, 42)), 4),
            "east3": ((2, 3, 4, 5), 0),
            "west3": (tuple(range(42, 50)), 6),
            "east4": (tuple(range(50, 55)), 4),
            "west4": (tuple(range(55, 72)), 11),
            "east5": (
                (1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16),
                7,
            ),
        }
        panels = tuple(
            PanelOrbit(
                name=name,
                quotient=paths[name][0][0],
                remainder=0 if name in CHECKSUM_FAMILY else 1,
                orbit=self._planted_orbit(*paths[name]),
            )
            for name in MESSAGE_ORDER
        )
        planted = signature(panels)
        self.assertTrue(planted.objective_gate_event)
        self.assertTrue(planted.broad_objective_gate_event)
        self.assertTrue(planted.predicted_full_partition_event)
        self.assertTrue(planted.broad_full_partition_event)
        self.assertTrue(planted.phase_event)
        self.assertTrue(planted.ordered_cycle_event)
        self.assertTrue(planted.header_overlap_event)

    def test_only_full_array_window_has_substantive_bridge(self) -> None:
        hits = []
        for start, item in common_window_signatures():
            if (
                item.objective_gate_event
                or item.predicted_full_partition_event
                or item.phase_event
                or item.ordered_cycle_event
            ):
                hits.append(start)
        self.assertEqual(hits, [0])

    def test_conditioned_sampler_preserves_frozen_information(self) -> None:
        generator = random.Random(12345)
        for name in MESSAGE_ORDER:
            spec = conditioned_table_spec(name)
            candidate = sample_conditioned_table(spec, generator)
            self.assertEqual(len(candidate), TABLE_SIZE)
            self.assertEqual(Counter(candidate), Counter(spec.base))
            self.assertTrue(
                all(
                    candidate[position] == spec.base[position]
                    for position in spec.fixed_positions
                )
            )
            self.assertFalse(
                any(
                    candidate[index] == candidate[index + 1]
                    for index in range(TABLE_SIZE - 1)
                )
            )
            self.assertNotEqual(candidate[-1], spec.continuation)
            quotient = panel_orbit(name).quotient
            self.assertEqual(
                tuple(
                    index
                    for index, value in enumerate(candidate)
                    if value == quotient
                ),
                tuple(
                    index
                    for index, value in enumerate(spec.base)
                    if value == quotient
                ),
            )

    def test_checksum_family_is_exactly_the_zero_remainder_family(self) -> None:
        zero = tuple(
            panel.name
            for panel in canonical_signature().panels
            if panel.remainder == 0
        )
        self.assertEqual(zero, CHECKSUM_FAMILY)


if __name__ == "__main__":
    unittest.main()
