#!/usr/bin/env python3
"""Audit the wand-generator selector against the Eye alphabet and trie."""

from __future__ import annotations

import argparse
from pathlib import Path

from eye_mystery.corpus import (
    MESSAGES,
    MESSAGE_ORDER,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)
from eye_mystery.wak import WakArchive
from eye_mystery.prefix_hierarchy import breadth_first_prefix_clusters
from eye_mystery.wand_selector import (
    action_type_counts,
    action_type_enums,
    compressed_branch_degrees,
    compressed_control_scopes,
    hidden_subset_residue_count,
    procedural_wand_partition,
)


def read_path(archive: WakArchive, suffix: str) -> bytes:
    matches = [entry for entry in archive.entries if entry.path.endswith(suffix)]
    if len(matches) != 1:
        raise ValueError(f"expected one WAK path ending in {suffix!r}")
    return archive.read(matches[0])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()

    archive = WakArchive.open(args.archive)
    enums = action_type_enums(read_path(archive, "scripts/gun/gun_enums.lua"))
    action_counts = action_type_counts(
        read_path(archive, "scripts/gun/gun_actions.lua")
    )
    generator = read_path(
        archive, "scripts/gun/procedural/gun_procedural.lua"
    )
    gun_runtime = read_path(archive, "scripts/gun/gun.lua")
    partition = procedural_wand_partition()

    streams = {
        name: trigram_values(MESSAGES[name])[1:] for name in MESSAGE_ORDER
    }
    degrees = compressed_branch_degrees(streams)
    east5_first = MESSAGE_ORDER[-1:] + MESSAGE_ORDER[:-1]
    ordered_streams = {name: streams[name] for name in east5_first}
    breadth_clusters = breadth_first_prefix_clusters(ordered_streams)
    depths = tuple(cluster.length for cluster in breadth_clusters)

    print("procedural selector:")
    print(
        "  modifier outcomes:",
        f"{partition.modifier_outcomes[0]}..{partition.modifier_outcomes[-1]}",
    )
    print(
        "  draw-many outcomes:",
        f"{partition.draw_many_outcomes[0]}..{partition.draw_many_outcomes[-1]}",
    )
    print("  partition sizes:", len(partition.modifier_outcomes), len(partition.draw_many_outcomes))
    print("  domain size:", partition.domain_size)
    print("action enum values:")
    print("  MODIFIER:", enums["MODIFIER"])
    print("  DRAW_MANY:", enums["DRAW_MANY"])
    print("current gun_actions.lua definitions:")
    print("  MODIFIER:", action_counts["MODIFIER"])
    print("  DRAW_MANY:", action_counts["DRAW_MANY"])
    print("Eye compressed prefix tree:")
    print("  branch degrees:", degrees)
    print("  East-5-first breadth depths:", depths)
    print("  depth A1Z26:", "".join(chr(64 + depth) for depth in depths))
    print("  every branch lies in first 26-slot row:", max(depths) < 26)
    print("  branch nodes:", len(degrees))
    print("  outgoing compressed edges:", sum(degrees))
    leaves = 1 + sum(degree - 1 for degree in degrees)
    print("  leaves:", leaves)
    print("  actual tree action/card nodes:", len(degrees) + leaves)
    print(
        "  hypothetical node-plus-edge records:",
        len(degrees) + sum(degrees),
    )
    print("scope-consistency audit:")
    hidden_values = partition.draw_many_outcomes
    hidden_residue = sum(hidden_values) % 101
    print("  all hidden values sum mod101:", hidden_residue)
    for scope in compressed_control_scopes(streams):
        target = (-scope.visible_residue) % 101
        subset_hits = hidden_subset_residue_count(
            hidden_values, scope.structural_records, target
        )
        print(
            " ",
            scope.members,
            "depth",
            scope.depth,
            "visible",
            scope.visible_residue,
            "local records",
            scope.structural_records,
            "closing subsets",
            subset_hits,
        )
    print(
        "  70-residue six-message subtree owns 11, not 18, records:",
        compressed_control_scopes(streams)[2].structural_records == 11,
    )
    print("other same-source dimensional selectors:")
    print("  message count:", len(MESSAGE_ORDER))
    print(
        "  every complete visual row width:",
        sorted(
            {
                length
                for lengths in ROW_PAIR_TRIGRAM_LENGTHS.values()
                for length in lengths[:-1]
            }
        ),
    )
    print("  source has unshuffle capacity <= 9:", b"deck_capacity <= 9" in generator)
    print("  source has clamp to 2..26:", b"clamp( gun[\"deck_capacity\"], 2, 26 )" in generator)
    print("  source has 83/101 split:", b"Random(0,100) < 83" in generator)
    print("actual gun execution semantics:")
    print(
        "  draw_actions loops requested children:",
        b"for i = 1, how_many do" in gun_runtime,
    )
    print(
        "  drawn actions execute immediately:",
        b"play_action( action )" in gun_runtime,
    )
    print(
        "  action execution may recurse into draw_actions:",
        b"action.action()" in gun_runtime,
    )


if __name__ == "__main__":
    main()
