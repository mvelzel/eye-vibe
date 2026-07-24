# Seventeenth horizon lane E — graph fibration results

## Result

The exact directed equitable/fibration quotient is negative at its first
prerequisite. The complete Eye transition graph has 83 singleton fibers under
both support and multiplicity refinement.

This closes only an exact quotient of the observed directed graph. It does not
exclude a hidden-state cipher whose unobserved transitions would complete a
cover.

## Method and control

Starting from one color for all 83 labels, repeatedly split vertices by:

```text
current color
outgoing count to every current block
incoming count from every current block
```

Using Boolean counts gives the directed support graph; integer counts give the
observed transition multigraph. The stable partition is the unique coarsest
equitable partition. If it is discrete, no nontrivial exact equitable
partition of that observed graph exists.

A five-vertex directed base graph was lifted to three cover sheets with
nontrivial edge permutations. The implementation recovers exactly five fibers
of size three and verifies every in/out block count. The positive control
passes before Eye scoring.

## Eye results

P is the three factoradic-header panels `east1,west1,east2`; all nine panels
are the transfer set. Results are:

```text
graph         copied opening   P blocks  P singleton  largest P  all blocks
support       retained         77        76           7          83
multiplicity  retained         77        76           7          83
support       trimmed          75        74           9          83
multiplicity  trimmed          75        74           9          83
```

In every P partition, the sole nonsingleton block is the set of labels not
distinguished by the sparse training graph. Q immediately splits it. None of
the four P partitions remains equitable after all panels are added.

The training result already exceeds the 42-fiber gate, and the complete result
is maximally discrete. Degree-preserving random controls are therefore not
opened: there is no low-fiber survivor whose rarity needs calibration.

## Decision

Close:

- exact directed-support graph covering of the observed body transitions into
  at most 42 fibers;
- exact directed-multiplicity covering;
- the same two models after removing all known natural copied openings.

Retain:

- incomplete sampling of an underlying cover with additional unobserved
  transitions;
- state-dependent action labels, graph bundles with hidden edge colors, and
  non-equitable quotient notions;
- Lane F's context-specific bisimulation, which is weaker than a global
  equitable partition.

No graph quotient is passed to a language optimizer.
