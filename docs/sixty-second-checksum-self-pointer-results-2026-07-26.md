# Sixty-second pass — checksum-quotient self-pointer results

## Result

Retain a new high-priority odd-East construction lead:

```text
full sum / 101 -> quotient q
locate q in its own message
measure shortest circular mod-83 distances from q to those positions
```

For the three messages whose full sums close modulo 101, the complete
all-occurrences output is:

```text
message  sum   q   occurrence positions  circular-distance packet  packet sum
E1       4040  40  27,33                 13,7                      20
E3       5656  56  45,69,118             11,13,21                  45
E5       4545  45  75                    30                        30
```

This is not a body decoder or plaintext. The mechanism was discovered
retrospectively, so it remains a lead rather than a promoted fact. It is much
cleaner than the original one-occurrence observation because it consumes all
six occurrences without discarding an outlier.

## Primary self-pointer observation

Before circular reduction, the absolute position distances are:

```text
E1  13,7
E3  11,13,62
E5  30
```

Selecting one occurrence per message recovers independently known quantities:

```text
E1  7   row-2 phase budget
E3  11  clean-repeat gap
E5  30  late common-phase length
```

Under exact controls that keep each first glyph, sum, quotient, quotient
occurrence count, and all other body data fixed while uniformly relocating
only the quotient occurrences:

```text
typed 7|11|30 event             12931/410873085  = .000031472006
all target-to-message orders   1732222/9176165565 = .000188774057
```

These rates correct occurrence choice, distance sign, and target assignment.
They do not correct the retrospective choice of this three-target subset or
of the quotient self-pointer hypothesis itself.

## Typed coordinate graph

The selected positions are also established field values:

```text
E1 positions 27,33  = two final-row headers from {27,77,33}
E3 position 45      = a checksum quotient from {40,56,45}
E5 position 75      = a final gap anchor from {75,81,48}
```

Exact conditional rates are:

```text
typed field assignment                         .000001092532
any H/Q/A assignment, at least one hit each   .000628861201
```

The stronger-looking rule that *every* message occurrence belongs to its
assigned field class is false: E3 also has occurrences at 69 and 118. This
negative result is preserved rather than hiding those positions.

## All-occurrences packet

Position 118 reduces to 35 modulo 83, whose shortest distance from 56 is 21.
The resulting six values:

```text
13,7 | 11,13,21 | 30
```

all belong to the previously executed state-machine scalar ledger:

```text
3,4,6,7,11,13,15,17,20,21,25,28,29,30,34
```

The exact conditional containment rate is:

```text
4277/2203161 = .001941301612
```

More specifically, the three packet sums are:

```text
13+7       = 20  E4 bridge width
11+13+21   = 45  E5 checksum quotient
30         = 30  late common-phase width
```

The fixed typed sums occur at:

```text
5837/2446977484 = .000002385392
```

Allowing all six assignments of `{20,45,30}` to the three packets gives:

```text
367453/36704662260 = .000010011072
```

These are overlapping measurements of the same six positions and must not be
multiplied.

## Header repair interpretation

Subtracting the packet sums from the three checksum headers gives:

```text
50-20 = 30  late phase width
63-45 = 18  invisible 101-83 states
33-30 = 3   Gate/phase repair operator
```

The exact typed residual is algebraically identical to the fixed packet-sum
event. Allowing all six assignments of residuals `{30,18,3}` gives:

```text
74201/3670466226 = .000020215688
```

This offers a possible typed interpretation for the packet targets, but it is
still retrospective and mixes three different kinds of control quantity.

## Six-panel holdout

The universal nine-message extractor fails:

```text
message  sum   q   remainder  positions  packet
W1       4124  40  84         none       none
E2       4754  47   7         42         5
W2       4295  42  53         10,44      32,2
W3       4748  47   1         42,68      5,21
E4       5385  53  32         none       none
W4       4936  48  88         none       none
```

Three packets are empty and four of the five emitted values are outside the
frozen scalar ledger. The identical rule is therefore specific, if real, to
the odd-East zero-remainder checksum subsystem.

## Evidential boundary and next prediction

The conditional probabilities answer a narrow question: given the observed
quotient multiplicities, the positions form an unusually coherent record.
They do not account for every conceivable arithmetic transform that could
have been tried after seeing the corpus. The result should therefore guide
new tests, not be advertised as a solved cipher layer.

The next advance must be independent:

1. derive why quotient occurrences are references from a header type or
   in-game interface;
2. predict how packet order/sign is consumed before inspecting another body
   quantity; or
3. find an authored `sum/101 -> locate quotient -> mod83 distance` operation
   in source or assets and use it to predict a held-out Eye field.

Do not mine alternate moduli, distance conventions, packet aggregations, or
larger scalar ledgers around this result.
