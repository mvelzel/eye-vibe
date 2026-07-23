# Transferable lessons from the five sdlwdr practice ciphers

This is the method summary requested for applying the practice puzzles to the
Eye Messages.  It separates solved mechanisms from useful negative results;
the exercises are valuable only if the route to an answer is explicit.

## Cipher 1: recover hidden cycles from isomorph maps

Chaining equality-pattern maps exposed two 41-cycles inside an 83-symbol
ciphertext alphabet.  Interleaving them produced an 82-position ciphertext
wheel, while the exceptional `J` acted as an operation that emitted the prior
plaintext character and flipped parity.  Directed ciphertext distances then
accumulated on a 42-position plaintext wheel.  A source match to Rune XLII of
John Martin Crawford's *Kalevala* closed the ambiguity, and the author
confirmed it.

**Lesson:** derive the group skeleton from repeated structure before assigning
letters.  A rare value may change state rather than represent a rare letter.

## Cipher 2: diagnose drift and reversal statistically

Position bands split the ciphertext into the same hidden cycles as Cipher 1.
Aligned windows differed by only `0` or `±1` within a band, revealing slow
one-directional drift.  The sole `J` coincided with an exact reversal of both
wheel traversals.  Accumulating directed distances recovered passages from
Rune XLIX under one shared 42-character alphabet.

**Lesson:** compare transition geometry and position bands, not only symbol
frequencies.  Local discontinuities can identify control symbols and reversal
points before the plaintext is known.

## Cipher 3: turn a hypothesis into an exact exclusion

Cipher 3 remains unsolved.  Its proposed position-progressive reading was
encoded exactly: an arbitrary permutation `P` would decode position `i` by
`P^-i`.  A single 83-cycle cannot confine all data to a 42-symbol plaintext
alphabet; the exact solver returns UNSAT.  More permissive `82+1` and `41+41+1`
cycle decompositions did not close within their time bounds, and scans of
standard selected-card update laws did not collapse the alphabet.

**Lesson:** an unresolved puzzle can still teach model discipline.  State the
precise permutation family, distinguish UNSAT from timeout, and retain only the
part actually excluded.

## Cipher 4: peel off a group action without inventing the inner codec

Standard `C83` adjacent differences expose exact common blocks up to 200
symbols, validating the outer cyclic reduction.  The 53-action inner stream
then resists calibrated English/Finnish homophone attacks, Wadsworth wheels,
adaptive 57-card alphabets, Chaocipher variants, and exact source scans.

The more transferable attack writes an arbitrary cyclic deck update as
`p[i+1] = sign*delta[i] + q(p[i]) mod 83`.  Repeated candidate plaintext
symbols must request the same value of the otherwise arbitrary function `q`.
Seven English/Finnish corpora fail this key-free consistency test under both
orientations and both update-timing conventions; every affine `q` is also
excluded on the natural 27- and 42-position plaintext sets.  The only
57-position affine survivors set the state multiplier to zero and reproduce
the known rank stream. A later case-sensitive bijection test adds a useful
boundary: four natural 57-character prose alphabets fail by roughly 10,700
log-score units while matched controls recover 99.9233% of the text.

A later breadth-first codec pass tested complete printable ASCII, substituted
Base64, all contiguous quotient widths `2..28`, and direct English/Finnish
readings before deepening anything. The readable-codec lanes fail. The
numeric order does retain a narrower clue: consecutive pairs give a
29-state quotient plus parity, while triples give a 19-state quotient plus a
nearly memoryless ternary selector. Both quotients are ordered, but neither
is direct prose under the calibrated static maps.

The bounded follow-up is instructive because its strongest statistic initially
looks like a breakthrough. A leave-one-portion-out context predicts the
binary/ternary selector with corrected `1/1001` tails under four null models.
Carrier attribution then shows `0/23` and `0/42` correct predictions whenever
the coarse context represents a genuinely new full-rank bigram. Almost all
success is exact action-bigram/trigram reuse from the known homologous
plaintext. Separately, 206 walk/control laws and 396 fixed routes pass their
planted controls but are negative on the real data.

**Lesson:** repeated structure can prove one layer while leaving the next
layer unknown.  Convert the recovered group into a functional recurrence: it
can turn plaintext repetition into an exact oracle before any language score.
Calibrated failure is preferable to treating unstable pseudo-language as a
solve. When an exact range factors conspicuously, screen neighboring widths as
well: a quotient can be a mechanism clue without being the plaintext. Then
identify the exact carrier of every significant projection; a low-dimensional
view that merely indexes already repeated full symbols is not a decoder.

## Cipher 5: enumerate implementation details with a key-free oracle

Long equality-pattern isomorphs selected one recursive shuffle family before
any words were guessed.  The winning operation peels packets of increasing
width and concatenates them in reverse order as recursion unwinds.  Decoding
the current ciphertext-card rank, then applying the plaintext-selected update,
recovers all 2,212 revised ciphertext positions and re-encodes them exactly.

**Lesson:** prose hints define a family, not an implementation.  Enumerate
off-by-one choices, packet collection order, and update timing; score the
family against equality invariants; use language only after the state law has
separated.

## Combined attack protocol for the Eyes

1. **Start with label-invariant structure.**  Prefixes, equality patterns,
   reconvergence, and repeat contexts are harder to overfit than language.
2. **Recover the acting group before the alphabet.**  Look for cycles,
   position bands, directed distances, and small state operations.
3. **Allow explicit control events.**  Test rare markers, reversals, resets,
   and branch-local state changes instead of forcing every glyph to be text.
4. **Enumerate bounded mechanism families.**  Implementation details are
   hypotheses to search, not assumptions to bury.
5. **Require held-out verification.**  A crib or optimized key must predict an
   unused continuation, and a full solution should replay the ciphertext.
6. **Calibrate every heuristic.**  Run planted positives and matched nulls;
   reject unstable language-like output.
7. **Keep layers separate.**  Metadata, traversal order, outer group action,
   inner codec, source text, and in-game key are distinct claims.
