# Eleventh wide horizon — second mixed batch results

## A. Symbolic ordinary-GAK feasibility

The promoted ciphertext-only orphan test now has two independent exact
encodings:

1. complete unordered permutation enumeration on the four-card calibration
   deck;
2. an SMT-LIB model with unknown plaintext schedules, unknown permutation
   operations, identity reset, no top-fixed operation, and distinct operation
   source positions at the top.

Both decide the calibration pair identically:

```text
BCBDBCDA    SAT
BCBDBCDAC  UNSAT
```

Every SAT answer is accepted only after the recovered operations and plaintext
schedule replay the ciphertext exactly. The same symbolic model decides
constructed nonparents beyond the toy deck:

```text
deck 5, two operations: 13010212020  UNSAT
deck 6, two operations: 13023101020  UNSAT
```

It also reaches a planted SAT instance at deck size 12. This crosses both
predeclared calibration gates. Runtime is not monotone: otherwise similar
planted deck-8 and deck-10 instances hit 30 seconds, while deck 12 solved in
about 6.8 seconds. The implementation is therefore an exact decision
procedure when it returns `sat` or `unsat`, not a reliable complexity scale.

### Shared reset-message encoding

For Eye use, all nine messages must share one set of operations and each begin
from the identity deck. A second SMT encoding unrolls only the observed top:

```text
C[t] = p[q0](p[q1](...p[qt](0)...)))
```

Each operation is represented as a partial injection on the arguments actually
reached by these compositions. Any satisfying partial injection is extended
deterministically to a full 83-card permutation and replayed through the
ordinary GAK implementation. The lazy encoding independently reproduces the
four-card parent and orphan, so it does not gain speed by relaxing the model.

The exact Eye-prefix frontier at a 30-second ceiling is:

```text
shared operations  prefix length  decision
9                  1              SAT
9                  2              SAT
9                  3              SAT
9                  4              UNKNOWN
9                  5              UNKNOWN (20-second pilot)
26                 3              SAT
26                 4              SAT
26                 5              UNKNOWN
26                 8              UNKNOWN
26                 10             UNKNOWN
```

The SAT witnesses replay all nine prefixes exactly. They do not support GAK:
short prefixes have many more operation degrees of freedom than observations.
`UNKNOWN` is a resource limit, not evidence of incompatibility. In particular,
the apparent difference between nine and 26 operations at prefix four is
solver behavior plus model flexibility, not an inferred plaintext alphabet.

**Decision:** freeze this exact frontier. Promote the lane again only after a
new constraint representation decides at least ten glyphs across all nine
reset messages or an external clue fixes operations/plaintext relations.
Do not spend further time tuning Z3 on unconstrained prefixes.

Reproduction:

```text
PYTHONPATH=src python3 -m unittest tests.test_unknown_gak_smt
PYTHONPATH=src python3 scripts/calibrate_unknown_gak_smt.py
PYTHONPATH=src python3 scripts/analyze_eye_unknown_gak_frontier.py
```

## C. Reset-regime identifiability audit

The proposed new classifier is already subsumed by committed exact negatives:

- all 72 directed panel pairs have zero literal suffix/prefix overlap;
- equality-isomorphic overlap is also zero when at least two repeat
  validations are required;
- every one of the `9!` panel orders scores zero;
- fixed-base continuous-state scans are negative;
- row-reset-at-26 scans are negative for both fixed-base/top-swap and
  selected-card action models.

No label-invariant feature remains that distinguishes reset from continuation
without first choosing a cipher mechanism. A new generic classifier would
rename the same zero overlaps.

**Decision:** close lane C. Reopen only with a planted mechanism that proves a
different ciphertext-visible reset invariant.

## D. Renderer counterfactual audit

The retained renderer-position effects do not survive their own promotion
gate:

- the 26-column mutual-information peak is in-sample and fails
  leave-one-prefix-family-out prediction;
- equality column/run-edge controls give corrected tails `0.839580` and
  `0.653673`;
- the recent change-point scan selects glyph 42 at fixed lag five, or glyph 55
  after allowing lags 2–10, rather than 25 or 26.

Absolute glyph index, renderer column, and distance from a row boundary
therefore provide no held-out signal that selects the authored width.

**Decision:** close generic renderer-position inference. A later clue may
still name a particular coordinate, but it must predict a body event not used
to choose that coordinate.
