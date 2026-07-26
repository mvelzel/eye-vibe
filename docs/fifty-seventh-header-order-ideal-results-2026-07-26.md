# Header-ordered codebook boundary — results

**Date:** 26 July 2026  
**Outcome:** both frozen static codebook channels are negative.

## Construction tested

This wide pass combined three real facts:

```text
complete eye cube       5^3 = 125
visible glyphs                  83
omitted glyphs                  42
```

and the independently recovered factoradic marker order. Two distinct
per-message transforms were frozen before their results:

1. **omission count:** full-cube rank minus visible-codebook rank, necessarily
   in `0..42`;
2. **visible rerank:** the glyph's bijective rank within the fixed visible
   `0..82` codebook.

Both use only the marker or its inverse as the global eye collation. Four
established nonliteral contexts select that route; three untouched contexts
score literal output equality. Every one of the 6,806 affine permutations of
`0..82` reruns the selection while preserving the complete equality and
copied-prefix structure.

## Omission-count result

The route scores `(training / 63, holdout / 85)` are:

```text
header           17/63   36/85
inverse-header   20/63   62/85   selected
```

Selected holdout details:

```text
last-west4   22/30
last-east5   30/30
last-east3   10/25
```

The exact matched-control result is:

```text
heldout upper tail   70/6806 = .010285043
control maximum      67/85
real output support  10 values
support lower tail   201/6806 = .029532765
value 42 used        yes
```

This misses the predeclared `.01` gate. More importantly, the perfect
East4/East5 cell is not a hidden 42-symbol plaintext. East5's inverse marker
induces the canonical eye order, for which every visible word has omission
count zero. The complete holdout pairs are:

```text
last-west4  (0,0) or (0,25)
last-east5  (0,0) only
last-east3  (0,0) or (0,17)
```

Across whole bodies, East5 is constant zero and East4 uses only `{0,5}`.
The apparent literalization is therefore a coarse-bucket artifact already
charged by the exact controls.

## Bijective visible-rerank result

The separately frozen non-degenerate follow-up gives:

```text
route             training   holdout
header               1/63       0/85
inverse-header       3/63       1/85   selected

heldout upper tail   3665/6806 = .538495445
control maximum      8/85
```

Its one holdout match lies in `last-east5`; the other two holdouts have zero.
Thus the real headers do not transport the known nonliteral maps into a
canonical visible-label space.

## Decision

Close these exact static interfaces:

```text
factoradic marker collation -> rank in visible 83-word codebook
factoradic marker collation -> count of preceding omitted cube words
```

Do not rescue the omission channel with a chosen letter assignment, offset,
extra component order, or message-specific route. The wider header-orbit,
conditional no-repeat, ordered-trie, and externally selected stateful lanes
remain distinct and untested.

## Reproduction

```text
PYTHONPATH=src python3 scripts/audit_header_order_ideal.py
PYTHONPATH=src python3 scripts/audit_visible_codebook_rerank.py
```

Implementation and tests:

- `src/eye_mystery/header_order_ideal.py`
- `tests/test_header_order_ideal.py`
