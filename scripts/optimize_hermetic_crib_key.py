#!/usr/bin/env python3
"""Extend the verified four-transposition Hermetic crib witness.

Ranks and the lower witness's first hidden swap remain fixed.  Greedy
coordinate descent exhausts every non-top transposition for the two remaining
hidden slots (and all three slots of upper-only letters), scoring exact
reencryption of the 24-letter upper and 20-letter lower ciphertext prefixes.
"""

from __future__ import annotations

import argparse

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.sparse_deck import encrypt_sparse_deck_hidden_sequences


UPPER = "THATWHICHISABOVEISLIKETO"
LOWER = "THEREISNOGOODTHATCAN"

RANKS = {
    "T": 66,
    "H": 18,
    "A": 68,
    "W": 13,
    "I": 2,
    "C": 36,
    "S": 60,
    "B": 61,
    "O": 40,
    "E": 49,
    "R": 75,
    "N": 29,
    "G": 59,
    "D": 15,
    "V": 14,
    "L": 78,
    "K": 70,
}

TOP14_RULES = {
    "T": ((5, 18), (3, 62), (48, 60)),
    "H": ((18, 55), (48, 68), (60, 68)),
    "A": ((3, 66), (9, 61), (55, 60)),
    "W": ((2, 29), (18, 75), (36, 48)),
    "I": ((9, 18), (24, 36), (24, 60)),
    "C": ((54, 68), (2, 42), (36, 70)),
    "S": ((59, 66), (17, 24), (9, 13)),
    "B": ((40, 61), (10, 40), (32, 40)),
    "O": ((9, 40), (18, 36), (7, 64)),
    "E": ((18, 54), (1, 9), (9, 36)),
    "R": ((18, 49), (1, 24), (1, 60)),
    "N": ((59, 60), (17, 18), (7, 13)),
    "G": ((9, 18), (18, 18), (40, 64)),
    "D": ((29, 47), (2, 2), (1, 36)),
    "V": ((1, 1), (1, 1), (1, 1)),
    "L": ((1, 1), (1, 1), (1, 1)),
    "K": ((1, 1), (1, 1), (1, 1)),
}

FULL_RULES = dict(TOP14_RULES)
FULL_RULES.update(
    {
        "S": ((59, 66), (2, 8), (9, 13)),
        "B": ((1, 9), (1, 15), (32, 40)),
        "V": ((8, 29), (49, 59), (49, 81)),
        "L": ((9, 49), (1, 1), (1, 1)),
    }
)


def build_rules(
    by_letter: dict[str, tuple[tuple[int, int], ...]],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    rules = [((1, 1), (1, 1), (1, 1)) for _ in range(83)]
    for letter, swaps in by_letter.items():
        rules[RANKS[letter]] = swaps
    return tuple(rules)


def score(
    by_letter: dict[str, tuple[tuple[int, int], ...]],
    upper_plaintext: str,
    lower_plaintext: str,
) -> tuple[int, int, int]:
    rules = build_rules(by_letter)
    upper = encrypt_sparse_deck_hidden_sequences(
        tuple(RANKS[letter] for letter in upper_plaintext), rules
    )
    lower = encrypt_sparse_deck_hidden_sequences(
        tuple(RANKS[letter] for letter in lower_plaintext), rules
    )
    upper_target = trigram_values(MESSAGES["east1"])[
        1 : 1 + len(upper_plaintext)
    ]
    lower_target = trigram_values(MESSAGES["east4"])[
        1 : 1 + len(lower_plaintext)
    ]
    upper_misses = sum(
        observed != expected
        for observed, expected in zip(upper, upper_target, strict=True)
    )
    lower_misses = sum(
        observed != expected
        for observed, expected in zip(lower, lower_target, strict=True)
    )
    return upper_misses + lower_misses, upper_misses, lower_misses


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=20)
    parser.add_argument("--upper", default=UPPER)
    parser.add_argument("--lower", default=LOWER)
    parser.add_argument(
        "--start", choices=("top14", "full"), default="top14"
    )
    args = parser.parse_args()

    upper_plaintext = args.upper.upper()
    lower_plaintext = args.lower.upper()
    unknown = set(upper_plaintext + lower_plaintext) - set(RANKS)
    if unknown:
        raise SystemExit(f"missing fixed ranks for letters: {sorted(unknown)}")
    if len(upper_plaintext) > len(trigram_values(MESSAGES["east1"])) - 1:
        raise SystemExit("upper crib is longer than the East 1 body")
    if len(lower_plaintext) > len(trigram_values(MESSAGES["east4"])) - 1:
        raise SystemExit("lower crib is longer than the East 4 body")

    rules = dict(TOP14_RULES if args.start == "top14" else FULL_RULES)
    current = score(rules, upper_plaintext, lower_plaintext)
    print(
        f"start total={current[0]} upper={current[1]} lower={current[2]}",
        flush=True,
    )
    transpositions = ((1, 1),) + tuple(
        (left, right)
        for left in range(1, 83)
        for right in range(left + 1, 83)
    )
    lower_letters = set(lower_plaintext)
    used_letters = tuple(dict.fromkeys(upper_plaintext + lower_plaintext))
    coordinates = tuple(
        (letter, slot)
        for letter in used_letters
        for slot in range(1 if letter in lower_letters else 0, 3)
    )
    for round_index in range(args.rounds):
        best = current
        best_rules = rules
        best_change = None
        tested = 0
        for letter, slot in coordinates:
            for hidden_swap in transpositions:
                if hidden_swap == rules[letter][slot]:
                    continue
                proposal = dict(rules)
                swaps = list(proposal[letter])
                swaps[slot] = hidden_swap
                proposal[letter] = tuple(swaps)
                proposal_score = score(
                    proposal, upper_plaintext, lower_plaintext
                )
                tested += 1
                if proposal_score < best:
                    best = proposal_score
                    best_rules = proposal
                    best_change = letter, slot, hidden_swap
        if best_change is None:
            print(f"round={round_index + 1} no improvement tested={tested}")
            break
        rules = best_rules
        current = best
        print(
            f"round={round_index + 1} change={best_change} "
            f"total={current[0]} upper={current[1]} "
            f"lower={current[2]} tested={tested}",
            flush=True,
        )
        if current[0] == 0:
            break
    print("rules:")
    for letter in RANKS:
        print(f"  {letter} rank={RANKS[letter]} swaps={rules[letter]}")


if __name__ == "__main__":
    main()
