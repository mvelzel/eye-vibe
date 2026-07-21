#!/usr/bin/env python3
"""Print the strongest exact gap-pattern repetitions in the eye corpus."""

from __future__ import annotations

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.isomorphs import repeated_patterns, score


def main() -> None:
    messages = tuple(trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER)
    patterns = repeated_patterns(messages)
    patterns = {
        candidate: positions
        for candidate, positions in patterns.items()
        if candidate[0] != "."
        and candidate[-1] != "."
        and len(
            {
                tuple(messages[message][position : position + len(candidate)])
                for message, position in positions
            }
        )
        > 1
    }
    ranked = sorted(
        patterns.items(),
        key=lambda item: score(item[0], len(item[1])),
        reverse=True,
    )
    print(" score pattern                                       positions (0-based)")
    for candidate, positions in ranked[:50]:
        locations = ", ".join(
            f"{MESSAGE_ORDER[message]}:{position}" for message, position in positions
        )
        print(
            f"{score(candidate, len(positions)):>6.2f} "
            f"{candidate:<45} {locations}"
        )


if __name__ == "__main__":
    main()
