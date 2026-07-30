#!/usr/bin/env python3
"""Replay and print the public Aki/Patrick Eye automaton proposal."""

from __future__ import annotations

import math
from collections import Counter

from eye_mystery.corpus import MESSAGES
from eye_mystery.ninth_causal import CONTEXT_SPECS, equality_signature
from eye_mystery.public_automaton import GRAPH_SEED, decode, decode_all


def main() -> None:
    outputs = decode_all(MESSAGES)
    print("outputs:")
    for name, output in outputs.items():
        counts = Counter(output)
        entropy = -sum(
            (count / len(output)) * math.log2(count / len(output))
            for count in counts.values()
        )
        print(f"{name}\tlen={len(output)}\talphabet={len(counts)}\tentropy={entropy:.3f}")
        print(output)
    print("nonliteral context equality checks:")
    for name, left, left_start, right, right_start, length in CONTEXT_SPECS[6:]:
        left_signature = equality_signature(
            tuple(outputs[left][left_start : left_start + length])
        )
        right_signature = equality_signature(
            tuple(outputs[right][right_start : right_start + length])
        )
        agreements = sum(
            a == b for a, b in zip(left_signature, right_signature)
        )
        print(f"{name}\t{left_signature == right_signature}\t{agreements}/{length}")
    # Keep the source-authored graph.lua seed variant visible without mixing
    # it into the primary metrics above.
    graph_outputs = {name: decode(stream, seed=GRAPH_SEED) for name, stream in MESSAGES.items()}
    print("graph.lua alternate seed first lines:")
    for name, output in graph_outputs.items():
        print(f"{name}\t{output[:60]}")


if __name__ == "__main__":
    main()
