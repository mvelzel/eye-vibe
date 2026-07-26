#!/usr/bin/env python3
"""Audit the exact Eye-header/Kantele-song interface."""

from eye_mystery.kantele_header import (
    KANTELE_SONGS,
    ROUTES,
    kantele_header_audit,
    score_route,
)


def main() -> None:
    audit = kantele_header_audit()
    observed = audit.observed
    print(f"songs={KANTELE_SONGS}")
    for route in ROUTES:
        print(f"real_{route}={score_route(route).selection_score}")
    print(
        f"observed route={observed.route} "
        f"score={observed.selection_score} "
        f"tail={audit.exact_tail_count}/{audit.control_count}="
        f"{audit.exact_tail:.9f} "
        f"control_max={audit.maximum_control_score}"
    )
    for name, hits in observed.hits_by_message:
        if not hits:
            continue
        print(f"{name}:")
        for hit in hits:
            print(
                f"  {hit.song} [{hit.start},{hit.end}) "
                f"begin={hit.begins_fragment} end={hit.ends_fragment} "
                f"exact={hit.exact_fragment}"
            )
    print("histogram:")
    for score, count in audit.score_histogram:
        print(f"  {score}: {count}")


if __name__ == "__main__":
    main()
