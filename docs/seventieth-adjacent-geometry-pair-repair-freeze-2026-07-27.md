# Seventieth pass — unresolved-pair witness search freeze

## Scope

Three adjacent hidden-cycle context pairs remain UNKNOWN after bit-vector,
integer, and CNF solving:

```text
first-gap30 + first-cross
last-west4 + last-east5
last-east5 + last-east3
```

This pass is deliberately one-sided. It seeks exact SAT witnesses and cannot
establish UNSAT.

## Frozen search

For each pair in the order above, run:

1. direct constraint min-conflicts;
2. transitive distance-class min-conflicts.

Each search uses:

```text
seed                 20260724
restarts             10
steps per restart    100,000
noise                0.08
```

The search always maintains a complete permutation of the 83 cycle
coordinates. A claimed completion must satisfy every original pair constraint
under `constraint_holds`.

## Control and stop rule

Both repair algorithms must first recover the existing small SAT plant. No
negative control is needed because incomplete search has no negative
interpretation.

- A complete witness promotes that pair from UNKNOWN to SAT.
- An incomplete run reports only its best exact score.
- Do not tune noise, seed, restart count, or the target order after seeing the
  Eye scores.
- If all three remain incomplete, stop generic witness search and derive a
  cycle-space or separator method.
