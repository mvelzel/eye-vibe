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

## B. Composite-action collision calibration

This lane fails by exact non-identifiability before a statistical extractor is
admissible. A six-card, three-symbol XGAK fixture uses distinct output
positions:

```text
A -> 1
B -> 2
C -> 3
```

and the two reset plaintext paths:

```text
C A B C A
C B C B A
```

Under key 1, all three deck operations are identity. Under key 2, `A` alone
swaps hidden positions 4 and 5; `B` and `C` remain identity. Both keys emit
exactly:

```text
3 1 2 3 1
3 2 3 2 1
```

The paths have a shared prefix, diverge, contain no adjacent doubles, and
rejoin on the final visible card. Yet:

- `operation[A] == operation[B]` under key 1 and not under key 2;
- the two final hidden decks are equal under key 1 and unequal under key 2.

The hidden transposition is a legal one-swap XGAK action and every plaintext
symbol has a distinct output from the reset deck. Thus the complete proposed
ciphertext observation is identical while both the withheld operation-pair
relation and composed-state collision change. More swaps or matched controls
cannot repair a missing invariant.

**Decision:** close mechanism-independent inference from visible rejoin events.
A future deck-chaining attack must introduce additional observations—known
plaintext, fixed output positions, an independently bounded operation family,
or enough chosen paths to cover the hidden action domain.

## E. Executable later-clue interface

A static scanner was frozen around executable cardinality producers rather
than free numeric literals:

1. literal modulo by 9, 42, 83, or 101;
2. inclusive `Random(a,b)` domains of those exact sizes;
3. comparisons that partition a literal random domain into one of those exact
   sizes;
4. literal numeric `for` loops of those exact lengths;
5. direct or twenty-line assignment flow from a produced value into a Lua
   table index.

Across all 1,077 Lua files in the installed 14,745-entry WAK:

```text
cardinality  modulo  random domain  random partition  numeric loop
9            0       10             4                 1
42           0        0             0                 0
83           0        0             2                 0
101          0      114             0                 0

target-derived lookup flows: 0
```

The two 83 partitions are the already known copies of
`Random(0,100) < 83`. They choose modifier versus draw-many wand actions; they
do not retain the selected integer, walk an 83-state structure, or index the
83-name table. The four nine-sized partitions are three complements of
one-in-ten events and a Valentine's potion chance. The only nine-step loop
spawns nine clusterbomb fragments. The ten nine-way random domains are local
coordinate jitter, one biome coordinate, and a mimic event. None supplies an
Eye consumer.

The broader exact-size inventory remains unchanged: one copied 83-name list,
one ordinary 42-child creature XML, and no 42/101 Lua table. Native x86
immediates are too nonspecific for a literal-only claim: disassembly contains
77 uses of `0x53`, 125 of `0x65`, and 201 of `0x2a`, intermixed with character
bytes, dimensions, and ordinary constants. A native claim therefore needs a
named handler or semantic decompilation target; raw immediate mining is
forbidden.

**Decision:** close the bounded Lua/data arithmetic-interface lane. Preserve
the known 83-of-101 wand branch as genuine later construction vocabulary, but
it still predicts no unseen Eye quantity. Reopen native code only when another
clue selects a function or call path.

## F. Practice transfer backstop

No method produced in lanes A–E satisfies the practice-transfer gate:

- the unknown-GAK solver assumes identity-reset arbitrary permutations, while
  practice cipher 3 has a supplied cyclic/progression construction and cipher
  4 already has a solved cyclic outer layer;
- the XGAK result is a non-identifiability counterexample, not an inference
  method;
- the arithmetic-signature scanner is specific to authored Noita assets.

Applying any of these to practice 3 or 4 would therefore be an unconstrained
model change rather than a held-out transfer test.

**Decision:** close only this batch's transfer lane. Practice ciphers 3 and 4
remain unsolved and active on their own ledger entries. Resume them with a new
invariant native to their disclosed constructions, not because the Eye batch
needs another data set.

## Second-batch decision

No body decoder or plaintext results. All six lanes now have bounded outcomes:

- symbolic ordinary GAK crosses planted calibration but stalls at 3–4 Eye
  glyphs;
- visible XGAK reconvergence cannot identify hidden action equality;
- reset and renderer classifiers are subsumed by stronger negatives;
- installed Lua/data contains no executable target-cardinality lookup;
- no new method transfers honestly to the unsolved practice puzzles.

The next phase may therefore step back. It must begin with a broad map of
mechanisms that are not merely variants of these six lanes, freeze cheap
falsifiers for all of them, and deepen only after the mixed first batch is
complete.
