import unittest

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.wand_selector import (
    action_type_counts,
    action_type_enums,
    compressed_branch_degrees,
    compressed_control_scopes,
    hidden_subset_residue_count,
    procedural_wand_partition,
)


class WandSelectorTests(unittest.TestCase):
    def test_parses_action_enums_and_assignments(self) -> None:
        enums = action_type_enums(
            b"ACTION_TYPE_MODIFIER = 2\nACTION_TYPE_DRAW_MANY\t=\t3\n"
        )
        self.assertEqual(enums, {"MODIFIER": 2, "DRAW_MANY": 3})
        counts = action_type_counts(
            b"type=ACTION_TYPE_MODIFIER\ntype = ACTION_TYPE_DRAW_MANY\n"
            b"type = ACTION_TYPE_DRAW_MANY\n"
        )
        self.assertEqual(counts, {"MODIFIER": 1, "DRAW_MANY": 2})

    def test_selector_partitions_101_into_83_and_18(self) -> None:
        partition = procedural_wand_partition()
        self.assertEqual(partition.modifier_outcomes, tuple(range(83)))
        self.assertEqual(partition.draw_many_outcomes, tuple(range(83, 101)))
        self.assertEqual(partition.domain_size, 101)

    def test_eye_trie_tree_counts_distinguish_actions_from_node_edge_records(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name])[1:] for name in MESSAGE_ORDER
        }
        degrees = compressed_branch_degrees(streams)
        self.assertEqual(degrees, (2, 3, 3, 2, 3))
        self.assertEqual(len(degrees), 5)
        self.assertEqual(sum(degrees), 13)
        leaves = 1 + sum(degree - 1 for degree in degrees)
        self.assertEqual(leaves, 9)
        self.assertEqual(len(degrees) + leaves, 14)
        # Eighteen is a speculative node-plus-edge serialization, not the
        # number of cards executed by Noita's recursive draw machinery.
        self.assertEqual(len(degrees) + sum(degrees), 18)

    def test_checksum_complement_and_18_records_have_different_scopes(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name])[1:] for name in MESSAGE_ORDER
        }
        scopes = compressed_control_scopes(streams)
        self.assertEqual(
            tuple(scope.structural_records for scope in scopes),
            (18, 4, 11, 7, 4),
        )
        self.assertEqual(
            tuple(scope.visible_residue for scope in scopes),
            (30, 19, 70, 89, 13),
        )
        lower_six = scopes[2]
        self.assertEqual(len(lower_six.members), 6)
        self.assertEqual(lower_six.structural_records, 11)
        self.assertEqual(lower_six.visible_residue, 70)

        hidden = tuple(range(83, 101))
        self.assertEqual(sum(hidden) % 101, 31)
        self.assertEqual(
            hidden_subset_residue_count(hidden, 11, 31),
            5,
        )

    def test_all_18_hidden_values_do_not_close_any_natural_root_sum(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name])[1:] for name in MESSAGE_ORDER
        }
        root = compressed_control_scopes(streams)[0]
        hidden_residue = sum(range(83, 101)) % 101
        self.assertEqual(root.structural_records, 18)
        self.assertEqual(root.visible_residue, 30)
        self.assertNotEqual((root.visible_residue + hidden_residue) % 101, 0)


if __name__ == "__main__":
    unittest.main()
