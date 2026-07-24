# Thirteenth wide horizon: hidden geometry from isomorphs

## Why this pass exists

The sdlwdr cipher-3 reflection experiment separated two problems that are easy
to conflate: with the correct 83-point wheel, its 42-class substitution is
easy; recovering an arbitrary wheel from language score is not. The Eye
corpus has evidence that the practice puzzle lacks: seven independently
selected nonliteral equality-isomorphic windows. Those windows may constrain
a hidden geometry without assigning plaintext letters.

This document freezes a breadth pass before fitting such a geometry. “New”
below means that the exact test was not found in the local research archive or
the public material already recorded there. It cannot establish that nobody
has considered the broad idea privately.

## Fixed evidence and boundaries

- Use only the seven nonliteral contexts already frozen in
  `ninth_causal.CONTEXT_SPECS[6:]`: four in the first family and three in the
  last.
- They contain 141 aligned adjacent-step pairs and touch 71 of the 83 labels.
- Treating each whole context map as one rotation/reflection of a hidden
  83-cycle is **not** a new lead. It is a subgroup of the already excluded
  arbitrary-label affine action over `F83`.
- Literal circular distance in the displayed `0..82` order is also old and is
  not evidence for an unknown order.
- The repeated-plaintext interpretation of an equality isomorph remains an
  assumption. A negative result can reject a mechanism conditional on that
  assumption; a positive result must still beat equality-matched controls.

## Wide portfolio

| Lane | Model | First falsifier | Capacity / prior-work boundary |
|---|---|---|---|
| **A. Unsigned adjacent chords** | There is one unknown cyclic ordering `z` of all 83 labels. Corresponding adjacent steps in every aligned isomorph have equal circular magnitudes: `|z(b)-z(a)|_83 = |z(d)-z(c)|_83`. Each step may choose its sign independently. | Exact satisfiability of all 141 equations with injective coordinates. If unsatisfiable, extract the smallest reproducible context/lag boundary. | Strictly weaker than making a whole context one dihedral motion, and therefore not covered by the affine rejection. No language score or wheel optimizer is involved. |
| **B. Lag ladder** | The same chord equality applies only at selected textual separations `h=1,2,...`, or becomes rigid as more lags are added. | Solve each lag alone, then cumulative lags `1..h`; report the first exact contradiction and leave one context family out. | Prevents an arbitrary choice of “adjacent.” A local differential mechanism should prefer lag 1; a rigid geometric context should survive all lags. |
| **C. Chord-collision isomorphism** | Numeric magnitudes may differ between contexts, but equality of hidden chord classes is preserved: two source steps have the same chord iff their two target steps do. | Search for a wheel satisfying only these equality/inequality relations, then measure how many chord classes remain unidentified. | Weaker than lane A and easy to overfit. It can promote only if planted wheels are recoverable and Eye constraints predict withheld collisions. |
| **D. Piecewise orientation** | A context is locally a rotation or reflection, with a small number of sign changes caused by resets or control symbols. | Minimize sign-change breakpoints along each aligned window under one wheel; compare with fixed-domain/image isomorph controls. | The zero-breakpoint case is the old dihedral model. Breakpoints must be charged and located without reading plaintext. |
| **E. Context gain plus local reflection** | Directed hidden steps obey `delta_target = s_i a_j delta_source (mod 83)`, with one nonzero gain `a_j` per context and local signs `s_i`. | Exact solve, then require the same gains to predict held-out steps. | A constant sign is old affine structure. Free local signs make this a magnitude-rescaling model and require a held-out gate. |
| **F. Distance substitution** | Each context applies a permutation to the 42 unsigned distance classes, analogous to a keyed substitution over motions rather than labels. | Fit on part of a window and predict repeated distance-class relations in the remainder. | Forty-two free classes per context are too expressive unless collision reuse supplies predictions; raw fit never counts. |
| **G. Turn grammar** | Plaintext is carried by relations between consecutive hidden steps—same/opposite sign, equal magnitude, or a small ratio class—rather than by individual chords. | Enumerate only label-independent turn relations forced by a candidate wheel and test held-out contexts. | Different from prior raw-direction turn masks: the geometry is conjugated by an unknown label order. |
| **H. Circular betweenness** | Context maps preserve or reverse only cyclic order/betweenness, not metric distance. | Exact simultaneous circular-order solve; count compatible orders and predict held-out triples. | Whole-map order preservation collapses back to dihedral rigidity. The only new case is sparse, sequence-selected triples, which must be identifiable. |
| **I. Consensus wheel** | The first and last isomorph families are independent views of one hidden wheel. | Learn from one family and score exact equations in the other, then reverse train/test roles. | A joint optimum alone is not evidence. This is the mandatory validation wrapper for any relaxed lane. |
| **J. Completion entropy** | Partial constraints may identify most of the 71 observed labels even if 12 labels never occur. | Count or lower-bound non-dihedrally-equivalent solutions after fixing global rotation/reflection; measure forced adjacencies and distances. | A satisfiable but exponentially non-identifiable wheel does not earn a ciphertext run. |
| **K. Planted recoverability** | The proposed solver can actually reconstruct a hidden 83-cycle from the same seven window shapes and equality skeleton. | Generate planted cyclic-difference fixtures on the exact context incidence pattern and demand wheel/distance recovery, not merely objective improvement. | This directly repairs the failed arbitrary-wheel optimizer from practice cipher 3. |
| **L. Authored selector join** | A recovered, independently validated wheel may correspond to a Noita-authored 83-entry order or later construction clue. | Only after lanes I–K pass, compare one frozen wheel against named assets such as `gun_names`; require a held-out mapping or decoder consequence. | Cardinality alone is disallowed. Gate or other later assets may validate a machine vocabulary but may not select a fitted wheel retrospectively. |

## Ranking before implementation

1. **A + B** have the best information-to-capacity ratio: exact equations,
   no plaintext, no learned score, and a clean distinction from the old
   affine/dihedral rejection.
2. **K + J** are mandatory before interpreting any satisfiable wheel. They
   answer whether the problem is recoverable rather than merely interpolable.
3. **I** is the strongest protection against joint overfit once a relaxed
   score is introduced.
4. **C/D/E** are useful only if A fails in an informative way. They relax
   different assumptions and must not be searched simultaneously.
5. **F/G/H** remain breadth options but currently have weaker identifiability.
6. **L** is deliberately last; an in-game join cannot rescue a wheel selected
   from the same asset it is supposed to explain.

## First frozen experiment

Implement lanes A and B as exact finite-field constraints.

For every aligned chord pair `(a,b) ~ (c,d)`, require

```text
z[b] - z[a] = +(z[d] - z[c])  (mod 83)
```

or

```text
z[b] - z[a] = -(z[d] - z[c])  (mod 83).
```

All coordinates that occur in the equations must be distinct. Fix one
coordinate to zero to remove rotation; reflection remains an expected
two-fold symmetry. Test:

1. each context separately at every lag supported by it;
2. the four first-family and three last-family contexts separately;
3. all seven together at lag 1;
4. the cumulative lag ladder `1..h`;
5. planted fixtures on the exact context shapes.

If the exact solve is satisfiable, do **not** decrypt. First quantify solution
multiplicity, forced distances, and leave-family-out prediction. If it is
unsatisfiable, shrink the contradiction by contexts and aligned positions so
that the rejection is independently checkable.

## Post-freeze implementation correction

The equations are invariant not only under translation and reflection but
under multiplication of every coordinate by any nonzero element of `F83`.
The solver therefore fixes the endpoints of one constrained edge to `0` and
`1`, removing translation and all 82 nonzero scalings. This is a
symmetry-breaking correction only; it neither adds nor removes solutions.
