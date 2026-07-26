# Header orbit and conditional no-repeat ranks — results

**Date:** 26 July 2026  
**Outcome:** the orbit projection is non-identifying; the frozen dynamic
conditional-rank channel is negative.

## Header-orbit obstruction

The proposed row-1 train / rows-2–3 holdout design cannot select an `S6`
coordinate:

```text
coordinates 1..4   three row-1 singleton groups
coordinate 0       one all-three group (all headers fix center)
coordinate 5       one all-three group (P headers fix newline)
```

Coordinates 0 and 5 make different Q-row predictions but are identical on
training. Choosing between them from Q-body agreement would leak the holdout.
The exact lane therefore closes before a body statistic is fitted.

## Header-ordered no-repeat channel

For each message, the audit orders the visible 83 glyphs under its marker,
removes the previous glyph, and ranks the next among the remaining 82:

```text
rank = 41*sheet + magnitude
```

Four established nonliteral contexts select header or inverse-header from
magnitude agreement. Three other contexts are held out. All 6,806 affine
permutations of `0..82` preserve the complete equality structure and reselect
the route.

The real route scores are:

```text
route             train magnitude   holdout magnitude
header                    0/59              2/82
inverse-header            2/59              1/82  selected
```

Selected holdout details:

```text
last-west4   1/29 magnitude, 1/29 full rank
last-east5   0/29 magnitude, 0/29 full rank
last-east3   0/24 magnitude, 0/24 full rank
```

Exact controls:

```text
magnitude upper tail   5723/6806 = .840875698
control maximum        10/82
full-rank upper tail   3958/6806 = .581545695
```

Training selects equal sheets rather than complementary sheets, but heldout
agreement is only `41/82`, indistinguishable from a balanced bit.

## Decision

Close:

```text
fixed factoradic header collation
    -> delete previous glyph
    -> conditional rank in 0..81
    -> fixed 2x41 quotient
```

This does not reject a deck whose order changes after every emitted symbol.
It does reject the complete static marker-ordered no-repeat family, including
the most natural 41-class magnitude and full-rank readings.

## Reproduction

```text
PYTHONPATH=src python3 scripts/audit_header_no_repeat.py
```

Implementation:

- `src/eye_mystery/header_no_repeat.py`
- `tests/test_header_no_repeat.py`
