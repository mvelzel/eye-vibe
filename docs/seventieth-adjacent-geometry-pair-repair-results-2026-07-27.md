# Seventieth pass — unresolved-pair witness search results

## Outcome

Neither frozen repair method found a complete witness for any of the three
remaining pairs:

```text
pair                              direct     class constraints  class pairs
first-gap30 + first-cross         33/34      33/34              53/55
last-west4 + last-east5           52/58      43/58              63/87
last-east5 + last-east3           50/53      46/53              65/77
```

The jointly SAT control was recovered by both methods.

## Interpretation

These are incomplete heuristic scores and carry no evidence of SAT, UNSAT, or
closeness to either. The three pairs remain UNKNOWN. Per the frozen stop rule,
noise, seeds, and budgets are not tuned.

## Next decomposition

A diagnostic exact solve with coordinate injection disabled returned SAT for
all three pairs in under three seconds, but with respectively:

```text
24/31, 33/54, and 37/54 distinct occupied coordinates
```

This was inspected before the next freeze and is disclosed as retrospective
method selection. It isolates `AllDifferent`, rather than the chord equations,
as the practical bottleneck. The next exact pass therefore solves the chord
algebra first and lazily adds only violated coordinate inequalities.

## Reproduction

```text
PYTHONPATH=src python3 scripts/run_hidden_geometry_pair_repair.py
```
