# sdlwdr #3 — unresolved progression cipher

**Status:** Unsolved. One exact mechanism family is excluded; two broader
cycle decompositions remain undecided exactly, but corrected bounded searches
make them poor candidates for the complete corpus. A later breadth pass also
rejects direct reuse of the solved ciphers 1/2 wheel, fixed coordinate drift,
120,372 named physical-deck models, cipher 5's recursive update family, and
the frozen standard-coordinate quotient/action lane. A third wide pass rejects
undisclosed exact/affine common-tape factors, low-order `F83` recurrences,
direct MTF/BWT readings, anomalous LZ78 compression, and an equality-only
grammar. The complete 83-member affine two-sheet family
`x ~ a-x (mod 83)` also fails after a matched plant recovers its exact
reflection and held-out plaintext. A capacity-preserving search over the
arbitrary static `83 -> 42` two-sheet architecture likewise passes its matched
heldout plant and fails sharply on the real heldout groups. The complete
34,860-member projective-linear pair plus affine-quotient catalog also passes
overlap/block plants and fails real heldout text. A deliberate `8/43` literal
body-prefix tree is isolated, but does not yet select a decoder. A complete
17,280-member six-stream route catalog also fails: the row plant is
non-identifiable, while the calibrated column/additive selector recovers its
plant but retains no real route at the B 42-action gate.

## What was tested

The working **hypothesis** was that the ciphertext alphabet progresses with
position. The Discord puzzle thread contains only the ciphertext attachment
and a correction to A0; no author hint there endorses this mechanism.
That can be stated without guessing letters.  Let `P` be one permutation of
the 83 ciphertext symbols.  At zero-based position `i`, decode symbol `c[i]`
as

```text
P^-i(c[i])
```

and require all 2,247 decoded events to lie in at most 42 plaintext symbols.
The exact solver assigns every ciphertext symbol to one cycle coordinate and
counts every coordinate reached by its observed positions.  It therefore
tests arbitrary symbol labellings, not only the displayed `0..82` order.

## Exact result

For one 83-cycle, both the complete streams and the marker-stripped bodies are
inconsistent with a 42-symbol plaintext alphabet:

```text
full: events=2247, distinct-position constraints=1870, C83 -> UNSAT
body: events=2229, distinct-position constraints=1858, C83 -> UNSAT
```

This is a real exclusion: no rotation, initial coordinate assignment, or
substitution alphabet can repair that particular `C83` progression model.

Two natural relaxations were also encoded:

```text
C82 + fixed point
C41 + C41 + fixed point
```

Both returned `unknown: timeout` in fresh bounded runs. They are **not**
excluded.

An audit found that the first version of these two encodings reduced every
stream position modulo 83 before applying the cycle's own modulus. That is
valid for `C83`, but wrong for `C82` and `C41`. The exact and heuristic solvers
now retain the true reset-relative position. Corrected ten-second exact checks
find group A satisfiable at the 42-symbol limit for both decompositions; groups
B and C still time out.

A calibrated permutation annealer supplies a bounded diagnostic. In 400,000
swaps × two restarts it does recover 40/41-symbol witnesses for group A, so it
can reach the known satisfiable regime. On the harder groups its best decoded
alphabet sizes are far away:

```text
                 A    B    C    ALL
C82 + fixed     40   65   77     83
C41+C41+fixed   41   64   78     83
```

These are upper bounds, not impossibility proofs. Their value is strategic:
the same search that succeeds on A makes no approach to 42 on B, C, or all 18
streams. Without a new invariant or author hint, more blind depth on this
progression premise is not justified. A separate scan of standard
physical/near-size initial shuffles
followed by selected-card deck updates did not collapse a representative
message to a plausible small alphabet, but that scan is a finite negative,
not a proof about arbitrary deck operations.

The required new invariant was sought by abandoning rather than enlarging the
progression model. In a train-A/test-B-C mechanism-transfer pass:

```text
recovered C82 wheel      matched heldout tail .422886
fixed coordinate drift   78/82/82 states
physical deck winner     136/364/582 outside-42 events
cipher-5 update winner   159/351/581 outside-42 events
```

The `J` that controls solved ciphers 1 and 2 occurs 22 times here and its
complete bounded control family is null. Details are in
[`../docs/practice-cipher3-first-batch-results-2026-07-24.md`](../docs/practice-cipher3-first-batch-results-2026-07-24.md).
The standard-`C83` and label-invariant lanes were retained for the second
batch.

The second batch found the missing label-invariant structure:

```text
A4/A5 body prefix 43
A0/A4 body prefix  8
A0/A5 body prefix  8
A1/A3 body prefix  3
```

The unequal first symbols make a predecessor/IV interpretation plausible.
Ten thousand no-double multiset shuffles have maximum prefix at most 4
(`1/10001` corrected upper tail), so the tree is deliberate. It still does
not promote a simple predecessor-only action cipher. The 2,229 adjacent
events form 1,845 distinct directed edges, with maximum out/in degrees
`32/33`; occupancy corresponds to about `69.041053` equiprobable outgoing
choices rather than at most 42 language actions. A standard-`C83`
transform/width selected on A also fails to replicate on B/C.

A bounded static English-homophone optimizer remains gibberish and scores
about 2,966 log units below its matched planted control, but the control
recovers only 24.97%, so this is not a general exclusion. Four exact
English/Finnish source fingerprints are negative. Full results are in
[`../docs/practice-cipher3-second-batch-results-2026-07-24.md`](../docs/practice-cipher3-second-batch-results-2026-07-24.md).

A follow-up tested the exact `83 -> 42` reflection quotient. The transition
graph itself excludes a fresh single-direction half-cycle: it has 253
reciprocal edge pairs and maximum reciprocal degree 14, while one 42-step
half of an 83-cycle permits at most two reciprocal partners per state. The
direction-free quotient remains meaningful, so two finite coordinate families
were calibrated:

```text
standard raw wheel        real -15.538194, control -7.178008 / trigram
166 old-wheel insertions  real -15.394573, control -7.178008 / trigram
```

Both controls recover 100% plaintext; every real output is gibberish. An
arbitrary hidden-wheel optimizer is not a negative result: it recovers only
9.02% of its planted control after 500,000 steps, so the real corpus is not
interpreted under it. See
[`../docs/practice-cipher3-reflection-wheel-results-2026-07-24.md`](../docs/practice-cipher3-reflection-wheel-results-2026-07-24.md).

The next restart deliberately widened to sixteen mechanism classes before
testing five cheap ones. Outside the known A tree there is no exact shared
factor of length four, while the nine affine length-five coincidences all use
different maps and occur once. A-selected order-one/two recurrences leave
`77/75` residual symbols on A and all 83 on both B and C. Every body's
Berlekamp–Massey complexity is essentially half its length. Direct MTF uses
all 83 decoded values, three first symbols are invalid as literal BWT primary
indices, and neither direct nor inverse-BWT LZ78 counts are exceptional
against 1,000 matched shuffles. The strongest nondisclosed equality-isomorph
contains only two repeated constraints.

A complete read-only author-thread audit adds no operational clue. A 27 July
2026 re-audit found no newer post and verified every integer and stream order
in the 9 KB attachment plus separate A0 correction against the local corpus.
sdlwdr described the third puzzle as “a bit more unique” in 2025, and in 2026
said the source code was lost. A public Crawford *Kalevala* scan finds the
observed prefix-tree shape thousands of times, so it cannot identify a
plaintext passage without a stronger mechanism. Full results:
[`../docs/practice-cipher3-third-wide-first-batch-results-2026-07-24.md`](../docs/practice-cipher3-third-wide-first-batch-results-2026-07-24.md).
The exact source re-audit is
[`../docs/seventy-third-cipher3-source-reaudit-2026-07-27.md`](../docs/seventy-third-cipher3-source-reaudit-2026-07-27.md).

Construction genealogy then motivated a standard-coordinate affine
group-autokey test. Its complete 35,675-member structured catalog passes a
42-symbol plant, but the real A-selected minimum is 75 values:

```text
mode=skip, u(t)=70*t+60, A unique=75
```

The winner becomes invalid on B/C, and no A candidate reaches 42. This closes
four structured global update families in five first-symbol modes. A broader
arbitrary-update Z3 model is unresolved: all five group-A queries time out at
the 42-state boundary, as do all-message 82-state diagnostics. Full results:
[`../docs/practice-cipher3-affine-gak-results-2026-07-24.md`](../docs/practice-cipher3-affine-gak-results-2026-07-24.md).

The exact `83=2*42-1` static two-sheet interpretation was then tested without
an arbitrary pairing. All 83 affine involutions `x -> a-x mod83` were
exhausted; each gives 41 pairs and one fixed point. A group-A substitution
search recovered a planted `a=37` at rank one with 100% A accuracy and 99.95%
frozen-key B/C accuracy. On the real data, both full and body modes select
unstable gibberish and fall from about `-7.03` to `-15.70` log units per
held-out trigram. This closes the standard-coordinate affine symbol quotient,
not an arbitrary hidden pairing or stateful sheet schedule. Full results:
[`../docs/sixtieth-cipher3-affine-involution-results-2026-07-26.md`](../docs/sixtieth-cipher3-affine-involution-results-2026-07-26.md).

The remaining arbitrary static pairing was then represented directly as one
global `83 -> 42` map with exactly 41 doubletons and one singleton. The
capacity-preserving optimizer selected its key on A only. A matched plant
recovered 98.448368% of untouched full-mode B+C and 97.199785% in body mode.
The real frozen keys instead produced gibberish at `-15.749327` and
`-15.744717` heldout trigram score per window, more than eight log units below
their controls. This is a strong calibrated negative for the direct static
architecture, not exact UNSAT over its enormous key space; stateful or
polygraphic variants remain open. Full results:
[`../docs/practice-cipher3-arbitrary-two-sheet-results-2026-07-27.md`](../docs/practice-cipher3-arbitrary-two-sheet-results-2026-07-27.md).

The frozen polygraphic extension exhausts all 84 projective-linear functions
of consecutive pairs, all 83 affine two-sheet quotients, and five explicit
overlap/block routes. A likelihood-ratio screen searches all 34,860
structures, then optimizes the route-balanced shortlist on A only. It exactly
recovers hidden overlapping and disjoint controls at 100% and 96.544276%
heldout accuracy. The real A winner is gibberish and falls to `-15.865307` on
B+C, `8.283842` log units per trigram behind the matched disjoint plant. This
is a strong calibrated negative for the frozen English-character search, not
exact UNSAT or evidence against nonlinear/stateful polygraphs. Full results:
[`../docs/practice-cipher3-pair-quotient-results-2026-07-27.md`](../docs/practice-cipher3-pair-quotient-results-2026-07-27.md).

The remaining low-capacity route lane treated each group's six supplied
streams as rows of one object. It exhaustively searched 5,760 row
concatenations and 11,520 ragged column/snake reads. Controls preserved the
real lengths and hid a weighted 42-step modular action stream. The row
selector failed to identify its plant, so no real row winner was interpreted.
The column/additive selector recovered the planted A path up to reversal; B
removed the false parity route, and the true route retained supports `27/29`
on untouched B/C. On the real data the minimum A support is already 78, and
both members of its A equivalence class use all 83 steps on B. The separate
broad class likewise has no B survivor at an effective-choice bound of 42.
C was not inspected because the frozen B gate failed. Full results:
[`../docs/practice-cipher3-route-results-2026-07-27.md`](../docs/practice-cipher3-route-results-2026-07-27.md).

The exact identity `83=2*42-1` was then read as all signed displacements on a
42-position plaintext line rather than as two-sheet homophony. Both
first-value conventions were exhausted over every authored-order cut and
orientation:

```text
d(v) = ((sign*v + offset) mod83) - 41
2 * 83 = 166 maps
```

A same-length control uses every displacement and recovers its hidden map.
The real full and primer modes have zero survivors. This exactly closes the
166-map numeric signed-path family, while the arbitrary hidden permutation
remains unresolved because both general solvers timed out on their planted
controls before real data was opened. Full results:
[`../docs/practice-cipher3-signed-path-results-2026-07-27.md`](../docs/practice-cipher3-signed-path-results-2026-07-27.md).

## Solution

No verified plaintext has been recovered, so there is no solution text to
state. The complete result is the scoped negative above: the proposed
position-progressive mechanism cannot be one 83-cycle with at most 42 decoded
symbols. The supplied scripts retain the unresolved alternatives explicitly
instead of presenting a timeout as an impossibility proof.

## Transfer to the Eyes

- Translate a verbal mechanism into a label-independent constraint system.
- Use exact contradictions to discard whole key spaces before language search.
- Record `UNSAT`, finite scan failure, and timeout as three different outcomes.
- Calibrate a heuristic on a satisfiable subset before treating its failure on
  the whole corpus as evidence.
- Audit nested moduli: reducing positions by the alphabet size before applying
  a shorter cycle silently changes the model.
- Do not infer that a family is wrong merely because its more symmetric
  one-cycle member is wrong.
- Search reset streams again after removing a possible predecessor/IV; the
  strongest Cipher 3 copy was invisible at full-message position zero.
- A low edge-colouring number is only compatibility. Compare repeated-edge
  occupancy with the proposed plaintext action count before optimizing words.
- A mathematically exact quotient size does not recover its hidden coordinate.
  Require a planted wheel—not only a planted substitution—to succeed.
- When ragged-route parameters are observationally equivalent on training
  lengths, carry the whole coordinate-equivalence class forward. Let heldout
  geometry filter it; never let a lexical tie-break masquerade as recovery.
- Long equality-isomorphic factors are weak when almost every position
  introduces a fresh symbol; count repeated equality constraints explicitly.
- A source corpus may reproduce a prefix hierarchy many times. Treat that as
  compatibility, not identification, unless it predicts unseen text.
- Separate visible-symbol recurrence from hidden affine deck state: failure of
  the former does not test the latter.
- Let a selected update becoming undefined on heldout data count as a
  prediction failure; do not invent an exceptional multiplier afterward.
- A planted SAT instance validates an encoding, not its ability to decide the
  full corpus. Preserve real timeouts as unresolved.
- An exact alphabet identity such as `83=2*42-1` should first be tested through
  a complete low-capacity pairing family. Recover the planted pairing and
  freeze the key across held-out groups before widening to a hidden order.
- If the hidden order is widened, preserve the proposed quotient capacities
  exactly and select the key on one group only. Here, A-only optimization
  looked less bad in-sample while untouched B+C exposed decisive overfit.
- Score equality patterns against a matched null, not by absolute likelihood.
  Random high-alphabet streams overproduce the most common all-distinct
  pattern and can otherwise rank ahead of planted natural language.
- When alphabet size is `2n-1`, test signed displacement on an `n`-state line
  separately from cyclic magnitude and static two-sheet quotient. With an
  ignored primer, boundedness is exactly a cumulative-range test.

The exact checks are implemented in
`scripts/solve_sdlwdr_cipher3_cycle.py` and
`scripts/solve_sdlwdr_cipher3_progression.py`; the bounded deck scan is
`scripts/search_sdlwdr_cipher3_decks.py`. The heldout transfer batch is
implemented in `src/eye_mystery/practice_cipher3_wide.py`,
`scripts/run_practice_cipher3_first_batch.py`, and
`scripts/run_practice_cipher3_wheel_transfer.py`. The prefix/action and static
homophone checks are reproduced by
`scripts/run_practice_cipher3_second_batch.py` and
`scripts/audit_sdlwdr_cipher3_homophones.py`. Reflection-wheel tests are in
`src/eye_mystery/practice_cipher3_reflection.py` and
`scripts/run_practice_cipher3_reflection_wheel.py`. The third wide batch is
implemented in `src/eye_mystery/practice_cipher3_third.py` and
`scripts/run_practice_cipher3_third_batch.py`. The affine GAK batch is
`src/eye_mystery/practice_cipher3_affine_gak.py` and
`scripts/run_practice_cipher3_affine_gak.py`. The affine two-sheet quotient is
`src/eye_mystery/practice_cipher3_two_sheet.py` and
`scripts/run_practice_cipher3_two_sheet.py`. The arbitrary static quotient is
`src/eye_mystery/practice_cipher3_arbitrary_two_sheet.py` and
`scripts/run_practice_cipher3_arbitrary_two_sheet.py`. The projective pair
quotient is `src/eye_mystery/practice_cipher3_pair_quotient.py` and
`scripts/run_practice_cipher3_pair_quotient.py`. The six-stream route pass is
`src/eye_mystery/practice_cipher3_routes.py` and
`scripts/run_practice_cipher3_routes.py`. The signed-path pass is
`src/eye_mystery/practice_cipher3_signed_path.py` and
`scripts/run_practice_cipher3_signed_path.py`.
