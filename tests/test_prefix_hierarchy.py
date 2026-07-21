import unittest

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.prefix_hierarchy import (
    PrefixCluster,
    breadth_first_prefix_clusters,
    prefix_clusters,
    serialize_trie_edges,
)


class PrefixHierarchyTests(unittest.TestCase):
    def test_discovers_full_eye_prefix_tree_after_markers(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }
        self.assertEqual(
            prefix_clusters(streams, start=1),
            (
                PrefixCluster(MESSAGE_ORDER, 2),
                PrefixCluster(("east1", "west1", "east2"), 24),
                PrefixCluster(
                    ("west2", "east3", "west3", "east4", "west4", "east5"),
                    5,
                ),
                PrefixCluster(("east3", "east4", "west4", "east5"), 9),
                PrefixCluster(("east4", "west4", "east5"), 20),
            ),
        )

    def test_east5_first_breadth_first_depths_spell_bexit(self) -> None:
        order = MESSAGE_ORDER[-1:] + MESSAGE_ORDER[:-1]
        streams = {
            name: trigram_values(MESSAGES[name]) for name in order
        }
        depths = tuple(
            cluster.length
            for cluster in breadth_first_prefix_clusters(streams, start=1)
        )
        self.assertEqual(depths, (2, 5, 24, 9, 20))
        self.assertEqual("".join(chr(64 + depth) for depth in depths), "BEXIT")

    def test_trie_serialization_deduplicates_copied_eye_prefixes(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }
        depth_first = serialize_trie_edges(
            streams,
            MESSAGE_ORDER,
            start=1,
            breadth_first=False,
        )
        breadth_first = serialize_trie_edges(
            streams,
            MESSAGE_ORDER,
            start=1,
            breadth_first=True,
        )
        self.assertEqual(len(depth_first), 918)
        self.assertEqual(len(breadth_first), 918)
        self.assertEqual(sorted(depth_first), sorted(breadth_first))
        self.assertNotEqual(depth_first, breadth_first)


if __name__ == "__main__":
    unittest.main()
