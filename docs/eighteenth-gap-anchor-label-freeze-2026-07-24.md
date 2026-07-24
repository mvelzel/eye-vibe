# Gap-anchor orthogonal label controls — freeze

## Purpose

The matched position/multiset controls promote an association between the
final-row headers and the unique clean gap-11 body anchors. They do not by
themselves distinguish a special assignment of numeric labels from structure
created by the equality skeleton.

Freeze two orthogonal global-label nulls before calculating either.

## Fixed input

Use only the already selected six values:

```text
anchors: 75,81,48
headers: 27,77,33
```

The clean-gap selector is label-invariant, so a global permutation changes
the anchor values but cannot change their positions, gap, uniqueness, or the
set of candidate gaps in the broad search.

For each null run 50,000 Fisher-Yates permutations of all 83 labels, using
seed `0x18b0d`. Report exact ordered and broad unordered match counts with
plus-one corrected tails.

## Null A: body-label assignment

Apply the same random permutation to all three anchor values and leave the
three markers fixed. This preserves the complete body equality skeleton and
asks whether the labels assigned to the selected landmarks are specially
coupled to the fixed headers.

## Null B: natural numeric coordinate

Apply the same random permutation to both the anchor values and the header
values. This preserves their common abstract alphabet labels while destroying
the natural base-5/orthodox numeric arithmetic. It asks whether the
`0..82 mod 83` coordinate itself is special.

## Statistics and gate

For each null compute:

1. the exact reported ordered formula;
2. the same broad statistic as the matched control, allowing all six anchor
   orders and ignoring header-to-edge assignment.

Promote the natural modular-coordinate interpretation only if the broad
corrected tail is below `.01` under both nulls. Otherwise retain only the
position/multiset association and do not call subtraction an authored
operation.
