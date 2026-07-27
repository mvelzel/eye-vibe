#!/usr/bin/env python3
"""Print frozen separator profiles for unresolved geometry pairs."""

from __future__ import annotations

from eye_mystery.hidden_geometry_separators import pair_separator_profile


TARGET_PAIRS = (
    ("first-gap30", "first-cross"),
    ("last-west4", "last-east5"),
    ("last-east5", "last-east3"),
)


def main() -> None:
    for left, right in TARGET_PAIRS:
        item = pair_separator_profile(left, right)
        print(
            f"pair={left}+{right}; labels={item.labels}; edges={item.edges}; "
            f"cycles={item.cycle_rank}; "
            f"label_articulations={item.label_articulations}; "
            f"largest_biconnected={item.largest_biconnected}; "
            f"primal_variables={item.primal_variables}; "
            f"primal_width_upper={item.primal_width_upper}; "
            f"primal_articulations={item.primal_articulations}; "
            f"class_variables={item.class_variables}; "
            f"class_width_upper={item.class_width_upper}; "
            f"class_components={item.class_components}"
        )


if __name__ == "__main__":
    main()
