#!/usr/bin/env python3
"""Audit the metadata-selected quasi-uniform radix-5 rANS decoder."""

from eye_mystery.rans_358 import eye_rans_audit


def main() -> None:
    results = eye_rans_audit()
    for result in sorted(
        results,
        key=lambda value: (
            value.pattern_equal_contexts,
            value.common_prefix,
            value.literal_matches,
        ),
        reverse=True,
    ):
        print(
            f"singleton={result.singleton:<5} reverse={str(result.reverse):<5} "
            f"quotient={result.quotient} "
            f"literal={result.literal_matches}/{result.compared} "
            f"prefix={result.common_prefix} "
            f"patterns={result.pattern_equal_contexts}/7"
        )
        for context in result.contexts:
            print(
                f"  {context.name:<18} "
                f"lengths={context.left_length},{context.right_length} "
                f"literal={context.literal_matches}/{context.compared} "
                f"prefix={context.common_prefix} "
                f"pattern={context.pattern_equal}"
            )


if __name__ == "__main__":
    main()
