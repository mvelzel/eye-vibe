"""Structural profiles for unresolved hidden-geometry context pairs."""

from __future__ import annotations

from dataclasses import dataclass

from eye_mystery.hidden_geometry import chord_classes
from eye_mystery.hidden_geometry_pairs import pair_constraints

try:
    import networkx as nx
    from networkx.algorithms.approximation import treewidth_min_fill_in
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    nx = None  # type: ignore[assignment]
    treewidth_min_fill_in = None  # type: ignore[assignment]


@dataclass(frozen=True)
class SeparatorProfile:
    labels: int
    edges: int
    cycle_rank: int
    label_articulations: tuple[int, ...]
    largest_biconnected: int
    primal_variables: int
    primal_width_upper: int
    primal_articulations: int
    class_variables: int
    class_width_upper: int
    class_components: tuple[int, ...]


def networkx_available() -> bool:
    return nx is not None and treewidth_min_fill_in is not None


def pair_separator_profile(left: str, right: str) -> SeparatorProfile:
    """Return the frozen label, primal, and cycle-class graph profile."""

    if not networkx_available():
        raise RuntimeError(
            "separator profiling requires the optional networkx package"
        )
    constraints = pair_constraints(left, right)
    classes = chord_classes(constraints)
    edge_class = {
        edge: class_index
        for class_index, edges in enumerate(classes)
        for edge in edges
    }
    label_graph = nx.Graph()
    label_graph.add_edges_from(edge_class)

    primal = nx.Graph()
    for (left_label, right_label), class_index in edge_class.items():
        variables = (
            ("z", left_label),
            ("z", right_label),
            ("d", class_index),
        )
        for index, first in enumerate(variables):
            for second in variables[index + 1 :]:
                primal.add_edge(first, second)

    tree = nx.minimum_spanning_tree(label_graph)
    tree_edges = {
        tuple(sorted(edge)) for edge in tree.edges()
    }
    cycle_supports = []
    for left_label, right_label in label_graph.edges():
        closing = tuple(sorted((left_label, right_label)))
        if closing in tree_edges:
            continue
        path = nx.shortest_path(tree, left_label, right_label)
        cycle_edges = [
            tuple(sorted(edge))
            for edge in zip(path, path[1:])
        ]
        cycle_edges.append(closing)
        cycle_supports.append(
            tuple(sorted({edge_class[edge] for edge in cycle_edges}))
        )

    class_graph = nx.Graph()
    class_graph.add_nodes_from(range(len(classes)))
    for support in cycle_supports:
        for index, first in enumerate(support):
            for second in support[index + 1 :]:
                class_graph.add_edge(first, second)

    primal_width, _ = treewidth_min_fill_in(primal)
    class_width, _ = treewidth_min_fill_in(class_graph)
    biconnected = tuple(nx.biconnected_components(label_graph))
    return SeparatorProfile(
        label_graph.number_of_nodes(),
        label_graph.number_of_edges(),
        label_graph.number_of_edges()
        - label_graph.number_of_nodes()
        + nx.number_connected_components(label_graph),
        tuple(sorted(nx.articulation_points(label_graph))),
        max(map(len, biconnected), default=0),
        primal.number_of_nodes(),
        primal_width,
        len(tuple(nx.articulation_points(primal))),
        class_graph.number_of_nodes(),
        class_width,
        tuple(
            sorted(
                (len(component) for component in nx.connected_components(class_graph)),
                reverse=True,
            )
        ),
    )
