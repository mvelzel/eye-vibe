# Sixty-third pass — header/packet cardinality freeze

## Question

Can the previously established header control graph explain the cardinalities
of the new odd-East checksum-quotient packets without using their numeric
contents?

The checksum family is fixed independently as:

```text
E1,E3,E5
```

Its established control edges, from header digits
`middle -> first-1`, are:

```text
E1  0->1
E3  2->1
E5  1->0
```

The complete quotient-occurrence counts found in the sixty-second pass are:

```text
E1,E3,E5 = 2,3,1
```

## Discovered ledger

Within the induced three-edge control graph, source-node indegrees are:

```text
source node       0  2  1
indegree          1  0  2
packet count      2  3  1
sum               3  3  3
```

Equivalently:

```text
packet_count(message) =
    family_size - indegree(source(message))
```

This has an incidence interpretation: a message's packet has one slot for
each family edge whose target is not that message's source. The fixed mask in
`E1,E3,E5` row/column order is:

```text
        E1 E3 E5
E1       1  1  0
E3       1  1  1
E5       0  0  1
```

Its row sums are exactly `2,3,1`. This assigns packet *slots* but does not yet
assign the observed numeric distances to columns.

## Frozen tests

### A. Exact checksum-family ledger

Require all three equations:

```text
count + indegree(source) = 3
```

No packet value or position enters this test.

### B. Count-label permutation

Keep the three header edges fixed and assign the observed count multiset
`{1,2,3}` to the three messages in all six ways.

Report:

1. assignments satisfying the exact source-indegree complement;
2. assignments satisfying either monotone orientation
   `count=1+degree` or `count=3-degree` after selecting among:
   - source indegree;
   - source outdegree;
   - target indegree;
   - target outdegree.

The second statistic charges selection of endpoint, degree direction, and
orientation. A candidate formula must produce the exact count vector; no
fitted intercept is allowed.

### C. All-triple calibration

For every unordered three-message subset of the nine panels:

1. compute each full-sum Euclidean quotient `floor(sum/101)`;
2. count its body occurrences;
3. build the subset's induced control-edge graph;
4. test the same exact `count+indegree(source)=3` ledger.

Report all satisfying triples and whether their three full sums close modulo
101. The odd-East family was selected by checksum closure before the packet
ledger, so this is calibration rather than a replacement null.

### D. Slot-order boundary

Preserve the natural family order `E1,E3,E5` when writing included columns.
This gives tentative slot assignments:

```text
E1  (E1,E3)
E3  (E1,E3,E5)
E5  (E5)
```

Inventory the resulting sparse numeric matrix, but do not score arbitrary
matrix properties, reorder packet elements, or fill missing cells. A value
consumer must be predicted from another interface before it can be tested.

## Prospective slot-value test

After executing the cardinality calibration but before running any
position-control for values, the fixed incidence slots give:

```text
        E1 E3 E5
E1      13  7  -
E3      11 13 21
E5       -  - 30
```

The forced diagonal exists in all three rows and has sum:

```text
13 + 13 + 30 = 56 = q_E3
```

Freeze exactly these nested events under the sixty-second pass's conditional
position null:

1. **Natural diagonal:** assign each packet in stream-position order to the
   included columns in natural family order `E1,E3,E5`; require diagonal sum
   `56`.
2. **Target correction:** keep the natural assignment but allow the diagonal
   sum to equal any fixed checksum quotient in `{40,56,45}`.
3. **Full slot correction:** allow every bijection between a row's packet
   elements and its included columns and any target in `{40,56,45}`.

For the full correction, the event is equivalent to selecting any one
distance from each row packet whose sum is a checksum quotient. Enumerate it
exactly from the conditioned position subsets; do not use Monte Carlo.

Do not inspect row sums, column sums, off-diagonal sums, determinants,
symmetry, alternate row/column orders, directed distances, or another target
set in this pass. The already reported packet sums are not a prospective
matrix result.

## Decision rule

Promote the cardinality ledger as a constrained header/body link if:

- the exact relation holds;
- the count-assignment and formula-family calibrations show it is genuinely
  selective; and
- the all-triple inventory does not reveal that the same rule is ubiquitous.

Even a positive result explains only packet size. It does not validate
shortest circular distance, packet element order, packet sums, or plaintext.

## Bounded WAK follow-up

The earlier executable-interface audit already closed literal modulo/range
`42/83/101` and target-derived lookup flow. Do not repeat that scan.

The new self-pointer suggests one operation not covered by the old grammar:
integer quotient extraction by division by 101. Search every current-WAK Lua
file for:

1. literal division by `101`, including `math.floor(.../101)`;
2. an assigned quotient used as a table index within 20 lines;
3. a single function-sized window containing division by `101`, arithmetic
   by `83`, and a table lookup.

Report every path and source line. Free literals, `Random(0,100)`, localization
text, and native binary immediates do not qualify. With no named native call
path, do not mine the executable.
