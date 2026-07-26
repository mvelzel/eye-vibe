# Forty-second pass — cache/allocator results

## Result

The late equality trace does **not** drive a small adaptive allocator by
itself.

The strongest frozen family contained `55,360,004` models per panel. It
combined:

- every rotation/reflection of the 83-card source deck;
- seven independent source updates;
- seven independent target updates;
- every affine target deck `a*x+b mod 83`, `a != 0`.

No model reproduced the 30-symbol training window. The maxima were:

| Target panel | Dihedral target | Full affine target |
|---|---:|---:|
| E4 | 5/30 | 7/30 |
| W4 | 7/30 | 7/30 |
| E5 | 6/30 | 6/30 |

The affine co-best E4 and W4 models matched none of their held-out suffixes.
The representative E5 co-best set matched at most one later position, but
missed the first holdout (`6` predicted versus `72` actual). These partial
fits have no evidentiary value given the family size.

The promotion gate—complete training replay followed by a held-out
prediction—failed in every panel.

## The identifiability obstruction

The common training trace has 25 equality classes in 30 positions. Its
signature is unchanged by every injective relabeling of those classes.
With 83 available visible ranks, it is compatible with

```text
83 × 82 × ... × 59
= 16,785,454,253,887,894,484,829,623,545,293,779,238,912,000,000
```

numeric assignments, or about `153.556` bits of choice.

Consequently, a deterministic rule whose only input is the equality trace
cannot select the observed visible ranks. A cache can explain retrieval
events, but a fresh-value allocator requires a non-equivariant numeric input:

- another synchronized stream;
- a fixed numeric deck or key;
- arithmetic state seeded outside the trace;
- or a reproducible asset-derived control tape.

This is why replaying class IDs through FIFO/LRU/MTF-style policies is
circular unless the rule also identifies where new numeric values come from.

## Implication for the Gate theory

The result does not reject the Gate as later construction vocabulary.
It sharpens the missing part of the theory. The proposed Type6 cache may
classify references, but its unresolved first-seen branch is not a minor
implementation detail: it must contribute roughly 154 bits over this
30-symbol phase, or point to the independent carrier that does.

The next useful Gate test is therefore not another cache policy. It is a
search for a reproducible numeric carrier that is fixed without reading the
Eye labels and predicts at least one fresh value.

## Reproduction

```bash
PYTHONPATH=src python3 scripts/audit_cache_allocator.py
```

The implementation is in
`src/eye_mystery/cache_allocator_screen.py`; focused tests are in
`tests/test_cache_allocator_screen.py`.

