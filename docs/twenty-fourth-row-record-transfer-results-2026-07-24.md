# Twenty-fourth pass — first/second marker-row record transfer results

## Result

The final row's complete field grammar does **not** transfer to either earlier
row. The rejection is exact and occurs before body-landmark selection:

```text
row 1  numeric slot equations feasible, target-rank field impossible
row 2  numeric slot equations impossible
final  numeric slot equations and target-rank field feasible
```

Consequently no earlier body was searched for a favorable clean loop and no
matched-control tail is reported. The preregistered positive plant itself
cannot be constructed for row 1, so proceeding to body shuffles would violate
the calibration gate.

## Fixed equation

For each row and panel `j`, the final-row rule was held unchanged:

```text
h_j = a[order_j[0]] - a[order_j[2]] mod 83.
```

The omitted middle slot was required to equal the ordinary ascending ranks of
the three anchor values.

## Row 1

The row-1 orders and equations are:

```text
E1  012   a0-a2 = 50
W1  120   a1-a0 = 80
E2  201   a2-a1 = 36
```

They are numerically integrable because:

```text
50 + 80 + 36 = 166 = 0 mod 83.
```

There are exactly 83 solutions, one for each additive gauge. Every solution
has three distinct anchors. Across all gauges, their ordinary rank patterns
are exactly:

```text
021, 102, 210
```

The already fixed target column of `012,120,201` is `120`. It occurs zero
times. Thus a row-1 plant satisfying both frozen fields does not exist.

## Row 2

The row-2 orders and equations are:

```text
W2  021   a0-a1 = 76
E3  210   a2-a0 = 63
W3  102   a1-a2 = 34
```

Their cycle sum is:

```text
76 + 63 + 34 = 173 = 7 mod 83,
```

but every gradient around a closed cycle must sum to zero. Exhaustive
enumeration confirms that there are no anchor solutions.

## Positive calibration

The identical code recovers the known final record:

```text
anchors       75,81,48
headers       27,77,33
anchor ranks  1,2,0
```

The final equations have 83 gauge-shifted numeric solutions, 50 of which have
the required `120` rank field. The detector therefore accepts a legitimate
instance; the earlier-row negatives are not an implementation artifact.

## Interpretation

This closes the literal idea that all three marker rows repeat one
source-minus-remaining/ascending-rank record schema. It does **not** weaken
the promoted final-row record. Instead, it sharpens the row typing:

- row 1 is a genuine zero-circulation cycle and may carry a gradient/check
  field, but not with the final row's ordinary target-rank semantics;
- row 2 has a nonzero circulation residue `7`, so it must be a different
  record type if the edge interpretation is meaningful;
- the final row is the only one presently known to combine numeric
  differences, rank metadata, position order, and a pointer gauge.

Do not search earlier bodies under a different sign, rank direction, trim, or
gap as a rescue. A future row-typed model needs an independently selected
meaning for the row-2 residue `7` and must predict a body field before fitting
landmarks.

## Reproduction

```bash
PYTHONPATH=src python3 scripts/audit_row_record_transfer.py
PYTHONPATH=src python3 -m unittest tests.test_row_record_transfer
```

Implementation: `src/eye_mystery/row_record_transfer.py`.
