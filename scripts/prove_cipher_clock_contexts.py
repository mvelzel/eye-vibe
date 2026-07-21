#!/usr/bin/env python3
"""Test repeated-plaintext contexts against a fixed cipher-clock input ring.

The output ring is an arbitrary permutation of all 83 ciphertext labels.  The
input ring may start at any cyclic alignment, and can optionally be reversed.
For each message, the Wadsworth mechanism is reset before the marker or before
the marker-free body.  A context family asserts only that its aligned passages
decode to the same sequence of input-ring symbols; no plaintext is supplied.
"""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass

import z3

from eye_mystery.cipher_clock import AKI_DISK_INPUT_RING
from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values


@dataclass(frozen=True)
class ContextFamily:
    name: str
    length: int
    occurrences: tuple[tuple[str, int], ...]


# Positions are zero-based in the complete trigram messages, including their
# distinct initial markers.  These are the high-confidence public isomorphs
# used by the other exact group-autokey certificates in this workbench.
CONTEXTS = {
    "first-six": ContextFamily(
        "first-six",
        9,
        (
            ("east1", 40),
            ("east1", 68),
            ("west1", 40),
            ("west1", 70),
            ("east2", 45),
            ("east2", 80),
        ),
    ),
    "first-long": ContextFamily(
        "first-long",
        18,
        (
            ("west1", 34),
            ("west1", 64),
            ("east2", 39),
            ("east2", 74),
        ),
    ),
    "last-three": ContextFamily(
        "last-three",
        30,
        (
            ("east4", 68),
            ("west4", 71),
            ("east5", 69),
        ),
    ),
}


def constant_ring_array(ring: str) -> z3.ArrayRef:
    """Return an integer array containing compact codes for ring symbols."""

    symbol_codes = {symbol: index for index, symbol in enumerate(sorted(set(ring)))}
    result = z3.K(z3.IntSort(), z3.IntVal(-1))
    for index, symbol in enumerate(ring):
        result = z3.Store(result, index, symbol_codes[symbol])
    return result


def solve(
    ring: str,
    contexts: tuple[ContextFamily, ...],
    *,
    omit_markers: bool,
    timeout_ms: int,
    fixed_input_shift: int | None = None,
) -> tuple[z3.CheckSatResult, z3.ModelRef | None]:
    streams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)

    required_ends: dict[str, int] = {}
    for context in contexts:
        for message, start in context.occurrences:
            required_ends[message] = max(
                required_ends.get(message, 0), start + context.length
            )

    stream_start = 1 if omit_markers else 0
    used_symbols = sorted(
        {
            symbol
            for message, end in required_ends.items()
            for symbol in streams[message][stream_start:end]
        }
    )
    output_positions = {
        symbol: z3.Int(f"p_{symbol}") for symbol in used_symbols
    }
    solver.add(
        *(
            z3.And(0 <= position, position < 83)
            for position in output_positions.values()
        )
    )
    # An injective placement of every used label always extends to a full S83
    # output ring.  Omitting unused labels removes a factorial symmetry.
    solver.add(z3.Distinct(tuple(output_positions.values())))

    if fixed_input_shift is None:
        input_shift: z3.ArithRef = z3.Int("input_shift")
        solver.add(0 <= input_shift, input_shift < len(ring))
    else:
        if fixed_input_shift not in range(len(ring)):
            raise ValueError("fixed input shift is outside the ring")
        input_shift = z3.IntVal(fixed_input_shift)
    ring_array = constant_ring_array(ring)

    decoded: dict[tuple[str, int], z3.ArithRef] = {}
    for message, end in required_ends.items():
        previous: z3.ArithRef = z3.IntVal(0)
        for full_position in range(stream_start, end):
            offset = z3.Int(f"o_{message}_{full_position}")
            output_lap = z3.Int(f"k83_{message}_{full_position}")
            symbol = streams[message][full_position]
            solver.add(output_lap >= 0)
            solver.add(
                offset == output_positions[symbol] + 83 * output_lap
            )
            solver.add(offset > previous, offset <= previous + 83)
            ring_index = z3.Int(f"i_{message}_{full_position}")
            input_lap = z3.Int(f"k{len(ring)}_{message}_{full_position}")
            solver.add(0 <= ring_index, ring_index < len(ring))
            solver.add(input_lap >= 0)
            solver.add(
                offset + input_shift
                == ring_index + len(ring) * input_lap
            )
            decoded[(message, full_position)] = z3.Select(
                ring_array, ring_index
            )
            previous = offset

    for context in contexts:
        reference_message, reference_start = context.occurrences[0]
        for displacement in range(context.length):
            reference = decoded[
                (reference_message, reference_start + displacement)
            ]
            for message, start in context.occurrences[1:]:
                solver.add(
                    decoded[(message, start + displacement)] == reference
                )

    status = solver.check()
    return status, solver.model() if status == z3.sat else None


def context_mismatches(
    ring: str,
    contexts: tuple[ContextFamily, ...],
    output_positions: list[int],
    input_shift: int,
    *,
    omit_markers: bool,
) -> int:
    """Count failed aligned-symbol equalities for one concrete mechanism."""

    streams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    required_ends: dict[str, int] = {}
    for context in contexts:
        for message, start in context.occurrences:
            required_ends[message] = max(
                required_ends.get(message, 0), start + context.length
            )
    decoded: dict[tuple[str, int], str] = {}
    for message, end in required_ends.items():
        absolute_offset = 0
        stream_start = 1 if omit_markers else 0
        for full_position in range(stream_start, end):
            target = output_positions[streams[message][full_position]]
            distance = (target - absolute_offset % 83) % 83
            absolute_offset += distance or 83
            decoded[(message, full_position)] = ring[
                (absolute_offset + input_shift) % len(ring)
            ]
    mismatches = 0
    for context in contexts:
        reference_message, reference_start = context.occurrences[0]
        for displacement in range(context.length):
            reference = decoded[
                (reference_message, reference_start + displacement)
            ]
            mismatches += sum(
                decoded[(message, start + displacement)] != reference
                for message, start in context.occurrences[1:]
            )
    return mismatches


def anneal(
    ring: str,
    contexts: tuple[ContextFamily, ...],
    *,
    omit_markers: bool,
    restarts: int,
    iterations: int,
    seed: int,
    descent_rounds: int,
) -> tuple[int, int, tuple[int, ...]]:
    """Seek a concrete satisfying output order before invoking exact search."""

    rng = random.Random(seed)
    overall: tuple[int, int, tuple[int, ...]] | None = None
    for restart in range(restarts):
        positions = list(range(83))
        rng.shuffle(positions)
        input_shift = rng.randrange(len(ring))
        current = context_mismatches(
            ring,
            contexts,
            positions,
            input_shift,
            omit_markers=omit_markers,
        )
        best = (current, input_shift, tuple(positions))
        for iteration in range(iterations):
            old_shift = input_shift
            if rng.random() < 0.05:
                input_shift = rng.randrange(len(ring))
                changed = None
            else:
                left, right = rng.sample(range(83), 2)
                positions[left], positions[right] = positions[right], positions[left]
                changed = (left, right)
            proposal = context_mismatches(
                ring,
                contexts,
                positions,
                input_shift,
                omit_markers=omit_markers,
            )
            progress = iteration / max(1, iterations - 1)
            temperature = 8.0 * (0.03 / 8.0) ** progress
            if proposal <= current or rng.random() < math.exp(
                (current - proposal) / temperature
            ):
                current = proposal
                if current < best[0]:
                    best = (current, input_shift, tuple(positions))
                    if current == 0:
                        break
            else:
                input_shift = old_shift
                if changed is not None:
                    left, right = changed
                    positions[left], positions[right] = positions[right], positions[left]
        if overall is None or best < overall:
            overall = best
        print(
            f"restart {restart + 1}: mismatches={best[0]} shift={best[1]}",
            flush=True,
        )
        if overall[0] == 0:
            break
    assert overall is not None
    score, input_shift, frozen_positions = overall
    positions = list(frozen_positions)
    for round_index in range(descent_rounds):
        candidate = (score, input_shift, tuple(positions))
        for proposed_shift in range(len(ring)):
            proposed_score = context_mismatches(
                ring,
                contexts,
                positions,
                proposed_shift,
                omit_markers=omit_markers,
            )
            if proposed_score < candidate[0]:
                candidate = (proposed_score, proposed_shift, tuple(positions))
        for left in range(82):
            for right in range(left + 1, 83):
                positions[left], positions[right] = positions[right], positions[left]
                proposed_score = context_mismatches(
                    ring,
                    contexts,
                    positions,
                    input_shift,
                    omit_markers=omit_markers,
                )
                if proposed_score < candidate[0]:
                    candidate = (proposed_score, input_shift, tuple(positions))
                positions[left], positions[right] = positions[right], positions[left]
        if candidate[0] >= score:
            break
        score, input_shift, frozen_positions = candidate
        positions = list(frozen_positions)
        print(
            f"descent {round_index + 1}: mismatches={score} shift={input_shift}",
            flush=True,
        )
        if score == 0:
            break
    overall = (score, input_shift, tuple(positions))
    return overall


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--context",
        action="append",
        choices=tuple(CONTEXTS),
        help="context family to assert; repeat to combine (default: all)",
    )
    parser.add_argument("--omit-markers", action="store_true")
    parser.add_argument("--reverse-input-ring", action="store_true")
    parser.add_argument("--input-shift", type=int)
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--anneal", action="store_true")
    parser.add_argument("--restarts", type=int, default=8)
    parser.add_argument("--iterations", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=20260721)
    parser.add_argument("--descent-rounds", type=int, default=8)
    args = parser.parse_args()

    names = tuple(args.context or CONTEXTS)
    contexts = tuple(CONTEXTS[name] for name in names)
    ring = AKI_DISK_INPUT_RING[::-1] if args.reverse_input_ring else AKI_DISK_INPUT_RING
    if args.anneal:
        best = anneal(
            ring,
            contexts,
            omit_markers=args.omit_markers,
            restarts=args.restarts,
            iterations=args.iterations,
            seed=args.seed,
            descent_rounds=args.descent_rounds,
        )
        print("best mismatches:", best[0])
        print("input shift:", best[1])
        print("output positions:", " ".join(map(str, best[2])))
        return
    status, model = solve(
        ring,
        contexts,
        omit_markers=args.omit_markers,
        timeout_ms=round(args.timeout * 1000),
        fixed_input_shift=args.input_shift,
    )
    print("contexts:", ", ".join(names))
    print("marker handling:", "omit/reset body" if args.omit_markers else "full/reset message")
    print("input direction:", "reversed" if args.reverse_input_ring else "forward")
    print("input alignments:", len(ring))
    print("output order class: arbitrary S83")
    print("result:", status)
    if model is not None:
        print(
            "input shift:",
            args.input_shift
            if args.input_shift is not None
            else model[z3.Int("input_shift")],
        )
        positions = {
            symbol: model[z3.Int(f"p_{symbol}")].as_long()
            for symbol in range(83)
            if model[z3.Int(f"p_{symbol}")] is not None
        }
        print(
            "used output positions:",
            " ".join(f"{symbol}:{position}" for symbol, position in positions.items()),
        )


if __name__ == "__main__":
    main()
