#!/usr/bin/env python3
"""Run the frozen Cessation terminal sampler on the Earthquake wheel."""

from eye_mystery.cessation_wheel import run_cessation_wheel_audit


def print_result(label, result) -> None:
    print(label)
    print("  orientation:", result.orientation)
    print(
        "  training:",
        f"{result.training.agreements}/{result.training.changed_positions}",
        f"exact={result.training.exact_contexts}/{result.training.contexts}",
    )
    print(
        "  held out:",
        f"{result.heldout.agreements}/{result.heldout.changed_positions}",
        f"exact={result.heldout.exact_contexts}/{result.heldout.contexts}",
    )


def main() -> None:
    audit = run_cessation_wheel_audit()
    print_result("terminal-aware", audit.real)
    print_result("uniform endpoint", audit.uniform_endpoint)
    print("controls:", audit.controls)
    print("control hits:", audit.control_hits)
    print("inclusive exact tail:", f"{audit.tail:.9f}")
    print("passes:", audit.passes)
    print("held-out distribution:")
    for score, count in audit.heldout_distribution:
        print(f"  {score}: {count}")


if __name__ == "__main__":
    main()

