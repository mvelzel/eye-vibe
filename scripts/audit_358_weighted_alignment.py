#!/usr/bin/env python3
"""Run the preregistered 3,5,8 weighted Eye-panel audit."""

from __future__ import annotations

from eye_mystery.weighted_alignment import weighted_alignment_audit


def main() -> None:
    audit = weighted_alignment_audit()
    for row in audit.rows:
        print(
            f"{','.join(row.names)}: length={row.length} real={row.real_score} "
            f"null={row.null_min}..{row.null_max} "
            f"upper={row.null_upper}/{row.null_total}={row.exact_tail:.9f}"
        )
    print(
        f"total: real={audit.real_total} null={audit.null_min}..{audit.null_max} "
        f"upper={audit.null_upper}/{audit.null_total}={audit.exact_tail:.9f}"
    )


if __name__ == "__main__":
    main()
