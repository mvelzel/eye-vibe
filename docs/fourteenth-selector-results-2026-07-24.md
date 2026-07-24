# Fourteenth horizon: raw-eye selector result

## Outcome

The raw-eye selector-demultiplexing lane is negative.

The audit can recover its planted five-lane mechanism exactly. On the real
Eyes, the convention selected on the three P-header panels makes the six
Q-header panels substantially *less* language-like. Two of the first three
matched controls already beat the observed held-out result, making the frozen
`.01` promotion threshold unreachable.

No plaintext or candidate lane is promoted.

## Exact family

For each accepted trigram, one of the three raw eye digits is treated as a
selector in `0..4`. The other two, in their canonical field order, form an
opaque payload value in `0..24`. The payload is stably demultiplexed into five
selector lanes.

The complete family contains:

```text
3 selector positions
32 per-lane reversal masks
1 separate-lane convention
120 concatenated lane orders
11,616 distinct scored candidates
```

Both orders of the two payload fields were frozen originally. They need not be
run twice: swapping the fields maps every pair value `5a+b` bijectively to
`5b+a`, and the equality-pattern model is invariant under a global symbol
bijection. A unit test proves the equality signatures are identical for all
83 accepted labels. This is a symmetry quotient, not a data-dependent family
change.

The first 25 body glyphs are removed from every P panel and the first six from
every Q panel, so the known shared openings cannot directly create the score.
The complete convention is selected only on P. Q is consulted once for the
fixed winner. Global-label controls uniformly permute all accepted labels
`0..82`, preserving every equality, copied passage, message length, and
accepted-alphabet count while destroying the raw component roles.

## Positive control and calibration

The planted fixture splits an externally sourced text segment into five
contiguous payload chunks, interleaves them with explicit selector digits, and
places the selector in the third eye. The target inverse is:

```text
s2:concatenate:order=0,1,2,3,4:reverse=00000
```

The inherited order-8 pattern statistic selected a spurious reversal, so no
real score was admitted. Orders `8,10,12,14,16,20,24` were compared only on
the fixture. Order 14 is the smallest exact recovery and was frozen before the
real run.

Its planted result is:

```text
selected:             s2:concatenate:order=0,1,2,3,4:reverse=00000
exact target:         yes
train improvement:    +5.592867701
held-out improvement: +4.517634698
```

The method therefore has ample power to identify and generalize the mechanism
it is designed to test.

## Eye result

The P-selected Eye convention is:

```text
s1:concatenate:order=3,0,2,1,4:reverse=10111
train improvement:    +0.009392391
held-out improvement: -0.776995317
```

The train gain is negligible, and the held-out transform is actively harmful.
Matched control results began:

```text
controls run:          3 of planned 200
null held-out range:   -0.835055005 .. +0.476830329
null mean (first 3):   -0.239109946
null exceedances:      2
```

With the usual plus-one correction, two null exceedances imply a minimum
possible final tail of:

```text
(1 + 2) / (200 + 1) = 3/201 = 0.014925373
```

That already exceeds `.01`. Completing the other 197 controls can only
increase the numerator, so early stopping is an exact promotion rejection.
The three-control range and mean are diagnostics only, not estimates of the
complete null distribution.

## Interpretation

This rejects a stable global reading in which one eye routes the other two
into five payload lanes under any lane order and reversal mask in the frozen
family. It does not reject:

- a selector role that changes by panel or header type;
- a stateful selector-dependent substitution;
- cross-glyph reassociation of the eye tracks;
- another use of the three typed eye fields.

Those are not licensed repairs. Per the breadth horizon, the next move is
lateral to the shared-linear-generator or canonical-automaton lanes. A
per-header selector or fitted lane codebook would spend new capacity to rescue
a model whose global held-out prediction is already negative.

## Reproduction

```bash
PYTHONPATH=src python scripts/run_fourteenth_selector.py --controls 200
PYTHONPATH=src python -m unittest tests.test_fourteenth_selector -v
```

Definitions are in
[`fourteenth_selector.py`](../src/eye_mystery/fourteenth_selector.py), and the
frozen horizon is
[`fourteenth-wide-method-transfer-horizon-2026-07-24.md`](fourteenth-wide-method-transfer-horizon-2026-07-24.md).
