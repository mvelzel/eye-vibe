# Sixty-third pass — header/packet cardinality results

## Result

The established odd-East header control graph exactly predicts the checksum
self-pointer packet cardinalities:

```text
message  edge  source indegree  packet count  total
E1       0->1        1               2          3
E3       2->1        0               3          3
E5       1->0        2               1          3
```

Thus:

```text
packet_count = family_size - indegree(edge source)
```

This is a genuine header-side consumer that uses no packet values or
positions. Its selectivity is modest, and it does not validate the proposed
distance payload.

## Incidence interpretation

Give a row one slot for each checksum-family edge whose target is not the
row edge's source. In `E1,E3,E5` order the header-derived mask is:

```text
        E1 E3 E5
E1       1  1  0
E3       1  1  1
E5       0  0  1
```

Its row sums are `2,3,1`, exactly the observed quotient-occurrence counts.
The rule therefore supplies a plausible reason that the three packets have
different lengths and a tentative set of column roles for each packet.

## Assignment and formula calibration

Assigning the observed count multiset `{1,2,3}` to the three fixed edges in
all six ways gives:

```text
exact source-indegree complement     1/6
any endpoint/direction/orientation   2/6
```

The broadened family allows:

```text
endpoint     source or target
degree       in or out
orientation  1+degree or 3-degree
```

Only one formula matches the observed vector:

```text
source indegree, 3-degree
```

The other accepted count assignment is the opposite monotone orientation
`1+source_indegree`. The relation is therefore structurally exact but not a
small-probability discovery on three labels.

Across every unordered three-message subset:

```text
2/84 triples satisfy count+source_indegree=3
```

They are:

```text
E1,W2,W3  counts 2,2,2  sum remainders 0,53,1
E1,E3,E5  counts 2,3,1  sum remainders 0,0,0
```

The odd-East family is the only satisfying triple whose three full sums close
modulo 101. Checksum closure selected that family before this ledger, so this
is useful specificity rather than an independent `1/84` probability.

## Prospective matrix-value test

Assigning packet elements in stream order to the included columns in natural
family order gives:

```text
        E1 E3 E5
E1      13  7  -
E3      11 13 21
E5       -  - 30
```

The diagonal sum is `13+13+30=56=q_E3`. Exact conditional position controls
give:

```text
natural diagonal equals 56               .017007903217
natural diagonal equals any quotient      .039143708098
any slot assignment and any quotient      .181748976281
```

The fully corrected event is ordinary. Close the diagonal/matrix-value lane;
do not inspect other matrix sums, determinants, symmetry, row orders, or
missing-cell fills.

## Bounded current-WAK follow-up

The previous Lua audit covered modulo/range `42/83/101` but not quotient
extraction. A new exact scan of all 1,077 current-WAK Lua files searched
comment-stripped source for literal division by `101`, including
`math.floor(.../101)`.

```text
division-by-101 hits: 0
```

There can therefore be no Lua quotient-to-table-index or combined
`/101 -> mod83` flow in the current WAK. This does not exclude a construction
tool outside the shipped game, or a visual rather than executable later clue.
Native immediates remain out of scope without a named call path.

## Decision

Retain the cardinality equation as a constrained, low-strength header/body
link:

```text
quotient occurrences + source indegree = checksum-family size
```

It improves the checksum self-pointer lead because an independently
established header graph explains packet size. It is not enough to promote
the full extractor:

- the formula was recognized after seeing three counts;
- only three panels participate;
- the prospective slot values fail broad correction;
- no authored quotient interface is present in shipped Lua.

The next valid advance must predict the numeric payload's order or sign from
another established type, or find an independent construction-time operation.
Do not continue mining the sparse matrix.
