# Freeze: desert paired-record quotient on held-out contexts

## Hypothesis

The historical desert-glyph construction pairs accepted Eye trigrams, uses
component orders:

```text
y = 021
x = 120
```

and emits `x²+y`.  Its high IoC is partly an intrinsic collision effect, so
language scoring is not justified.  A narrower possibility remains: the lossy
quotient may deliberately make separately labelled versions of the same
record agree.

This test treats each of the seven fixed nonliteral context windows as one
record and resets the paired-trigram operation at the record boundary.  That
is a new, explicit record-local hypothesis; it is not silently presented as
the historical whole-message phase.

## Frozen transform

For each source and target context sequence:

1. convert every accepted rank `0..82` to its natural base-five trigram;
2. pair record trigrams as `(y,x)` from the record start;
3. append `000` only if the record length is odd;
4. read `y` in order `021` and `x` in order `120`;
5. emit the three values `x²+y` per pair.

The primary transform is fixed to `x²+y`.  The lossless `5x+y` reading is a
negative sanity check only.  No component order, phase, formula, or padding
rule is selected on the real contexts.

## Scoring

Contexts:

```text
descriptive/training:
  first-gap30, first-cross, first-cross-late, first-gap28

primary/held out:
  last-west4, last-east5, last-east3
```

For each aligned original input pair `(y,x)`, compare the three output
coordinates.  If both source labels equal their aligned target labels, exclude
all three coordinates as literal carryover.  Otherwise count literal output
agreements among the three coordinates.

Report:

- agreements and eligible coordinates in each individual context;
- aggregate training and held-out agreements;
- exact transformed context records;
- lossless `5x+y` sanity score;
- the document order's descriptive rank among all six relative component
  alignments, with no significance claim.

The only primary statistic is aggregate held-out `x²+y` agreement.

## Matched null

Generate 50,000 global permutations of accepted labels `0..82`, seed
`0xD1A607`.  Apply each permutation to the complete canonical accepted
trigram streams before extracting and transforming contexts.

This preserves:

- all message lengths and context boundaries;
- every exact copied label and equality skeleton;
- all seven partial-isomorph structures;
- the accepted alphabet and global label frequencies;
- the same record-local pairing and odd padding.

It destroys only the natural base-five coordinate assigned to each accepted
label.  The empirical inclusive tail is:

```text
(controls with held-out score >= real + 1) / 50,001
```

Promote only below `.01`.  The historical IoC tails are not multiplied with
this result because the representation and corpus are shared.

## Positive fixture and stop rule

A planted fixture must demonstrate that a nontrivial relabelled record can
collapse under `x²+y`, while the scoring code excludes fully copied input
pairs and detects the planted held-out agreement.

If the primary tail fails, close the record-local quotient.  Do not choose a
different formula, component order, pair phase, context subset, label map, or
substitution alphabet afterward.  A later use of the desert assets would need
an independent in-game consumer.

