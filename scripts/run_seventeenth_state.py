#!/usr/bin/env python3
"""Run parameter-free state-reconstruction probes."""

from eye_mystery.seventeenth_state import (
    coarsest_equitable_partition,
    fibration_audit,
    partition_is_equitable,
    planted_regular_cover,
)


def main() -> None:
    plant, expected = planted_regular_cover()
    recovered = coarsest_equitable_partition(plant)
    print(
        "plant",
        f"expected={len(expected)}",
        f"recovered={len(recovered)}",
        f"equitable={partition_is_equitable(plant, recovered)}",
        f"exact={recovered == expected}",
    )
    print("real")
    for audit in fibration_audit():
        print(audit)


if __name__ == "__main__":
    main()
