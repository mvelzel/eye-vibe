# Practice cipher 3 — projective pair-quotient freeze

**Date:** 27 July 2026
**Status:** mechanism family frozen before real-corpus scoring

## Motivation

Cipher 3's direct static `83 -> 42` quotient is strongly negative, but the
previously declared polygraphic lane is untested. A small, complete extension
is to combine two adjacent raw values before taking the exact two-sheet
quotient:

```text
u = x + k*y mod 83,  k in F83
u = y                       (the projective point at infinity)
u ~ r-u,             r in F83
```

Normalizing the coefficient of `x` makes the 84 choices the complete
projective line `P1(F83)`. Translation is absorbed by `r`; scaling is absorbed
by projective normalization and the unrestricted final substitution. Thus the
family covers every nonzero affine-linear function of a pair, followed by an
affine involution with 41 doubletons and one singleton.

One global permutation maps the 42 quotient classes to sdlwdr's established
plaintext alphabet. There is no per-message substitution.

## Frozen routes

For a raw message `c[0..n)`, consume consecutive pairs beginning at `start`
and advancing by `stride`:

```text
(stride,start) = (1,0), (1,1), (2,0), (2,1), (2,2)
```

The first two are overlapping full/body routes. The last three are the unique
disjoint routes induced by an optional first-symbol header and either pair
phase. Unpaired prefix/suffix values are ignored. No other route, reversal,
triple, width, or state is admitted.

The complete structural catalog is:

```text
5 routes * 84 projective slopes * 83 reflections = 34,860
```

## Frozen selection protocol

Train two models on Project Gutenberg's *Sherlock Holmes*:

1. a substitution-invariant equality-pattern model over length-six windows;
2. the existing 42-symbol trigram model.

The equality model screens all 34,860 candidates using group A only. Keep an
equal-size shortlist from every route so route length cannot win by unequal
candidate allocation. Optimize a bijective 42-symbol substitution on A for
the structural shortlist, then refine a fixed global shortlist. Freeze the
best A key and score/render B+C once without refitting.

Search budget and shortlist sizes may be tuned only on planted controls. They
must be written here before the first real run.

The first budget passing both route classes is now frozen:

```text
equality-pattern width          6
structural shortlist/route     12
cheap substitution iterations  20,000
global refinement shortlist    8
refinement restarts            4
iterations/restart             120,000
seed                           20260727
```

## Positive controls

Use disjoint passages from Project Gutenberg's *Moby-Dick* with the decoded
lengths induced by the real 18 raw lengths. A passages may be selected only to
cover the 42-symbol alphabet; B/C passages remain disjoint and untouched.

Plant at least:

- one overlapping route;
- one disjoint route;

using a nonzero slope, one reflection, a random 42-symbol substitution, and
random valid representatives/preimages. Search all five routes for each
plant; do not disclose the true route to selection.

Exact inputs:

```text
Sherlock Holmes SHA-256
922e2a12ccb43a4c9544c260b2166c6ad2097aeb5957faeee113f173bb857cd0

Moby-Dick SHA-256
9a6844ac0703853720010787c7b6c70b0020f1ab1862dcd74452fa46474d1215
```

Operational gate:

```text
A event accuracy       >= 80%
B+C event accuracy     >= 60% with the frozen A key
true quotient relation retained by structural screening
```

If either route class fails, the corresponding real route remains unresolved.

Both controls pass at the frozen budget:

```text
plant       true structural rank   selected exactly   A accuracy   B+C accuracy
overlap     route 1, global 2       yes                100.000000%  100.000000%
disjoint    route 11, global 30     yes                 92.972973%   96.544276%
```

Their frozen-key B+C scores are `-7.229609` and `-7.581465` per trigram and
render untouched prose. No real pair-quotient result had been inspected when
this budget and these measurements were added.

## Promotion and stop gates

Promote only if one A-selected architecture produces coherent untouched B+C
plaintext and exact pair-level replay. A good A score, a rediscovered copied
prefix, or equality-pattern fit alone is insufficient.

If both planted route classes pass and real heldout text is sharply separated
from them, close only this complete projective-linear-pair plus affine-quotient
family. Do not generalize to triples, nonlinear pair maps, stateful sheets, or
arbitrary polygraphic codebooks.
