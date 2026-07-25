# Thirty-fifth pass — phase-overlap update results

## Outcome

Promote one constrained correspondence across the final-row map switch:

```text
old equality class 7 -> new equality class 24
```

Both East panels contain this edge, using different visible labels, and West
does not. It is the only exact class edge shared by any panel pair.

This is evidence for one preserved state or cache entry across the reset. It
does not recover the rest of the update map, the allocation rule for new
labels, or plaintext.

## Independently selected edge

Three already promoted fields selected the edge before the matched control
audit:

```text
row-2 circulation budget     7
common old phase length     17
East newline preimage        4
```

They give:

```text
old class                    7
new class                 7+17 = 24
new first position        24+4 = 28
```

New class 24 is in fact introduced at position 28 in each East panel. It is
the last new class in the common 30-position phase.

## Observed overlap maps

Each old bridge and new 30-symbol phase was canonicalized independently by
first occurrence. An edge is present when the same actual visible label
occurs in both phases:

```text
E4: 0->7, 7->24, 8->0, 14->23, 15->20
W4: 1->9, 10->12, 12->10, 14->20
E5: 7->24, 10->21
```

The shared edge uses different labels:

```text
E4: label 69 realizes 7->24
E5: label 31 realizes 7->24
```

Therefore the result is about equality-class roles, not a coincidental common
numeric label.

## Exact conditional probability

The matched null preserves, separately for every panel:

- complete old and new equality signatures;
- every class multiplicity;
- the observed number of reused labels;
- the complete multiset of
  `(old multiplicity, new multiplicity)` reuse types.

For a requested edge of a fixed type, its exact marginal probability is:

```text
compatible reuse tokens
------------------------------------------
compatible old classes × compatible new classes
```

The target `7->24` has type `(1,1)`. Thus:

```text
P(E4 target) = 3/(13×20) = 3/260
P(E5 target) = 2/(13×20) = 1/130

P(both East targets) = 3/33,800
                     = 0.000088757
                     ≈ 1 in 11,267

P(both East, absent West)
  = (3/33,800) × (1-3/260)
  = 771/8,788,000
  = 0.000087733
```

These probabilities are conditional specificity measures. The target was
recognized before the freeze but was assembled from previously promoted
fields; it is not a fully prospective discovery p-value.

## Randomized controls

Fifty thousand independently randomized compatible overlap maps gave:

```text
event                         hits       plus-one rate
both East contain 7->24       1/50,000   0.000039999
East only contains 7->24      1/50,000   0.000039999
some pair shares c->c+17     67/50,000   0.001359973
some pair shares any edge  5051/50,000   0.101037979
```

The exact calculation supersedes Monte Carlo noise for the narrow event. The
broad control is important: finding some shared edge after inspection is not
rare. What is constrained is the independently selected `+17` edge and,
more narrowly, the exact `7->24` correspondence in both East panels.

The events are nested and their probabilities must not be multiplied.

## Interpretation

The least-capacity account is:

1. the old phase has a distinguished role at class 7;
2. the 17-step common trace advances that role to class 24;
3. both East panels carry the corresponding visible value across the map
   switch;
4. the East newline field schedules its reintroduction at position 28.

This resembles one cache/state preservation operation more than a wholesale
substitution. It makes the Gate dossier's cache vocabulary somewhat more
relevant, but does not validate its eight cached roles or first-seen
allocator. No Gate quantity was needed to select this edge.

## Next falsification target

Freeze a rule using `7->24` as the sole known preserved state and predict one
additional, currently withheld fact:

- another old-to-new edge;
- which panel reuses a value;
- the first-seen allocation order; or
- the phase exit.

A rule that merely completes the remaining partial bijections after seeing
them is not evidence.

## Reproduction

```bash
PYTHONPATH=src python scripts/audit_phase_overlap.py \
  --controls 50000 --seed 0xCACE17
```

Implementation:

- `src/eye_mystery/phase_overlap.py`
- `tests/test_phase_overlap.py`
- frozen protocol:
  `docs/thirty-fifth-phase-overlap-update-freeze-2026-07-26.md`
