# Seventy-first pass — lazy injection geometry results

## Outcome

The lazy exact solver passed its controls but did not decide any of the three
remaining pairs within 120 seconds:

```text
pair                              rounds  collision cuts  outcome
first-gap30 + first-cross             4              38  UNKNOWN
last-west4 + last-east5              12             237  UNKNOWN
last-east5 + last-east3              79             856  UNKNOWN
```

No timeout is interpreted as evidence.

## Controls

The solver:

- recovered the jointly SAT pair with unique coordinates;
- accepted both halves of the split equal-distance star;
- confirmed that the star union is SAT without injection;
- rejected that union only after adding collision cuts.

This verifies that the lazy loop enforces the intended complete injection
condition rather than merely replaying chord algebra.

## Structural diagnostic

The promised separator check finds no cheap decomposition.

```text
pair                         labels edges cycles primal width class width
first-gap30 + first-cross       31    50     20       11          7
last-west4 + last-east5         54    87     34       13         11
last-east5 + last-east3         54    82     29       13         16
```

Widths are deterministic min-fill upper bounds, not exact treewidth. The first
label graph is biconnected. Each last-family graph has one articulation, but
the distance-class variables reconnect the corresponding primal graph, which
has no articulation. Every cycle-class graph is connected.

Thus neither context intersection nor an articulation splits the exact CSP.
The next method should exploit the ternary constraint
`distance(z[u],z[v])=d[class]` directly rather than another monolithic solver.

## Reproduction

```text
PYTHONPATH=src python3 scripts/run_hidden_geometry_lazy.py
PYTHONPATH=src python3 scripts/analyze_hidden_geometry_separators.py
PYTHONPATH=src python3 -m unittest tests.test_hidden_geometry_lazy
```
