# Twelfth wide horizon — second lateral batch results

## Outcome

All five lateral screens close. One intentionally broad control produced a
false raw-phase anomaly; the required accepted-trigram-preserving validation
made it disappear. The only other sharp descriptive rank—the P-header
line-digraph split—fails the exact model by 6,046 false-positive transitions
and has only 9.22% predictive precision.

Reproduce with:

```sh
PYTHONPATH=src python3 scripts/run_twelfth_second_batch.py --controls 200
```

The fixed seed is `0xE1E1202`. A 5,000-control refinement of the strict
raw-phase occupancy null gives upper tail `.902020`.

## F. Visible symbols as line-digraph edges

Give every visible label a hidden tail and head. Each observed transition
`u->v` forces `head(u)=tail(v)`. On all 843 distinct body transitions, the
equality closure is:

```text
hidden states:          1
predicted transitions:  6,889 / 6,889
forced absent edges:    6,046
```

Thus the exact support is maximally false: the closure collapses the graph and
predicts every absent transition.

Training only on the independently defined P-header triple gives 16
components. Against the six Q panels:

```text
novel predictions: 5,377
novel truth:         594
hits:                496
precision:        .092245
recall:           .835017
F1:               .166136
rank:                 1/84 training triples
```

The rank-one F1 is retained as a descriptive fact, not promoted. The P panels
also share the largest copied prefix, leaving a smaller and less connected
training support; the resulting closure predicts most of the alphabet square.
High recall from 5,377 guesses does not repair 9.22% precision or the exact
6,046-edge contradiction.

## H. Rejected raw phases

At each accepted-glyph boundary the two crossing base-5 trigrams visit the
unused `83..124` range:

```text
phase totals:       314, 312
marker/body hits:     0,   3  of 9
row-boundary hits:   16,   5  of 34
```

The initially frozen within-visual-row direction shuffle gives a seemingly
strong maximum-total tail `.004975`. That control preserves row direction
counts but destroys the defining fact that each accepted trigram is a legal
`0..82` glyph. It is therefore a useful sensitivity check, not a valid
occupancy null.

The stricter validation shuffles whole accepted trigrams separately within
each authored row-pair and downward/upward parity lane. It preserves every
accepted glyph, row-pair multiset, and triangle parity while changing only
adjacency. Under 200 controls:

```text
strict null maximum: 310..330, mean 318.075
observed maximum:    314
upper tail:          .910448
```

The 5,000-control refinement gives `.902020`. Boundary selection is also
negative: marker familywise tail `.800995`, row tail `.069652`, and joint-max
tail `.054726`. The two descriptive maxima occur in different phases, so
there is no marker/row replication. No rejected-phase side channel advances.

## I. `AG(2,3)` panel line sums

For each aligned body column 25–97, the nine panels occupy a 3×3 affine plane.
Each of four directions closes when its three parallel line sums agree.
All row orders and independent within-row orders consistent with the three
natural panel rows are selected on columns 25–60 and tested on 61–97.

```text
field  natural train/test  selected train/test  heldout upper tail
F5     1 / 6               6 / 7                .388060
F83    0 / 1               0 / 1                .094527
```

The `F83` training scan has no closure at all and its heldout singleton is an
ordinary chance event. The `F5` selected grid does not generalize. No affine
plane design advances.

## J. Bounded physical shuffle actions

The frozen dictionary contains 373 distinct actions on 83 positions:
all nontrivial cuts, reversal, four odd-deck interleaves, four Monge variants,
Josephus deals, inverses, and powers two through eight of the eight core
interleave/Monge shuffles.

Against the seven nonliteral partial contexts:

```text
best common action:       monge-T-fwd^2
common support:           5 / 117
common upper tail:        1.000000
best per-context support: 2,2,2,1,2,2,3
exact contexts:           0 / 7
per-context-sum tail:     .995025
```

The observed corpus agrees with the named physical operations less than
shuffled injective maps do. The card-magic vocabulary remains historically
plausible, but this fixed repertoire is not the body action.

## K. Two-register header-controlled transducer

A deterministic table sees the previous two raw eye directions and predicts
the next. For each heldout panel it trains on the other two panels in the same
factoradic header class, and scoring begins only after that panel's established
deepest prefix-leaf exit.

```text
P/Q-west/Q-east: 626 / 2,601 = .240677
rank:             81 / 280 triple partitions
unconditioned:   628 / 2,601 = .241446
best partition:  675 / 2,601 = .259516
```

The independently established header partition is ordinary and slightly worse
than training on all other panels. This exact tiny transducer closes; larger
state machines are not justified by this result.

## Decision

No second-batch lane advances. The remaining genuinely different families in
the wide horizon are spectral organization, a five-ary convolutional
syndrome, exact engine-storage bitplanes, conventional-mode necessary
conditions, and independently selected executable clue interfaces. The
signed-projective quotient is deferred because its parent projective lane
already failed and it would not restore breadth.
