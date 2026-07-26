import unittest

from eye_mystery.header_trie_syndrome import (
    audit_header_trie_nodes,
    header_trie_route_is_identified,
)


class HeaderTrieSyndromeTests(unittest.TestCase):
    def test_every_shared_node_has_multiple_header_collations(self) -> None:
        audit = audit_header_trie_nodes()
        self.assertEqual(
            tuple(
                (
                    node.depth,
                    node.members,
                    node.direct_orders,
                    node.inverse_orders,
                )
                for node in audit
            ),
            (
                (
                    2,
                    (
                        "east1",
                        "west1",
                        "east2",
                        "west2",
                        "east3",
                        "west3",
                        "east4",
                        "west4",
                        "east5",
                    ),
                    9,
                    7,
                ),
                (24, ("east1", "west1", "east2"), 3, 3),
                (
                    5,
                    ("west2", "east3", "west3", "east4", "west4", "east5"),
                    6,
                    5,
                ),
                (9, ("east3", "east4", "west4", "east5"), 4, 4),
                (20, ("east4", "west4", "east5"), 3, 3),
            ),
        )
        self.assertTrue(all(not node.has_unique_route for node in audit))
        self.assertFalse(header_trie_route_is_identified())


if __name__ == "__main__":
    unittest.main()
