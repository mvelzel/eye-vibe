# Discarded A–Z initial-state audit — results

## Outcome

The 26-step initializer is executable but does not rescue either bounded
cipher family.

The implementation passes two planted continuations: after encrypting and
discarding a known prefix, both the affine-GAK state and the materialized
base/top-swap deck decode the untouched visible suffix exactly. Decoding the
same suffix from the canonical reset fails, so the audit is sensitive to the
proposed mechanism.

## Eye results

The affine audit combines the three frozen alphabet readings, three marker
modes, and every valid member of the four already-used multiplier families:

```text
valid candidates       2,205
zero mismatches            0
best mismatch score  119/230
decoded support           82
```

Including the empty-warm-up control raises the valid count to 3,189 but leaves
the optimum at `119/230`. The initializer changes candidates without creating
the expected small plaintext alphabet or repeated plaintext.

The physical-deck audit exhausts 15,236 distinct bases: all 6,806 affine
`F83` permutations plus the deduplicated named interleave, Mongean, Josephus,
fixed-card `82`, and removed-dummy `84` constructions. With two marker modes:

```text
warm-up candidates      91,416
zero mismatches              0
best warm-up score       86/230
decoded support              82

empty-control candidates 30,472
best empty-control score 85/230
decoded support             82
```

All three warm-up readings attain 86 mismatches at best. The canonical reset
is one mismatch better. Selection across the complete finite family is already
included in these minima; there is no survivor to calibrate statistically.

## Interpretation

Reject the exact discarded `A-Z` / Trailer-Altar initializer for:

1. the structured affine-GAK multiplier families;
2. a fixed structured base permutation followed by one plaintext-selected
   top swap.

Do **not** reject the general initial-state idea, arbitrary GAK/XGAK, or the
possibility that the deliberately overflowing 26-glyph render width is an
English-alphabet hint. Those broader claims still lack an independently known
operation set and are not identifiable from this ciphertext-only test.

## Reproduction

```bash
PYTHONPATH=src python scripts/audit_alphabet_warmup.py --family all --limit 40
PYTHONPATH=src python -m unittest tests.test_alphabet_warmup
```
