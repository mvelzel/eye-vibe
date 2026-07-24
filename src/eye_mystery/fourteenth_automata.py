"""Canonical finite-language automata for the fourteenth Eye horizon."""

from __future__ import annotations

from collections import Counter
from collections import deque
from collections.abc import Mapping, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class DictionaryAutomaton:
    trie_nodes: int
    trie_transitions: int
    minimal_nodes: int
    minimal_transitions: int
    accepting_classes: int
    class_sizes: tuple[int, ...]
    internal_merged_nodes: int
    transition_total: int
    transition_residue: int
    label_multiplicities: tuple[int, ...]


@dataclass(frozen=True)
class FailureLinkSieve:
    trie_nodes: int
    selected_nodes: int
    incoming_total: int
    incoming_residue: int
    label_multiplicities: tuple[int, ...]
    failure_depth_histogram: tuple[int, ...]
    depth_drop_word: tuple[int, ...]
    bexit_positions: tuple[int, ...]


def minimal_dictionary_automaton(
    streams: Mapping[str, Sequence[int]],
    *,
    alphabet_size: int,
    modulus: int = 101,
) -> DictionaryAutomaton:
    """Build the unique minimal acyclic DFA for a finite word dictionary.

    Trie states are equivalent exactly when they have the same accepting flag
    and the same label-to-equivalence-class continuation map.  Interning those
    signatures bottom-up produces the canonical right-language quotient.
    """

    if alphabet_size < 1:
        raise ValueError("alphabet size must be positive")
    transitions: list[dict[int, int]] = [{}]
    accepting: list[bool] = [False]
    for stream in streams.values():
        node = 0
        for label in stream:
            if label not in range(alphabet_size):
                raise ValueError("stream label lies outside the alphabet")
            child = transitions[node].get(label)
            if child is None:
                child = len(transitions)
                transitions[node][label] = child
                transitions.append({})
                accepting.append(False)
            node = child
        accepting[node] = True

    signatures: dict[
        tuple[bool, tuple[tuple[int, int], ...]], int
    ] = {}
    class_by_node = [-1] * len(transitions)
    for node in reversed(range(len(transitions))):
        signature = (
            accepting[node],
            tuple(
                sorted(
                    (label, class_by_node[child])
                    for label, child in transitions[node].items()
                )
            ),
        )
        class_by_node[node] = signatures.setdefault(
            signature, len(signatures)
        )

    quotient_edges = {
        (class_by_node[source], label, class_by_node[target])
        for source, outgoing in enumerate(transitions)
        for label, target in outgoing.items()
    }
    counts = Counter(label for _, label, _ in quotient_edges)
    class_counts = Counter(class_by_node)
    accepting_classes = {
        class_by_node[node]
        for node, is_accepting in enumerate(accepting)
        if is_accepting
    }
    internal_merged_nodes = sum(
        size - 1
        for class_id, size in class_counts.items()
        if class_id not in accepting_classes and size > 1
    )
    total = sum(label for _, label, _ in quotient_edges)
    return DictionaryAutomaton(
        trie_nodes=len(transitions),
        trie_transitions=len(transitions) - 1,
        minimal_nodes=len(signatures),
        minimal_transitions=len(quotient_edges),
        accepting_classes=len(accepting_classes),
        class_sizes=tuple(
            sorted(class_counts.values(), reverse=True)
        ),
        internal_merged_nodes=internal_merged_nodes,
        transition_total=total,
        transition_residue=total % modulus,
        label_multiplicities=tuple(
            counts[label] for label in range(alphabet_size)
        ),
    )


def failure_link_sieve(
    streams: Mapping[str, Sequence[int]],
    *,
    alphabet_size: int,
    modulus: int = 101,
    target_word: Sequence[int] = (2, 5, 24, 9, 20),
) -> FailureLinkSieve:
    """Build the frozen Aho–Corasick non-root failure-link record tape."""

    if alphabet_size < 1:
        raise ValueError("alphabet size must be positive")
    transitions: list[dict[int, int]] = [{}]
    depth = [0]
    incoming: list[int | None] = [None]
    for stream in streams.values():
        node = 0
        for label in stream:
            if label not in range(alphabet_size):
                raise ValueError("stream label lies outside the alphabet")
            child = transitions[node].get(label)
            if child is None:
                child = len(transitions)
                transitions[node][label] = child
                transitions.append({})
                depth.append(depth[node] + 1)
                incoming.append(label)
            node = child

    failure = [0] * len(transitions)
    queue: deque[int] = deque()
    bfs_order = [0]
    for _, child in sorted(transitions[0].items()):
        queue.append(child)
    while queue:
        node = queue.popleft()
        bfs_order.append(node)
        for label, child in sorted(transitions[node].items()):
            fallback = failure[node]
            while fallback and label not in transitions[fallback]:
                fallback = failure[fallback]
            failure[child] = transitions[fallback].get(label, 0)
            queue.append(child)

    selected = tuple(
        node for node in bfs_order[1:] if failure[node] != 0
    )
    selected_labels = tuple(
        incoming[node] for node in selected
    )
    if any(label is None for label in selected_labels):
        raise AssertionError("non-root nodes must have incoming labels")
    concrete_labels = tuple(
        int(label) for label in selected_labels
    )
    drops = tuple(
        depth[node] - depth[failure[node]] for node in selected
    )
    target = tuple(target_word)
    positions = tuple(
        index
        for index in range(len(drops) - len(target) + 1)
        if drops[index : index + len(target)] == target
    )
    depth_counts = Counter(depth[failure[node]] for node in selected)
    maximum_depth = max(depth_counts, default=0)
    label_counts = Counter(concrete_labels)
    total = sum(concrete_labels)
    return FailureLinkSieve(
        trie_nodes=len(transitions),
        selected_nodes=len(selected),
        incoming_total=total,
        incoming_residue=total % modulus,
        label_multiplicities=tuple(
            label_counts[label] for label in range(alphabet_size)
        ),
        failure_depth_histogram=tuple(
            depth_counts[value] for value in range(maximum_depth + 1)
        ),
        depth_drop_word=drops,
        bexit_positions=positions,
    )
