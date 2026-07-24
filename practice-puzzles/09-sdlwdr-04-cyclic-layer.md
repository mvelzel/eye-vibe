# sdlwdr #4 — recovered cyclic layer, unresolved plaintext

**Status:** Unsolved; the outer mechanism is strongly identified, and a later
wide codec pass found two numeric quotient leads, but no plaintext or exact
replay has been recovered.

**Thread:** [Practice cipher #4](https://discord.com/channels/453998283174576133/1398401433153572934)

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
9. **Case-sensitive injective substitution.**  The exact 57-wide action band
   was mapped bijectively into four conventional `A-Z`/`a-z`/space/punctuation
   pools with a raw character four-gram model.  Matched planted controls recover
   99.9233% of 1,304 characters at scores near `-11,000`.  Real candidates
   remain seed-unstable gibberish near `-21,700..-21,950`.  This rejects the
   previously untested “straightforward 57-character case alphabet” reading;
   it does not reject a second codec or non-prose plaintext.
10. **Complete printable ASCII.**  Treating the three first ciphertext values
    only as primers, an arbitrary injective map from the 53 differences into
    all 95 printable ASCII characters remains about 10,762 score units below
    a planted control.  The control recovers `99.9231%`; the real output is
    seed-unstable punctuation-heavy gibberish.
11. **Substituted Base64.**  The three difference lengths are all legal
    unpadded Base64 lengths.  An arbitrary injective 53-to-64 digit optimizer
    recovers clean planted prose (`96.8205%` byte accuracy, `975/975`
    printable), but its best real decode has only `691/975` printable bytes
    and trails by more than 17,300 score units.  Natural-phase Base64 is
    rejected.
12. **Contiguous pair/triple quotients.**  A width screen over every grouping
    `2..28` finds real structure at widths 2 and 3.  Width 2 gives a 29-state
    quotient plus parity; width 3 gives a 19-state quotient plus an almost
    memoryless ternary remainder.  Random label assignments make the observed
    pair grouping's low coordinate dependence only `98/10001` of the time.
    These are structural survivors, not decoded text.
13. **Natural quotient alphabets.**  The 29-state quotient is not an injective
    substitution over either English `A-Z + space + period + comma` or Finnish
    `A-Z + Ä + Ö + space`: both planted controls recover exactly, while real
    results remain roughly 9,000–10,000 score units worse.  Exact 24-symbol
    equality-pattern scans also find no match in large English or Finnish
    corpora.
14. **Selector-controlled walks.**  All 206 direct/unsigned/signed/carry/
    toggle/lane laws across widths 2 and 3 were screened on the plausible
    `19..42` rings.  Planted quotient walks decode cleanly; every real
    state/control law loses to the untouched quotient.
15. **Selector prediction with carrier attribution.**  Neighboring quotient
    context predicts the binary and ternary selectors with corrected
    `1/1001` tails under four strict nulls.  This is not a control mechanism:
    predictions on seen coarse contexts are correct `0/23` and `0/42` times
    when the complete rank bigram is genuinely new.  Nearly all success is
    memorized exact rank-bigram/trigram reuse from the disclosed shared
    plaintext.
16. **Fixed route transpositions.**  A label-invariant equality-pattern model
    exhausts 396 odd/even, rail, ragged rectangular, snake, and fixed-block
    routes.  It exactly recovers a planted route.  Real best improvements have
    selection-corrected tails `0.651741` and `0.179104`, so neither quotient
    supports a promoted route.
17. **Exact public-source homophones.**  The 200-symbol common block has 50
    symbols and 150 equality constraints.  With no cap on how many action
    symbols may encode one character, it has zero compatible windows across
    2,040,251 letters-only and 2,478,970 space-preserving characters from
    *Sherlock Holmes*, English/Finnish *Kalevala*, and Finnish *Seven
    Brothers*.  This exactly excludes those passages, not arbitrary sources.
18. **Selector demultiplexing.**  All 68 width-2/3 lane orders, concatenation
    modes, and reversal masks were selected on portions 1–2 and tested on
    portion 3 under 2,000 selector-shuffle controls.  The planted interleaving
    is recovered (`1/201`), while the real winner hurts held-out score and is
    null-ordinary (`1080/2001`).
19. **Typed coordinate reassociation.**  All 186 width-2/3, period-2..32
    selector shifts/reversals were audited after choosing pattern order only
    on a planted fixture.  The planted period-7 transform is recovered exactly
    (`1/101`); the real winner again hurts held-out score (`77/101`).
20. **Canonical signed band and nonlinear GAK restart.**  The previously
    omitted zigzag interpretation of the odd 57-band—signed steps
    `0,-1,+1,...,-28,+28`—does not produce language on rings 19..83, including
    a standard 83-character wheel.  The more general necessary recurrence
    `p'=delta+q(p) mod83` remains open.  An exact all-message model with the
    long common blocks constrained returns `unknown` at 30 seconds for compact
    27, natural-position 27, and natural 42 alphabets.  A packed 250,000-state
    character beam reaches only transition 49 on the real 200-action block.
    Crucially, it also reaches only transition 49 and loses the known target on
    a matched 201-character natural-English plant.  The beam result is
    therefore **inadmissible as negative evidence**; it identifies a search
    limitation, not a cipher exclusion.

The signed-band and packed-beam reproductions are
[`analyze_sdlwdr_cipher4_signed_band.py`](../scripts/analyze_sdlwdr_cipher4_signed_band.py)
and
[`search_sdlwdr_cipher4_nonlinear_gak.py`](../scripts/search_sdlwdr_cipher4_nonlinear_gak.py).

The full homophone/fractionation checkpoint, including both positive controls
and complete numeric results, is in
[`docs/practice-cipher4-fractionation-results-2026-07-24.md`](../docs/practice-cipher4-fractionation-results-2026-07-24.md).

## Verdict

The puzzle has **not** been solved.  The defensible result is narrower: its
visible ciphertext is a standard `C83` running state, adjacent differences
recover the repeated action stream, and the missing inner map is neither the
tested Wadsworth wheel, ordinary static homophones, the tested adaptive
57-card alphabet, a conventional case-sensitive 57-character bijection, nor
an Eye-derived in-game key.  No plaintext is stated because none has been
verified.  The pair/triple quotient structure remains a descriptive numeric
fact, but the bounded selector and route follow-up finds no executable lift
law.  Its strongest apparent predictor is fully explained by exact action-
bigram reuse, so the speculative `57=29+28` two-cycle branch is not opened.
The arbitrary nonlinear cyclic-GAK transition remains the best mechanistically
grounded open inner layer, but it now has an explicit dependency: a crib,
source hit, or stronger constraint-guided search that passes the matched prose
plant.  Raising the same language-only beam is not a valid next experiment.

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
- Numeric label order can carry information after a group reduction.  Screen
  a whole family of quotient/remainder widths before promoting a conspicuous
  factor, then distinguish a structured quotient from a readable plaintext.
- Attribute a significant projection to its exact full-symbol carriers.
  Several strong nulls do not turn memorized homologous transitions into a
  predictive mechanism.
