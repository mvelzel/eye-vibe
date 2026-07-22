# Sixth wide expansion — algebra, codebooks, and construction traces

This pass begins wide again after the fifth fan-out and the bounded stop on
sdlwdr practice cipher 3. It does not deepen the prefix checksum, Gate, Waite,
wand-table, or arbitrary-deck favorite. Instead it asks what representations
have not yet received even one cheap necessity test.

“Novel” means absent from the public/local material checked so far. It cannot
establish that nobody has privately considered an idea. Results discovered
during implementation must be recorded even when they make the motivating
numerology disappear.

## Frozen facts and capacity rules

- The accepted object is nine streams of three base-five direction digits,
  canonically valued `0..82`; the numeric order is engine-authored.
- The first value may be a check or control. The bodies have an exact prefix
  tree, no adjacent equal values, and strong partial isomorphism maps.
- The full direction cube has 125 words and 42 unused words, but generic
  `83+42` pairings are already old community territory.
- Modulus 101 is independently selected by the three full-message checks and
  merged body-trie checksum.
- A null must preserve the equality/prefix structure whenever that structure
  can affect the selected statistic.
- A lane promotes only below its frozen `0.01` threshold and with a second
  held-out consequence. A suggestive exact count is not a decoder.

## Wide portfolio before selection

| Lane | Representation | Cheap necessity | Prior-work boundary |
|---|---|---|---|
| **A. Literal affine action on `F5^3`** | A context isomorphism acts on the three displayed eye coordinates, rather than on an arbitrary 83-label renaming. | For every strong partial context map, solve all 12 affine coefficients over `F5` exactly. | Earlier affine exclusions concern conjugated actions on `F83`, not literal 3D eye geometry. |
| **B. Polynomial/check-root headers** | A body is a polynomial over `F101` or `F83`; its first glyph is a checksum, evaluation point, or root. | Exhaust forward/reverse geometric hashes and the parameter-free `P(header)=0` rules; select maximum panel coverage. | Earlier moments used polynomial *position weights* of degree 0–4, not geometric powers or a header-selected evaluation point. |
| **C. Adjacent quasigroup completion** | Two visible trigrams determine a third base-five word; the result may lie in the 42 unused glyphs and carry a hidden alphabet. | Test only componentwise `z=k-x-y (mod 5)`, all five constants and six global component orders. | Earlier digitwise 3×3 tests combine aligned panels, not adjacent symbols into the missing cube. |
| **D. Neutral-eye word quotient** | Centre is an empty action and the four directions are generator letters, so a trigram is a word of length at most three rather than a base-five integer. | Count exact codebook equivalence classes after deleting centre; then add only the natural opposite-direction cancellation rule. | Turtle paths and `S3` products evaluate actions; they do not audit the static short-word codebook. |
| **E. `81+2` finite geometry** | Labels `0..80` are `F3^4` points and 81/82 are sentinels. | Fit literal affine `F3^4` maps to context edges not touching the sentinels, then require every held-out nonsentinel edge. | This is deliberately crazy and has no selector yet; even a fit cannot promote without an in-game `81+2` clue. |
| **F. Twenty-six-column phase channel** | The 34 complete displayed records are samples of a column-structured object. | Deduplicate copied rows; select the strongest column/label association and compare with independent cyclic row rotations. | The prior 26-column audit only rejected rows as 26-symbol permutations. |
| **G. Synchronizing/error-detecting codebook** | `0..82` is a chosen subset of the 125 length-three direction words; the unused 42 are invalid/error/control words. | Measure static Hamming distance and one/two-symbol splice closure of the complete visible set. | The de-Bruijn probe tested observed transitions, not whether the alphabet itself is a code. |
| **H. Without-replacement packets** | Bodies are card deals or permutation packets rather than top-card output from a mutating deck. | Test exact and near coupon depletion in independently supplied 26- and 83-wide windows. | Existing deck attacks allow repeats; the earlier row audit checked only exact 26-permutations. |
| **I. Algebraic reconvergence cocycle** | Repeated/reconvergent passages identify graph vertices; edge labels may be a mod-101 potential difference. | Build only identifications forced by exact shared substrings and test cycle sums before choosing vertex potentials. | A prefix trie alone is acyclic and makes this vacuous; reconvergence cycles are essential. |
| **J. Straight-line grammar payload** | The nine panels are a compact conformance program whose copied regions are literal subroutines. | Infer a smallest shared phrase grammar and compare its description length with prefix-preserving controls; require a repeated non-prefix production. | Directed-edge reuse and local cellular fits do not measure phrase-level grammar. |
| **K. Exact Noita RNG trajectories** | The arrays were generated offline by a developer-known PRNG and then pasted into native code. | Test only RNGs actually present in eligible Noita code, using headers as the sole seeds/stream selectors. | Generic LCG/xorshift fitting is disallowed; code provenance must choose the generator first. |
| **L. Arithmetic/range-coded packets** | Base-83 bodies are entropy-code digits whose boundaries are the displayed rows. | A candidate frequency table must come from an authored 83-entry/42-entry source and predict row termination; direct printable radix score is irrelevant. | The fifth fan-out rejected raw base-83-to-128/256 conversion, not model-based range coding. |

Lanes G–L remain on the breadth ledger even if the first batch A–F is
negative. They should not be silently converted into large parameter searches.

## First batch frozen tests

### A. `F5^3` affine context maps

Use the seven strong contexts already fixed in
`scripts/test_affine_isomorph_embedding.py`. For each context independently,
solve

```text
y = A x + b  (mod 5)
```

on all distinct observed source→target label pairs, where labels use their
literal canonical base-five digits. Exact consistency is the primary result.
Promote only if at least two independent contexts fit exactly and their
compositions predict a third context. A best-subset affine regression does not
count.

### B. Polynomial headers

For modulus 83 and 101, both body directions, and every global base `a`, test

```text
header + sum(body[i] * a^i) = 0
header - sum(body[i] * a^i) = 0.
```

Also test the parameter-free root rule

```text
sum(body[i] * header^i) = 0
```

in both directions and moduli. The primary statistic is maximum exact panel
coverage after selecting the whole family. A 2,000-sample global relabeling
null permutes labels `0..82` everywhere, including headers, and reruns the
complete selection. Promote below corrected `0.01` only if one fixed rule also
predicts at least two panels outside the known checksum diagonal.

### C. Missing-cube completion

For every adjacent body pair `x,y`, write their three digits and form
`z_j=k-x_j-y_j mod 5`. Select one global constant `k` and one global component
order from 30 models. The statistic is the number of results in the literal
unused range `83..124`. A 2,000-sample global relabeling null preserves the
entire prefix/equality skeleton and reruns the selection. Promotion requires a
corrected upper tail below `0.01`; a survivor must then predict held-out family
membership or language without changing `k` or the component order.

### D. Neutral/cancelling word inventory

This lane was partially calculated during ideation, before this document was
frozen, so its first count is an audit rather than a preregistered discovery.
Delete every centre digit from all 125 trigrams and count distinct words. Then
reduce adjacent up/down and left/right inverse pairs and count again. Record
the visible `0..82` and unused `83..124` class overlap. Promotion would require
the visible set to be one representative of a naturally selected 83-class
code; a merely nearby total such as 85 is not evidence.

### E. `F3^4+2` affine contexts

Use labels 0–80 as four base-three digits. Drop an entire context from this
literal test if fewer than five nonsentinel pairs remain; otherwise solve one
affine map on all nonsentinel→nonsentinel pairs and count sentinel-touching
edges separately. This lane cannot promote on statistics alone because it has
no independent selector. An exact fit in at least two contexts only earns a
search for a developer-authored `81+2` construction.

### F. Column phase

Reconstruct the exact displayed 26-wide trigram rows and deduplicate identical
rows. For each column, form its empirical label distribution; use total
column-vs-label mutual information as the sole statistic. Independently rotate
each unique row in 2,000 controls. This preserves row contents and texture but
destroys shared column phase. Promote below `0.01` only if the effect survives
leave-one-prefix-family-out validation.

## Selection rule

Run A–F before deepening any one of them. If several survive, rank them by
independent selector, held-out prediction, and chronology—not by smallest raw
p-value. If none survives, retain G–L as qualitatively different future probes
and return to the highest-value in-game clue/known-plaintext search rather than
inflating these literal models.

## Results

The first batch has no survivor.

| Lane | Observed result | Calibrated result | Decision |
|---|---:|---:|---|
| A. literal `F5^3` affine action | `0/7` contexts consistent | exact necessity | stop |
| B. polynomial headers | 3/9, `F101`, forward, base 1, additive | `138/2001 = 0.068966` | stop; rediscovers diagonal checksum |
| C. adjacent completion | `441/1018`, `k=1`, order `(0,2,1)` | `1325/2001 = 0.662169` | stop |
| D. neutral word quotient | full 85 classes; visible only 55 | exact inventory | stop |
| E. literal `F3^4+2` action | `0/7` contexts consistent | exact necessity | stop |
| F. column phase | MI `1.882712351` | `1/2001 = 0.000500` primary | nuisance validation required |

### A and E: literal finite geometry fails every context

None of the seven strong partial maps is affine in the authored base-five
coordinates. Pair counts are 13, 13, 13, 6, 25, 25, and 22. The deliberately
strange `F3^4+2` representation also fits none; only one edge among all seven
contexts touches its proposed 81/82 sentinels, so the failure is not caused by
discarding too much data. These results reject the literal coordinate actions,
not label-conjugated arbitrary group actions.

### B: geometric hashing adds nothing to the known checksum

The selected polynomial rule is exactly the existing diagonal identity:

```text
header + sum(body[i] * 1^i) = 0 mod 101.
```

It covers East 1, East 3, and East 5. No reverse, nontrivial global base, or
header-as-root rule improves on three panels. Global relabeling controls reach
at least three after the complete family selection in 137 of 2,000 trials, so
the corrected upper tail is `138/2001 = 0.068966`. The new family does not
predict an off-diagonal record.

### C and D: the 42 missing words do not emerge

The best adjacent quasigroup completion produces 441 missing-range outputs,
less than the control median of 449. Its upper tail is ordinary
(`1325/2001 = 0.662169`).

Deleting centre from all 125 three-slot words gives the expected 85 free-monoid
classes, but the visible numeric prefix `0..82` occupies only 55 classes and
the unused suffix occupies 38, with eight classes shared. Adding native
opposite-direction cancellation reduces the full set to 53 classes; visible
and unused occupy 35 and 29 with eleven shared. The tempting `85≈83` count is
therefore a property of the complete cube, not an 83-class visible codebook.

### F: a strong in-sample phase effect fails family-held-out prediction

The 34 complete rows have unusually high column/label mutual information under
independent intact-row rotations (`1/2001 = 0.000500`). Dropping the first
complete row of every message—thereby removing every main copied body
prefix—leaves 25 rows and a still-low `11/2001 = 0.005497` tail.

That is not enough. For the required predictive audit, hold out each natural
prefix family in turn:

```text
(E1,W1,E2)  (W2,E3,W3)  (E4,W4,E5)
```

Learn same-column label counts from the other six messages and score only the
held-out family, using suffix rows after every first row. The observed parts
are `45,46,49`, total 140. Independently rotating every intact suffix row gives
median 136 and corrected upper tail `856/2001 = 0.427786`. Thus the original
MI is in-sample alignment from repeated/equality structure, including later
aligned coincidences; it does not predict a new prefix family and fails the
frozen promotion rule.

## Outcome

No A–F lane earns depth. G–L remain recorded as qualitatively different future
possibilities, especially the game-provenance-gated RNG and range-coding lanes,
but they have no permission to expand without their stated selector. The next
work returns to broad read-only acquisition of externally supplied clues and
known-plaintext constraints rather than rescuing one of these numerical forms.

Reproduction is in `scripts/run_sixth_wide_expansion.py` and
`src/eye_mystery/sixth_wide.py`.
