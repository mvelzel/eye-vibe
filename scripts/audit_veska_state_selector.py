#!/usr/bin/env python3
"""Reproduce the frozen Veska state-selector audit."""

from __future__ import annotations

from eye_mystery.veska_state_selector import audit_veska_selector


def main() -> None:
    audit = audit_veska_selector()
    for field in (
        "components",
        "number",
        "increment",
        "fixed_repeated_splits",
        "fixed_all_class_splits",
        "repeated_cross_hits",
        "repeated_cross_probability",
        "all_class_cross_hits",
        "permuted_splits",
        "panel_suffix_matches",
        "terminal_class",
        "loop_suffix",
        "returned_header",
        "restarted_phase",
        "late_phase_length",
        "locale_text",
    ):
        print(f"{field}: {getattr(audit, field)}")
    print(f"selector_executes: {audit.selector_executes}")


if __name__ == "__main__":
    main()
