import unittest

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.wand_selector import (
    action_type_counts,
    action_type_enums,
    compressed_branch_degrees,
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

    def test_eye_trie_has_five_draw_two_or_three_nodes_and_18_records(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name])[1:] for name in MESSAGE_ORDER
        }
        degrees = compressed_branch_degrees(streams)
        self.assertEqual(degrees, (2, 3, 3, 2, 3))
        self.assertEqual(len(degrees), 5)
        self.assertEqual(sum(degrees), 13)
        self.assertEqual(len(degrees) + sum(degrees), 18)


if __name__ == "__main__":
    unittest.main()
