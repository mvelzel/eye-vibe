"""Identifiability audit for header-ordered prefix-trie traversals."""

from __future__ import annotations

from dataclasses import dataclass

from eye_mystery.header_order_ideal import header_eye_order
from eye_mystery.marker_orders import eye_prefix_clusters


@dataclass(frozen=True)
class TrieNodeOrderAudit:
    """Header-order multiplicity at one shared body-prefix node."""

    depth: int
    members: tuple[str, ...]
    direct_orders: int
    inverse_orders: int

    @property
    def has_unique_route(self) -> bool:
        """Whether either frozen global route supplies one node collation."""

        return self.direct_orders == 1 or self.inverse_orders == 1


def audit_header_trie_nodes() -> tuple[TrieNodeOrderAudit, ...]:
    """Count distinct member-header collations at every shared trie node.

    A header-ordered traversal needs one eye-symbol collation at each shared
    node.  The corpus supplies one header per message, rather than one header
    per node.  Multiple distinct member headers therefore leave the traversal
    undefined unless another rule selects or combines them.
    """

    results = []
    for cluster in eye_prefix_clusters():
        direct = {
            header_eye_order(name, "header")
            for name in cluster.members
        }
        inverse = {
            header_eye_order(name, "inverse-header")
            for name in cluster.members
        }
        results.append(
            TrieNodeOrderAudit(
                depth=cluster.length,
                members=cluster.members,
                direct_orders=len(direct),
                inverse_orders=len(inverse),
            )
        )
    return tuple(results)


def header_trie_route_is_identified() -> bool:
    """Return whether every shared node has a unique frozen-route collation."""

    return all(node.has_unique_route for node in audit_header_trie_nodes())
