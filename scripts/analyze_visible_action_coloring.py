#!/usr/bin/env python3
"""Report the exact direct visible-action cover of the Eye transitions."""

from __future__ import annotations

from eye_mystery.visible_action_coloring import (
    audit_pivot_freedom,
    audit_visible_actions,
    canonical_full_contexts,
    canonical_full_streams,
)


def main() -> None:
    audit = audit_visible_actions()
    print(f"transition events:             {audit.transition_events}")
    print(f"unique edges:                 {audit.unique_edges}")
    print(f"repeated edge events:         {audit.repeated_edge_events}")
    print(f"maximum edge multiplicity:    {audit.maximum_edge_multiplicity}")
    print(f"maximum distinct outdegree:   {audit.maximum_distinct_outdegree}")
    print(f"maximum distinct indegree:    {audit.maximum_distinct_indegree}")
    print(f"effective uniform choices:    {audit.effective_uniform_choices:.9f}")
    print(f"expected unique at K=26:      {audit.expected_unique_edges_26:.6f}")
    print(f"expected unique at K=42:      {audit.expected_unique_edges_42:.6f}")
    print(f"aligned event classes:        {audit.aligned_classes}")
    print(f"all event classes:            {audit.event_classes}")
    print(f"internal alignment conflicts: {audit.internally_conflicting_classes}")
    print(f"class conflict pairs:         {audit.conflict_pairs}")
    print(f"action lower bound:           {audit.lower_bound}")
    print(f"constructed actions:          {audit.constructed_actions}")
    print(f"exact minimum:                {audit.exact_minimum}")
    freedom = audit_pivot_freedom()
    print(f"pivot source:                 {freedom.pivot_source}")
    print(f"pivot targets:                {list(freedom.pivot_targets)}")
    print(f"anchored action classes:      {freedom.anchored_classes}")
    print(f"nonanchor action classes:     {freedom.nonanchor_classes}")
    print(
        "one-step mutable nonanchors: "
        f"{freedom.one_step_mutable_nonanchors}"
    )
    print(f"forced nonanchors:            {freedom.forced_nonanchors}")
    print(
        "available colors/nonanchor:  "
        f"{freedom.minimum_available_colors_nonanchor}"
        f"..{freedom.maximum_available_colors_nonanchor}"
    )
    print(
        "available-color histogram:  "
        f"{dict(freedom.available_color_histogram)}"
    )
    full_streams = canonical_full_streams()
    full_contexts = canonical_full_contexts()
    full_audit = audit_visible_actions(full_streams, full_contexts)
    full_freedom = audit_pivot_freedom(full_streams, full_contexts)
    print(
        "marker-inclusive robustness: "
        f"{full_audit.constructed_actions} actions, "
        f"{full_freedom.one_step_mutable_nonanchors}/"
        f"{full_freedom.nonanchor_classes} mutable"
    )


if __name__ == "__main__":
    main()
