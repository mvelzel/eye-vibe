"""Predictive recursive branch checks for the fourteenth Eye horizon."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True, order=True)
class RecursiveRule:
    incoming: int
    children: int
    outdegree: int
    depth: int

    @property
    def name(self) -> str:
        return (
            f"a={self.incoming},b={self.children},"
            f"c={self.outdegree},d={self.depth}"
        )


@dataclass(frozen=True)
class RecursiveCheckAudit:
    branch_paths: tuple[tuple[int, ...], ...]
    heldout_rules: tuple[RecursiveRule, ...]
    heldout_values: tuple[int, ...]
    leave_one_out_correct: int
    selected_rule: RecursiveRule
    selected_branch_values: tuple[int, ...]
    selected_branch_zeros: int
    root_value: int

    @property
    def root_zero(self) -> bool:
        return self.root_value == 0


@dataclass(frozen=True)
class _Trie:
    children: tuple[dict[int, int], ...]
    depth: tuple[int, ...]
    incoming: tuple[int, ...]
    paths: tuple[tuple[int, ...], ...]
    branches: tuple[int, ...]


def recursive_rules() -> tuple[RecursiveRule, ...]:
    return tuple(
        RecursiveRule(a, b, c, d)
        for a in (-1, 1)
        for b, c, d in product((-1, 0, 1), repeat=3)
    )


def _build_trie(
    streams: Mapping[str, Sequence[int]],
    modulus: int,
) -> _Trie:
    children: list[dict[int, int]] = [{}]
    depth = [0]
    incoming = [0]
    paths: list[tuple[int, ...]] = [()]
    for stream in streams.values():
        node = 0
        for label in stream:
            if label not in range(modulus):
                raise ValueError("stream label lies outside the field")
            child = children[node].get(label)
            if child is None:
                child = len(children)
                children[node][label] = child
                children.append({})
                depth.append(depth[node] + 1)
                incoming.append(label)
                paths.append(paths[node] + (label,))
            node = child
    branches = tuple(
        sorted(
            (
                node
                for node, outgoing in enumerate(children)
                if len(outgoing) >= 2
            ),
            key=lambda node: paths[node],
        )
    )
    return _Trie(
        tuple(children),
        tuple(depth),
        tuple(incoming),
        tuple(paths),
        branches,
    )


def recursive_values(
    streams: Mapping[str, Sequence[int]],
    rule: RecursiveRule,
    *,
    modulus: int = 101,
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[tuple[int, ...], ...]]:
    """Return every node value, branch node ids, and canonical branch paths."""

    trie = _build_trie(streams, modulus)
    values = [0] * len(trie.children)
    for node in reversed(range(len(trie.children))):
        values[node] = (
            rule.incoming * trie.incoming[node]
            + rule.children
            * sum(values[child] for child in trie.children[node].values())
            + rule.outdegree * len(trie.children[node])
            + rule.depth * trie.depth[node]
        ) % modulus
    return (
        tuple(values),
        trie.branches,
        tuple(trie.paths[node] for node in trie.branches),
    )


def _select_rule(
    values_by_rule: Mapping[RecursiveRule, tuple[int, ...]],
    training_branches: Sequence[int],
) -> RecursiveRule:
    return min(
        values_by_rule,
        key=lambda rule: (
            -sum(
                values_by_rule[rule][node] == 0
                for node in training_branches
            ),
            rule,
        ),
    )


def audit_recursive_checks(
    streams: Mapping[str, Sequence[int]],
    *,
    modulus: int = 101,
) -> RecursiveCheckAudit:
    rules = recursive_rules()
    values_by_rule = {}
    branches = None
    paths = None
    for rule in rules:
        values, current_branches, current_paths = recursive_values(
            streams, rule, modulus=modulus
        )
        if branches is None:
            branches = current_branches
            paths = current_paths
        elif current_branches != branches or current_paths != paths:
            raise AssertionError("trie topology changed between rules")
        values_by_rule[rule] = values
    assert branches is not None and paths is not None

    heldout_rules = []
    heldout_values = []
    for heldout in branches:
        training = tuple(node for node in branches if node != heldout)
        selected = _select_rule(values_by_rule, training)
        heldout_rules.append(selected)
        heldout_values.append(values_by_rule[selected][heldout])

    selected = _select_rule(values_by_rule, branches)
    selected_branch_values = tuple(
        values_by_rule[selected][node] for node in branches
    )
    return RecursiveCheckAudit(
        paths,
        tuple(heldout_rules),
        tuple(heldout_values),
        sum(value == 0 for value in heldout_values),
        selected,
        selected_branch_values,
        sum(value == 0 for value in selected_branch_values),
        values_by_rule[selected][0],
    )


def planted_branch_dictionary() -> dict[str, tuple[int, ...]]:
    """Five nested branch checks for ``incoming - depth = 0``."""

    return {
        "p1": (1, 51),
        "p2": (1, 2, 52),
        "p3": (1, 2, 3, 53),
        "p4": (1, 2, 3, 4, 54),
        "p5": (1, 2, 3, 4, 5, 55),
        "p6": (1, 2, 3, 4, 5, 56),
    }
