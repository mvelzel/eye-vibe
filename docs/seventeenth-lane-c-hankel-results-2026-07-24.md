# Seventeenth horizon lane C — predictive Hankel results

## Result

The frozen shallow empirical-Hankel test is negative. A calibrated periodic
plant is recovered, but the Eye heldout split is full rank over every
registered field and has corrected control tail `1.0`.

This closes only low empirical Hankel rank at depths `(1,1)`, `(2,1)`, and
`(1,2)` after the known copied openings are removed. It does not exclude a
larger automaton, a symbol quotient selected independently, panel-dependent
state, or a state signature requiring longer words.

## Positive control

The fixed 36-step hub/leaf period is evaluated through exactly the same
message lengths, P/Q split, rank code, and 200 no-adjacent-double multiset
shuffles as the Eyes:

```text
split  depth  shape   ranks over F83,F101,F257  score
P      1,1    28x28   20,20,20                  .285714286
Q      1,1    28x28   20,20,20                  .285714286
```

No shuffled control reaches the real heldout deficit. The corrected tail is
`1/201 = .004975124`, Q adds zero rank, and the plant passes. As predicted by
the pre-data algebraic audit, every control selects `(1,1)`.

The deeper plant blocks are full at their smaller dimension. This is the
finite reset/boundary behavior that motivated retaining them as diagnostics
rather than retroactively adding them to the original selected-block gate.

## Eye matrices

Markerless bodies are trimmed by 24, 5, or 20 symbols according to the known
copied-opening classes. Reset boundaries are never crossed.

```text
split  depth  shape    ranks over F83,F101,F257  score
P      1,1     75x75   72,72,72                  .040000000
P      2,1    298x75   75,75,75                  .000000000
P      1,2     75x298  75,75,75                  .000000000

Q      1,1     84x84   84,84,84                  .000000000
Q      2,1    679x84   84,84,84                  .000000000
Q      1,2     84x679  84,84,84                  .000000000
```

P's shallow three-rank deficit does not transfer. Q contains all 83 glyph
labels, and its empty word plus 83 singleton words form an invertible
`84x84` empirical block in all three fields. Its selected deficit is zero.
All 200 controls have a Q deficit at least zero, so the corrected upper tail
is:

```text
201/201 = 1.000000000
```

The continuation prediction also fails:

```text
d_P = 72
d_Q = 84
heldout rank excess = 12
```

## Decision

Do not infer a 72-state machine from P. Its deficit disappears completely on
the independently heldout panels and has no rarity under the matched null.
Close the registered shallow raw-label empirical-Hankel lane and move
laterally in the seventeenth horizon.

Possible future Hankel work needs an independently justified quotient or
state representation before it is opened. Increasing word depth alone is not
licensed by this result and cannot repair the already full Q `(1,1)` block.
