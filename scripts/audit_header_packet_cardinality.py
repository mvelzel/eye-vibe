#!/usr/bin/env python3
"""Run the frozen header/packet cardinality audit."""

from eye_mystery.header_packet_cardinality import run_audit


def main() -> None:
    audit = run_audit()
    print("checksum-family ledger")
    for row in audit.rows:
        print(
            f"  {row.name}: edge={row.edge[0]}->{row.edge[1]} "
            f"source-indegree={row.source_indegree} "
            f"packet-count={row.packet_count} closes={row.closes}"
        )
    assignment = audit.assignment
    print(
        f"count assignments: exact={assignment.exact_hits}/"
        f"{assignment.assignments} broad={assignment.broad_hits}/"
        f"{assignment.assignments}"
    )
    print(f"  exact assignments={assignment.exact_assignments}")
    print(f"  broad assignments={assignment.broad_assignments}")
    print(
        "  observed formula hits="
        + ",".join(
            f"{hit.endpoint}-{hit.degree_direction}-{hit.orientation}"
            for hit in assignment.observed_formula_hits
        )
    )
    print(f"all-triple hits={len(audit.triple_hits)}/84")
    for hit in audit.triple_hits:
        print(
            f"  {hit.names}: counts={hit.counts} "
            f"remainders={hit.remainders} all-close={hit.all_close}"
        )
    print("sparse packet matrix")
    for row in audit.sparse_matrix:
        print("  " + " ".join("-" if value is None else str(value) for value in row))
    for label, probability in (
        ("natural diagonal=56", audit.natural_diagonal_probability),
        ("natural diagonal in quotient set", audit.natural_any_target_probability),
        ("any slot assignment and quotient", audit.full_slot_probability),
    ):
        print(
            f"{label}: {probability.numerator}/{probability.denominator}="
            f"{float(probability):.12f}"
        )


if __name__ == "__main__":
    main()
