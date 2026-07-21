#!/usr/bin/env python3
"""Report label-invariant lower bounds for simple adaptive deck models."""

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.deck_invariants import (
    forced_adaptive_rank_count,
    repeated_working_set_ranks,
)


def main() -> None:
    messages = tuple(trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER)
    ranks = tuple(
        rank for message in messages for rank in repeated_working_set_ranks(message)
    )
    print("repeated occurrences:", len(ranks))
    print("distinct forced move-to-front ranks:", len(set(ranks)))
    print("forced rank range:", min(ranks), max(ranks))
    print("forced ranks above 25:", sum(rank > 25 for rank in ranks))
    print(
        "lower bound with first trigram skipped:",
        forced_adaptive_rank_count(messages, skip_first=True),
    )
    print("move-to-back has the same count via rank = 82 - working-set rank")


if __name__ == "__main__":
    main()
