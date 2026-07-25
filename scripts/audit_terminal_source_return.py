#!/usr/bin/env python3
"""Reproduce the frozen terminal source-state return audit."""

from __future__ import annotations

from eye_mystery.terminal_source_return import (
    all_pair_marker_hits,
    audit_compatible_returns,
    audit_conditional,
    compatible_aligned_marker_hits,
    fixed_source_repeat_hits,
    source_any_marker_hits,
    terminal_source_observation,
)


def ratio(numerator: int, denominator: int) -> str:
    return f"{numerator}/{denominator} = {numerator / denominator:.9f}"


def main() -> None:
    observed = terminal_source_observation()
    matched = audit_compatible_returns()
    conditional = audit_conditional()
    print(f"observed: {observed}")
    print(f"compatible_return_audit: {matched}")
    print(f"fixed_source_repeat_hits: {fixed_source_repeat_hits()}")
    print(f"source_any_marker_hits: {source_any_marker_hits()}")
    print(f"all_pair_marker_hits: {all_pair_marker_hits()}")
    print(
        "compatible_aligned_marker_hits: "
        f"{compatible_aligned_marker_hits()}"
    )
    for field in (
        "return_header",
        "return_and_topology",
        "return_terminal_topology",
    ):
        print(
            f"{field}: "
            f"{ratio(getattr(conditional, field), conditional.assignments)}"
        )


if __name__ == "__main__":
    main()
