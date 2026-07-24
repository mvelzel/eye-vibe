# Twelfth wide horizon — first mixed batch results

## Outcome

All five predeclared screens close. None predicts held-out Eye structure or
crosses the repository's `0.01` promotion threshold. This is useful breadth:
five mechanism classes were tested without plaintext scoring and without
adding flexibility after inspection.

Reproduce with:

```sh
PYTHONPATH=src python3 scripts/run_twelfth_novelty_batch.py --controls 200
```

The run uses seed `0xE1E12`. Primitive and frozen-corpus tests are in
`tests/test_twelfth_novelty.py`.

## A. Projective context maps

Any three distinct source/target pairs determine a unique fractional-linear
map. The test fits every three-edge subset over `F83` and `F101`, then counts
the largest exact support.

The apparent near-exact fits in the first six contexts are not evidence. Those
segments are the already-known copied prefixes plus a different first marker.
The identity map therefore explains all but the marker:

```text
F83 all supports:
20,20,5,5,18,18,4,4,4,3,6,5,5
```

The frozen test discards those six contaminated contexts. Across the seven
nonliteral contexts:

```text
field  maximum supports  exact  extra support over three  corrected tail
F83    4,4,4,3,6,5,5     0/7    10                        .781095
F101   4,4,4,3,5,6,4     0/7     9                        .925373
```

The controls independently shuffle each context's image set over its fixed
domain, preserving edge count, injectivity, domain, and codomain. The observed
extra support is central in both null distributions. No context is an exact
Möbius map, and the rare natural `P¹(F83)` 84-point completion earns no depth.

## B. Header-conditioned Coxeter words

For each panel, remove newline from its unranked `S6` header. The resulting
five-symbol order ranks the five raw eye directions. Map those ranks
bijectively to the five adjacent transpositions `s1..s5` and compose the three
generators in each raw trigram.

The independently natural rank assignment gives context-equality counts:

```text
1,3,0,0,5,8,0,0,1,0,0,3,3
```

Its body quotient uses:

```text
east1 west1 east2 west2 east3 west3 east4 west4 east5
26    23    25    25    27    28    25    25    26
```

states. Exhausting all 120 rank-to-generator bijections gives:

```text
best total:                  27 / 252
random-header upper tail:    .746269
training-selected:           20 / 104
held-out:                     4 / 148
held-out upper tail:          .830846
```

The control reassigns the nine intact factoradic headers to the nine intact
bodies and repeats the complete 120-model scan. The observed association is
worse than typical, so the exact new Coxeter construction closes. This does
not undo the independent factoradic-header result.

## C. Natural nine-state directed-edge code

Interpret values `0..80` as the row-major ordered edges of a nine-state graph
and `81,82` as sentinels. Eight row/column, transpose, and coordinate-reversal
orientations were tested. Their complete body join counts, among 977 eligible
adjacencies, are:

```text
125,102,102,125,95,114,114,95
```

The first four panels select ordinary row-major orientation with `50/388`
joins. It predicts `75/589` joins in the other five panels:

```text
held-out corrected tail: .149254
scanned-total tail:       .328358
```

Controls globally relabel the 81 nonsentinel values into the same 9×9 edge
grid, keep both sentinels fixed, and repeat orientation selection. The modest
excess is ordinary and supplies no sentinel role or path decoder.

## D. Cross-panel polynomial shares

Use the nine distinct first markers as evaluation coordinates. To remove the
known copied-prefix opportunity, only aligned body columns 25 through 97 are
tested. The unique degree-at-most-eight polynomial through all nine panels has
the following degree histograms:

```text
F83:  degree 7: 2, degree 8: 71
F101: degree 7: 1, degree 8: 72
```

No column has degree six or less. Independently permuting the nine values
within every column gives corrected upper tails `.213930` and `.497512` for
the degree-seven counts. Thus the apparent shares are exactly the chance
one-linear-check events expected from finite-field interpolation, not a common
low-degree polynomial or Reed–Solomon/Shamir mechanism.

## E. Spatial Hodge defects

The accepted renderer interleave was inverted to exact staggered visual rows.
Directions become vectors on the triangular lattice, and each interior vertex
receives a frozen six-neighbour integer divergence/curl stencil. Exact
seven-eye stencil copies between panels are excluded before measuring aligned
feature agreement.

Within-row shuffles preserve every authored row's five direction counts. The
results are:

```text
statistic                         observed              corrected tail
distinct divergence/curl pairs   94                    .781095 lower
zero pairs                       112/2274 = .049252    .771144 upper
nontrivial aligned agreement     228/8302 = .027463    .248756 upper
```

The broad vector-field ingredient is old community prior art; this exact
discrete test is new to the local workbench but negative. No source, sink,
vortex, or aligned defect is selected for a deeper geometric model.

## Decision

No first-batch lane advances. In particular:

- do not add hidden projective points or per-context label isomorphs;
- do not change Coxeter multiplication order or fit a header per context;
- do not search arbitrary 9-state labelings after the natural labeling fails;
- do not increase polynomial degree, which only approaches tautological
  interpolation;
- do not choose a Hodge stencil after seeing the field.

Per the frozen horizon, the next lateral batch should come from:

1. visible-symbol-as-edge line-digraph factorization;
2. the two rejected overlapping trigram phases;
3. a nine-panel `AG(2,3)` design;
4. bounded physical card-shuffle fingerprints;
5. a low-complexity header-controlled transducer.

These remain different mechanism classes rather than repairs to A–E.
