#!/usr/bin/env python3
"""Run the frozen minimal-dictionary-automaton Eye audit."""

from __future__ import annotations

from collections import Counter

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.fourteenth_automata import (
    failure_link_sieve,
    minimal_dictionary_automaton,
)
from eye_mystery.trie_checksum import (
    signature_preserving_relabeling_calibration,
)


def count_vector(values) -> tuple[int, ...]:
    counts = Counter(values)
    return tuple(counts[label] for label in range(83))


def main() -> None:
    streams = {
        name: trigram_values(MESSAGES[name])
        for name in MESSAGE_ORDER
    }
    bodies = {name: stream[1:] for name, stream in streams.items()}
    result = minimal_dictionary_automaton(
        bodies,
        alphabet_size=83,
        modulus=101,
    )
    print("MINIMAL DICTIONARY AUTOMATON")
    print(
        f"  trie nodes/transitions="
        f"{result.trie_nodes}/{result.trie_transitions}"
    )
    print(
        f"  minimal nodes/transitions="
        f"{result.minimal_nodes}/{result.minimal_transitions}"
    )
    print(
        f"  accepting_classes={result.accepting_classes}; "
        f"internal_merged_nodes={result.internal_merged_nodes}"
    )
    print(f"  class_sizes={result.class_sizes[:20]}")
    print(
        f"  transition_total={result.transition_total}; "
        f"residue101={result.transition_residue}"
    )

    diagonal = tuple(
        count_vector(streams[name])
        for name in ("east1", "east3", "east5")
    )
    marker_labels = tuple(streams[name][0] for name in MESSAGE_ORDER)
    calibration = signature_preserving_relabeling_calibration(
        result.label_multiplicities,
        diagonal,
        fixed_labels=marker_labels,
    )
    print(
        f"  matched_zero={calibration.zero_count}/"
        f"{calibration.total}="
        f"{calibration.zero_count / calibration.total:.9f}"
    )

    failure = failure_link_sieve(
        bodies,
        alphabet_size=83,
        modulus=101,
    )
    print("FAILURE LINK SIEVE")
    print(
        f"  trie_nodes={failure.trie_nodes}; "
        f"selected_nodes={failure.selected_nodes}"
    )
    print(
        f"  incoming_total={failure.incoming_total}; "
        f"residue101={failure.incoming_residue}"
    )
    print(
        f"  failure_depth_histogram="
        f"{failure.failure_depth_histogram}"
    )
    print(
        f"  depth_drop_prefix={failure.depth_drop_word[:40]}"
    )
    print(f"  bexit_positions={failure.bexit_positions}")

    failure_calibration = signature_preserving_relabeling_calibration(
        failure.label_multiplicities,
        diagonal,
        fixed_labels=marker_labels,
    )
    print(
        f"  matched_zero={failure_calibration.zero_count}/"
        f"{failure_calibration.total}="
        f"{failure_calibration.zero_count / failure_calibration.total:.9f}"
    )


if __name__ == "__main__":
    main()
