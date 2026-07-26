#!/usr/bin/env python3
"""Reproduce the matched phase-shift collision audit for Cipher 4."""

from __future__ import annotations

import json
from pathlib import Path

from eye_mystery.practice_cipher4_collisions import phase_shift_audit


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    messages = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher4.json").read_text()
    )
    audit = phase_shift_audit(messages)
    observed_pooled = (
        audit.within_bigram_collisions
        + audit.observed.cross_message_bigrams
    )
    bigram_ioc = (
        2 * observed_pooled
        / (audit.bigram_positions * (audit.bigram_positions - 1))
    )

    print("observed aligned unigram collisions:", audit.observed.aligned_unigrams)
    print(
        "observed cross-message bigram collisions:",
        audit.observed.cross_message_bigrams,
    )
    print("fixed within-message bigram collisions:", audit.within_bigram_collisions)
    print("observed pooled bigram collisions:", observed_pooled)
    print("observed pooled bigram IoC:", f"{bigram_ioc:.12f}")
    print("uniform Z83xZ83 baseline:", f"{1 / 83**2:.12f}")
    print("phase configurations:", audit.configurations)
    print(
        "aligned-unigram lower tail:",
        audit.unigram_lower_or_equal,
        f"corrected={audit.corrected_tail(audit.unigram_lower_or_equal, audit.configurations):.12f}",
    )
    print(
        "cross-bigram upper tail:",
        audit.bigram_upper_or_equal,
        f"corrected={audit.corrected_tail(audit.bigram_upper_or_equal, audit.configurations):.12f}",
    )
    print(
        "joint tail:",
        audit.joint_tail,
        f"corrected={audit.corrected_tail(audit.joint_tail, audit.configurations):.12f}",
    )
    print(
        "cross-bigram null min/mean/max:",
        audit.cross_bigram_minimum,
        f"{audit.cross_bigram_sum / audit.configurations:.12f}",
        audit.cross_bigram_maximum,
    )


if __name__ == "__main__":
    main()
