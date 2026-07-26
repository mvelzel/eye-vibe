#!/usr/bin/env python3
"""Report whether the message headers identify a prefix-trie traversal."""

from eye_mystery.header_trie_syndrome import (
    audit_header_trie_nodes,
    header_trie_route_is_identified,
)


def main() -> None:
    print("depth direct inverse members")
    for node in audit_header_trie_nodes():
        print(
            f"{node.depth:>5} {node.direct_orders:>6} "
            f"{node.inverse_orders:>7} {','.join(node.members)}"
        )
    print(f"identified traversal: {header_trie_route_is_identified()}")


if __name__ == "__main__":
    main()
