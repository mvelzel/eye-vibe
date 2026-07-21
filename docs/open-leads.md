# Open lead ledger — 21 July 2026

This is a durable ledger, not a claim that every lead should be pursued at
once.  A paused lead remains here until evidence rejects it or its dependency
is satisfied; it is not silently dropped when another experiment becomes
active.  Each entry records why it remains open, the next bounded test, and
what would stop or promote it.  Completed and rejected branches remain in
[`research-log.md`](research-log.md).

## Active and high value

### Procedural wand selects exactly `0..82` from `0..100`

**Status:** exact independently authored 83-of-101 selector; the proposed
18-structural execution match is demoted by scope and runtime accounting.

The installed Lua contains `Random(0,100) < 83` in the standard procedural-wand
generator and its `wand_petri` sibling. Because Noita's integer bounds are
inclusive, the branch's successful outcomes are exactly the Eye alphabet
`0..82`, while the whole random domain has size 101. The branch chooses a
modifier card rather than a draw-many card, putting the identity inside Noita's
wand/deck vocabulary rather than an unrelated asset.

The 18 complementary outcomes `83..100` all select
`ACTION_TYPE_DRAW_MANY`. The compressed Eye trie has five branch nodes with
degrees `(2,3,3,2,3)` and thirteen edges. But `5+13=18` counts internal nodes
and edges as separate records; Noita actually executes five internal cards and
nine leaf cards, fourteen card nodes total. The exact roll is also discarded
after selecting a type, so no missing value is assigned to a branch.

The checksum scopes independently fail to line up. The attractive `70+31=101`
closure uses the lower-six descendant payload, while the 18 hypothetical
node-plus-edge records belong to the entire nine-leaf tree. That lower-six
subtree owns only 11 such records; the all-nine scope owns 18 but has visible
descendant residue 30, which does not close with 31.

An inventory finds 74 direct `Random(0,100)` comparisons and 22 distinct
operator/threshold pairs in the current WAK; `<83` appears only in these two
duplicated sources. The loose repository labelled early access contains the
same two copies, but was uploaded in October 2022. The earliest independently
timestamped public-data copy found is 9 February 2021—after the Eyes, but fully
eligible as a later clue.

**Next test:** look only for a game-authored format that explicitly serializes
node and edge records separately, or another independent 83/18 operation near
the Eyes. Do not infer that `ACTION_TYPE_MODIFIER` literally means visible Eye
values, and do not count the duplicated Lua copies as two independent clues.
Without such a rule, retain the number match but stop extending the wand-tree
decoder.

The detailed ground-up audit and machine hypothesis are in
[`procedural-wand-architecture.md`](procedural-wand-architecture.md).

### Prefix-trie sieve closes modulo 101

**Status:** strongest breadth-first positive; exact pre-registered statistic,
with shared-data rather than pristine null calibration.

Strip the nine independently identified markers, merge all copied body
prefixes, and count every distinct labeled trie edge once.  The resulting 918
values sum to `37,774 = 374 * 101`.  Traversal and sibling order cannot alter
the multiset.  Suffix-trie, raw-direction, nearby-offset, row-family, and
leave-one-panel-out controls fail.  The equation is formally independent of
the nine individual message-sum equations: adding its label-count vector
raises their rank over `F101` from 9 to 10.

Global relabeling calibrations put an unconditioned exact zero near one percent
(71/6,806 affine `F83` permutations; 1,895/200,000 seeded arbitrary label
permutations).  These controls preserve the complete equality trie but not the
three existing diagonal zero sums, so they are diagnostics rather than a
discovery p-value.  A second common start offset, 41, also closes; it was not
selected independently, whereas offset 1 is exactly the established
marker/body boundary.

A stronger exact subgroup control does preserve the three diagonal sums.
Labels with identical East 1/East 3/East 5 count triples may be permuted freely
without changing any of those complete sums or the equality trie.  Exactly
`1,307,844,501,760 / 132,090,377,011,200 = 0.990113%` of that subgroup closes;
freezing all nine marker labels gives
`8,174,134,656 / 825,564,856,320 = 0.990126%`.  The earlier checks therefore do
not make the trie equation routine within this large matched subgroup.

**Next test:** derive a small recursive checksum law from the fixed trie and
demand a held-out branch or header prediction.  Independently inspect later
developer assets for a literal merge/deduplicate-once sieve coupled to 101.
Reject semantic readings that merely rename `37,774`; promote only another
quantity predicted without choosing a new traversal or fitted weight.

The five internal branch descendant residues are `30,19,70,89,13`; the lower
six after their length-five shared prefix uniquely give 70.  That echoes the
Eye checksum grid's known main-diagonal mirror total, but it is not independent
Gate corroboration because both are derived from the Eye corpus.  The proposed
70-pixel Seula residual still cannot be reproduced from raw sprite masks.

Veska's objective `9|8=17` pictograms also meet two exact trie factors:
`918=54*17` and `37,774=22*17*101`.  Joint divisibility by `17*101` occurs in
`0.094754%` of the diagonal-check-preserving subgroup (`0.100646%` with marker
labels fixed), but this is exploratory and does not calibrate the fixed edge
count.  The natural 17-record interpretation is negative: eight selected
DFS/BFS traversals, each split into consecutive and cyclic 54-edge records,
produce no 2,222-sum record and no consecutive mod-101 closure.  Retain 17 as
a weak possible grouping selector, not a decoded Gate instruction.

There is a stronger internal architecture.  `Z101` has 18 labels absent from
the visible `0..82` alphabet.  The compressed body trie has five branch nodes
and thirteen exits, also 18; `BEXIT` may literally distinguish those record
types.  The missing values `83..100` sum to 31 modulo 101, while the lower-six
descendant trie uniquely sums to 70, giving a second closure `70+31=101`.

The exact joint event (full trie zero and lower branch 70) occurs in
`80,918,060 / 825,564,856,320 = 0.0098015%` of the diagonal-check-preserving,
marker-fixed subgroup.  Accounting by a union bound for inspecting the four
eligible proper branches gives at most `0.03922%`.  This is post-hoc
architecture evidence, not a discovery p-value. The procedural-wand audit now
adds a stronger structural objection: the lower-six branch producing 70 owns
only 11 hypothetical node-plus-edge records, while all 18 belong to the full
tree. Actual recursive execution has 14 card nodes rather than 18 records.
Thus a canonical assignment is not merely missing; the present scopes and
record semantics are inconsistent.

**Promotion test for the 18-state architecture:** find an independently
authored game selector or a key-free body identity that orders/types all 18
records.  Do not search 18! assignments or score plaintext; that would make the
hypothesis unfalsifiable.

### S3 header sieve and body `!Fi` echo

**Status:** structural construction clue; exact cross-layer identity selected
retrospectively, while its most natural predictive body action is rejected.

The first six marker control edges enumerate all six permutations of the three
eye components: the first natural row is `A3` and the second is its odd coset.
At their canonical East 2/West 2 boundary, a frozen root/frame/exit operation
reproduces the complete marker-BWT output from body data:

```text
reverse universal root under East 2 order: 010,231 -> 001,123
first West 2 symbol after the five-value row prefix: 234 -> 243
combined: 001123243 = 1,38,73 = !Fi
```

The exact output occurs once among the nine even-header/odd-exit pairs.  The
rule was discovered after `!Fi`, however, and includes inspected choices, so it
is evidence of possible construction redundancy rather than plaintext.

A held-out Coxeter test now rejects the simplest decoder interpretation.  If
the final-row `W4=(12)` and `E5=(01)` headers name the observed East 4→West 4
and East 4→East 5 body-context permutations, both maps must square to the
identity and obey `ABA=BAB`.  Instead every observed square edge is nonidentity
(`7/7` and `8/8`), and the braid words force `31->41` versus `31->69`.
No completion of the partial permutations can repair this.  The header `S3`
may still organize a global sieve or conformance suite, but it does not act
literally as those body transforms.

**Next test:** retain the frozen root/frame/exit identity only while a broad
pass tests other mechanism families.  Promote it only if a later developer
asset independently selects the even/odd boundary operation or it predicts a
second quantity without new choices.  Do not fit another per-panel `S3`
transform after the direct action failed.

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
were reportedly verified; the author also warned that the encoding scales
cubically with the ciphertext alphabet and that short texts admit many
equivalent models.  The subsequently published
[implementation](https://github.com/CyclohexAnon/noita_deck_cipher_sat)
(commit `7acc7eedf025aa65b40e60d93d437d1dad492b58`) has now been inspected and
reproduced locally with Kissat 4.0.4.

The method is now independently reproduced with a finite-width SMT encoding
that avoids explicit Boolean-matrix multiplication.  A deterministic
three-message, 54-bit toy recovers an exact replay witness through deck size 14
within 30 seconds.  Sizes 16, 18, and 26 return `unknown` at the same bound.
The recovered key need not equal the generator key, confirming that a
satisfiable result is only a feasibility witness.  This is a useful attack
primitive but not yet an Eye-scale solver.

The committed CNF uses an identity reset deck and forward-only Boolean-matrix
product implications.  Those implications are sufficient because all three
matrices are independently constrained as permutations.  The chat-described
ban on operation entry `(0,0)` is not present in the committed script, but it
is unnecessary for its published ciphertext.  Our bit-vector solver also
recovers and exactly replays this public toy pair.

**Pause reason and next test:** the known-plaintext primitive is now verified,
but both implementations remain unsuitable for unknown plaintext at size 26
or 83.  Resume after inferring the `2-to-26` plaintext serialization, obtaining
a small exact crib, or finding a backend/encoding that passes a 26-card replay
calibration.  Do not interpret one satisfiable model as a unique recovered key
and do not scale to the Waite East-2 crib before that threshold.

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

**Status:** outer cyclic layer solved, inner codec unsolved.  The arbitrary
cyclic-GAK recurrence is now explicit: candidate plaintext repeats must define
one consistent update function.  Seven English/Finnish corpora give no
200-transition hit under eight orientation/timing variants, and exhaustive
affine updates give no natural 27- or 42-position language schedule.  The only
57-state affine survivors erase the previous state and restate the direct
difference ranks.

**Next test:** seek a genuinely nonlinear deck invariant or a new author hint;
do not extend blind SAT or rerun generic language optimization.  A candidate
source can now be rejected cheaply by the exact recurrence oracle before any
full key recovery.

### Exact 42-class complement of the Eye alphabet

**Status:** exact architecture count, canonical decoders negative.  The raw
three-eye cube has `125=83+42` glyphs, and reflection on `C83` independently
has 42 orbits.  This composes neatly with the 42-position plaintext wheel used
in the solved practice ciphers, but that wheel is community-authored
calibration rather than Noita evidence.

The arithmetic is not newly discovered here.  Read-only Discord history shows
the `83+42=125` observation by July 2023, a generic paired 42-to-83 homophone
proposal by January 2024, and the two exact 42 identities together by April
2024.  An older scratch digest had also already recorded the same contiguous
42 unused trigrams (`83..124`); failing to promote that fact into the current
ledger caused the mistaken initial novelty assessment.  The new local result
is the negative calibration of two canonical orderings, not the count itself.

All 83 circular-distance centers, marker-selected centers, rolling centers,
and the canonical-origin multiplicative quotient-log family (40 generators,
global or marker centers, two zero placements) are language-negative.  The
strongest structure statistics are ordinary under global-label controls.

**Next test:** none without an external selector.  Do not fit an arbitrary
permutation of the 42 classes.  Reopen only if a game-authored 42-state table,
ordering, or cycle is found.

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

The first breadth pass is now preserved in
[`novel-synthesis-2026-07-21.md`](novel-synthesis-2026-07-21.md).  It suspends
the prose, one-symbol-per-character, repeated-plaintext, independent-message,
83-state, and same-layer assumptions; records twenty mechanism families; and
scores the first cheap falsification tests.  The direct “nine complete BWT
rows” interpretation is already rejected, while weaker suffix/LCP metadata,
nominal cache traces, `Z101` visible/null walks, 26-column records, 3×3 check
objects, and raw-direction routing remain queued.

The second expansion is now preserved in
[`wide-approach-map-2026-07-21.md`](wide-approach-map-2026-07-21.md).  It adds
eighteen lanes and completes six unrelated cheap probes before following a
survivor.  The apparent `34x27` trie-record effect survives a strict fixed-phase
checksum null but loses selectivity when all record phases are admitted, and
its boundaries have no trie role.  Both canonical 83-to-42 quotient decoders
are language-negative.  No new favorite replaces the ledger; the next wide
cycle should prioritize untouched external-selector, serialization, snapshot,
and metadata-only lanes rather than reopening a rejected numeric transform.
