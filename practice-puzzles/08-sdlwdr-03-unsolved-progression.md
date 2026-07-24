# sdlwdr #3 — unresolved progression cipher

**Status:** Unsolved. One exact mechanism family is excluded; two broader
cycle decompositions remain undecided exactly, but corrected bounded searches
make them poor candidates for the complete corpus. A later breadth pass also
rejects direct reuse of the solved ciphers 1/2 wheel, fixed coordinate drift,
120,372 named physical-deck models, cipher 5's recursive update family, and
the frozen standard-coordinate quotient/action lane. A third wide pass rejects
undisclosed exact/affine common-tape factors, low-order `F83` recurrences,
direct MTF/BWT readings, anomalous LZ78 compression, and an equality-only
grammar. A deliberate `8/43` literal body-prefix tree is isolated, but does
not yet select a decoder.

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

A complete read-only author-thread audit adds no operational clue. sdlwdr
described the third puzzle as “a bit more unique” in 2025, and in 2026 said
the source code was lost. A public Crawford *Kalevala* scan finds the observed
prefix-tree shape thousands of times, so it cannot identify a plaintext
passage without a stronger mechanism. Full results:
[`../docs/practice-cipher3-third-wide-first-batch-results-2026-07-24.md`](../docs/practice-cipher3-third-wide-first-batch-results-2026-07-24.md).

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
- Long equality-isomorphic factors are weak when almost every position
  introduces a fresh symbol; count repeated equality constraints explicitly.
- A source corpus may reproduce a prefix hierarchy many times. Treat that as
  compatibility, not identification, unless it predicts unseen text.
- Separate visible-symbol recurrence from hidden affine deck state: failure of
  the former does not test the latter.

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
`scripts/run_practice_cipher3_third_batch.py`.
