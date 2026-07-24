# Sixteenth wide horizon — first batch results

## Outcome

All four frozen A/C/D/E mechanisms close after passing their positive
controls:

- the exact `PG(2,5)` decomposition is real, but none of the seven repeated
  contexts descends to a projective bijection and the 31-ray tape is ordinary
  under global-label controls;
- no header-derived three-type bracket convention makes even one Eye panel a
  valid Dyck prefix;
- the raw directions violate a five-successor rotor schedule in the first
  five relevant East-1 occurrences;
- none of 720 low-degree `P1(F25)` row-code candidates fits a single P record.

This result rejects four declared consumers. It does not make the projective
inventory false, reject the factoradic headers, or resolve the Eye plaintext.

Reproduce with:

```bash
PYTHONPATH=src python scripts/run_sixteenth_novel_batch.py \
  --controls 2000 --plant-controls 200
PYTHONPATH=src python -m unittest tests.test_sixteenth_novel -v
```

The complete Z3-enabled suite passes 504 tests.

## A. `PG(2,5)` ray homophony

### Exact alphabet decomposition

Canonical normalization of every nonzero vector makes its first nonzero
coordinate one. The observed alphabet inventory is:

```text
projective points: 31 / 31
visible nonzero representatives: 82
representatives per point: 2..4

17*2 + 8*3 + 6*4 = 82
17*(4-2) + 8*(4-3) + 6*(4-4) = 42 missing
```

This is a mathematically exact factorization of the `1..124` nonzero cube into
31 rays of four scalar representatives. It is worth preserving independently
of the failed cipher tests below.

### Positive controls

An invertible `F5` matrix maps all 31 planted projective points. The detector
recovers a functional injective relation and preserves every one of
`4,495/4,495` collinearity comparisons.

A separate planted 27-symbol language tape chooses visible scalar
representatives of fixed projective points. Its canonical ray projection
beats 200 complete global-label controls on both P and Q:

```text
P corrected tail: 1/201 = .004975124
Q corrected tail: 1/201 = .004975124
```

Thus both the exact geometry gate and the label-merging language statistic can
detect their intended object.

### Projected context result

Projectivizing the seven nonliteral repeated contexts immediately destroys
functionality or injectivity:

```text
context           functional  injective  first failure
first-gap30       no          no         reverse conflict at 7
first-cross       no          yes        forward conflict at 12
first-cross-late  no          no         reverse conflict at 5
first-gap28       yes         no         reverse conflict at 6
last-west4        no          no         forward conflict at 8
last-east5        no          no         forward conflict at 8
last-east3        no          no         forward conflict at 8
```

For example, in `first-cross` the same source ray 5 must map first to ray 21
and later to ray 15. In `first-gap28`, two different source rays must map to
target ray 4. A projective collineation is a bijection, so no `PGL(3,5)` fit is
opened. These conflicts are stronger than a poor best fit.

### Canonical 31-ray language result

After removing only the known copied openings, the fixed projective-point
tape scores:

```text
P score: -18.465837375   corrected upper tail 132/2001 = .065967016
Q score: -18.375232530   corrected upper tail 298/2001 = .148925537
```

Neither split reaches `.01`, let alone both. The scalar tape is not promoted
to a second channel because its prerequisite ray payload failed.

**Boundary:** repeated-context maps are not projective collineations of the
canonical rays, and direct ray merging is not an exceptional homophonic
language channel. The exact 31-ray/42-complement inventory remains an
interesting authored-coordinate fact. Outer-`S6` is a separate six-symbol
header hypothesis and was not tested by this result.

## D. Header-induced Dyck syntax

### Positive control

The plant uses each unranked header to order three opening and three closing
types. The detector uniquely selects `header-aligned` and accepts:

```text
P:  977/977 symbols
Q: 2190/2190 symbols
```

All nine planted tapes are valid typed Dyck prefixes.

### Eye result

Every candidate fails in P:

```text
candidate          P valid prefix   Q valid prefix
header-aligned          5/977           26/2190
header-reversed         5/977           31/2190
inverse-aligned         5/977           12/2190
inverse-reversed        5/977           10/2190
```

Training selects `header-aligned`. East 1 fails at tape index 5: stack type 2
is open but closing type 1 arrives. The fixed convention's first heldout
failure is West 2 index 4, expecting type 1 and observing type 2. No panel is
a valid prefix:

```text
P: 0/3
Q: 0/6
```

**Boundary:** the factoradic header does not assign the six renderer symbols
the frozen three-type visibly pushdown syntax. Cyclic cuts, private bracket
roles, and post-hoc row resets are forbidden repairs.

## E. Five-state rotor router

### Positive control

Five distinct local successor cycles generate nine independently reset raw
direction streams. The detector recovers all five cycles modulo rotation and
predicts every heldout stream exactly.

### Eye result

The model fails before a schedule can be learned. In East 1, the first five
successors observed when the current raw direction is zero are:

```text
1, 1, 2, 0, 1
```

A five-state rotor's first complete turn must be a permutation of
`0,1,2,3,4`. The repeated 1 and absent 3/4 are an exact contradiction; Q is
not opened.

**Boundary:** the markerless raw-eye stream is not generated by one global
five-successor cycle per current direction with panel-reset phase. Shorter,
repeating-subset rotors or 83-label local schedules are different,
higher-capacity hypotheses and are not licensed by this failure.

## C. `P1(F25)` extended row code

### Positive control

The finite catalog contains:

```text
10 irreducible quadratic field representations
 6 ordered output-eye pairs
 2 record directions
 6 exact degrees (0..5)
--------------------------------
720 candidates
```

The plant uniquely recovers

```text
x^2 + 2
output eyes 0,2
forward record order
degree 3
```

and closes all complete records:

```text
P: 10/10
Q: 24/24
exact P candidates: 1
```

The infinity coordinate is checked as the leading coefficient, so the plant
is an extended projective-line codeword rather than a generic interpolation.

### Eye result

All 720 candidates fit zero P records. The deterministic tie is the first
catalog entry,

```text
x^2 + 2, eyes 0,1, forward, degree 0
P: 0/10
Q: 0/24
exact P candidates: 0
```

There is therefore no field, eye pair, direction, or low degree to carry into
heldout testing.

**Boundary:** complete 26-glyph records are not degree-`0..5` extended
Reed–Solomon words on `P1(F25)` under the frozen natural construction. This
does not revisit or alter the older cross-panel polynomial-share result.

## Decision

No first-batch mechanism earns depth. In particular:

- do not assign letters to the 31 projective points after the calibrated
  projection failed;
- do not use the projective count identities as evidence for outer-`S6`;
- do not rotate or privately re-pair Dyck tapes;
- do not shrink or individualize rotors after the five-cycle contradiction;
- do not raise the `F25` degree toward tautological interpolation.

The next breadth choice should compare the queued exceptional outer-`S6`
consumer with unrelated reset/Hankel/Lyndon or archaeology lanes before
implementing any one. The original trie checksum, arbitrary lag-one wheel,
factoradic metadata, Gate construction vocabulary, practice ciphers 3/4,
source ancestry, and chronology remain active.
