# Fourteenth wide horizon: method transfer before depth

## Purpose

This pass follows the rule “start wide before going deep.” It was triggered by
the completed sdlwdr Cipher 4 fractionation audit, but it does not assume that
the Eyes use Cipher 4's mechanism. Instead it asks which *methods* learned from
that audit expose genuinely different Eye-message objects.

“New” below means that the exact construction was not found in this
repository or in the public material already captured here. It cannot prove
that nobody has privately considered the broad idea. A fresh Discord novelty
audit is also currently unavailable because the read-only browser session is
at Discord's login screen; that affects novelty attribution, not the
cryptographic tests.

## Saturated versus underexplored objects

The previous thirteen horizons heavily cover:

- direct transforms of the `0..82` values;
- fixed reading orders, row routes, and component permutations;
- affine/projective maps, small group quotients, and whole-context
  permutations;
- ordinary and extended GAK/deck models;
- direct language substitutions, source cribs, bit packing, Base64, and
  conventional-mode necessities;
- visual paths, local stencils, carry summaries, transition graphs, and
  simple convolutional syndromes;
- first-symbol additive/polynomial checks;
- prefix tries, RePair grammars, and selected Gate/in-game interfaces.

The less explored objects are:

1. **typed fields inside one trigram**, where one eye controls routing of the
   other two rather than all three forming one symbol;
2. **shared generators**, where the ciphertext itself is an automatic
   sequence rather than encrypted prose;
3. **canonical automata of the complete message dictionary**, which merge
   suffix-equivalent states or add failure links rather than only shared
   prefixes;
4. **label-invariant timing**, such as return intervals and renewal structure;
5. **metadata selecting an algorithm class**, rather than being the checksum
   value;
6. **operation-interface archaeology**, where a later game clue selects a
   machine primitive before any Eye number is compared.

## Wide portfolio

| Lane | Hypothesis | First bounded test | Prior-work boundary and promotion gate |
|---|---|---|---|
| **A. Raw-eye selector demultiplexing** | One eye digit `s in 0..4` is a lane tag; the ordered pair of other eyes is a `0..24` payload symbol. Stable subsequences by `s` carry the readable streams. | Exhaust the three selector positions, both payload orders, separate-lane scoring, and every global lane order/reversal for concatenation. Select on the three independently identified P-header panels after their copied opening and test the fixed winner on the six Q panels after their copied openings. Repeat the whole selection under global permutations of the 83 accepted glyph labels. | Earlier tests permuted eye order or ran small header-controlled machines; none removed a component and used it as a positional selector. Promote only with a calibrated planted interleaving and corrected held-out tail below `.01`. |
| **B. Typed cross-glyph reassociation** | The three displayed eye tracks were aligned at different short offsets before trigram packing. | For block periods 2–26, hold two component tracks fixed and shift or reverse exactly one; require every reconstructed trigram to remain in `0..82`. Select by an equality-pattern model on P and test Q under complete global-label controls. | This is not a global eye order, snake, or middle-eye rotation. It changes which positions are associated while preserving field types. An order is admissible only after it recovers a planted delayed track. |
| **C. Shared linear generator** | Each panel is a different seed/reset of one LFSR or linear recurrence, over either `F83` glyphs or one of the raw `F5` eye tracks. | After deleting known copied openings, solve exact shared recurrences of orders 1–32. Fit coefficients on P, then count exact Q equations without refitting. Repeat for raw, first difference, and the six fixed component orders only. | Prior affine recurrence work is order one and plaintext/state driven; the convolutional test searched parity checks on suffixes. This asks whether the ciphertext itself is one shared automatic sequence. Promote only an exact or exceptional held-out recurrence that a planted fixture recovers. |
| **D. Minimal dictionary automaton** | The nine bodies are accepted words of one canonical finite language. Merging suffix-equivalent trie states exposes a construction checksum or state count hidden by the ordinary prefix trie. | Build the unique minimal acyclic deterministic automaton (DAFSA) of the nine marker-stripped bodies. Freeze its transition-label sum modulo 101, node/edge counts, and merge profile before comparing them with equality- and diagonal-check-preserving controls. | RePair and the ordinary prefix trie do not merge identical continuations. A modulo-101 hit alone must survive the existing matched subgroup and predict an independently frozen count or Gate interface. |
| **E. Failure-link sieve** | The developer constructed a multi-pattern matcher: copied prefixes are trie edges, while repeated internal phrases are cache/failure links. | Build the canonical Aho–Corasick automaton of the nine bodies. Test only the incoming-edge labels selected by non-root failure links, their mod-101 sum, and the fixed depth-change word. | This is distinct from RePair and suffix-trie sums because failure links are canonical and consume internal repeats. It advances only if the checksum and one structural word replicate under a matched control; inspecting arbitrary transition-table cells is forbidden. |
| **F. Return-time channel** | Numeric labels are opaque, but gaps between repeated labels encode plaintext classes, deck return times, or separators. | Replace each occurrence after the first by its backward recurrence distance, with first uses typed separately. Test fixed logarithmic bins, exact small distances 1–42, and row resets using an external equality-pattern model. Preserve the complete equality skeleton in controls and vary only message/row segmentation. | Cache/reuse audits counted role frequencies; they did not treat the full return-time tape as a possible ciphertext. Promotion needs held-out language structure not already forced by copied full-label passages. |
| **G. Renewal/deletion decoder** | Some visible values are state updates and others are emissions; plaintext appears after deleting a deterministic recurrence class. | Freeze deletion masks from first-use/repeat, return-distance parity, and component-change count, then score retained equality patterns with length-matched masks. | Earlier metadata/payload splits used headers or fixed positions, not label-invariant renewal events. No mask may be selected from language words, and retained copied prefixes are charged. |
| **H. Morphic or uniform-substitution generator** | The nine panels are prefixes/leaves of an L-system or automatic sequence, explaining long copies and scaled reappearances without encryption. | Search uniform morphism lengths 2–5 using equality constraints only; learn productions on P and require literal production consistency on Q after removing shared openings. | RePair measures compression but does not demand one substitution rule. A satisfiable interpolation does not count unless production names and images are identifiable on a planted control and predict Q. |
| **I. Minimal predictive-state partition** | Visible values are emissions of a small hidden process; future-equivalent histories should merge even when current labels differ. | Construct bounded context trees of depths 1–5 on P, minimize by future-distribution equivalence, and evaluate Q code length. Compare to degree-, equality-, and copied-prefix-preserving controls. | Transition spectra and line-digraph factorizations used support only. This tests predictive causal states. State count must be charged; a full-context lookup is inadmissible. |
| **J. Checksum-type metadata** | The factoradic header classes identify *which* fixed check algorithm applies, rather than containing plaintext or one universal check value. | Freeze a small standard dictionary: additive and alternating sums, Fletcher first/second accumulators, xor, digit sums, and forward/reverse low-degree moments over 83 and 101. Select one rule for P, Q-east, and Q-west using within-class leave-one-out prediction. | Generic checksum scans ignored the independently recovered header type system; per-panel fitting is forbidden. Promotion requires all withheld markers or a corrected matched-control tail below `.01`, not another three-panel diagonal rediscovery. |
| **K. Complement end-around arithmetic** | Encoding an `F83` operation in three base-five digits uses the missing 42 cube states as reduction/carry states, analogous to end-around carry rather than ordinary radix-five borrow. | For each adjacent transition, compute the unique raw `0..124` sum/difference representative and its `±83` reduction event. Across the seven frozen nonliteral isomorphs, test equality of the complete reduction-state word with global-label controls. | Earlier carry tests compared digit borrows and high/low-eye ablations; they did not treat the 42 excluded values as explicit reduction states. Promote only family-held-out replication. |
| **L. Adjacent motion-class transducer** | The unresolved lag-1 hidden-geometry equations define motion classes consumed by a stateful transducer; longer chords need not be geometric. | Work directly with the 44 forced adjacent chord classes. Fit a bounded deterministic turn machine on the first isomorph family and predict class equalities in the last family, while retaining exact wheel realizability as a separate constraint. | Multi-lag wheel geometry is exactly rejected; adding lag 2 is forbidden. This lane may deepen only if the class machine predicts withheld constraints and the lag-1 CSP remains satisfiable. |
| **M. Canonical branch-check recursion** | The mod-101 trie closure is the terminal value of a small recursive checksum, not a one-off sum. | Freeze standard bottom-up recurrences using child sum, child count, depth, and incoming label with coefficients in `{-1,0,1}`. Select on complete proper branches and predict the root or a held-out branch, with the entire coefficient family repeated in diagonal-preserving controls. | This is the direct high-value continuation of the strongest existing breadth result. It cannot promote by restating `37,774 mod 101 = 0`; it must predict an unscored node quantity. |
| **N. Operation-interface archaeology** | A later Noita asset restates one of the machines above—five-way demultiplex, delayed typed tracks, failure links, LFSR taps, or recursive branch checks. | Search installed and historical scripts/assets for executable data flow matching one frozen interface, not for the numbers 83/42/101. Trace inputs, state, and outputs into one predicted Eye statistic. | The Gate theory remains inspiration only. The asset must select the operation before seeing its Eye fit and predict a quantity not used for selection. The renderer, Gate, WAK, and native-code negative boundaries remain in force. |
| **O. Version-differential clue dating** | A decoding aid was added after the Eyes and can be isolated by when a new interface appeared. | Build a manifest of historical depots/snapshots at major clue releases and diff only files whose executable interface matches lane N. | Internal invention may predate public release, and decoder clues may postdate the ciphertext. Chronology rejects only externally sourced construction material that did not yet exist; it never rejects developer-created ideas merely because the asset shipped later. |

## Ranking before implementation

Scored qualitatively by independence, capacity control, cheap falsifiability,
and transfer value:

1. **A** is the strongest immediate method transfer. It changes the object
   from 83 glyphs to a typed selector plus payload, has a clean held-out split,
   and can reuse the positive-control discipline that just rejected Cipher 4.
2. **C** is the cheapest exact generative-family test and can close a bounded
   order/representation family without language scoring.
3. **D/E** are canonical continuations of the strongest trie evidence. Their
   representations make no arbitrary traversal or key choices.
4. **M** is higher-value than another numeric transform, but has more
   coefficient-selection capacity and therefore follows D/E.
5. **B** is a natural second fractionation transfer only after its planted
   calibration is fixed without viewing the real winner.
6. **F–I** are label-invariant but need careful capacity accounting.
7. **J/K/L** connect strong existing observations but are easier to overfit.
8. **N/O** are acquisition lanes. They can leapfrog cryptographic ranking
   only when an authored executable interface is actually obtained.

## First frozen experiment

Implement lane A only after this horizon is committed.

For every marker-stripped panel and each candidate selector component:

1. turn the other two components into ordered pair values `0..24`;
2. stably split those values into five subsequences by selector digit;
3. render either five separate sequences or one concatenation under all 120
   lane orders and 32 per-lane reversal masks;
4. score equality patterns with a fixed externally trained model;
5. select the complete convention on P panels after deleting their known
   copied opening;
6. apply that exact convention to Q panels after deleting their known copied
   openings.

The primary statistic is Q-side improvement over the unsplit ordered-pair
baseline. Controls apply a uniform random permutation to the accepted
`0..82` glyph labels, preserving every message length, equality, copied
prefix, header/body boundary, and accepted-alphabet size; the complete
candidate family is reselected on P for every control.

A planted fixture must recover a five-way interleaving before the real result
is admissible. Promotion requires a plus-one corrected held-out upper tail
below `.01`. A high P score, a pretty lane, or an uncorrected winner is
insufficient.

## Positive-control calibration

The order-8 equality-pattern model inherited from the Cipher 4 route audit
failed the planted fixture: it found the correct selector and lane order but
spuriously reversed lane 4. No real Eye score was calculated.

Pattern orders `8,10,12,14,16,20,24` were then compared **only on the planted
fixture**. Orders 14 and 24 recover the exact planted selector, concatenation,
lane order, and zero reversal mask. Order 14 is the smallest successful model
and is frozen for the real audit. Orders 10/12 choose a wrong lane order;
orders 16/20 choose separate-lane scoring. This calibration changes only the
external pattern statistic, not the candidate family, held-out split, or
global-label null.

## Branching rule

- Commit this horizon before calculating lane A.
- If A fails with a passing positive control, move laterally to C or D; do not
  add selector-dependent substitutions.
- If A promotes, freeze its exact convention and demand a second consequence:
  either Q-panel replication by header subtype or a source fingerprint on one
  lane. Do not translate symbols immediately.
- Keep the unresolved lag-1 geometry and recursive trie checksum on the
  ledger. Breadth-first selection pauses them; it does not reject them.

## First-lane result

Lane A is closed in its frozen form. The order-14 positive control recovers
the exact planted five-way selector, concatenation, lane order, and reversal
mask. The real winner has train improvement `+0.009392391` and held-out
improvement `-0.776995317`. Two of the first three global-label controls
exceed the observed held-out result, proving a corrected tail of at least
`3/201 = 0.014925373`; the `.01` promotion line cannot be reached.

Full results are in
[`fourteenth-selector-results-2026-07-24.md`](fourteenth-selector-results-2026-07-24.md).
Per the frozen branch rule, continue laterally to lane C or D rather than
adding selector-dependent codebooks.

## Second-lane result

Lane C is exactly closed through order 32. The planted `F83` recurrence
`(2,5,7)` is uniquely recovered on P and predicts `462/462` Q equations. On
the Eyes, raw ranks, rank differences, and all six raw-component
serializations are inconsistent on P at every scanned order. At order 32 each
coefficient matrix has rank 32 and each augmented matrix rank 33.

Full results are in
[`fourteenth-linear-results-2026-07-24.md`](fourteenth-linear-results-2026-07-24.md).
The next lateral object is lane D's canonical minimal dictionary automaton,
not a recurrence order large enough to interpolate the finite corpus.

## Third-lane result

Lane D adds no independent structure. The body trie has 919 states and 918
transitions; its minimal acyclic dictionary automaton has 911 states but still
918 transitions. The only merge is the nine terminal leaves becoming one
accepting state. There are zero internal suffix-equivalent merges.

The transition sum remains `37,774 mod 101 = 0` with the exact same
multiplicity vector and `8,174,134,656 / 825,564,856,320` matched calibration
as the existing prefix trie. It is the same event, not corroboration. Full
results:
[`fourteenth-dictionary-automaton-results-2026-07-24.md`](fourteenth-dictionary-automaton-results-2026-07-24.md).

Lane E's failure-link automaton remains distinct because it can consume
internal phrase suffixes even when complete right languages differ.

Lane E's previously broad depth-change descriptor is now fixed before
calculation in
[`fourteenth-failure-link-freeze-2026-07-24.md`](fourteenth-failure-link-freeze-2026-07-24.md).
Use numeric-label BFS order, retain nodes with non-root failure targets, sum
their incoming labels modulo 101, and test exactly one pre-existing word:
`BEXIT=(2,5,24,9,20)` in the retained depth-drop tape. Both are required.

## Fourth-lane result

Lane E closes both frozen conditions. Twelve trie nodes have a non-root
failure target, and every target is at depth one. Their incoming labels total
`792`, residue `85 mod 101`; zero of the
`825,564,856,320` diagonal-check- and marker-preserving subgroup relabelings
can make this fixed checksum close. The complete depth-drop tape is

```text
11,29,32,46,64,71,75,78,79,104,109,112
```

and contains no `BEXIT`. Full results:
[`fourteenth-failure-link-results-2026-07-24.md`](fourteenth-failure-link-results-2026-07-24.md).
The next ranked cryptographic lane is M's predictive recursive trie checksum;
the cache/failure-link representation receives no flexible repair.

Lane M is now made non-tautological and frozen before coefficient evaluation
in
[`fourteenth-recursive-check-freeze-2026-07-24.md`](fourteenth-recursive-check-freeze-2026-07-24.md).
Its 54 bottom-up rules must predict all five branch zeros under
leave-one-branch-out selection and then close the unscored root. The ordinary
trie sum is only one member; 5/5, root closure, a planted selection control,
and a joint matched tail below `.01` are all mandatory.
