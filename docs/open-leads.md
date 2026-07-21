# Open lead ledger — 21 July 2026

This is a durable ledger, not a claim that every lead should be pursued at
once.  A paused lead remains here until evidence rejects it or its dependency
is satisfied; it is not silently dropped when another experiment becomes
active.  Each entry records why it remains open, the next bounded test, and
what would stop or promote it.  Completed and rejected branches remain in
[`research-log.md`](research-log.md).

## Active and high value

### Waite suffix for message 3

**Status:** phrase/suffix remains source-backed and compatible; the stronger
three-complete-excerpt hypothesis is rejected under perfect GAK/XGAK.

Arthur Edward Waite's 1893 *A Demonstration of Nature* contains the 81-character
sentence:

```text
SUBLIME THAT WHICH IS THE LOWEST, AND MAKE THAT WHICH IS THE HIGHEST, THE LOWEST.
```

Placed at raw East-2 offset 37, it ends exactly with the 118-symbol message and
puts `THAT WHICH` at offsets 45 and 80.  More strongly, every left-maximal
repeated substring of length at least two passes the necessary perfect-
isomorphism test; the longest is `E THAT WHICH IS THE `, length 20.  The
archived early-access `orb_plan.txt` explicitly names the *Hermetic Museum*
as a source several times, and it is byte-identical to the installed current
file.  The repository identifies the snapshot as early-access data, supporting
pre-1.0 familiarity with the source family.  Its sole Git commit was uploaded
in October 2022, however, so it is archival evidence rather than a
contemporaneously timestamped file.

A complete OCR scan makes the coincidence more specific but also supplies a
negative control.  Across Waite's two volumes, there are five source pairs at
the observed gap 28, four at gap 30, and two at gap 35.  The gap-35 candidate
sentence is the only one of its two that passes the complete East-2 internal
isomorphism check.  After aligning full source windows, 3/5 East-1, 3/4 West-1,
and 1/2 East-2 candidates pass separately.  None of the nine surviving joint
combinations passes cross-message perfect isomorphism; the least-conflicting
combination has 8 conflicts among 186 maximal repeated-substring checks.
Therefore the three complete messages are not contiguous excerpts from this
OCR-normalized source under exact GAK/XGAK.  This does not reject the narrower
ten-character phrase or East-2 suffix proposal, because their unknown
surrounding plaintext need not come from the same source windows.

A finite reset-deck realization is also negative.  The 117-character
contiguous East-2 body candidate was checked against 8,598 distinct standard
83-card bases and 26 variants per base: top swap only, a fixed anchor rule,
and ring/mirror hidden swaps through offset 12.  None of the 223,548 models
admits an injective decoded-symbol/character map.  The best has 564 equality-
relation conflicts, including 517 of the plaintext's 542 required equal-
character pairs.  An unrestricted one-hidden-transposition SMT model remains
`unknown` at both 30 and 117 symbols, so this is a rejection of the finite
standard family only.

Under perfect GAK/XGAK, the six-window extension has an exact boundary.  The
ciphertext equality patterns at raw `40/68`, `40/70`, and `45/80` are
identical across all six occurrences through length 10.  At length 11 they
split: East 1 has
`A.B.CB.AC..`, while West 1 and East 2 have `ABC.DC.AD.B`.  Thus a single
common plaintext can extend through at most ten characters under perfect
GAK/XGAK.  Independently, the longest OCR string repeated at all three source
gaps is the unique 15-character ` THAT WHICH IS `.  This makes the Waite
fingerprint more specific while rejecting its common `IS ` continuation in the
Eyes.  The exact ten-character core remains compatible; East 2's longer suffix
can still be different from the other two messages after that core.

A two-symbol rolling-state generalization is a genuine but limited escape
hatch.  The memory length was selected from Qualia's deliberately artificial
Discord counterexample, not predicted from independent Eye data.  Trimming the
first two outputs of each candidate occurrence nevertheless restores a
single isomorphism class through raw end 17, so the shared plaintext
`THAT WHICH IS THE` is compatible with this higher-order model.  Conditioned
on the already selected ten-symbol isomorph and the no-adjacent-double rule,
`2,634/200,000 = 1.317%` simulated extensions reach seven additional symbols.
Scanning every repeat-rich equality-pattern group at seed lengths 6–14 finds
no independent replication: all positive trim-two gains are nested or shifted
views of the same six passages.  This is enough to retain and formalize the
model, but not enough to promote the phrase to plaintext.

A matched control makes the source-only fingerprint worth retaining.  The same
normalization and gaps were applied to 17 Project Gutenberg alchemy-subject
texts.  None reaches the Waite length 15; their maximum is 12.  Concatenating
the controls with unique boundary separators and cutting nine non-overlapping
blocks of exactly Waite's 1,318,231 normalized characters again gives 0/9 at
length 15, with maximum 12.  This limited calibration is deliberately not
reported as a p-value: the source family, gaps, phrase length, and corpus were
all chosen after inspecting the Eyes.  It establishes only that the Waite
three-gap phrase is unusual in the available matched controls.

**Next test:** fit East 2 locally to a more general but still capacity-
controlled state family and freeze its learned operations before measuring
held-out symbols.  Separately search for an external in-game mechanism that
would select Waite or the three gaps independently.  Source fit and isomorph
compatibility alone are not enough.

**Reject/promote:** reject under perfect GAK/XGAK if any exact repeated
plaintext substring produces non-isomorphic ciphertext.  Promote only after a
mechanism predicts unseen symbols or a second independently constrained source
passage.

### Gate Guardian construction vocabulary

**Status:** plausible later visual clue; proposed decoder under-specified.

The mod-101 diagonal total 70, Q-C successor edges, authored 72-pixel Veska
layer, paired Molari/Mokke silhouettes, and three-egg art are reproducible.
The `12|43|9|8` Veska split, 70-pixel Seula residual, side tape, and fresh Type6
allocator are not reproducible from the published rules.

**Next test:** obtain or independently derive frozen masks without fitting to
70, then predict one of the eight unresolved first-seen Type6 values.  Continue
historical asset retrieval only if it can yield a held-out quantity.

### Arbitrary `A83`/`S83` GAK or XGAK

**Status:** leading cryptographic family, structurally underdetermined.

Cyclic, dihedral, and both affine transitive groups are excluded under the
strong repeated-plaintext premise.  Sparse observed context maps cannot choose
`A83` versus `S83`.  XGAK adds a plaintext-selected output position and may
resynchronize around limited plaintext differences.

**Next test:** use a source-backed crib such as the Waite suffix or an external
in-game key to learn a small, explicitly described operation family and demand
held-out prediction.  The rolling two-plaintext-symbol state update now passes
the selected first-family boundary test but its length came from an artificial
counterexample and it has no independent repeat-rich replication; use it only
in a capacity-controlled construction with a held-out prediction.

Henry reported a more direct known-plaintext attack in the read-only
`silmä-cryptography` discussion on 21 July 2026: encode the unknown initial
deck and plaintext-selected permutations in CNF, then use Kissat to recover
models consistent with a supplied plaintext/ciphertext pair.  Toy examples
were reportedly verified, but the implementation had not yet been linked when
observed; the author also warned that the encoding scales cubically with the
ciphertext alphabet and that short texts admit many equivalent models.

The method is now independently reproduced with a finite-width SMT encoding
that avoids explicit Boolean-matrix multiplication.  A deterministic
three-message, 54-bit toy recovers an exact replay witness through deck size 14
within 30 seconds.  Sizes 16, 18, and 26 return `unknown` at the same bound.
The recovered key need not equal the generator key, confirming that a
satisfiable result is only a feasibility witness.  This is a useful attack
primitive but not yet an Eye-scale solver.

**Next bounded experiment:** obtain Henry's code read-only if its promised
repository link appears and compare its clauses and scaling against the local
bit-vector model.  Separately infer the `2-to-26` plaintext serialization or a
small exact crib before invoking a known-plaintext solver.  Do not interpret
one satisfiable model as a unique recovered key, and do not scale to the Waite
East-2 crib until a 26-card calibration replays exactly.

### External in-game key or later hint

**Status:** high-value search track.

Cessation proves that Noita puzzles may use an independently supplied in-world
state sequence.  Its literal Void-Liquid cycle does not decode the Eyes, but
the construction principle remains live.  A later clue may legitimately decode
the 2020 ciphertext.

**Next test:** inspect confirmed puzzle assets and developer-authored state
sequences for an 83-label correspondence, deck permutation, or missing context
map—not for superficial reuse of their plaintext.

## Retained, lower priority or dependency-bound

### sdlwdr practice cipher 3

**Status:** unsolved.  One exact single-`C83` progression model is UNSAT;
multi-cycle variants timed out.  Resume when a new invariant or author hint can
reduce the model rather than extending blind SMT time.

### sdlwdr practice cipher 4

**Status:** outer cyclic layer solved, inner codec unsolved.  Revisit with a
new homophonic/deck invariant or author hint.  Current language solvers,
Wadsworth, Chaocipher, source scans, and Eye-corpus reuse are negative.

### Qualia `2-to-26 deck cipher` practice puzzle

**Status:** newly identified calibration dependency.  It maps binary plaintext
to a 26-symbol ciphertext with an arbitrary initial state and two arbitrary
plaintext-selected permutations; its small plaintext alphabet makes it a
better first target for validating the CNF/Kissat formulation than the Eyes.

**Next test:** archive the attached JSON read-only, recover at least one model,
verify it by forward simulation, and document the attack separately.  Pause
only while awaiting either the attachment or a computationally tractable
solver encoding; this does not supersede sdlwdr puzzles 3 and 4.

### Large-group known-plaintext GAK practice puzzle

**Status:** retained training problem posted by Torben on 3 July 2026.  Its
stated goal is reconstructing swaps from known plaintext for increasingly hard
deck ciphers up to `S83`.

**Next test:** use it only after the small `2-to-26` solver is independently
verified.  It is the scale bridge between a toy CNF model and any Eye/Waite
feasibility claim.

### Finnish *Corpus Hermeticum* translation

**Status:** chronologically eligible source, inaccessible digitally.  Pursue a
physical copy only after the public Waite lead and available Finnish Hermetic
texts fail source-tree searches; developer-created decoding clues remain
independent of the translation's publication date.

### `LUMIKKI` half-word

**Status:** unexplained historical clue/easter egg, literal key/source attacks
negative.  The remaining useful test is contemporaneous evidence for the
reverse-hash search universe or developer construction process.

### Ongoing Discord delta sweep

**Status:** read-only watchlist, never a substitute for the local log.  Add
only reproducible constraints, source documents, or finite attacks not already
recorded.  The January 2023 Hidden Secret ARG is legacy/hoax material and is not
an active evidence source.

## Scheduled synthesis checkpoint

After the current known-plaintext SAT experiment reaches a bounded result,
stop expanding that branch and rebuild the problem from the evidence ledger.
The first pass must be broad rather than deep: generate mutually different
mechanism families across representation, state evolution, message ordering,
error/check structure, non-text payloads, spatial/game-world selection, and
later-added in-game keys.  Include deliberately strange proposals, but keep
hard observations separate from community assumptions.

Score every family against the same frozen facts and require at least one
observation that would distinguish it from GAK/XGAK and from a fitted crib.
Only after this breadth pass may the strongest few receive implementation or
asset work.  Preserve the discarded candidates and their kill reasons here or
in the research log so the search does not repeatedly collapse onto the same
idea.
