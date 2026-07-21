#!/usr/bin/env python3
"""Calibrated coordinate search for plaintext-selected sparse deck shuffles.

The model is ``swap(top, rank); swap(u_rank, v_rank)`` with the second swap
fixed for each plaintext instruction and restricted below the top card.  One
coordinate round exhaustively tests every hidden transposition for every rank
encountered by the current decode, then commits the single best change.

Synthetic mode first generates messages satisfying the same 230 equality
constraints and encrypts them with a requested number of planted active rules.
This measures the search's recovery radius before a negative real-data result
is interpreted.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.deck_base_generic import (
    BaseOrbitTables,
    build_base_orbit_tables,
)
from eye_mystery.deck_shuffles import standard_base_candidates
from eye_mystery.sparse_deck import no_swap_rules
from search_sparse_deck import comparison_pairs


@dataclass(frozen=True)
class Layout:
    ciphertexts: tuple[tuple[int, ...], ...]
    offsets: tuple[int, ...]
    body_indices: tuple[int, ...]
    comparisons: tuple[tuple[int, int], ...]
    base: tuple[int, ...]
    tables: BaseOrbitTables
    position_shift: int


@dataclass(frozen=True)
class Score:
    objective: int
    mismatches: int
    body_unique: int
    full_unique: int
    decoded: tuple[int, ...]

    @property
    def key(self) -> tuple[int, int, int]:
        return self.objective, self.mismatches, self.body_unique


def build_layout(
    ciphertexts: tuple[tuple[int, ...], ...],
    base: tuple[int, ...] | None = None,
    *,
    position_shift: int = 0,
) -> Layout:
    if base is None:
        base = tuple(range(83))
    offsets = []
    total = 0
    for message in ciphertexts:
        offsets.append(total)
        total += len(message)
    name_index = {name: index for index, name in enumerate(MESSAGE_ORDER)}
    comparisons = tuple(
        (
            offsets[name_index[left_name]]
            + left_position
            - position_shift,
            offsets[name_index[right_name]] + right_position - position_shift,
        )
        for (left_name, left_position), (
            right_name,
            right_position,
        ) in comparison_pairs()
    )
    body_indices = tuple(
        offsets[message_index] + position
        for message_index, message in enumerate(ciphertexts)
        for position in range(0 if position_shift else 1, len(message))
    )
    return Layout(
        ciphertexts,
        tuple(offsets),
        body_indices,
        comparisons,
        base,
        build_base_orbit_tables(base, max(map(len, ciphertexts))),
        position_shift,
    )


def decode_layout(
    layout: Layout, rules: tuple[tuple[int, int], ...]
) -> tuple[int, ...]:
    size = len(rules)
    result: list[int] = []
    for ciphertext in layout.ciphertexts:
        coordinate_of = list(range(size))
        card_at_coordinate = list(range(size))

        def swap_coordinates(left: int, right: int) -> None:
            if left == right:
                return
            left_card = card_at_coordinate[left]
            right_card = card_at_coordinate[right]
            card_at_coordinate[left], card_at_coordinate[right] = (
                right_card,
                left_card,
            )
            coordinate_of[left_card], coordinate_of[right_card] = right, left

        for step, card in enumerate(ciphertext, start=1):
            card_coordinate = coordinate_of[card]
            rank = layout.tables.inverse_powers[step][card_coordinate]
            result.append(rank)
            swap_coordinates(
                layout.tables.top_coordinates[step], card_coordinate
            )
            coordinates = layout.tables.coordinates_at_positions[step]
            left, right = rules[rank]
            swap_coordinates(coordinates[left], coordinates[right])
    return tuple(result)


def score_rules(
    layout: Layout,
    rules: tuple[tuple[int, int], ...],
    *,
    mismatch_weight: int,
    unique_weight: int,
) -> Score:
    decoded = decode_layout(layout, rules)
    mismatches = sum(
        decoded[left] != decoded[right]
        for left, right in layout.comparisons
    )
    body_unique = len({decoded[index] for index in layout.body_indices})
    full_unique = len(set(decoded))
    return Score(
        mismatch_weight * mismatches + unique_weight * body_unique,
        mismatches,
        body_unique,
        full_unique,
        decoded,
    )


class DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


def synthetic_layout(
    template: Layout,
    rng: random.Random,
    *,
    active_rules: int,
    alphabet_size: int,
) -> tuple[Layout, tuple[tuple[int, int], ...]]:
    total = sum(map(len, template.ciphertexts))
    sets = DisjointSet(total)
    for left, right in template.comparisons:
        sets.union(left, right)
    marker_indices = set(template.offsets) - set(template.body_indices)
    component_values: dict[int, int] = {}
    plaintext = [0] * total
    for index in range(total):
        if index in marker_indices:
            message_index = template.offsets.index(index)
            plaintext[index] = alphabet_size + 1 + message_index
            continue
        root = sets.find(index)
        component_values.setdefault(root, rng.randrange(1, alphabet_size + 1))
        plaintext[index] = component_values[root]

    rules = list(no_swap_rules(83))
    marker_ranks = set(range(alphabet_size + 1, alphabet_size + 10))
    used_body_ranks = sorted(set(plaintext) - marker_ranks)
    if active_rules > len(used_body_ranks):
        raise ValueError("more active rules requested than used plaintext ranks")
    for rank in rng.sample(used_body_ranks, active_rules):
        rules[rank] = tuple(rng.sample(range(1, 83), 2))
    planted = tuple(rules)
    ciphertexts = tuple(
        encrypt_base_sparse_deck(
            plaintext[offset : offset + len(message)],
            template.base,
            planted,
        )
        for offset, message in zip(
            template.offsets, template.ciphertexts, strict=True
        )
    )
    return build_layout(
        ciphertexts,
        template.base,
        position_shift=template.position_shift,
    ), planted


def encrypt_base_sparse_deck(
    plaintext: list[int] | tuple[int, ...],
    base: tuple[int, ...],
    rules: tuple[tuple[int, int], ...],
) -> tuple[int, ...]:
    deck = list(range(len(base)))
    ciphertext = []
    for rank in plaintext:
        deck = [deck[base[position]] for position in range(len(base))]
        deck[0], deck[rank] = deck[rank], deck[0]
        ciphertext.append(deck[0])
        left, right = rules[rank]
        deck[left], deck[right] = deck[right], deck[left]
    return tuple(ciphertext)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=1)
    parser.add_argument("--mismatch-weight", type=int, default=100)
    parser.add_argument("--unique-weight", type=int, default=1)
    parser.add_argument("--seed", type=int, default=20260721)
    parser.add_argument(
        "--synthetic-active-rules",
        type=int,
        help="calibrate on a planted cipher with this many nontrivial rules",
    )
    parser.add_argument("--synthetic-alphabet", type=int, default=26)
    parser.add_argument(
        "--base",
        default="identity",
        help="standard base-candidate name, or identity",
    )
    parser.add_argument(
        "--marker-mode", choices=("full", "reset"), default="full"
    )
    parser.add_argument(
        "--initial-rule",
        action="append",
        default=[],
        metavar="RANK:LEFT:RIGHT",
        help="seed a learned non-top rule; may be repeated",
    )
    args = parser.parse_args()

    rng = random.Random(args.seed)
    candidates = dict(standard_base_candidates(83))
    if args.base == "identity":
        base = tuple(range(83))
    elif args.base in candidates:
        base = candidates[args.base]
    else:
        raise SystemExit(f"unknown standard base: {args.base}")
    position_shift = 1 if args.marker_mode == "reset" else 0
    template = build_layout(
        tuple(
            trigram_values(MESSAGES[name])[position_shift:]
            for name in MESSAGE_ORDER
        ),
        base,
        position_shift=position_shift,
    )
    layout = template
    planted = None
    if args.synthetic_active_rules is not None:
        layout, planted = synthetic_layout(
            template,
            rng,
            active_rules=args.synthetic_active_rules,
            alphabet_size=args.synthetic_alphabet,
        )

    mutable_rules = list(no_swap_rules(83))
    for specification in args.initial_rule:
        try:
            rank, left, right = map(int, specification.split(":"))
        except ValueError as error:
            raise SystemExit(
                f"invalid --initial-rule {specification!r}"
            ) from error
        if not 0 <= rank < 83 or not 0 < left < 83 or not 0 < right < 83:
            raise SystemExit(
                f"out-of-range --initial-rule {specification!r}"
            )
        mutable_rules[rank] = (left, right)
    rules = tuple(mutable_rules)
    current = score_rules(
        layout,
        rules,
        mismatch_weight=args.mismatch_weight,
        unique_weight=args.unique_weight,
    )
    if planted is not None:
        planted_score = score_rules(
            layout,
            planted,
            mismatch_weight=args.mismatch_weight,
            unique_weight=args.unique_weight,
        )
        print(
            f"planted: mismatches={planted_score.mismatches} "
            f"body_unique={planted_score.body_unique} "
            f"full_unique={planted_score.full_unique}",
            flush=True,
        )
        print(
            "active planted rules:",
            {
                rank: swap
                for rank, swap in enumerate(planted)
                if swap[0] != swap[1]
            },
            flush=True,
        )
    print(
        f"start: mismatches={current.mismatches} "
        f"body_unique={current.body_unique} "
        f"full_unique={current.full_unique}",
        flush=True,
    )

    transpositions = tuple(
        (left, right)
        for left in range(1, 83)
        for right in range(left + 1, 83)
    )
    hidden_candidates = transpositions + ((1, 1),)
    for round_index in range(args.rounds):
        candidate_ranks = sorted(set(current.decoded))
        best = current
        best_rules = rules
        tested = 0
        for rank_index, rank in enumerate(candidate_ranks, start=1):
            for hidden_swap in hidden_candidates:
                if hidden_swap == rules[rank]:
                    continue
                proposal_rules = list(rules)
                proposal_rules[rank] = hidden_swap
                proposal_rules_tuple = tuple(proposal_rules)
                proposal = score_rules(
                    layout,
                    proposal_rules_tuple,
                    mismatch_weight=args.mismatch_weight,
                    unique_weight=args.unique_weight,
                )
                tested += 1
                if proposal.key < best.key:
                    best = proposal
                    best_rules = proposal_rules_tuple
            if rank_index % 10 == 0 or rank_index == len(candidate_ranks):
                print(
                    f"round={round_index + 1} ranks={rank_index}/"
                    f"{len(candidate_ranks)} tested={tested} "
                    f"best={best.mismatches}/{best.body_unique}",
                    flush=True,
                )
        if best.key >= current.key:
            print("no improving single-rule change", flush=True)
            break
        changed = tuple(
            rank
            for rank, (old, new) in enumerate(zip(rules, best_rules, strict=True))
            if old != new
        )
        rules = best_rules
        current = best
        print(
            f"commit round={round_index + 1} rank={changed[0]} "
            f"swap={rules[changed[0]]} mismatches={current.mismatches} "
            f"body_unique={current.body_unique} "
            f"full_unique={current.full_unique}",
            flush=True,
        )

    print(
        "active learned rules:",
        {
            rank: swap
            for rank, swap in enumerate(rules)
            if swap[0] != swap[1]
        },
    )


if __name__ == "__main__":
    main()
