from __future__ import annotations

import unittest
from collections import Counter

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.trie_checksum import (
    affine_f83_relabeling_calibration,
    branch_descendant_checksums,
    random_relabeling_zero_count,
    signature_preserving_relabeling_calibration,
    signature_preserving_joint_calibration,
    trie_checksum,
    vector_rank_mod,
)


class TrieChecksumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }
        cls.result = trie_checksum(cls.streams, MESSAGE_ORDER, start=1)

    def test_distinct_body_trie_edges_close_modulo_101(self) -> None:
        self.assertEqual(self.result.edge_count, 918)
        self.assertEqual(self.result.total, 37_774)
        self.assertEqual(self.result.residue, 0)
        self.assertEqual(len(self.result.label_multiplicities), 83)

    def test_closure_needs_trigram_bodies_and_forward_prefixes(self) -> None:
        self.assertEqual(
            tuple(
                trie_checksum(self.streams, MESSAGE_ORDER, start=start).residue
                for start in range(4)
            ),
            (63, 0, 35, 30),
        )
        reversed_bodies = {
            name: tuple(reversed(stream[1:]))
            for name, stream in self.streams.items()
        }
        self.assertEqual(
            trie_checksum(reversed_bodies, MESSAGE_ORDER, start=0).residue,
            92,
        )
        raw_streams = {name: MESSAGES[name] for name in MESSAGE_ORDER}
        raw = trie_checksum(raw_streams, MESSAGE_ORDER, start=3)
        self.assertEqual((raw.edge_count, raw.total, raw.residue), (2751, 4669, 23))

    def test_lower_six_branch_has_the_only_descendant_residue_70(self) -> None:
        branches = branch_descendant_checksums(self.streams, start=1)
        self.assertEqual(
            tuple(
                (branch.cluster.members, branch.cluster.length,
                 branch.descendant_residue)
                for branch in branches
            ),
            (
                (MESSAGE_ORDER, 2, 30),
                (("east1", "west1", "east2"), 24, 19),
                (("west2", "east3", "west3", "east4", "west4", "east5"), 5, 70),
                (("east3", "east4", "west4", "east5"), 9, 89),
                (("east4", "west4", "east5"), 20, 13),
            ),
        )
        self.assertEqual(2 * len(branches) + len(MESSAGE_ORDER) - 1, 18)
        self.assertEqual(sum(range(83, 101)) % 101, 31)

    def test_affine_relabeling_control_is_about_one_percent(self) -> None:
        calibration = affine_f83_relabeling_calibration(
            self.result.label_multiplicities
        )
        self.assertEqual((calibration.zero_count, calibration.total), (71, 6806))
        self.assertEqual(calibration.zero_translations, (0,))
        self.assertEqual(
            random_relabeling_zero_count(
                self.result.label_multiplicities,
                samples=1_000,
                seed=20_260_721,
            ),
            17,
        )

    def test_trie_equation_is_not_formally_implied_by_message_sums(self) -> None:
        def count_vector(values: tuple[int, ...]) -> tuple[int, ...]:
            counts = Counter(values)
            return tuple(counts[value] for value in range(83))

        messages = tuple(
            count_vector(self.streams[name]) for name in MESSAGE_ORDER
        )
        self.assertEqual(vector_rank_mod(messages, 101), 9)
        self.assertEqual(
            vector_rank_mod(messages + (self.result.label_multiplicities,), 101),
            10,
        )

    def test_exact_null_preserves_diagonal_checks_and_markers(self) -> None:
        def count_vector(values: tuple[int, ...]) -> tuple[int, ...]:
            counts = Counter(values)
            return tuple(counts[value] for value in range(83))

        diagonal = tuple(
            count_vector(self.streams[name])
            for name in ("east1", "east3", "east5")
        )
        free = signature_preserving_relabeling_calibration(
            self.result.label_multiplicities,
            diagonal,
        )
        self.assertEqual(free.total, 132_090_377_011_200)
        self.assertEqual(free.zero_count, 1_307_844_501_760)

        fixed = signature_preserving_relabeling_calibration(
            self.result.label_multiplicities,
            diagonal,
            fixed_labels=tuple(
                self.streams[name][0] for name in MESSAGE_ORDER
            ),
        )
        self.assertEqual(fixed.total, 825_564_856_320)
        self.assertEqual(fixed.zero_count, 8_174_134_656)

        joint = signature_preserving_relabeling_calibration(
            self.result.label_multiplicities,
            diagonal,
            checksum_modulus=17 * 101,
        )
        self.assertEqual(joint.zero_count, 125_161_099_264)
        joint_fixed = signature_preserving_relabeling_calibration(
            self.result.label_multiplicities,
            diagonal,
            fixed_labels=tuple(
                self.streams[name][0] for name in MESSAGE_ORDER
            ),
            checksum_modulus=17 * 101,
        )
        self.assertEqual(joint_fixed.zero_count, 830_894_368)

        lower_six = branch_descendant_checksums(self.streams, start=1)[2]
        bivariate = signature_preserving_joint_calibration(
            self.result.label_multiplicities,
            lower_six.label_multiplicities,
            diagonal,
            fixed_labels=tuple(
                self.streams[name][0] for name in MESSAGE_ORDER
            ),
        )
        self.assertEqual(bivariate.total, 825_564_856_320)
        self.assertEqual(bivariate.count(0, 70), 80_918_060)


if __name__ == "__main__":
    unittest.main()
