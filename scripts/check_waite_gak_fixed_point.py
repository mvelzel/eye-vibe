#!/usr/bin/env python3
"""Print the exact ordinary-GAK contradiction in the Waite East-2 crib."""

from __future__ import annotations

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.gak_fixed_point import find_stabilizer_contradictions
from check_waite_m3_suffix import EAST2_RAW_OFFSET, WAITE_M3_SUFFIX


def main() -> None:
    ciphertext = trigram_values(MESSAGES["east2"])[EAST2_RAW_OFFSET:]
    contradictions = find_stabilizer_contradictions(
        WAITE_M3_SUFFIX,
        ciphertext,
    )
    print("certificates:", len(contradictions))
    for index, item in enumerate(contradictions, 1):
        print(f"certificate {index}:")
        print("  observations:", item.observation_offsets)
        print(
            "  first:",
            (item.first.start, item.first.end),
            repr("".join(item.first.word)),
            "fixes" if item.first.fixes_top else "does not fix",
        )
        print(
            "  second:",
            (item.second.start, item.second.end),
            repr("".join(item.second.word)),
            "fixes" if item.second.fixes_top else "does not fix",
        )
        print(
            "  combined:",
            (item.combined.start, item.combined.end),
            repr("".join(item.combined.word)),
            "fixes" if item.combined.fixes_top else "does not fix",
        )
        print(
            "  cards:",
            tuple(ciphertext[offset] for offset in item.observation_offsets),
        )


if __name__ == "__main__":
    main()
