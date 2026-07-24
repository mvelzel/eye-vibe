# Twenty-fourth pass — first/second marker-row record transfer freeze

## Question

The final header row is a closed, self-describing record.  This test transfers
only its minimum field grammar to the two earlier rows:

1. each panel selects one clean equal-endpoint loop at a common gap;
2. the marker is `anchor[source] - anchor[remaining] mod 83`;
3. the omitted target column predicts the ordinary ascending ranks of the
   three anchor values.

No pointer convention, position order, language score, new arithmetic
operator, or panel-specific repair is admitted in this pass.

## Fixed rows

The established control edge is `middle -> first-1`; a non-self edge names
the component order `(source,target,remaining)`.

```text
row 1
E1  marker 50  order 012
W1  marker 80  order 120
E2  marker 36  order 201

row 2
W2  marker 76  order 021
E3  marker 63  order 210
W3  marker 34  order 102

row 3, already decoded
E4  marker 27  order 012
W4  marker 77  order 021
E5  marker 33  order 102
```

The natural copied openings are removed after the marker: 24 symbols in row
1, five in row 2, and 20 in row 3.  Clean loops and gaps have exactly the
definition used by the promoted final-row audit.  The prospective gap family
remains `2..30`.

## Header-only necessity

Before consulting the earlier bodies, test whether each row's three markers
can even be a gradient under the fixed slot rule.  For a row with orders
`o_j`, anchors `a=(a0,a1,a2)` must satisfy:

```text
h_j = a[o_j[0]] - a[o_j[2]] mod 83.
```

This is an exact linear feasibility check, not a statistic.  An infeasible row
rejects the same numeric record type for that row and its body is not searched
for a rescue.

## Primary row-1 prediction

For every gap `2..30`, find clean loops independently in E1, W1, and E2.
Admit a gap only when each panel has exactly one clean loop.  Let their
endpoint values, in panel order, be `a`.

The numeric field matches only if the fixed `source-minus-remaining` rule
reproduces `(50,80,36)` exactly.  The withheld field then asks whether:

```text
ordinal_ranks(a) = (1,2,0),
```

which is the already fixed target column of `012,120,201`.  This is also the
target column independently observed in the final row; it is not selected
from the real row-1 anchors.

Report:

- every real numeric-match gap and its anchors/positions;
- whether any also has the exact target-rank column;
- the number of controls with any numeric match;
- the number with any joint numeric-plus-rank match.

The joint event is primary.  Multiple real gaps are not cherry-picked: the
control reselects the complete gap family in the same way.

## Calibration and matched controls

A synthetic three-stream plant must contain one unique common-gap loop per
panel, reproduce the row-1 marker vector through the fixed slot rule, and
carry target ranks `(1,2,0)`.  The detector must recover it before the Eye
result is accepted.

Run 50,000 deterministic controls.  Independently shuffle each row-1 trimmed
body while preserving:

- exact length;
- exact symbol multiset;
- no adjacent doubles.

Markers, component orders, copied-opening trims, modulus, slot pair, rank
direction, and gap family remain frozen.  Use plus-one corrected inclusive
tails.

## Promotion and stop

Promote the field grammar to row 1 only if:

1. at least one real gap has one clean loop per panel;
2. the fixed slot rule reproduces all three markers;
3. the withheld target ranks are exact;
4. the fully reselected joint corrected tail is below `.01`.

A numeric-only match is retained as a failed prediction, not promoted.
Infeasibility or no joint match closes this exact transfer without trying a
different operator, sign, rank direction, trim, or gap range.  A promoted
result earns a separately frozen pointer/position prediction; this pass does
not inspect those fields.
