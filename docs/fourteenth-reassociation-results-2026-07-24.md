# Fourteenth horizon: typed cross-glyph reassociation result

## Outcome

The frozen typed cross-glyph reassociation lane is exactly negative.

The audit recovers its planted mechanism exactly. On the real Eyes, however,
none of the 225 predeclared routes can reconstruct every P-panel glyph inside
the observed `0..82` alphabet. The same is independently true of the six Q
panels. This necessary range condition fails before language scoring, model
selection, or controls.

No reassociated stream or plaintext is promoted.

## Exact family

Write every accepted glyph as its three typed base-five eye components. For
one component at a time, partition its track into blocks of period 2 through
26 and apply exactly one operation within every block:

```text
shift-left by one
shift-right by one
reverse
```

The other two component tracks remain fixed. Partial final blocks are routed
using their actual length. Recombine the three components into raw base-five
ranks and reject a candidate if any rank lies in the 42 unused cube positions
`83..124`.

The complete frozen family therefore contains:

```text
3 moved components × 25 periods × 3 routes = 225 candidates
```

The first 25 body glyphs are removed from each P panel and the first six from
each Q panel, matching the earlier protection against the known copied
openings. Had a route survived the range gate, it would have been selected on
P by the already frozen order-14 equality-pattern model and tested unchanged
on Q under complete global-label controls.

## Positive control

The planted fixture uses plaintext values only in `0..24`, encrypts by moving
component 2 one place right inside period-seven blocks, and keeps both
ciphertext and plaintext inside the accepted alphabet. Its exact inverse is:

```text
c2:p7:shift-left
```

The complete selector recovers exactly that route:

```text
selected:             c2:p7:shift-left
exact target:         yes
train improvement:    +5.842783471
held-out improvement: +4.030816846
```

The family therefore has enough power to identify and generalize the
mechanism it is intended to test.

## Eye result

The number of routes valid on every panel in each frozen split is:

| Split | Valid routes |
|---|---:|
| P training panels | `0 / 225` |
| Q held-out panels | `0 / 225` |
| All nine panels | `0 / 225` |

For diagnosis only, the per-panel valid-route counts are:

| Panel | Valid routes |
|---|---:|
| East 1 | 19 |
| West 1 | 8 |
| East 2 | 56 |
| West 2 | 0 |
| East 3 | 8 |
| West 3 | 40 |
| East 4 | 33 |
| West 4 | 3 |
| East 5 | 71 |

West 2 alone excludes the complete family, while both the P and Q
intersections are empty even without relying on that single-panel fact.
Because validity is a prerequisite rather than a score, no winner exists and
there is no language statistic or Monte Carlo tail to report.

## Interpretation

This rejects every stable global rule in the frozen family that cyclically
shifts or reverses exactly one typed eye track in short blocks while requiring
the reconstructed text to use the same accepted `0..82` alphabet as the
visible messages.

It does not reject:

- a transformation whose intermediate or plaintext alphabet deliberately
  uses ranks `83..124`;
- a route selected by panel, header class, or an external authored control;
- offsets that cross the frozen block boundaries in a different way;
- a stateful reassociation involving more than one component;
- typed eyes serving another non-positional role.

Those are different hypotheses, not repairs licensed by this failure.
Allowing the 42 missing cube states would especially change the data model
from “misaligned accepted glyphs” to a larger-alphabet code and must be tested
as its own broad lane with an independent reason for reduction.

## Reproduction

```bash
PYTHONPATH=src python scripts/run_fourteenth_reassociation.py --controls 200
PYTHONPATH=src python -m unittest tests.test_fourteenth_reassociation -v
```

Definitions are in
[`fourteenth_reassociation.py`](../src/eye_mystery/fourteenth_reassociation.py),
and the frozen portfolio is in
[`fourteenth-wide-method-transfer-horizon-2026-07-24.md`](fourteenth-wide-method-transfer-horizon-2026-07-24.md).
