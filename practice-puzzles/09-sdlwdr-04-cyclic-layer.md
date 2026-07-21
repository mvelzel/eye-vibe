# sdlwdr #4 — recovered cyclic layer, unresolved plaintext

**Status:** Unsolved after a bounded final attack; the outer mechanism is
strongly identified, but no plaintext or exact replay has been recovered.

**Thread:** [Practice cipher #4](https://discord.com/channels/453998283174576133/1227024108286644284/threads/1398401433153572934)

## What is actually known

The author said the puzzle is deck-based, that its three portions have much
shared plaintext, that all three use the same straightforward initial
plaintext-alphabet ordering, and that the original generator was lost.  A
solver independently stated that the effective group is cyclic and its
equivalent ciphertext-alphabet order is standard.

Let `c[i]` be a ciphertext value in `0..82`.  Under that standard cyclic order,
the identity-state action stream is

```text
d[0] = c[0]
d[i] = c[i] - c[i-1] mod 83
```

This is not merely a plausible transform.  It exposes the disclosed shared
plaintext structure with exact, very long blocks:

| Portions | Exact maximal shared blocks | SequenceMatcher ratio |
|---|---|---:|
| 1 and 2 | 97, 105, and 48 symbols | 0.792 |
| 1 and 3 | 94, 105, and 48 symbols | 0.590 |
| 2 and 3 | 200 and 60 symbols | 0.567 |

Across all 1,304 positions, the transformed stream uses exactly 53 values:
all values from `22` through `78` except `23`, `25`, `73`, and `75`.  The
frequency distribution is unusually flat; its most frequent value occurs only
73 times (`5.60%`).  Thus the cyclic layer is recovered, but its actions do not
look like ordinary spaced prose under a static one-to-one alphabet.

The deck hint permits a stronger test than treating those differences as
substitution symbols.  In oriented coordinates an arbitrary cyclic GAK must
obey a recurrence of the form

```text
p[i+1] = sign_c * (c[i+1] - c[i]) + q(p[i])  mod 83
```

where `q` may be any function selected by the current plaintext symbol.  The
reflected plaintext orientation and the convention in which the next symbol
selects `q` give eight finite variants.  A proposed source needs no known key
to be tested: every repeat of the same selector must demand the same value of
`q`.  That functional-consistency oracle is the main new method recovered from
this puzzle.

## Final attack and negative results

The final pass treated each remaining interpretation as a finite model with a
positive or structural control:

1. **Wadsworth/two-wheel accumulation.**  Standard-order cyclic distances were
   accumulated on every plausible plaintext ring from 27 through 83, under
   both directions, origins, straightforward alphabets, and all 82 nonzero
   generator scalings at the most plausible sizes 42, 53, and 57.  No candidate
   produced language.
2. **Static homophones with spaces.**  The 53 actions were assigned many-to-one
   to `A-Z` plus space under paired and frequency-weighted allocations.
   Annealing produced unstable pseudo-language and no common decode.  No single
   action is frequent enough to be an ordinary English space.
3. **Two case-homophones per unspaced letter.**  The exact `52+1` hypothesis
   was tested against English and Finnish five-gram models.  On planted
   1,304-character English and Finnish controls the same optimizer recovered
   about `99.85%` and `98.77%` of the plaintext, with scores near `-14,100` and
   `-14,250`.  Real Cipher 4 candidates remained near `-20,300..-20,900` and
   changed with the seed.  This is a calibrated rejection, not a failed run
   promoted to evidence.
4. **Exact cyclic-recurrence source compatibility.**  The 200-transition
   common block was scanned against seven available English and Finnish
   corpora: 3,743,827 letters-only characters and 4,557,173 space-preserving
   characters.  The scan covers compact and natural-42 space positions, both
   ciphertext and plaintext orientations, and current/next-symbol update
   timing.  There are no complete hits.  The best candidate fails after only
   19 transitions.  This excludes those concrete passages under the arbitrary
   cyclic-GAK recurrence above; it does not exclude other source text or a
   non-GAK deck mechanism.
5. **Adaptive 57-card plaintext alphabets.**  Subtracting 22 makes every action
   a rank in `0..56`.  Six straightforward initial alphabets, every rotation
   and reversal, and thirteen small update laws—move-to-front/back,
   transposition, swaps, prefix/suffix reversal, and cyclic cuts—were tested.
   The best output was punctuation-heavy gibberish.  Stateful rules also
   damaged equality across the exact common blocks; only the static identity
   rule preserved all 757 aligned symbols.
6. **Chaocipher-style disks and common encodings.**  Generalized 57-position
   Chaocipher update conventions, uppercase/lowercase Bacon readings, Base64,
   and whole-stream base-57 integer decoding all failed basic readability and
   byte-structure checks.
7. **Reuse of the Eye corpus.**  The transformed actions were compared with
   Eye trigrams, bodies, adjacent differences, raw directions, known corpus
   orders, and every no-replacement whole-message concatenation of the needed
   length under arbitrary bijective relabeling.  There is no full match.  The
   longest partial match is only 26 symbols with 25 distinct values, the kind
   of weak coincidence expected in a high-alphabet comparison.
8. **Affine cyclic update schedules.**  Every recurrence
   `p' = sign*difference + u*p + v mod 83` was exhausted over the complete
   second portion.  No schedule keeps the plaintext inside either `A-Z` plus
   natural-position space or the complete contiguous natural-42 alphabet.  A
   contiguous 57-state band has exactly two schedules, but both have `u=0`:
   `p'=difference-22` and its reflection `p'=-difference-5`.  The arbitrary
   starting symbol is immediately discarded.  These are just the already
   known direct rank stream, not a hidden stateful decoder.

## Verdict

The puzzle has **not** been solved.  The defensible result is narrower: its
visible ciphertext is a standard `C83` running state, adjacent differences
recover the repeated action stream, and the missing inner map is neither the
tested Wadsworth wheel, ordinary static homophones, the tested adaptive
57-card alphabet, nor an Eye-derived in-game key.  No plaintext is stated
because none has been verified.

## Transfer to the Eyes

- Group reduction should be judged first by whether it strengthens exact
  cross-message structure; Cipher 4's long blocks are the model example.
- A language optimizer needs a planted positive control at the real length and
  alphabet size.  Pseudo-words from an unconstrained homophonic solve are not
  evidence.
- Shared plaintext can expose an outer group action while leaving a separate
  inner codec unresolved.  Do not collapse those two achievements into a
  claimed solution.
- Once an acting group is known, derive its state recurrence before applying a
  language score.  Repeated candidate plaintext symbols then impose exact
  function-consistency constraints even when the key function is arbitrary.
- A supposed in-game key should survive a direct equality-pattern test before
  receiving interpretive attention.  The Eye-reuse branch fails that test.
