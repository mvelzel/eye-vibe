#!/usr/bin/env python3
"""Audit Cipher 3's literal prefix tree and standard C83 action streams."""

from __future__ import annotations

import argparse

from eye_mystery.practice_cipher3_wide import (
    action_width_scores,
    load_cipher3,
    prefix_relations,
    shuffled_body_prefix_maxima,
    transition_graph_audit,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix-controls", type=int, default=10_000)
    parser.add_argument("--width-controls", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0x53444C57445203)
    args = parser.parse_args()

    streams = load_cipher3()
    print("literal prefix tree")
    for relation in prefix_relations(streams):
        print(
            f"  {relation.left}/{relation.right}: "
            f"full={relation.full_length} body={relation.body_length}"
        )
    maxima = shuffled_body_prefix_maxima(
        streams,
        controls=args.prefix_controls,
        seed=args.seed,
    )
    observed = max(
        relation.body_length for relation in prefix_relations(streams)
    )
    upper_tail = (
        1 + sum(value >= observed for value in maxima)
    ) / (len(maxima) + 1)
    print(
        f"  observed maximum={observed}; "
        f"control range={min(maxima)}..{max(maxima)}; "
        f"corrected upper tail={upper_tail:.6f}"
    )

    graph = transition_graph_audit(streams)
    print("previous-ciphertext transition graph")
    print(
        f"  events/unique/repeated={graph.events}/"
        f"{graph.unique_edges}/{graph.repeated_events}; "
        f"maximum multiplicity={graph.maximum_multiplicity}"
    )
    print(
        f"  maximum out/in degree={graph.maximum_outdegree}/"
        f"{graph.maximum_indegree}; "
        f"effective uniform choices={graph.effective_uniform_choices:.6f}"
    )

    print("standard C83 transform/width screen")
    rows = action_width_scores(
        streams,
        controls=args.width_controls,
        seed=args.seed ^ 0xC83,
    )
    for row in sorted(
        rows,
        key=lambda value: (
            -value.training_excess,
            value.transform,
            value.width,
            value.coordinate,
        ),
    )[:20]:
        print(
            f"  {row.transform:<20} width={row.width:>2} "
            f"{row.coordinate:<9} excess A/B/C="
            f"{row.training_excess:+.6f}/"
            f"{row.heldout_b_excess:+.6f}/"
            f"{row.heldout_c_excess:+.6f}"
        )


if __name__ == "__main__":
    main()
