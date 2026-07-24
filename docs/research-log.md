# Research log — 21 July 2026

## Re-established facts

- Nine messages, 1,036 trigrams, lengths `99, 103, 118, 102, 137, 124,
  119, 120, 114`.
- The accepted triangular reading gives every value from 0 through 82 and no
  other value.
- No message contains the same trigram twice consecutively.
- After their distinct markers, all nine messages share two values. The full
  prefix trie then branches into East 1/West 1/East 2 (24 shared values) and
  the other six (five); within the latter, East 3/East 4/West 4/East 5 share
  nine, and East 4/West 4/East 5 share 20.
- Raw frequency nonuniformity is explained by those copied prefixes. Removing
  shared material makes the distribution compatible with uniformity in the
  public 2025 frequency workbook.
- Strong causal isomorphs, reconvergence, and alphabet-chaining conflicts are
  the decisive structural evidence. The top `A.B.CB.AC` pattern occurs six
  times where random expectation is negligible.

## New experimental results

### Five-eye affine walk

An exhaustive scan found a degenerate candidate with generator 1, vertical
translations `+1/-1`, centre negation, displayed trigram orders `123/312`, and
horizontal identities. It uses 25 states and has normalized IoC 1.6930.

Fixed-rule null tests:

| Null model | Trials | `P(unique <= 25)` | Joint `P(unique <= 25, IoC >= 1.693)` |
|---|---:|---:|---:|
| Within-message trigram shuffle | 10,000 | 0.001900 | 0.000300 |
| Independent uniform `0..82` | 10,000 | 0.001500 | 0.000200 |

Because the rule was selected from roughly 47,000 variants, these fixed-rule
p-values do not survive the search multiplicity by themselves. More decisively,
16 simulated-annealing restarts with 200,000 iterations each could not turn the
two alternating state alphabets into English. The best score per tetragram was
`-12.1439`; an in-corpus English reference scored `-9.6453`. Outputs were stable
gibberish. This branch is rejected.

### Gaussian extension-field walk

Because `83 = 3 mod 4`, the equation `i^2 = -1` has no solution in `F_83` but
does in its quadratic extension. This gives a particularly natural encoding of
the five eyes as `0, +1, -1, +i, -i` in `F_83^2`. The implementation exhausts
six centre operations, six observations, four initial states, both reset
policies, and all 36 parity-dependent trigram orders: 10,368 concrete walks.

The best candidate misses 108 of the 230 equality constraints in the strongest
published contexts and still uses 37 observed symbols. Candidates using as few
as 32 symbols miss at least 116 constraints. This is substantially worse than
the ordinary standard-deck baseline of 87 mismatches. It rejects this natural
additive/centre/observation family, not arbitrary ciphers over `F_83^2`.

### Structured deck ciphers

Direct move-to-front/back, transpose, swap-front, prefix-reversal, and rotation
decoders all retain 82–83 values with normalized IoC near 1.

The original scan used ascending and descending numeric initial decks. A
label-invariant result is available for move-to-front and move-to-back: at each
repeated card, the move-to-front rank is the number of distinct cards accessed
since its previous occurrence. This working-set distance is independent of the
initial deck. Across the Eye corpus, repeated occurrences alone realize 59
distinct ranks (and 59 after dropping every first trigram); 189 repeated
occurrences have rank above 25. Move-to-back maps the same invariant through
`rank = 82 - distance`, preserving the count. Both models therefore need at
least 59 plaintext instructions under every card labeling.

The more relevant `S_83` construction

1. apply a fixed affine permutation of the deck positions;
2. swap the top with a plaintext-selected position;
3. optionally apply a second simple hidden swap;
4. emit the top card

was scanned over all 6,806 affine bases, with and without treating the first
trigram as an out-of-band indicator. Every tested form still needs at least 81
decoded instructions. Beam searches for an arbitrary second swap also exceed 40
instructions within the first 186 ciphertext values for canonical base shuffles.
This rules out the concrete construction, not arbitrary deck/GAK ciphers.

A generic decoder made it possible to remove the affine-base restriction while
retaining the same fixed-base-plus-top-swap construction. It scanned 8,430
distinct standard physical or near-size shuffles: ordinary interleaves,
Mongean deals, all Josephus steps, affine shuffles on 82 positions with one
fixed card, and affine shuffles on 84 positions with one removed dummy. The
strong contexts contribute 230 equality comparisons. The best candidate still
misses 87 of them and uses all 83 instructions (82 after skipping message
markers). No candidate approaches a conventional plaintext alphabet.

A second scan added one plaintext-selected hidden swap after the output-making
top swap. Across 25 anchored, neighboring, and mirrored rules for every
standard base—210,750 models—the best reset-marker candidate misses 89 of 230
comparisons and still uses 81 instructions. The earlier full-stream best missed
91. The extra swap does not produce a plausible alphabet.

The public allomorph analysis suggests an upper scale of roughly four swaps per
plaintext action. A staged scan therefore extended the same construction to as
many as three deterministic hidden swaps after the output-making top swap. It
tested 292,972 candidates built from 8,598 standard, affine, and near-size
bases and 25 anchored, ring-offset, or mirror rules, plus an explicit no-op.
All bases and single rules were exhausted; pair and triple combinations were
searched on the union of the 50 best bases with and without a hidden swap. The
best exact one-, two-, and three-hidden-swap candidates missed 89, 92, and 93
of 230 context equalities and used 81, 80, and 81 instructions respectively.
Allowing cancelling rules merely recovers the no-hidden baseline of 87 misses
and 81 instructions. This rejects the concrete formula family, not arbitrary
four-transposition deviations from an unknown base.

To test genuinely plaintext-specific sparse rules rather than another formula
family, a coordinate optimizer now learns the concrete action

```text
apply common base; swap(top, plaintext rank); swap(u_rank, v_rank)
```

where the second transposition is arbitrary, fixed per decoded instruction,
and cannot touch the top card. A round is exhaustive in its one-coordinate
neighborhood: for every rank in the current decode it tests all 3,321 unordered
non-top swaps, then commits the single best rule. Its objective prioritizes the
230 strong equality comparisons and then body alphabet size. The distinct
message markers are included as ordinary encrypted symbols, so their actions
can establish different post-marker states.

Calibration uses synthetic plaintext with the same message lengths and all 230
equalities, encrypted on the same best full-stream standard base
`affine-82-fixed82-15-17`:

| Active planted rules | No-op decode | Rounds | Greedy result |
|---:|---:|---:|---:|
| 1 | 9 misses / 48 body ranks | 1 | 0 / 26; exact rule recovered |
| 5 | 44 / 66 | 5 | 0 / 26; all five exact rules recovered |
| 26 | 92 / 76 | 5 | 74 / 76; outside the greedy recovery basin |

Endpoint order is immaterial for a transposition. On the real corpus, the same
base begins at 87 misses and 82 body ranks. Ten exhaustive rounds learn ten
arbitrary rules and reach 65 misses, but the alphabet never drops below 82.
This is a calibrated rejection of the one- and five-active-rule neighborhoods
of that particular base, and a stronger sparse negative than the formulaic
scan. The 26-rule control is an explicit warning not to generalize it to a
dense plaintext alphabet, several hidden swaps per letter, or an unknown base.

The generic decoder also accepts an arbitrary initial card order. Simulated
annealing was first calibrated on planted synthetic data: after 100,000 moves it
reduced a 10-symbol instance from 83 apparent instructions to 31. On the real
messages, representative interleave, Mongean, Josephus, and 84-position bases
stalled at 76–80 instructions under the same budget. This is a useful heuristic
negative, not a proof.

The newly discovered East-5-first marker order suggests that the panels might
be consecutive chunks of one stateful stream rather than nine resets. That
interpretation was tested without pruning at all nine cyclic starts. The 6,806
affine bases give 61,254 candidates; the best still uses 81 instructions and
misses 176 of 230 context equalities. The 8,430 non-duplicate standard
physical/near-size bases give 75,870 candidates; the best uses 81 instructions
and misses 177. East 5 is not the best start in either family. Thus the order is
not persistent state for this fixed-base-plus-top-swap construction.

The base permutation itself was then made unrestricted. A separate annealer
scores both the full 230 equality constraints and decoded alphabet size. Its
calibration is deliberately sobering: exhaustive best-swap descent repairs a
one-swap perturbation of a planted 26-symbol instance immediately, but a
five-swap perturbation can stall far above the planted alphabet. On the real
corpus the best long run misses 78 equality constraints and still needs 81
instructions; best-swap descent stops at 85 misses. This strongly disfavors the
common-base-plus-top-swap mechanism while remaining a heuristic, not an exact
rejection of every arbitrary base.

Finally, an exact Z3 encoding was built for an unrestricted common base,
arbitrary initial labeling, a top swap, and at most 26 plaintext positions.
Selected first-family, last-family, and combined runs all timed out after 60
seconds with `unknown`, under both integer and bit-vector encodings. This marks
the present solver boundary; it is not evidence of satisfiability or
impossibility.

Two further physical-card families have now been closed conditionally. A
generalized 83-symbol Chaocipher implementation was first verified against the
published 26-letter `WELLDONE...` example. It then crossed 13 constrained
alphabets (natural, reverse, the two historical alphabets, `BDMAGICK`,
`LUMIKKI`, `SNOWWHITE`, and six other Noita/metadata keywords), both odd-deck
nadir choices, every left/right pairing, and marker-full/reset modes: 676
candidates. Every candidate retained all 83 output states; the best missed 127
of the 230 strong equality comparisons. This rejects those exact
generalizations, not an arbitrary pair of 83-symbol Chaocipher alphabets.

The top-swap scan was also broadened to selected-card handling. Each round
applies one of the same 8,599 identity/standard/near-size bases, emits the card
at the plaintext-selected rank, and then performs one of six ordinary actions:
move the card to the front or back, cut to or after it, or reverse the prefix or
suffix packet. Full-message and marker-free resets give 103,188 models. The
best result misses 93/230 equalities and still needs 82 plaintext instructions;
packet cuts and reversals are worse. This closes a simple magician's-deck gap
between the no-base adaptive tests and the common-base/top-swap test.

#### The 26-trigram row boundary

Every complete interleaved visual row-pair contains exactly 26 trigrams. The
archived early-access `gun_procedural.lua` and the current version both clamp
ordinary generated wand `deck_capacity` to 26; the game also names the
reshuffle flag `shuffle_deck_when_empty`. This is genuine shared in-game
vocabulary, although special constructions can reach 30 and the correspondence
does not by itself identify a cipher.

It suggests a precise decoder rule that had not been tested: reset the hidden
deck at every visual row-pair. Exhausting all 8,599 bases in the common-base
plus top-swap family, with and without treating the initial marker as
out-of-band, gives 17,198 candidates. The best misses 100/230 equalities and
uses all 83 instructions. Repeating the row-reset test for the six selected-
card actions adds 103,188 candidates; the best misses 109 and uses 82
instructions. Thus the 26 coincidence remains a plausible passive alphabet or
deck hint, but it is not a literal row-boundary reset in these mechanisms.

### Position-progressive permutation

The public research log left the model

```text
cipher_i = P^i(S[plain_i])
```

as a tentative possibility, where `P` is an arbitrary permutation and `S` a
substitution. Direct optimization over arbitrary cycle structures was first
calibrated on planted data. It repairs one- and five-label perturbations of a
known 26-symbol instance by exhaustive best-swap descent, while searches from
unrelated starts are much weaker. On the real corpus, random and fixed-cycle
searches retain 79–80 decoded values, far from an ordinary alphabet. A broad
Z3 encoding timed out even at loose bounds, so neither heuristic is the result.

The decisive test is a small exact certificate. First consider a common
starting phase. If the two strong length-30 last-family alignments are copies of
one plaintext passage, East 4 at position 68 to East 5 at 69 defines `P`, while
East 4 at 68 to West 4 at 71 defines `P^3`. The partial `P` map contains

```text
31 -> 33 -> 62 -> 8
69 -> 31 -> 33 -> 62
```

but the independent `P^3` map requires `31 -> 69` and `69 -> 17`. Both are
immediate contradictions. Therefore no permutation, cycle structure, or
substitution alphabet satisfies the common-phase model.

More strongly, unknown per-message phases do not rescue it. Call the East
4→East 5 map `A` and East 4→West 4 map `B`; arbitrary phases merely change which
powers of `P` these maps are, so they must still commute. Four observed edges
give

```text
A(3)=44   B(3)=22   A(22)=23   B(59)=23
```

Commutativity requires `B(44)=B(A(3))=A(B(3))=23`. Since `B(59)=23` and `B` is
injective, this would force the distinct symbols 44 and 59 to be equal. Thus
the entire single-permutation progression family is excluded, including
arbitrary cycle structures, alphabets, and per-message starting phases.

### Partial-permutation completion bounds

Each high-confidence repeated passage defines an injective partial permutation
of the 83 ciphertext labels. Decomposing its observed directed graph into paths
and cycles gives sharp, label-independent completion bounds: a path with `k`
edges costs `k` transpositions when closed, while a `k`-cycle costs `k-1`.

The marker-plus-shared-prefix contexts are exceptionally simple. Depending on
the family, they fix 5, 18, or 20 distinct labels and add one marker edge; each
can be completed with one transposition moving two labels. This is exact
support for the intuition that the different marker actions can be very close,
though it does not determine their common base.

The later contexts are much less sparse:

| Context family | Observed edges | Minimum transpositions | Minimum support |
|---|---:|---:|---:|
| first gap-28 | 6 | 6 | 11 |
| first length-18 maps | 13 | 13 | 22–24 |
| last East 4→East 3 | 22 | 22 | 40 |
| last length-30 maps | 25 | 25 | 42–43 |

These are cumulative context transformations, not individual plaintext
actions, so the large bounds do not contradict a sparse generator by
themselves.

Crucially, every map leaves at least two source and target labels unassigned.
Closing paths gives a concrete minimum completion, and exchanging the targets
of two unobserved sources flips its sign without changing any observed edge.
Therefore every tested context has both even and odd completions. For the two
length-30 maps the minimum even completion uses 26 transpositions; the minimum
odd one uses 25. The present context evidence cannot choose `A83` over `S83` or
vice versa. Any parity attack needs a context covering at least 82 labels or an
independent relation that fixes the remaining completion choices.

### Partial-map closure, transferred from practice `two`

The solved practice cipher `two` was cracked by extracting complete 12-label
maps from equality-pattern repeats and composing them until they closed to a
small permutation group. The same operation is now implemented for the seven
strong Eye contexts rather than merely cataloguing their repeat locations.
Their maps expose `6/13/22/25` edges out of 83, so inverses and short words are
kept only where every constituent edge is observed. If two partial words send
the same source label to different targets, they are provably distinct in
every full permutation-group completion. A clique of such conflicts therefore
gives an exact, model-conditional lower bound on group order without choosing
arbitrary values for the missing edges.

At reduced-word depth five, retaining words with at least two forced edges,
the results are:

| Symbols trimmed from each repeat end | Forced partial-word restrictions | Greedy certified distinct-element clique |
|---:|---:|---:|
| 0 | 4,339 | 109 |
| 1 | 3,661 | 108 |
| 2 | 2,471 | 85 |
| 3 | 1,303 | 70 |

Every pair among the seven direct context maps conflicts at trims zero through
two; 20 of 21 pairs still conflict at trim three. The clique algorithm is not
claimed to find the maximum, but every element it reports has an explicit
pairwise conflict witness, so each displayed number is a valid lower bound.

Unlike practice `two`, however, these restrictions do **not** close to a small
or stable group. The bound grows with word depth and falls materially when one
more boundary symbol is removed. More decisively, a matched null independently
shuffles each map between its exact observed domain and image sets while
preserving its fixed-point count. At trim two, 9 of 10 nulls equal or exceed the
observed clique of 85 (null median 87, range 70–96). At trim three, 11 of 40
equal or exceed 70 (median 65, range 52–81). Large conflict cliques are thus an
ordinary consequence of composing seven overlapping sparse injections, not
evidence for a recovered Eye group.

This is a useful negative transfer: the practice-`two` route needs maps close
to complete, whereas the strongest Eye repeat covers only 25 of 83 labels and
composition rapidly loses observed edges. A new longer repeat, a way to join
contexts, or an in-game clue that supplies missing label correspondences would
be required before genuine group closure becomes identifiable.

### Affine group autokey

For hidden affine state `(a,b)` and visible coordinate `x=b/a`, normalize each
plaintext operation by `t=v/u`. Then

```text
t_i = (x_i - x_(i-1)) * a_(i-1) mod 83
a_i = u(t_i) * a_(i-1) mod 83
```

All affine, exponential, power, and shifted-reciprocal choices tested for `u(t)`
retain 81–82 plaintext values. An unrestricted beam reaches 27 values after 100
symbols, 38 after 200, and exceeds 40 after 243. Exact integer and finite-enum
SMT formulations at 27 and 40 values time out; they do not prove impossibility.

Those calculations assign field coordinates `0..82` directly to the displayed
glyph values. That is a special labeling, whereas a general group-autokey model
allows an arbitrary permutation between ciphertext labels and the points on
which the hidden group acts.

To remove that assumption, `affine_embedding.py` assigns an unknown, injective
field coordinate to every observed ciphertext label and one unknown affine map
to each repeated-plaintext context. A second implementation independently
eliminates most coordinates by propagating affine expressions over a directed
spanning forest. Both encodings give the same result for the last-family
contexts:

| Group | Context assumptions | Exact result |
|---|---|---:|
| `C83:C41` | East 4→West 4 and East 4→East 5, length 30 | `UNSAT` |
| `C83:C82` | either one or any pair of the three contexts | `SAT` |
| `C83:C82` | both length-30 contexts plus nested East 4→East 3, length 25 | `UNSAT` |

Thus `C83:C41` is excluded under only the strong three-occurrence isomorph.
Using just this last family, excluding full `AGL(1,83)` would also require the
weaker assumption that East 3's nested 25-character pattern represents the same
plaintext. The pairwise `SAT` results explain why the public literature treated
that conclusion as tentative.

The `C83:C41` result also has a dependency-free exhaustive certificate. Once
the two affine multipliers are fixed, the unknown label coordinates and the two
translations form a linear system over `F_83`. Of the `41^2 = 1,681`
multiplier pairs, 1,664 systems are inconsistent. Each of the other 17 forces
at least one equality between the coordinates of distinct ciphertext labels,
violating the required relabeling permutation. There are no open cases. This
independently reproduces the SMT result in about two seconds.

The same linear method produces a stronger `C83:C82` result from two independent
high-confidence isomorph families. Across all `82^2 = 6,724` multiplier pairs,
the two length-30 mappings reject 6,644 by inconsistent equations and 76 by
forced coordinate collisions. Only `(4,24)`, `(42,30)`, `(45,7)`, and `(52,32)`
remain linearly open. Adding only West 1's length-18, gap-30 self-repeat tests 82
possible multipliers for each survivor; all 328 extensions are inconsistent.

Consequently both affine transitive groups are excluded without identifying
glyph labels with numeric field coordinates and without using the weaker East 3
context. The conclusion remains conditional in the ordinary cryptanalytic
sense that the strong ciphertext isomorphs are being interpreted as repeated
plaintext passages—the same premise on which the public GAK model is built.

The analogous first-family contexts do not provide such a rejection:
`C83:C82` is satisfiable, while the `C83:C41` run timed out at 30 seconds.

### Initial trigrams as metadata

The nine first values are `50, 80, 36, 76, 63, 34, 27, 77, 33` in the
canonical East/West order. They are all distinct and greater than 26, and each
shares a nontrivial divisor with the universal second value 66. Under simple
fixed, without-replacement nulls, those two events have probabilities 0.02305
and 0.03823 respectively.

More strikingly, the first eye of each message is one direction clockwise from
the second eye of the next message. In canonical order eight of the nine
circular links work: West 4→East 5 is the sole failure, while the previously
overlooked East 5→East 1 link succeeds. Rotating the list to

```text
East 5, East 1, West 1, East 2, West 2, East 3, West 3, East 4, West 4
```

therefore gives a perfect eight-link linear chain through every message, and
East 5 is the unique successful cyclic start. Exact enumeration over nine
distinct values drawn from `0..82`, while retaining the canonical trigram digit
multiplicities, gives

```text
236930178600 / 119276318345184000 = 1.98639748e-6
```

for at least eight of nine circular links under this fixed rule. To estimate
some of the inspection multiplicity, one million seeded samples were also
tested for every current-digit/next-digit pairing and every constant integer
offset: the fixed rule occurred 4 times and some such rule occurred 248 times.
The latter `2.48e-4` rate is still not a universal correction for every rule a
human might notice, but makes an accidental order marker substantially less
plausible than the old uncalibrated seven-link calculation did.

The content immediately after the markers has a complementary hierarchy. All
nine share two values. They then split into a 24-value East 1/West 1/East 2
branch and a five-value branch containing the other six; inside the latter,
East 3/East 4/West 4/East 5 share nine, and East 4/West 4/East 5 share 20. This
is the complete non-singleton prefix trie. The order chain and prefix tree are
exact metadata-like structure, but neither supplies plaintext.

The chain has a useful graph interpretation. For a marker `(a,b,c)`, regard
`b -> a-1` as a directed edge on the three states `0,1,2`. The East-5-first
order is then an edge-continuous trail through all nine labeled edges. The
unused third digits have the exact sorted multiset

```text
0, 0, 1, 1, 2, 2, 3, 3, 4
```

and provide a second ordering. Sorting markers lexicographically by ascending
`(third, first, middle)` gives

```text
East 1, West 1, East 2, West 2, East 4, West 4, East 5, East 3, West 3
```

Every non-root cluster of the observed prefix trie is an interval in this
order. Only the `(third, first)` digit pair and its complete reversal have this
property among the 24 signed choices of two sorting digits.

An exact conditional null enumerates every assignment of the observed marker
multiset to the nine fixed messages. The denominator for every row is `9!`:

| Assignment event | Count |
|---|---:|
| fixed East-5-first trail | 168 |
| fixed ascending `(third, first)` trie order | 864 |
| both fixed rules | **1** |
| any circular trail start and fixed trie order | 8 |
| any circular start and any signed two-digit trie order | 22 |

The observed assignment is that unique fixed-rule intersection. More
post-hoc freedom raises the last event to `22/362880 = 6.0626e-5`, still a
strong conditional composition. This result decodes two header orderings; it
does not identify the body plaintext or key. A direct cipher follow-up also
fails: concatenating bodies in the trie-compatible order and scanning every
affine and standard common-base/top-swap deck leaves at least 82 and 81 decoded
ranks. The best standard body-only candidate misses 178/230 context equalities.

#### A cyclic BWT payload

The two independently decoded marker orders have the exact relationship of a
Burrows-Wheeler transform. Reading the unused third marker digits in the
East-5-first trail order gives last column

```text
L = 300113422
```

Stable sorting gives `F = 001122334`; its stable occurrence order is exactly
the ascending `(third,first)` trie-compatible message order. The LF map is

```text
(6, 0, 1, 2, 3, 7, 8, 4, 5)
```

and is one nine-cycle. East 5 independently fixes primary row zero. Cyclic BWT
inversion then gives `001123243`; regrouping the established base-five
trigrams gives `(1,38,73)`, and the public ASCII+32 representation reads
`!Fi`. Since the recovered object is cyclic, it can naturally be displayed as
`Fi!`.

The exact observed-payload-multiset null is:

| Event | Count out of 22,680 distinct orderings |
|---|---:|
| one LF cycle | 2,520 |
| inverse trigrams all in `0..82` | 1,031 |
| punctuation + uppercase + lowercase form | 15 |
| case-insensitive `fi` suffix | 2 |
| exact `!Fi` | **1** |

Conditioning instead on assignments of all nine observed markers to the fixed
messages leaves 168 assignments satisfying the fixed trail, 37 with one LF
cycle, 14 whose inverse gives three values in `0..82`, and only the observed
assignment giving exact `!Fi`. This is not a universal human-inspection p-value,
but the BWT construction was selected after both constituent orders had already
been decoded and calibrated.

Several literal follow-ups are negative. None of the nine bodies is itself a
valid one-cycle BWT last column, and using its marker value as a primary row
does not round-trip. Fibonacci differencing and all `83^2 = 6,889` two-lag
linear recurrences retain 82–83 outputs. Keywording the 83-card initial order
with `FI`, `FINNISH`, or `FIBONACCI` and scanning 15,236 bases in both marker
modes also bottoms out at 81 decoded instructions. The payload is a strong
hint, not a direct transform or key under those families.

LF traversal associates the rows with
`E5,W3,W4,E3,E4,W2,E2,W1,E1`; reversing that traversal associates the restored
digits with `E1,W1,E2,W2,E4,E3,W4,W3,E5`. A continuous deck scan tested both
orders, marker-present and body-only, over all 6,806 affine and 8,430 standard
bases: 60,944 candidates in total. The best still needs 81 decoded instructions
and misses 177 of 230 repeated-context equalities. Neither derived permutation
is the missing continuous-state key in this model.

Two stronger BWT compositions were checked. At the individual-eye level,
inverse move-to-front plus marker-indexed cyclic BWT was exhausted over all 120
five-symbol initial lists, six marker-digit orientations, and primary-index
adjustments `-1,0,+1`. None of the 2,160 candidates even round-trips the first
message. At the trigram level, concatenating all marker-free bodies in canonical
order gives LF cycle lengths `(1026,1)` over 1,027 values. Three separate
one-value deletions yield one cycle, but their primary-row-zero inverses are
gibberish. A seeded 10,000-trial prefix-tree-preserving parity-shuffle null has
15 maximum cycles of at least 1,026, including ten exact `(1026,1)` patterns and
five full 1,027-cycles. The observed near-cycle is unusual at roughly the
per-mille level, but is neither unique nor a decryption.

#### Wadsworth/cipher-clock exclusion

The historical cipher-clock interpretation has a key-independent obstruction.
Let its plaintext ring have `m` positions and its mixed ciphertext ring have
83. Each plaintext transition advances the ciphertext ring by between one and
`m` positions. If both directed digrams `u->v` and `v->u` occur, their two
clockwise distances sum to 83, so `2m >= 83` and `m >= 42`, regardless of the
mixed ring's ordering. The Eye bodies contain 59 such reciprocal digram pairs;
West 3 alone includes `37,0,37`. This exactly excludes the classical construction
with 29 Finnish letters or 30 letters-plus-space. It does not exclude a
nonclassical physical ring with repeated symbols and at least 42 positions.

Aki's published disk-derived candidate is one such nonclassical ring: 114
physical positions containing 37 distinct plaintext symbols. Its exact
next-occurrence mechanism was reproduced and scanned with every one of the
6,806 affine permutations of the 83-position output ring, resetting each
message, in full-stream and marker-free modes. Against transliterated
*Kalevala* Finnish, the best scores are `-15.3843` and `-15.4314` per
tetragram, while the training-corpus self-score is `-8.8862`; both outputs are
visibly digit-heavy gibberish. This is a conditional negative for that input
ring, affine output ordering, and reset rule. An arbitrary mixed output ring or
a different repeated-symbol physical ring remains outside the scan.

#### Finnish language controls

Two public-domain Finnish corpora were used, with `ä`, `ö`, and `å` retained as
distinct placeholder symbols rather than merged with `a` and `o`. On the old
25-state full-stream alternating walk, the best Finnish score is `-11.4691`
per tetragram versus an in-corpus reference of `-10.9524`. Ten nulls jointly
shuffle every disjoint prefix-tree edge, preserving copied prefixes, message
lengths, and parity frequencies; they range from `-13.1903` to `-13.0532`.
The analogous English experiment has a smaller advantage over independently
shuffled nulls (`-12.2334` versus `-13.5226..-13.6878`) and is much farther from
its in-corpus reference (`-9.6862`). This is evidence that the marker's `Fi`
reading is language-relevant, not evidence that the walk is correct.

The cleaner cipher test removes the now-confirmed marker before resetting and
tracing each body. It necessarily reproduces every copied plaintext prefix.
The best 25-state reflection and 26-state negation walks, each with alternating
triangle alphabets, score `-11.8874` and `-11.9044`; their five respective
prefix-tree nulls occupy `-13.2540..-13.0903` and
`-13.2980..-13.1018`. Both outputs remain stable Finnish-looking gibberish.
The stricter monoalphabetic variants score only `-12.9385` and `-13.2077`.
The 16-state odd-East/checksum walk scores `-11.7572`, inside its simple shuffle
range `-11.8627..-11.4698`, and remains rejected. Allowing arbitrary
many-to-one state readouts without a distribution constraint degenerates to
`SISISISI...`, a standard finite-n-gram maximum rather than plaintext. A
chi-square Finnish unigram constraint still collapses into short
`ISI/ATA/NEN` cycles and scores implausibly above held-in Finnish; the
homophonic relaxation is non-identifying under this objective.

A source check is now exhaustive for Project Gutenberg's Finnish catalog.
All 3,648 texts loaded successfully. The scanner generated 2,631,331 candidate
lines, sentences, or paragraphs under letters-only normalization and 2,772,407
with spaces preserved. Neither set contains a complete exact-length
`2/24/5/9/20` nine-entry prefix tree. More strongly, neither contains even the
24-character three-entry upper branch. Letters-only partial counts are five
deep-20, one nested-9, zero lower-6, and zero joined roots; space-preserving
counts are two, one, zero, and zero. The public Finnish translation of *Corpus
Hermeticum* XIII likewise has no complete first-family fingerprint. This still
does not cover the 2020 Finnish print translation or custom text.

#### A candidate embedded instruction

The marker order and prefix trie compose in an unexpectedly legible way. Start
the message ordering at East 5, as independently required by the unique perfect
marker-chain rotation. A breadth-first traversal of the non-singleton prefix
trie, preserving that message order between sibling branches, has cumulative
depths

```text
2, 5, 24, 9, 20  ->  B E X I T
```

under ordinary A1Z26. The universal two-value root gives the initial `B`; the
four proper branch nodes spell `EXIT`. It is possible to read this
self-referentially as “breadth-first: EXIT.” This is not merely an anagram:
with the six-message root branch first, breadth-first order is exactly
`5,24,9,20`. A depth-first walk would instead give `5,9,20,24`.

This interpretation has substantial post-hoc freedom: A1Z26, cumulative rather
than edge depths, breadth-first traversal, and exclusion or interpretation of
the root were all considered after inspecting the tree. A uniform random-
cutpoint calculation would badly misrepresent natural repeated prose, so no
discovery p-value is claimed. No indexed public report of this exact reading
was found in the web sources checked on 21 July 2026.

Nevertheless, `EXIT` suggests a concrete internal check. Arrange the canonical
message order in its natural 3x3 checkerboard:

```text
East 1  West 1  East 2
West 2  East 3  West 3
East 4  West 4  East 5
```

and treat each component of a marker trigram as the documented direction
`centre, up, right, down, left`. Starting at East 5, all three component fields
leave the grid:

```text
first:   East 5 -> West 3 -> East 2 -> north
middle:  East 5 -> West 3 -> East 2 -> east
third:   East 5                         -> south
```

Thus the independently selected start and the literal instruction have an
exact directional realization. A full audit weakens the uniqueness claim but
adds a separate multiplicity fact: East 3, West 3, and East 5—and no other
starts—each have the complete north/east/south exit signature. Shuffling the
observed marker multiset over the fixed grid gives the exact counts

```text
fixed East 5 has NES:       2,688 / 362,880
at least one NES start:     5,328 / 362,880
exactly three NES starts:     312 / 362,880
```

Holding the observed East 5 marker fixed while shuffling the other eight gives
48/40,320 assignments with three starts. A seeded one-million-trial null using
nine distinct uniform values from `0..82` found 1,602 fixed East 5 events,
5,447 grids with any NES start, and 75 with at least three. Allowing any
repeated signature made of three distinct exit directions, rather than the
inspected `NES` target, raised the last count to 1,167. These are useful
conditional calibrations, not a discovery p-value: the 3x3 layout, routing
interpretation, and target signature were all selected post hoc.

The first two East 5 paths visit markers 33, 34, and 36, leaving 35 (`120` in
base five) as a tempting missing value, but 35 occurs seven times in four
message bodies and has not produced a consistent next step. Inspecting the
ciphertext symbols immediately after each prefix exit also produced neither
text nor a complete marker-pointer chain. `BEXIT` is therefore the strongest
new lead, not a decryption.

The most literal cipher-key follow-up is also negative. Interpreting `EXIT` in
the established ASCII+32 alphabet gives card labels `37,56,41,52`; placing
those first and the remaining labels in ascending order defines an unambiguous
keyed initial deck. Move-to-front/back, swap-front, prefix reversal, rotation,
and every transpose distance all retain 82 decoded ranks. An exhaustive scan
then combined this initial deck with 15,236 unique affine and standard bases in
both full-message and marker-reset modes (30,472 candidates). The minimum
alphabet is 81; the best candidate at that minimum misses 89 of 230 context
equalities, matching rather than improving the prior structured baseline.
The same exhaustive scans with `NES` and `BEXITNES` also retain at least 81
ranks and bottom out at 90 and 89 equality misses respectively. None of these
metadata strings is a key for these deck families.

The A1Z26 depths suggest a more useful class of cribs. The famous Emerald
Tablet wording `THATWHICHISABOVEISLIKETO` is exactly 24 letters, apparently a
perfect fit for the first branch. Completing the 20-letter last branch with
`THATWHICHISBELOWISLI`, however, is rejected without choosing a key. Both
phrases contain `HICHI` at offset five. Its ciphertext pattern in the first
branch is `.....`, while in the last branch it is `A...A`; a perfectly
isomorphic cipher cannot map the same plaintext fragment to both patterns.

A second completion survives. Mead's *Corpus Hermeticum VI* contains the
sentence “There is no Good that can be got from objects in the world.” Its
normalized first 20 letters are exactly `THEREISNOGOODTHATCAN`. Assigning
`THERE` to the six-message branch, `THEREISNO` to East 3 plus the last-family
messages, and that 20-letter phrase to East 4/West 4/East 5 produces no
perfect-isomorphism conflict through the entire proposed prefix. This is a
source-backed crib, not a decryption: the wording was selected after seeing
the lengths, many Hermetic sentences start with “there is no,” and a sentence
scan of the downloaded public-domain Mead volumes I–III found no set with
the complete assigned 2/24/5/9/20 tree. Their combined normalized text also
contains zero instances of the full first-family 18/30, 18/35, nested 9/28
source fingerprint.

Combining the upper and lower assignments still produces no key-free
perfect-isomorphism conflict. A stronger, model-specific check encodes a reset
83-card deck in `QF_AUFBV`. Every plaintext symbol has an injective top-swap
rank and one to three arbitrary fixed non-top transpositions; an optional fixed
common base is applied first. This is the concrete sparse construction, not
general `S83` GAK.

For the identity base, the lower 20-letter phrase is `SAT`. The model supplies
12 letter ranks and hidden swaps, and an independent materialized-deck test
re-encrypts `THEREISNOGOODTHATCAN` to the exact East 4 body prefix. Since the
lower-family ciphertext prefixes are literal copies, it also covers the five-
and nine-letter lower branches. The upper phrase is independently `SAT` through
23 of its 24 letters; the final repeated `O` remains `unknown` after four
120-second seed variants and one 180-second run.

The shared-key combination is more restrictive. The first ten upper letters
`THATWHICHI` and the first 17 lower letters are `SAT`, but those ten plus the
full 20-letter lower phrase are exactly `UNSAT`; the full 24+20 assignment is
also `UNSAT`. The same 10+20 query on the best nontrivial structured base is
`unknown` after 120 seconds. Thus the coherent Hermetic tree survives general
GAK and has a concrete lower-prefix witness, while one natural identity-base,
two-transposition realization is rejected when its shared letter rules are
enforced across branches.

Widening the model changes that conclusion in a controlled way. Holding the
verified lower ranks and its first hidden-swap table fixed, a second hidden
swap per letter gives a concrete shared key for all 20 lower letters and the
first ten upper letters `THATWHICHI`. An independent materialized-deck test
reproduces both ciphertext prefixes. With those two slots fixed, a third hidden
swap extends the same construction through 14 upper letters,
`THATWHICHISABO`, again with an independently verified witness. Counting the
output-making top swap, this uses at most four transpositions per plaintext
action—the scale suggested by the public allomorph estimate. The particular
two-hidden witness cannot absorb upper character 11, while a free third slot
does; direct SMT solving of character 15 remains `unknown`.

A calibrated coordinate descent resolves compatibility without resolving
likelihood. Starting from the independently materialized 14+20 witness, each
round exhausts all 3,321 non-top transpositions for every mutable letter/slot.
It reduces the seven remaining upper mismatches one or two at a time and reaches
zero in seven rounds, giving one common rank map and at most three hidden swaps
that exactly re-encrypts the full `THATWHICHISABOVEISLIKETO` and
`THEREISNOGOODTHATCAN` prefixes. A separate materialized-deck unit test locks in
the complete witness. Three composition-matched suffix permutations stop at
one to three mismatches, but that control is biased because the new-letter
ranks were inferred from the Hermetic ordering itself; no discovery likelihood
is claimed. These witnesses show concrete compatibility, not likelihood: the
key was fitted to the crib, and many degrees of freedom remain.

The literal Mead continuation
`THEREISNOGOODTHATCANBEGOTFROMOBJECTSINTHEWORLD` was then tested one branch at
a time. East 4, West 4, and East 5 are all `SAT` through character 23
(`...BEG`); West 4 is also `SAT` through character 24 (`...BEGO`), while East
4 and East 5 are `unknown` there. Adding the repeated `T` at character 25 is
`unknown` for West 4 even when the 24-character prefix is solved first and the
solver is allowed 180 seconds. No branch is rejected or uniquely selected by
this extension. The fitted full shared witness makes a cleaner held-out
prediction and fails immediately: none of its next five encrypted outputs for
`BEGOT` matches East 4. Allowing coordinate refitting repairs three but stalls
at two mismatches. Three exact 24+25 checks with the ranks and first hidden
swaps fixed, but the remaining two swaps free, each time out at 120 seconds
with `unknown`. The short exact witness should therefore be treated as an
overfit compatibility construction.

The total numeric sums of the messages in canonical order are

```text
4040  4124  4754
4295  5656  4748
5385  4936  4545
```

East 1, East 3, and East 5—the odd-numbered East messages and the main diagonal
in this arrangement—are all divisible by 101. Their common gcd is 101, while
every other three-message subset has gcd at most 8. Removing the first values
shows that the markers themselves are exact check digits:

```text
message                 East 1  East 3  East 5
body sum mod 101            51      38      68
required marker (-sum)      50      63      33
actual marker               50      63      33
```

An exact convolution of the independent uniform `0..82` sum distributions
gives `P(gcd >= 101) = 4.11776714e-5` for that fixed triple. In one million
seeded draws from those exact marginals, 44 fixed triples and 3,422 arbitrary
three-message subsets reached the threshold, giving a post-hoc estimate of
`0.003422` for finding some such triple.

Two observed-distribution nulls avoid assuming uniform independent symbols. In
100,000 seeded trials, shuffling the 1,036 observed values into the fixed
message lengths produced 2 fixed-diagonal and 317 any-triple events. Holding the
nine markers fixed while shuffling only bodies produced 4 and 316. Conditional
on the observed body sums and marker multiset, exact enumeration of all `9!`
marker assignments gives 720 assignments (`1/504`) in which the three natural
family representatives all satisfy the mod-101 checksum; the same 720 also
cover one representative from each prefix family. These nulls condition on
different information and must not be multiplied as independent evidence.

The checksum is tied to the distinguished numeric reading rather than merely
to 83 arbitrary labels. All `6 × 6 = 36` choices of a separate eye order for
the two triangle parities were tested. Only the accepted order makes both
parities separately cover `0..82`; it is also the only order with diagonal gcd
101. Every other order gives diagonal gcd 1. This is evidence that the numeric
values—and at least three initial markers—were intentional, but a checksum over
ciphertext does not reveal the hidden-state key.

As a direct follow-up, all field and deck scans were repeated on only these
three messages. The only compressed five-eye walk uses 16 states, but a
monoalphabetic language solve trained on 12.7 MB of alchemical English scores
`-12.7946` per tetragram versus `-9.7204` for held-in natural text and produces
stable gibberish. The diagonal is likely a selected/checksummed channel, but
that walk is another search artifact.

### Public construction and in-game clue audit

Patrick's public Sampo/eye notes propose a 25-position board with five
eye-selected operations. The implementation now exhausts all 36 triangular
operation orders under both the published top/bottom/top readout and a clean
alternating readout. Every stream uses all 25 cells; the best normalized IoC is
only 1.081, versus roughly 1.7 for ordinary language, and every candidate has
adjacent doubles whereas the canonical Eye trigram stream has none within a
message. This rejects that exact automaton, not the broader idea that an
in-game board supplies state.

The alternative published "Master reading" was measured rather than dismissed
visually. It uses 125 symbols, has nine adjacent doubles, only six repeated-
pattern classes, and contains no `A.B.CB.AC` class. The canonical reading uses
exactly 83 symbols, has zero doubles, 67 pattern classes, and six copies of the
top class. The 125-symbol reading is therefore structurally much weaker.

The earthquake/altar ring's full visible `BDMAGICK` sequence was also treated
as a keyed 83-card initial order, rather than only as the shorter `MAGICK`
motif. Across 15,236 affine and standard bases in both marker modes, the best
candidate still needs 81 instructions and misses 89/230 equalities. Direct
keywording does not connect that altar to the body cipher in this family.

The twelve early-access buried glyph texts are old enough to be construction
material and are independently confirmed Noita puzzle prose. Their normalized
lengths and exact repetitions have been inventoried. One text happens to have
103 letters, but the set has neither the nine-message length profile nor the
Eye prefix tree, and direct orb-lore/text-index and key walks are negative. The
current Kantele and eye-placement Lua likewise contain no handler joining music
or an interaction to the Eye ciphertext. These code checks only reject a
current runtime trigger; they do not rule out a passive clue, a native-code
check outside the retrieved functions, or a decoder clue added after 1.0.

The retrieved public progress document and analytical notes do not name
Chaocipher, Solitaire, or Pontifex. This is a statement about the available
written record, not evidence that nobody tried them privately. Standard
Solitaire/Pontifex is structurally a poor match because an independent running
keystream does not naturally create the observed causal isomorphs and
reconvergences. The generalized Chaocipher test is reported in the structured
deck section above.

#### Developer-statement check

The oft-repeated line that Arvi said "the eye decorations do contain a message"
is a paraphrase, not a verbatim interview quote. In the official April 2021
Noita Summit Q&A, at about 53:42, Arvi jokes about a bungee jump, mayonnaise,
and getting a vision of "what the message is." His wording supports the modest
claim that there is a message, but supplies no cryptographic method or
authorship clue. The written follow-up question document contains no Eye
answer.

Petri remains a plausible but unconfirmed author. Nolla's 2019 AMA says Petri
and Olli broadly handled programming, and the renderer is native C++; a profile
of Petri also documents his lifelong performance of card magic. Those facts
make simple deck constructions worth testing, but neither proves he designed
the Eyes. The coincidence between an 83-symbol alphabet and Petri's reported
birth year 1983 is too unconstrained to use as a key.

### The `LUMIKKI` storage-word lead

The high 32 bits of the first stored 64-bit Eye block are exactly
`0xacf68674`. The community document calls this CRC-32b of `lumikki`, but the
standard reflected CRC-32/ISO-HDLC value is `0x5bfc21b9`. An independent
bit-level audit finds one exact mundane match: non-reflected CRC-32/BZIP2 of
UTF-8 lowercase `lumikki`. Common case, whitespace, null-termination, UTF-16/
UTF-32, other CRC-32 models, and standard digest chunks add no second match.
The number is real; its historical label was imprecise.

The first packed word is
`0xacf686745634505c`. Its base-seven rendering has a discarded zero padding
digit and 22 visible stored digits in `1..6` (five eyes plus line break). Base seven is forced by the six
stored states, so Snow White's seven dwarfs is a thematic association rather
than an additional numeric decode. White snow, red blood, and black ebony also
echo the alchemical white/red/black stages, but this was noticed after the hash
word and must be treated as post-hoc support only.

A calibration scan parsed 283 distinct 32-bit constants from the decompilation
and hashed 103,834 modern Finnish dictionary words with eight common CRC-32
models, optionally byte-reversed. It finds zero overlaps. `Lumikki` is a proper
name/title absent from that word list, so the scan neither reproduces nor
validates the original reverse lookup; its unknown search universe is the main
multiple-testing problem. No `lumikki` or Snow White string occurs in the
retrieved game data, and no retrieved engine, modding, or serialization source
shows CRC-32/BZIP2 as Noita's ordinary string hash.

The installed Windows executables now settle the runtime-hash alternative for
the current build. Steam build 17130612 contains a release `noita.exe` compiled
25 January 2025 and a developer executable compiled four minutes earlier. In
the release binary, `0xacf68674` occurs exactly once, at virtual address
`0x61edc9`, as the immediate high half written beside `0x5634505c` to create the
first Eye storage word. No CRC-32/BZIP2 polynomial, four-entry table prefix,
full table, `lumikki`, or `BZIP` string is present. The engine does contain one
CRC-32/ISO-HDLC implementation using the reflected polynomial `0xedb88320`.
All three of its direct call sites are contiguous in the PNG encoder and build
the `IHDR`, `IDAT`, and `IEND` chunk checksums. The developer executable has the
same PNG CRC routine, but none of the first twelve 32-bit Eye-word halves.

Thus the target is Eye payload data, not a second reference to a runtime hash,
and the CRC family Noita actually uses is the wrong one. This sharply demotes
the engine-string-hash hypothesis. It does not decide whether a developer chose
the half-word offline as an easter egg, nor does it calibrate the community's
reverse-lookup search space.

The external-source chronology is clean at the public boundary. J. A.
Hahnsson's Finnish `Lumikki` translation dates to 1876, and Project Gutenberg
made ebook 45046 public in 2014. The extracted story has 14,450 normalized
letters. Under letters-only and space-preserving normalizations it supplies
zero complete Eye message trees and zero first-family fingerprints. A scan of
1,940 fixed-start Cessation-style walks through that text has best Finnish
tetragram score `-13.0014`, versus `-8.9209` for held-in Finnish, with visibly
random previews. `LUMIKKI`, `SNOWWHITE`, and alchemical color-stage keyword
decks also stay at 81 instructions and at least 88 repeated-context misses.
The hash is therefore still an unexplained clue/easter egg, not a source, key,
or decryption under the tested literal mechanisms.

### Engine and archive audit

The Emerald Tablet directory links the decompiled C++ routine that renders the
messages. The function contains the nine ciphertexts as hardcoded 64-bit
chunks. It selects a message, walks the chunk vector backwards, divides each
number by 7, emits successive base-7 remainders minus one, reverses the string,
and calls the renderer. The least-significant base-7 digit is discarded
padding. All ordinary chunks are divisible by 7; apparent exceptions occur only
where Ghidra omitted a zero high word for shortened final chunks. Reconstructing
the high word as zero restores valid `0..5` streams and the published messages.
There is no encryption routine, plaintext buffer, or runtime key in this path.

The linked current-data repository spans 56 asset snapshots beginning 9
February 2021; its eye-related Lua only controls placement/visibility. The
early-access repository contains an early `data.wak` and unpacked assets but no
eye-message source or executable. These archives therefore cannot provide a
pre-cipher historical version. The result closes a datamining branch: the
payload is deliberately precomputed and hardcoded in engine code.

The installed January 2025 `data.wak` adds a stronger current-state audit. A
small reader validates its directory boundary and all 14,745 file extents, then
searches each file without allowing matches to cross file boundaries. It finds
no textual `lumikki`, Snow White, CRC-32/BZIP, Eye-message/glyph, Hermeticum,
Chaocipher, Solitaire, or Pontifex reference. Its 60 `eye`/`glyph` filenames are
ordinary enemies/items plus the known eye-related secrets. The five `eyespot`
entities are unambiguous in Lua: a nearby Evil Eye exposes them; simultaneous
extreme tripping spawns `book_s_a` through `book_s_e`. Those notes describe the
Sun-seed sequence and have no direct Eye-message handler.

Line-ending-normalized comparison with the complete March 2023 data tree gives
481 added, 225 changed, 237 removed, and 14,039 identical paths. A deliberately
broad filename filter for eyes, secrets, books, orbs, Cessation, cauldrons,
calendars, Void, music, Kantele/Ocarina, altars, Sampo, glyphs, and puzzles leaves
25 relevant additions and eight changes. The additions include the known
Cessation reward, Barren Temple puzzles, Leukaluu Kantele, and a wall-eye enemy.
The wall eye only fires projectiles and blinks randomly; the Evil Eye change
only keeps it inside the world; the Kantele change adds an entity tag; and the
remaining changes are ending fixes, damage balance, biome edges, or tablet-rain
rewards. No named later addition bridges to the Eye payload. This is a bounded
negative through January 2025, not an exclusion of a clue hidden in native code,
visual composition, or an innocuously named mechanic.

#### Native placement, overlap seed, and glyph assets

The installed release binary supplies an exact mechanism for the community's
special overlap seed. Eye placement initializes its RNG from
`world_seed XOR 0x0e4bc7e0`. At world seed `239847392` (`0x0e4bc7e0`) the XOR
is zero; Noita's RNG normalization maps that to its modulus `2147483647`, which
is a fixed point of the update. All five East messages therefore receive the
same coordinates, and the four West messages receive their corresponding
mirrored coordinates. This reproduces the seed independently documented by
Lymm's Binoculars and shows that the alignment is a real engine consequence,
not a coordinate-rounding coincidence.

Reconstructing the visible rows and unioning directions at each aligned cell
gives 411 East cells and 372 West cells. The five-layer East union contains
every nonempty direction subset, masks `1..31`; the four-layer West union
contains exactly `1..30`, as mask 31 is impossible without the missing fifth
layer. Direct base-32, A1Z26-like, packed five-bit, row-reversed, bit-reversed,
and direction-permuted readings are gibberish. Optimizing printable bytes over
the natural variants yields 118 of 256 bytes for East and 107 of 232 for West.
Under 1,000 within-layer position shuffles, East has median 117, range 109–130,
and upper-tail `p=0.4296`; West has median 113, range 104–126, and
`p=0.9950`. The composite therefore has no direct byte signal by this measure.

The same binary's renderer at virtual address `0x61e880` constructs exactly
five 11x7 one-colour bitmaps: centre, up, right, down, and left. Character value
5 is newline; there is no hidden sixth graphic. A vectorized archive scan then
tested every installed `.png` for an exact foreground mask at integer
nearest-neighbour scales 1 through 4, permitting arbitrary foreground colour
and arbitrary nonmatching background. It decoded all 9,028 real images and
found zero hits. The two remaining `.png` paths,
`data/biome_impl/spliced/boss_arena/1.png` and `5.png`, are identical two-byte
CR/LF placeholders rather than images. The negative is deliberately bounded:
it does not cover a rotated, redrawn, antialiased, partial, or procedural clue.

#### Cauldron Room sand “star field”

A recent Secrets Storehouse observation noted that the Cauldron Room's sand
resembles a star field and suggested it might carry information. The installed
archive identifies the visible pattern more narrowly. The material definition
for `sand_static` names `data/materials_gfx/earth.png` as its texture; it is not
a seed-generated pattern or a Cauldron-specific scene asset. The tile is a
48-by-45, two-colour PNG with 203 minority-colour pixels and SHA-256
`22d0ec83c6ea7d12778284f90413b8edc0abbf07fba623cb38fba55796db79ad`.
The archived early-access data and the current data tree contain byte-identical
copies. `earth_bright.png` and `earth_bright_red.png` use the exact same
203-pixel binary mask with different palettes.

The dimensions create a tempting numerical coincidence:

```text
48 * 45 = 2160 = 83 * 26 + 2.
```

This is not unique in the archive. Of 9,028 decodable PNGs, 14 have area 2,160
and all 14 are 48-by-45 files under `data/materials_gfx`; no other PNG lies
within two pixels of `83*26`. Thus 48-by-45 is a shared material-texture format,
not an Eye-specific dimension chosen only for `earth.png`.

The natural direct use was nevertheless tested. All eight image orientations
and the three boundary-padding splits (`0+2`, `1+1`, `2+0`) give 24 distinct
26-by-83 bit tables. Looking up each Eye trigram by its displayed row-pair
position and value, then scanning the same bounded 7/8-bit framings used for
the Meditation Chamber mask, produces no plaintext. The best alternating
result is mechanically dominated by 67 copies of byte `U`: sparse error bits
over `01010101`, not language. Against 2,000 global-alphabet permutations its
score has upper-tail `p=0.072964`. Static-only output has `p=0.298351`, and the
minimum selected foreground count has lower-tail `p=0.329335`.

Therefore the fixed texture and the `83*26+2` arithmetic are real, but the
texture is generic and its direct sieve reading is negative. It could only be
revived by an independent clue specifying a different use; arbitrary cropping
or remapping would be post-hoc.

#### Public-lead provenance checks

The January 2023 “Hidden Secret” email trail is not developer correspondence.
The preserved document describes unsolicited messages from an anonymous Gmail
account, and the sender explicitly wrote “I am not a Creator.” Its 3D/avarice
claims never supplied a reproducible transform or plaintext. It remains a
finite untrusted hypothesis, but cannot support claims about intended method or
developer statements.

A July 2026 proposal that the opening animation demonstrates the five Eye
directions is also rejected at the asset level. The installed intro frames
`01_00.png` through `01_07.png` contain only the outlined egg/creature shape;
they do not contain authored internal pupil marks. The apparent moving dots in
video frames are multiple background stars visible through the transparent
interior. Moreover, the proposed direction-to-digit permutation still produces
83 distinct trigram values spread over `0..124`, with 42 holes, rather than
explaining the exact contiguous `0..82` alphabet. This is a useful example of a
visual false positive, not an in-game key.

### Source-text fingerprinting

The first-family repeated-plaintext assumption was converted into an exact
literal-source fingerprint: the same 18-letter block at gaps 30 and 35, with
its inner nine letters repeated at gap 28. Seventeen English alchemy books from
Project Gutenberg contain 9,733,222 normalized letters and no complete joint
fingerprint (also none when normalized with spaces).

A larger crawl of 1,295 pages from the Alchemy Texts archive contains
119,979,237 normalized letters. Four letter-only joint hits survive, but all
are transcription/layout artifacts: one crosses a table of contents around
“ode of the second book,” and three overlap the repeated placeholder “in non
Latin alphabet.” Space-preserving normalization produces many common prose and
navigation phrases rather than a unique candidate. The archive therefore
contains no plausible exact crib under this test, though this exploratory
fingerprint is not a general exclusion of alchemical plaintext.

The all-Finnish Gutenberg census produces seven letters-only fingerprint hits,
all rotations of the repeated bibliography notation `Pipp. l. N:o` in book
53047. Its three space-preserving hits are rotations of the repeated joik line
`Ooppee Mikko Hetta` in book 57770. Manual inspection identifies both as
high-period reference/refrain artifacts rather than candidate prose. Together
with the zero complete trees above, this closes the public-domain Finnish
Gutenberg branch under the tested literal-source model.

Azazelin Tähti supplies a second bounded Finnish corpus outside Gutenberg. Its
public sitemap lists 112 occult/esoteric articles, including its Finnish
*Corpus Hermeticum* XIII and 2004/2006 Emerald Tablet translations. Filtering
to entries with sitemap `lastmod` no later than 15 October 2020 retains 100
articles; every page loaded. The letters-only pass covers 1,089,988 normalized
characters and 2,278 sentence/paragraph candidates in the Eye length range;
the space-preserving pass covers 1,242,004 and 2,194. Both produce zero exact
first-family fingerprints, zero full trees, and zero upper-24, deep-20,
nested-9, lower-6, or joined-root partials. Sitemap modification dates are only
a reproducible public-availability filter, not evidence of Noita's unknown
internal construction date. These results reject literal cutting from this
corpus, not transformed use of its vocabulary.

The current English `common.csv` from Noita's data archive was also scanned as
a possible built-in crib. It contains 3,413 localization rows. With letters
only, seven strings have one of the nine exact Eye-message lengths; with spaces
preserved, seven do. Neither normalization produces a single complete
first-family fingerprint. In particular, the 102-letter `bookdesc02` is only a
length match: it lacks the required nested repeats. The localization table
therefore supplies no exact literal-source candidate under this test. The
current `common.csv` and `common_dev.csv` have no Finnish-language column, so
the `Fi!` lead cannot be tested as an unpublished in-table localization.

Aki's active repository contains nine explicitly labeled sample Hermetic
passages used for cipher experiments. Seven currently have exactly the
corresponding Eye-message length; West 2 and East 3 differ by `+2` and `-2`.
Even the seven aligned lines fail a key-free necessary condition for a perfect
GAK: repeated plaintext `the` produces ciphertext pattern `...` in 23 places
but `A.A` at West 3 position 76. Perfect isomorphism requires the equality
pattern of every repeated plaintext sequence to be invariant under starting
state. The sample is therefore not a candidate solution under the leading
model. A reusable checker now applies this test to future cribs before any key
search.

The untested source gap is concrete. The Finnish *Corpus Hermeticum* was
published on 26 March 2020 (ISBN 9789518995268), translated by Sampsa Kiianmaa,
H. M. Lampikoski, and Pentti Tuominen, and catalogued as based on Copenhaver's
1992 and Mead's 1906 editions. No lawful searchable full text was found. Every
exact ISBN record found labels it `nidottu`, `pehmeäkantinen`, or paperback.
Exact-title and ISBN searches of the publisher/society shop and major Finnish
ebook channels found no authorized PDF or EPUB edition as of 21 July 2026; the
society's separate ebook page does not list it, while its store calls this
edition a 224-page paperback.

#### Source chronology

The chronology preserves this lead, but does not strengthen it cryptographically:

- the Finnish translation's retail release date is 26 March 2020;
- Noita 1.0 shipped on 15 October 2020, with the official notes advertising
  new secrets;
- the community-maintained Eye Glyph Timeline dates the first recorded Eye
  post in the Noita Discord to 18 October 2020;
- the specialist Puzzling Stack Exchange summary independently says the puzzle
  was added in October 2020, and a contemporary 21 October Reddit discussion
  describes it as added in 1.0.

The book therefore predates the 1.0 release by 203 days and the first recorded
sighting by 206 days. No pre-26-March sighting, screenshot, asset, or community
discussion has been found. The cipher's actual internal construction date is
unknown, however. For a borrowed external text, the correct necessary condition
is that the text existed before the developers used it to construct the cipher;
public Eye release dates cannot establish that. Conversely, a developer-created
idea may have existed internally long before its public implementation, and a
decoder clue may be added to the game after the ciphertext. The evidence here
is therefore only “not ruled out by known public dates.” Fingerprinting a
physical copy remains a valuable finite check, but is deferred while stronger
source-independent leads remain.

#### Comparison with the solved Cessation cipher

The Cessation cipher, added with Epilogue 2 in April 2024, is a confirmed Noita
construction with two potentially relevant motifs. Its six spatial fragments
are merged along exact shared strings, and its six glyph values are forward
skip distances through a cyclic binary key; zero and line boundaries reset the
pointer. The key is supplied independently by the Void-Liquid calendar. This
public date does not prove when the developers first conceived the mechanism,
so it cannot by itself exclude Cessation-like construction vocabulary from the
Eyes. More importantly, a 2024 addition could deliberately supply a decoder
clue for a 2020 ciphertext. What the public evidence does establish is later
Noita puzzle vocabulary: visual values, external keys, exact fragment merging,
and a small deterministic state walk.

The direct analogues are negative:

- The explicit Cessation calendar key was tested against raw Eye directions and
  accepted trigrams under all direction-to-skip assignments, eight decoded
  message orders, message-reset and continuous state, four key
  orientation/complement choices, both bit orders, and all byte phases: 139,008
  byte interpretations. The best has only 200/387 printable bytes (`51.7%`) and
  is visibly random; natural ASCII would be almost entirely printable.
- Treating the five directions as skips through the 26-letter Noita keyed
  alphabet, the 29-letter Finnish alphabet, ASCII+32, or the 114-position disk
  ring also fails. The scan includes both ring directions, marker-present and
  body-only streams, trigram skips, and DFS/BFS serializations that emit every
  marker-free prefix-trie edge once. Under the Cessation start convention the
  best Finnish tetragram score is `-16.1854`, versus `-14.4181` for a raw
  held-in corpus slice, and all previews are gibberish.
- A related absolute-position reading takes successive Eye trigrams as cursor
  positions, so their affine-ordered differences become skips through the
  Noita or Finnish alphabet. All 54,448 affine, offset, direction, and marker
  variants bottom out at `-16.0158`, versus `-10.9991` for held-in Finnish.
- Assigning the solved plaintext `SEEKING TRUTH, THE WISE FIND INSTEAD ITS
  PROFOUND ABSENCE` as the common Eye prefix at depths `2/24/5/9/20` is rejected
  without choosing a key. Its repeated `NGTRU` at offset five has ciphertext
  pattern `.....` in the upper branch but `A...A` in the lower branch, violating
  perfect isomorphism.

Thus Cessation supplies a sensible construction family but neither its key,
its plaintext, nor the literal skip-key mechanism solves the Eyes. The broader
lesson—look for a separate in-world key and deduplicate exact fragments before
decoding—remains live.

### Practice-cipher checkpoint and a fresh Eye attack

The five numbered sdlwdr exercises now have one method-centered record each.
Numbers 1, 2, and 5 are solved; number 3 remains unresolved after an exact
single-`C83` progression exclusion; number 4 remains unresolved after its outer
cyclic layer was recovered.  Cipher 4's standard mod-83 adjacent differences
expose exact common blocks up to 200 symbols, but calibrated English/Finnish
homophone solvers, Wadsworth wheels, adaptive 57-card alphabets, Chaocipher
variants, exact source compatibility, and reuse of the Eye corpus all fail.
This is a useful failure: it demonstrates that exact shared structure can
prove an outer group action while leaving a separate inner codec unknown.

The most direct transfer back to the Eyes starts from their absolute no-double
rule.  Every adjacent difference is nonzero modulo 83, hence lies in the cyclic
multiplicative group `F_83*` of order 82.  This gives a finite analogue of the
82-position Wadsworth cycles that solve practice ciphers 1 and 2.  The new scan
orders differences by all 40 primitive roots, tests four direct/accumulated
logarithm and logarithmic-distance readings on every plaintext modulus 26..42
in both directions, and exactly optimizes independent per-message phases
against 234 published repeat-context comparisons: 5,440 candidates total.

The best candidate still misses 190 of 234 equalities; the best at the
practice-motivated modulus 42 misses 198.  Its visible outputs are gibberish.
A correct same-plaintext cycle model should be close to zero, not merely beat
random by a few dozen votes.  The complete multiplicative-difference/Wadsworth
family is therefore rejected.  This was the requested fresh pure-cryptographic
attempt, and it failed cleanly without inventing a plaintext.

### Gate Guardian ground-up audit

The July 2026 cyclical-sieve dossier was read in full and then rebuilt from the
installed game data rather than accepted as a package.  The strongest direct
facts survive:

- the checksum grid is `0,84,7 / 53,0,1 / 32,88,0`; main-diagonal circular
  reflection magnitudes are `31,25,14`, totaling 70;
- the exact independent uniform fixed-axis probability is about 1.459%;
- the three claimed Q-C edges are literal carry-free third-eye `+1` transitions,
  although the complete corpus has seven such adjacent transitions;
- Veska has exactly 72 pixels of one authored dark-mark color, with plausible
  9-pixel `1,5,3` and 8-pixel `plus+3` pictograms;
- Molari and horizontally mirrored Mokke have opaque silhouettes differing at
  only one pixel.

The source reconstruction also exposes the selection gaps.  A simple spatial
partition of Veska gives `11 remainder + 44 middle + 9 upper + 8 lower`, so the
claimed `12+43+9+8` needs an extra one-pixel reclassification rule.  No natural
Seula vertical-mirror mask produces 70: per-color half-residuals are
`411,4,302,109`, all-RGBA is 480, and alpha is zero.  The dossier does not
publish the residual or seven-pixel side-band masks.

All four sprites tile by their dimensions into the original `126×121` gate,
with Seula above, Molari/Mokke at the sides, and Veska central.  The actual Lua
activation rule is three eggs.  The XML spawner executes Veska, Molari, Mokke,
Seula at frames `220,225,230,235`; deaths use card-drop seed offsets `0,1,2,3`.
There is no Type4/Type6, cache, or Eye dataflow in Gate-specific Lua/XML, and
the executables contain the four names only in their enemy/progress registry.

The dossier itself concedes that its full interval update and direct Boolean
application are negative and that eight first-seen Type6 values remain
unexplained.  The defensible status is therefore “possible later visual
construction clue,” not “executable decoder.”  The complete source-backed
audit and derived assembly are in `docs/gate-guardian-audit.md` and
`artifacts/gate-guardian/assembled-static.png`.

### July 2026 Discord delta audit

A read-only sweep of the current `silmä-cryptography` and `silmä-novel`
discussions was compared against this log before promoting any lead.  The
channel's new cipher-hierarchy diagram mostly confirms work already recorded
here: arbitrary `A83`/`S83` deck/GAK remains the hard residual family, while
cyclic, dihedral, and affine transitive actions are excluded.  Our exact
certificates are stronger than the linked public wiki, which still describes
the two affine cases as incompletely excluded.

The genuine additions are narrower:

- `XGAK` generalizes GAK by giving each plaintext symbol both a fixed deck
  permutation and a fixed output position.  It is the last currently known
  class inside the perfectly-isomorphic region.  No perfectly-isomorphic
  cipher outside XGAK is presently known, but the converse has not been
  proved.  This enlarges the residual hypothesis space; it does not supply a
  key or a finite attack.
- The current discussion distinguishes perfect isomorphism from word- or
  phrase-level mechanisms.  Word-boundary rules or rare state resets could
  break perfect isomorphism while retaining the long observed repeats.  This
  imperfectly-isomorphic region remains under-classified and should not be
  dismissed merely because a simple Chaocipher configuration lacks systematic
  isomorphs.
- A concrete proposed extension lets the state update depend on a rolling
  plaintext window, analogous to a higher-order hidden-state model.  The
  specific two-symbol memory was introduced by Qualia as a deliberately
  artificial counterexample: a flag raised by plaintext `A`, retained for two
  outputs, and used to choose an inverse permutation.  It was not inferred
  from nearby Eye isomorphs and is not an independent Eye-derived bound.  It
  remains useful as a falsifiable example of how offset isomorphs can arise.
- XGAK can resynchronize more easily than ordinary GAK.  Long repeats should
  still normally reflect common plaintext, but limited differences may occur
  off the repeatedly constrained “backbone” positions.  Crib rejection should
  therefore report whether it assumes exact GAK, XGAK, or only an equality-
  pattern witness.

The `silmä-novel` pins are dominated by a January 2023 fan ARG that the channel
itself labels a hoax/legacy material.  Its fresh-save, three-plane, avarice,
cauldron, and email claims are not evidence about the developer-made Eye
cipher.  Recent material/alchemy-as-shuffle suggestions are presently ideas
without a mapping.  Neither category is promoted into the active lead list.

### Waite's message-3 suffix

One current Discord crib is materially stronger than the unsupported novel
ideas.  Waite's 1893 translation of *A Demonstration of Nature* contains the
81-character sentence (preserving spaces and punctuation):

```text
SUBLIME THAT WHICH IS THE LOWEST, AND MAKE THAT WHICH IS THE HIGHEST, THE LOWEST.
```

East 2 has 118 ciphertext symbols.  Starting the sentence at raw offset 37
fills the message exactly and places `THAT WHICH` at raw offsets 45 and 80,
the two known isomorph occurrences.  An exhaustive internal necessary-condition
check finds no perfect-isomorphism conflict among any equal plaintext
substrings of length at least two.  After eliminating nested copies that can be
extended left, the longest repeated pair is the 20-character
`E THAT WHICH IS THE ` at suffix offsets 6 and 41; its ciphertext gap patterns
are exactly equal.  The repeated ` THE LOWEST` pair, length 11, also has equal
all-distinct patterns, which is compatible but carries little information.

There is independent construction chronology.  Both the archived early-access
and current installed `scripts/biomes/orbrooms/orb_plan.txt` are byte-identical
(SHA-256 `9e3d741bbe350477e1939e6391599f79e218661a286a5073d6c2ebc78130df47`)
and explicitly mark several orb-text sources `[Hermetic Museum]`.  Waite's
*A Demonstration of Nature* is one tract in that work.  Thus the source family
was demonstrably in the developers' pre-1.0 vocabulary; it is not a later
translation introduced after the Eyes were constructed.

This remains a crib rather than plaintext.  It was found to fit an already
known isomorph, the exact 81-character endpoint was selected retrospectively,
and compatibility leaves arbitrary GAK/XGAK operations unconstrained.  The
next useful test is held-out prediction from one common state model, not more
semantic continuation.  Reproduction is in
`scripts/check_waite_m3_suffix.py`; the full queue is in `docs/open-leads.md`.

The full two-volume OCR gives a stronger finite source test.  It contains five
`THAT WHICH` pairs at the East-1 gap 28, four at the West-1 gap 30,
and two at the East-2 gap 35.  Complete source windows aligned to the observed
raw offsets leave 3/5, 3/4, and 1/2 internally compatible candidates,
respectively; the proposed `LOWEST/HIGHEST` sentence is the sole surviving
gap-35 window.  Treating symbol zero as either a marker or plaintext does not
change the candidate census.

The three messages cannot all be those contiguous source excerpts under a
perfectly isomorphic cipher.  Cross-comparing every equal maximal substring in
every combination leaves zero joint-compatible triples.  The best triple has
8 conflicts among 186 cross-message checks after excluding the probable check
markers.  This rejects the complete-excerpt hypothesis under exact GAK/XGAK,
not the narrower `THAT WHICH` or East-2 suffix crib.  Reproduction is in
`scripts/search_waite_that_which.py` using the Internet Archive OCR files.

The direct Noita provenance is also narrower than “same tract.”  The planning
file's identifiable excerpts map to *The Golden Tract* (`hm104`), *An Open
Entrance* (`hm206`), and *A Subtle Allegory* (`hm207`).  Neither the title *A
Demonstration of Nature* nor its `SUBLIME` sentence occurs in the extracted
game data.  The evidence is therefore anthology-level developer familiarity,
not proof that `hm107` itself was selected for the Eyes.

The archive chronology has one caveat.  `defektu/noita-early-access-data`
identifies its snapshot as “Early Access Data,” but its single Git commit was
uploaded on 2 October 2022.  The byte-identical early/current file is strong
archival support for pre-1.0 source familiarity, not an independently
timestamped 2020 artifact.

The first finite construction test is negative.  Taking the 117 source
characters aligned to the East-2 body, a complete scan covers 8,598 unique
standard 83-card bases and 26 operations per base: top swap alone, one anchor
rule, and ring/mirror plaintext-selected hidden swaps with offsets 1..12.
None of 223,548 reset-deck models has an injective decoded-symbol-to-character
mapping.  The best incurs 564 equality-relation conflicts and fails 517 of the
candidate's 542 required same-character pairs.  This decisively rejects that
finite physical-deck family for the contiguous body candidate.  A free
one-hidden-transposition-per-character SMT model is not thereby rejected: it
returns `unknown` after 30 seconds at both 30 and 117 characters.  Reproduction
is in `scripts/search_waite_sparse_decks.py`.

The six-window propagation has now been closed exactly.  The equality patterns
of all six windows are identical for lengths 1 through 10.  At length 11 they
split into two classes: East 1 is `A.B.CB.AC..`; West 1 and East 2 are
`ABC.DC.AD.B`.  The three within-message pairs continue much farther—rightward
lengths `19,26,26`, with maximal `(left,right)` contexts `(7,19)`, `(7,26)`,
and `(6,26)`—but those are three different cross-message classes.  Under exact
GAK/XGAK, one common plaintext at all six positions therefore stops after ten
characters.  `THAT WHICH IS THE ` cannot be the shared 18-character phrase,
although it remains compatible with the two East-2 occurrences alone.

A source-only fingerprint points in the same direction with an informative
tension.  At length 10, eight sliding strings recur somewhere in both Waite
volumes at every one of gaps `28,30,35`; they reduce to two phrase families,
`THAT WHICH` and `THE SPIRIT`.  Extending without reference to the ciphertext
leaves one unique maximal string at length 15: ` THAT WHICH IS `.  Thus the
three gaps genuinely select the proposed Waite phrase family, but the Eye
ciphertext itself rejects the common `IS ` continuation under perfect
isomorphism.  Reproduction is in `scripts/classify_that_which_windows.py` and
`scripts/search_waite_that_which.py`.

A small matched-corpus calibration supports retaining this source fingerprint.
Seventeen Project Gutenberg files from the alchemy subject corpus were given
the identical normalization and fixed-gap test.  Their longest all-three-gap
strings range from 5 to 12 characters; none reaches Waite's 15.  To reduce the
large text-size difference, the normalized controls were joined with unique
single-character boundary separators and partitioned into nine non-overlapping
blocks of exactly Waite's 1,318,231 normalized characters.  Those blocks range
from length 8 to 12, again 0/9 at length 15.  Formatting artefacts such as
`[SIDENOTE:` and table bars actually produce several control maxima, making
this a conservative text-cleaning comparison.

This is not a valid tail probability for discovering the crib.  The source,
three gaps, ten-character starting length, and control collection are all
post-selection choices, and several Gutenberg files are alternate editions of
the same work.  The result says only that ` THAT WHICH IS ` is exceptional in
the available size-matched alchemical prose, not that it is Eye plaintext.
Reproduction is in `scripts/calibrate_waite_gap_fingerprint.py`.

The proposed rolling-plaintext-window extension has now received a bounded
corpus test.  Its two-symbol length was selected from Qualia's artificial
counterexample, not from held-out Eye evidence.  A deterministic update that
depends on the current plaintext and its two predecessors need not make the
first two outputs of two repeated phrases isomorphic.  After trimming those
two outputs, the six first-family
windows at raw `40/68`, `40/70`, and `45/80` remain in one isomorphism class
through raw end 17; at end 18 they split.  Thus the 17-character plaintext
`THAT WHICH IS THE` is compatible with a two-symbol-memory construction even
though perfect GAK/XGAK rejects its common continuation after ten characters.

The extension is modest evidence, not a decode.  A null that freezes the six
observed ten-symbol isomorphs and independently draws later values subject to
the corpus's no-adjacent-double rule reaches a seven-symbol extension in
`2,634/200,000 = 1.317%` seeded trials.  Because the windows and trim were
selected retrospectively, this is a conditioned diagnostic rather than a
discovery p-value.  A scan of all repeat-rich equality-pattern groups with at
least three occurrences, at least two repeated labels, and seed lengths 6–14
finds no independent replication.  Every positive trim-two gain is a shifted
or nested view of the same six passages; independent groups have zero gain.
The result promotes two-symbol memory from a verbal possibility to a precise
compatibility constraint, but it does not independently support that memory
length and leaves the model below a held-out key prediction.  Reproduction is in
`scripts/test_two_symbol_memory.py` and
`scripts/analyze_delayed_isomorph_groups.py`.

The same read-only discussion supplied a stronger attack lead later on 21 July
2026.  Henry reported a handwritten CNF encoding for known plaintext and
ciphertext that lets Kissat reconstruct an initial deck and the
plaintext-selected shuffle permutations.  The toy cases reportedly reproduce
their generators.  The author cautioned that many shuffle orders explain
short texts and that the constraint count grows cubically with the ciphertext
alphabet.  A later explanation represents each operation and deck state as a
Boolean permutation matrix, composes them by matrix multiplication, and
asserts the observed top-card entry; no code link was visible at the time of
the observation.

The core method has now been independently reproduced in
`src/eye_mystery/arbitrary_gak_sat.py`.  Rather than materializing cubic Boolean
matrix products, it represents positions as finite-width bit-vectors and uses
conditional multiplexers for
`new_deck[i] = old_deck[operation[plaintext][i]]`.  Non-top position relabelling
is removed by choosing a canonical reset deck for a fixed initial top card.
Every accepted model is converted back to concrete permutations and required
to re-encrypt the complete known-plaintext corpus exactly.

On a deterministic binary-plaintext calibration with three 18-symbol messages
(54 known bits), arbitrary decks of sizes 5, 6, 8, 10, 12, and 14 return `sat`
inside a 30-second bound and replay every emission.  Sizes 16, 18, and 26
return `unknown` under the same bound.  The solver often recovers a witness
different from the generator key, directly confirming the underdetermination
warning.  This is an independent method reproduction and a measured scaling
boundary, not plaintext recovery and not an Eye result.

Qualia's new `2-to-26 deck cipher` attachment is archived at
`artifacts/practice-ciphers/deck_cipher_binary_stripped.json` (3,221 bytes,
SHA-256
`1f0f10ffc3999fe4c470a87af296f22bebcb5e9b8772e7d4e20060db4cbd95d4`).
It contains nine ciphertexts of lengths 291–422.  Their binary plaintext and
the serialization of the stated 27-symbol English alphabet are not supplied,
so the known-plaintext solver cannot honestly be applied yet.  This puzzle and
Torben's earlier large-group known-plaintext GAK exercise remain a natural
small-to-`S83` calibration ladder before any Waite crib feasibility test.

Henry's code was published minutes later at
`CyclohexAnon/noita_deck_cipher_sat`, commit
`7acc7eedf025aa65b40e60d93d437d1dad492b58`.  A clean temporary build of
Kissat 4.0.4 (`8af8e56f174b778aef3aa45af9f739b2a5f492c2`) reproduces the committed
six-card toy: 648 Boolean variables, 6,319 clauses, `SATISFIABLE`, a recovered
four-operation table different from the generator table, and exact decryption
of all 13 supplied characters.  The local bit-vector solver independently
recovers another witness for the same public plaintext/ciphertext pair and
replays it exactly.

The code audit sharpens the scope.  Its update orientation agrees with the
ordinary convention `new_deck[i] = old_deck[operation[i]]`.  The one-way
product clauses are logically sufficient because the input, operation, and
output matrices are all permutations: every true product cell forces the
unique true output cell in its row.  The script assumes an identity reset deck
and does not include the `(0,0)=0` operation clauses described in chat.  The
latter omission does not invalidate the published toy; it merely means the
committed model itself does not enforce no adjacent ciphertext doubles.
Together with the size-16/18/26 timeouts, this closes the present bounded SAT
experiment as a verified primitive rather than an Eye-scale attack.

## Breadth-first synthesis and S3 header audit

A deliberate wide pass suspended the prose, one-symbol-per-character,
independent-message, 83-state, English/Finnish, and contemporaneous-clue
assumptions before selecting another deep attack.  Twenty mechanism families
and cheap discriminators are frozen in
`docs/novel-synthesis-2026-07-21.md`.  The first probes reject several literal
versions without discarding their broader families: the nine bodies are not
all rows of one BWT rotation matrix; none of 720 natural trigram alphabet
orders sorts them in the marker-derived trie order; no 26-wide row is a
26-symbol permutation; a literal eight-entry LRU cache covers only 105 of 469
repeat events; and an affine mod-101 cumulative walk does not collapse the
bodies to a small state set.

The pass also found a new exact header organization.  Read a marker's first
two digits as the already established edge `middle -> first-1`, then name a
component order `(source,target,remaining)`.  The first six canonical panels
enumerate all six elements of `S3`: the first row is the even subgroup `A3`
and the second row is the odd coset.  The final row is identity plus the two
standard adjacent generators.  Directly permuting every body trigram by its
own header destroys the copied prefixes and expands the alphabet from 83 to
117, so it is not a per-panel component unscrambler.

At the exact even/odd row boundary, a retrospective body construction
nonetheless reproduces every digit of the independent marker-BWT result.
Reverse the universal two-symbol root under East 2's component order and append
the first West 2 symbol after its row's length-five prefix under West 2's
order: `010,231,234 -> 001,123,243`, or values `1,38,73 = !Fi`.  It is unique
among the nine frozen even-header/odd-exit pairs, but the target and several
construction choices were inspected first, so it is not a p-value or decode.

The most natural held-out prediction fails decisively.  If final-row headers
`E4=e`, `W4=(12)`, and `E5=(01)` name the strong East 4→West 4 and East 4→East
5 body-context permutations `B` and `A`, then `A^2=B^2=e` and `ABA=BAB`.
The partial observations force seven nonidentity edges of `A^2`, eight of
`B^2`, and the braid conflict `ABA(31)=41` versus `BAB(31)=69`.  No full
permutation completion can fix them.  This rejects the direct header-to-body
Coxeter action while retaining the objectively clean header organization as a
possible global construction/check clue.  Reproduction is in
`scripts/analyze_conformance_grid.py` and
`scripts/test_s3_context_relations.py`.

A second low-capacity `S3` use is also negative after calibration.  Exhausting
all 4,320 injective mappings of the five raw directions into `S3`, together
with all fixed eye orders, finds one unique model whose body products carry
the encoded header source to target for eight of nine panels.  It fits every
non-self edge and fails only East 4.  However, an exact intact-body reassignment
null finds at least an eight-edge optimum for 356,904 of all 362,880 body/header
assignments (`98.353%`) and a perfect nine-edge optimum for 74,436 (`20.512%`).
The observed near-fit therefore has no useful association evidence.  This
illustrates why unique best models inside a flexible finite scan still need a
matched outer calibration.  Reproduction is in
`scripts/analyze_s3_direction_transducer.py`.

The pre-registered prefix-trie payload probe is positive.  Removing the nine
established markers, merging their copied body prefixes, and emitting every
distinct trie edge exactly once gives 918 values totaling
`37,774 = 374 * 101`.  This multiset is invariant to depth/breadth traversal
and sibling order.  Keeping markers gives residue 63; starts 2 and 3 give 35
and 30; the reversed/suffix trie gives 92; and the raw-direction trie after its
three-digit markers gives 23.  None of the three natural row-family tries or
nine leave-one-panel-out tries closes.  Scanning all common starts finds one
other zero at offset 41, which is a post-hoc expected-scale hit; offset 1 is
independently selected as the marker/body boundary.

The closure is not a symbolic consequence of the earlier message checks.  The
nine complete message label-count vectors have rank 9 over `F101`; adding the
deduplicated trie-edge count vector raises the rank to 10.  Under all 6,806
affine permutations of `0..82`, 71 retain zero (`1.043%`), and only identity
does among the 83 additive translations.  A seeded 200,000-sample arbitrary
global permutation control, preserving the exact equality skeleton and trie
topology, closes 1,895 times (`0.9475%`).  These are not conditional discovery
p-values because they do not preserve the three diagonal zero sums and the
modulus was already selected.

An exact matched subgroup now conditions those checks.  Partition the 83
labels by their three occurrence counts in the complete East 1, East 3, and
East 5 streams.  Arbitrary permutations within each class preserve every
diagonal sum exactly and preserve the full equality trie.  Convolving the
small within-class residue histograms counts all
132,090,377,011,200 relabelings: 1,307,844,501,760 close (`0.990113%`).  If all
nine visible marker labels are additionally frozen, 8,174,134,656 of
825,564,856,320 close (`0.990126%`).  The residue distribution is nearly
uniform, so the known diagonal checks do not explain the trie zero within this
large exact subgroup.  This remains a post-result conditional universe rather
than a universal discovery p-value.

This is the strongest new mechanical lead from the wide pass because its exact
statistic—serialize each distinct trie edge once and test checksums—was frozen
before evaluation.  It suggests that the copied prefixes may be a merge/sieve
instruction rather than repeated prose.  It does not yet decode anything.
Reproduction is in `scripts/analyze_trie_checksum.py`.

At the five documented internal branch nodes, summing every distinct edge
strictly below the shared prefix gives residues `30,19,70,89,13` in canonical
cluster order.  The lower six messages after their length-five prefix are the
unique 70.  This retrospectively equals the main-diagonal mirror-difference
total in the mod-101 grid.  It does not repair the Gate asset claim: both
quantities are Eye-derived, while direct Seula sprite masks still produce no
70-pixel residual without an unpublished extra mask.  The match is retained as
an internal echo and explicitly not counted as independent corroboration.

The defensible Gate `9|8=17` pictograms motivate one additional exploratory
factor test.  The deduplicated trie has `918=54*17` edges and total
`37,774=22*17*101`.  In the exact diagonal-check-preserving subgroup, total
divisibility by `17*101` holds for 125,161,099,264 of
132,090,377,011,200 relabelings (`0.094754%`); with all marker labels fixed it
holds for 830,894,368 of 825,564,856,320 (`0.100646%`).  The factor was noticed
after the trie total and the null fixes the edge count, so these are not
discovery p-values.

The first concrete 17-role construction is rejected.  Four independently
available sibling orders—canonical, East-5-first trail, marker-trie, and
marker-LF—were serialized under DFS and BFS, then partitioned both into 17
consecutive 54-edge blocks and 17 position-mod-17 lanes.  No record has sum
2,222, no consecutive block closes modulo 101, and only one of 136 cyclic
lanes closes.  The arithmetic factor and later Gate selector stay logged, but
they do not yet define a trie traversal, partition, or plaintext.

A more coherent `Z101` architecture follows from three exact counts.  The
visible labels `0..82` leave 18 missing values `83..100`.  The compressed
nine-leaf prefix trie has five branch nodes and thirteen outgoing compressed
edges, also 18.  Those missing values total 1,647, or residue 31; the lower-six
descendant trie uniquely has residue 70, so adding the complete missing range
closes modulo 101.  This offers a literal but unproven parse of the earlier
breadth-first depth output `BEXIT` as branch nodes plus exits.

The joint condition is not explained by the diagonal checks.  Exact bivariate
convolution over the diagonal-check-preserving subgroup gives
12,948,675,076 of 132,090,377,011,200 relabelings (`0.0098029%`) with both the
full trie at zero and the lower descendants at 70.  Freezing all nine marker
labels gives 80,918,060 of 825,564,856,320 (`0.0098015%`).  The four eligible
proper branch nodes each have an almost identical joint rate; summing them
gives a conservative post-hoc union bound of `0.03922%`.  The all-nine node is
linearly tied to the full checksum and cannot hit 70 when it closes.

This is exploratory evidence, because the 18-record interpretation and branch
target were formulated after inspecting the closure.  It is not operational:
no rule assigns the values `83..100` to the five nodes and thirteen exits.
Brute-forcing that 18! bijection against language would be unconstrained.  The
lead should be promoted only by an independent in-game ordering/typing clue or
a key-free body prediction.  Exact reproduction is included in
`scripts/analyze_trie_checksum.py`.

### Wide architecture controls and the procedural-wand selector

A second breadth-first pass was frozen before evaluation in
`docs/wide-approach-map-2026-07-21.md`. Three unrelated literal architectures
are clean negatives. The best order-two base-5 overlap has 52/1,018 matches,
ordinary under 5,000 body-multiset-preserving shuffles
(`1360/5001` upper-tail). After the longest row-prefix boundary, the natural
3×3 aligned body grid has only 1/74 zero determinants under both `F83` and
`F101`, ordinary under 5,000 independent message rotations. Low-degree
polynomial body moments predict no headers beyond the already-known East
1/East 3/East 5 negative-sum checks modulo 101.

One initially promising finite-field result was a null-model artifact. The
best shared rule `next=17*current+45 mod 83` matches 34/1,018 transitions and
beats a naive within-message shuffle at `2/201`. Those shuffles destroy the
exact copied prefix transitions. Arbitrary global relabeling preserves the
complete equality trie and every transition multiplicity; 219 of 500 such
controls meet or beat 34 (`220/501 = 0.439122` with the finite-sample
correction). Counting copied trie nodes once gives a different optimum of
26/917. There is no first-order affine recurrence lead.

The associated Discord correction did reveal one exact in-game identity worth
retaining. Both installed procedural-wand sources contain
`Random(0,100) < 83`, choosing `ACTION_TYPE_MODIFIER` rather than
`ACTION_TYPE_DRAW_MANY`. Noita's integer random bounds include 0 and 100, so
the successful set is literally `0..82`—the Eye alphabet—and the full domain
has 101 values—the checksum modulus. A complete direct-threshold inventory of
the current WAK finds 74 comparisons across 22 operator/threshold pairs; 83
appears only in these two duplicated copies. The loose early-access-labelled
tree has 25 comparisons across ten pairs and the same two copies.

Chronology limits the claim. The loose archive's sole commit was uploaded on
2 October 2022. The earliest independently timestamped occurrence in the
61-snapshot public data repository is commit `70696c9` on 9 February 2021.
This proves the rule existed after the October 2020 Eye release and is therefore
eligible as a later decoder clue. It does not independently prove pre-Eye
construction use. No renderer reference, prefix merge, missing-state
assignment, or 18-record order accompanies it.

The complementary branch initially appeared to supply a real second
correspondence.
The 18 rolls `83..100` all select `ACTION_TYPE_DRAW_MANY`, whereas `0..82`
select `ACTION_TYPE_MODIFIER`. Independently, the compressed Eye trie has five
branch nodes of degrees `(2,3,3,2,3)` and thirteen outgoing edges, so the
proposed hidden structure has exactly `5+13=18` branch instructions plus
continuations. The same source also contains the ordinary wand-capacity clamp
26 and the unshuffled-capacity limit 9, matching complete Eye row width and
panel count. This conjunction is retrospective and each constant has a
gameplay explanation, but the 83/18 type split is exact.

The actual gun runtime ultimately bounds rather than strengthens the analogy.
`draw_actions(n)`
executes children immediately and recursively, so its action stream is a
depth-first tree. The Eye degrees `(2,3,3,2,3)` are legal and yield nine leaves
by the exact tree identity `1+sum(d-1)=9`. All branch depths are below 26 and
their independently selected breadth order still spells `BEXIT`. But one
literal cast cannot emit the ciphertext trie: 26 card slots cannot account for
918 distinct payload edges. The next model must keep control topology and
payload representation separate, or it is rejected at the capacity bound.

A scope-consistency audit then demoted the structural interpretation. A real
tree with five internal nodes and nine leaves executes fourteen card nodes;
`5+13=18` counts the internal nodes and the thirteen relationships separately,
double-counting four non-root internal nodes relative to a card trace. The
checksum scopes also cross: the attractive `70+31=101` uses the lower-six
descendant payload, but that subtree owns only 11 hypothetical node-plus-edge
records. The whole tree owns 18 and has descendant residue 30, which does not
close with 31. Five unordered 11-value subsets happen to close the lower-six
residue, but neither the source nor corpus selects one. This rejects the
current local recursive-checksum/wand execution model while retaining the raw
83-of-101 selector as an unexplained later-clue candidate. Reproduction is in
`scripts/analyze_wand_selector.py` and the detailed audit is in
`docs/procedural-wand-architecture.md`.

Two further breadth controls are negative. Adjacent body trigrams change one,
two, and three base-five eye components `115,425,478` times. A global-label
relabeling null that preserves every equality and transition gives an
upper-tail `3713/5001 = 0.742451`, so the eye-component Hamming geometry is
ordinary. The first edge making each prefix-tree leaf unique gives lower-row
sums `69+78+23 = 77+60+33 = 170`, but exact relabelings preserving the three
diagonal checks and every marker retain equality at rate
`30,576,476,160/825,564,856,320 = 1/27`. This post-hoc branch summary is also
not promoted.

### Practice cipher 4: arbitrary cyclic recurrence, finite exclusions

The recovered standard `C83` layer supports a stronger attack than reading its
adjacent differences as monoalphabetic plaintext actions.  In oriented
coordinates an arbitrary cyclic group-autokey update has the necessary form

```text
p[i+1] = sign_c * delta[i] + q(p[i])  mod 83.
```

The reflected plaintext coordinate and the alternative next-symbol update
timing are included explicitly.  The update function `q` may otherwise be
arbitrary.  This turns a proposed source passage into a key-free consistency
test: two occurrences of the same selector symbol must require the same `q`
value.

The exact 200-transition block shared by portions 1 and 2 was scanned under
all eight orientation/timing conventions.  The source set comprises a large
English composite, Crawford's *Kalevala*, a separate Sherlock Holmes corpus,
Finnish *Seven Brothers*, Finnish *Kalevala*, and two further recovered
practice-source files.  It contains 3,743,827 letters-only characters and
4,557,173 space-preserving characters.  Compact-space and natural-42 space
positions were tested separately.  No window survives all 200 transitions;
the maximum consistent prefix is 19.  This is an exact exclusion of those
passages under this cyclic-GAK family, not a general exclusion of prose.

A second finite search exhausts every affine update
`p'=sign*delta+u*p+v mod 83` over the complete second portion.  There are no
survivors in either `A-Z` plus natural-position space or the contiguous
natural-42 alphabet.  The contiguous 57-state band has exactly two reflected
survivors, `p'=delta-22` and `p'=-delta-5`; both have `u=0`, discard their
arbitrary starting state immediately, and merely restate the known direct
rank reading.  General nonlinear `q` remains unresolved.  Reproduction is in
`scripts/scan_sdlwdr_cipher4_sources.py` and
`scripts/analyze_sdlwdr_cipher4_recurrence.py`.

### Practice cipher 4: calibrated case-sensitive bijection rejection

The exact `22..78` action span suggested a previously untested finite reading:
53 observed actions inside 57 positions might be an injective substitution of
a conventional case-sensitive alphabet (`A-Z`, `a-z`, space, and five ordinary
punctuation characters). Earlier attacks had case-folded the stream and forced
homophone allocations, so they did not cover this model.

A raw case/punctuation four-gram optimizer was tested on four frozen character
pools. For each pool, the same algorithm decoded a planted 1,304-character
control to 99.9233% accuracy, with best scores from `-10,984.01` to
`-11,097.55`. Real Cipher 4 runs remained between `-21,714.64` and
`-21,951.41`; independent seeds selected unrelated keys and produced only
isolated pseudo-words inside mixed-case gibberish. The score gap and instability
reject this conventional bijection family. They do not reject a second codec,
an unconventional alphabet, or non-prose plaintext.

The frozen protocol and full score table are in
`docs/practice-cipher4-case-bijection-2026-07-22.md`; reproduction is in
`scripts/solve_sdlwdr_cipher4_case_bijection.py`.

### Second wide fan-out and the exact 83-to-42 complement

A second deliberate breadth pass opened eighteen construction families before
deepening any of them.  Its central arithmetic observation is

```text
5^3 = 125 = 83 visible trigrams + 42 unused trigrams,
```

while reflection on the 83-cycle independently gives zero plus 41 signed
pairs, again 42 classes.  This is also the plaintext-wheel size used in the
solved sdlwdr practice ciphers, although that later community construction is
not evidence about Noita's developer key.

A targeted read-only Discord search corrects the initial novelty assessment.
The community explicitly noted [`83+42=125` in July
2023](https://discord.com/channels/453998283174576133/1063583558154854521/1128899292875198606),
proposed [pairing two ciphertext values per member of a 42-symbol alphabet in
January
2024](https://discord.com/channels/453998283174576133/817530812454010910/1192671913227583508),
and stated [both `42=(83+1)/2` and `42=5^3-83` in April
2024](https://discord.com/channels/453998283174576133/817530812454010910/1227134323140857926).
The count and generic pairing are therefore not new.  The local contribution
is the explicit reflection/log-quotient construction and the calibrated
negative results below.

The older scratch research was not silent either: its community-documents
digest explicitly recorded the contiguous 42 unused values `83..124`.
Failing to carry that observation into the maintained lead ledger caused the
mistaken novelty assessment.  The scratch `pairclass` campaign concerns the
four-class lossy surface of practice puzzle two; it is useful methodological
background, not a prior Eye-message 83-to-42 decoder.

Six unrelated cheap probes are negative.  Circular reflection centers,
no-repeat exclusion ranks split into 41 classes plus a bit, delayed component
tapes, arbitrary context functions through order four, header/length rules,
and the post-hoc `13x79` body layout are all ordinary under matched controls.
Merging copied prefixes once makes the label distribution more uniform
(entropy `6.267139 -> 6.289341`, normalized IoC `1.071586 -> 1.028964`), which
is compatible with a planted verification skeleton inside high-entropy cover
but supplies no decoder.

The post-hoc factor `918=34*27` initially survives.  Splitting the two fixed
marker-derived trie traversals into 34 records of width 27 gives selected
mod-101 closure counts three and four.  A strict sampler preserves all marker
labels and diagonal message count vectors and conditions on the known total
trie closure; only 35 of 5,000 accepted controls reach at least four, giving
`36/5001 = 0.00719856`.  But the record boundaries do not align with trie
returns, the zero rows have no common structural role, and allowing all 27
cyclic phases gives `106/1001 = 0.105894`.  The numeric curiosity is retained
without a record interpretation.

The second canonical 42-class ordering uses discrete logarithms on
`F83*/{+1,-1}`.  Exhausting 6,720 generator, center, and zero-placement models,
with field value 1 fixed at class zero, is language-negative: best
English/Finnish scores are `-16.94394/-16.08232`
per tetragram, far from held-in `-9.03528/-10.61812` and visually random.
Arbitrary class permutations are deliberately not searched.  Reproduction is
in `scripts/run_second_wide_probes.py`,
`scripts/calibrate_factored_34x27.py`, and
`scripts/search_reflection_quotient_logs.py`.

### Exact base-seven storage reconstruction

The serialization-side-channel lane is now bounded from primary packed data.
Start with the accepted visual rows, append renderer symbol `5` after every
row, translate storage symbols `0..5` to base-seven digits `1..6`, append one
zero padding digit, and greedily take the longest prefix whose resulting
integer fits in an unsigned 64-bit word.  This procedure derives all 150 engine
words exactly.  In little-endian message order their SHA-256 is
`5de6ccb3a045218827b7ddaad0f1493254f501b08addd1929495ce060242de94`, matching
the verified Xkeeper transcoder fixture; the first and last words are
`0xacf686745634505c` and `0x8c`.

The apparent boundary metadata is fully forced.  Of 141 nonfinal chunks, 112
have 22 symbols and 29 have 21; appending the next visible symbol to every one
would exceed `2^64-1`.  The nine final lengths are
`21,11,16,10,9,14,17,21,2`.  Chunk boundaries cross 69 newlines and end at only
16, excluding a hidden row-record convention.  Reading 21 versus 22 as a bit
and optimizing the natural reversal, inversion, bit-offset, and byte-order
conventions yields 8 printable bytes of 17.  Fixed-weight random bitstrings do
at least as well in `8258/10000` trials (corrected upper tail
`8259/10001 = 0.825817`).

Thus the u64 divisions, missing high words, and padding provide no independent
authored channel beyond the visible direction stream.  The capacity predicate
could still be recomputed as a derived nonlinear feature, but that weaker idea
now needs an external reason.  Reproduction is in
`scripts/analyze_storage_serialization.py` and
`src/eye_mystery/storage_serialization.py`.

### Snapshot alignment and a five-state equality tape

The predeclared snapshot/delta lane asks whether the prefix tree records
fixed-coordinate copies and replacements rather than repeated plaintext.  For
the two deepest sibling trios (`east1,west1,east2` and
`east4,west4,east5`), compare the cost of indexwise substitutions plus trailing
truncation with unrestricted unit-cost Levenshtein alignment.  The six savings
from allowing gaps are `0,7,1,2,2,0`, total 12.  In 2,000 controls, each leaf's
complete shared prefix and first unique exit remain fixed while the later
suffix is shuffled within that message.  Only five controls have total at
most 12, for corrected lower tail `6/2001 = 0.0029985`.

This is real evidence for fixed coordinate synchronization, not specifically
for construction snapshots.  The known later equality windows drive it, so a
position-synchronous cipher predicts the same result.  Nor does the signal
select the visual record width.  The 45 later aligned equality hits have
26-column chi-square `19.1333` (`0.839580` upper tail), and only two of 48
equality-run starts/ends lie within one cell of a row edge (`0.653673` upper
tail).  The fixed-coordinate constraint survives; a 26-column edit worksheet
does not.

This led to a deliberately strange representation test.  Three aligned values
have Bell number `B3=5` equality partitions: all equal, one of the three equal
pairs, or all distinct.  The two deepest sibling trios therefore produce two
independently selected five-state tapes of lengths 74 and 93 after their branch
points.  Treating a state as a base-five digit is negative: after searching all
120 state labels, common reversal, and trigram phase, zero values need exceed
82, but 493 of 500 state-count-preserving controls do at least as well
(`494/501 = 0.986028`).  The apparent range fit is a consequence of the
dominant all-distinct state.

Pairing the two tapes as row and column of a 5x5 Polybius alphabet is also
negative.  All `5!^2` row/column labels and independent reversals select score
`-12.65455` on the English model, with repetitive preview
`OTPOOOOOOOOOTOOODY...`.  Of 500 independently shuffled tape controls, 448
score at least as well, corrected upper tail `449/501 = 0.896208`.  Targeted
read-only Discord searches show that generic Polybius squares/cubes are old
ideas, while exact searches for `Bell number` and `five partitions` in the
cryptography and novel channels return none.  That does not establish global
novelty; it only preserves the provenance of this specific tested transform.

Reproduction is in `scripts/analyze_snapshot_delta.py` and
`scripts/search_partition_polybius.py`.  The durable new constraint is
position synchrony.  The five-state tape should not be fit further without an
external selector.

### Metadata-only `BEXIT` branch/exit identity

The metadata-only lane was frozen to objects already selected independently:
East 5 first from the marker trail, breadth-first branch order from the
`BEXIT` depth reading, distinct immediate outgoing trie labels, and modulus
101 from the message and merged-trie checks.  For the five records, the depths,
exit labels, raw exit sums, and depth-corrected residues are:

```text
depth  exits        exit sum  (sum + depth) mod 101
2      49,48          97              99
5      2,69,23        94              99
24     80,29,69      178               0
9      2,78           80              89
20     33,77,60      170              89
```

Thus the selected sequence is `99,99,0,89,89`: two equal pairs around a zero
center.  Expressed as three linear equations on the global label mapping, all
three add rank beyond the diagonal East 1/East 3/East 5 count vectors and the
full merged-trie count vector; the rank over `F101` rises from 4 to 7.

An exact cyclic-convolution calculation over the subgroup that preserves the
three diagonal sums and fixes all nine marker labels counts
`6,115,295,232 / 825,564,856,320 = 1/135` satisfying assignments.  Searching
the entire coefficient family `exit_sum + k*depth` for `k=0..100` does not
inflate this within that subgroup: coefficient one is the sole value with any
assignments.  A second seeded calibration samples 500,000 subgroup mappings
and accepts only the 5,008 that also preserve the known full-trie zero.  Of
those, 26 satisfy all three exit equations, for corrected conditional rate
`27/5009 = 0.0053903`.

This is a new check relation, not a solution and not a calibrated discovery
probability.  The node order and modulus were motivated in advance, while the
sum-plus-depth operator and paired-zero-paired target were recognized after
viewing the records.  Many metadata operations could have been tried.  The
identity earns a ledger entry because it is exact, independently ranked, and
strictly reproducible; promotion still requires a game-authored combine rule
or a held-out prediction.  Reproduction is in
`scripts/analyze_metadata_instruction.py`.

### Exact authored-table inventory and `gun_names`

The next wide cycle searched raw installed data for literal developer-authored
tables of the independently interesting sizes 5, 42, 83, and 101. A balanced
Lua scanner covers 1,077 files and finds table counts
`5:1011, 42:0, 83:4, 101:0`. All four 83 hits are equivalent copies of the
same `gun_names` array in `gun_procedural.lua`,
`gun_procedural_better.lua`, `gun_utilities.lua`, and `wand_petri.lua`. The
NUL-joined entries hash to
`9ef2ead9b050c32b8440930d4ff7480b1c77298f7758c162fca8e5e54daf94ae`.
At runtime a uniform `Random(1,#gun_names)` merely chooses a wand-name prefix.

XML and text inventories add no comparable table. Among 4,325 XML files, the
only 42-child element is the component root of `maggot_tiny.xml`; there are no
83/101 child lists. Nonblank CSV/TSV/TXT line counts contain none of 42, 83,
or 101. Three hundred and one XML files are not standalone-parseable, so this
is a scoped inventory, not a proof over arbitrary encodings.

The identical 83-name list occurs in the archive labelled early-access data,
which lacks the Eye payload strings, and its `gun_utilities.lua` is
byte-identical to the February 2021 public-data copy. This makes pre-Eye
availability plausible but not independently timestamped: the early-access
repository's one commit dates to 2 October 2022. The table would be eligible
as a later decoder clue in either case.

Discord provenance prevents a false novelty claim. Defektu noted the exact 83
names and `wand_petri` copy on 22 August 2022; sirreldar tried selecting letters
from the indexed adjectives in September 2024; sdlwdr revisited the list as a
possible ordering in May 2026. The new contribution is a bounded calibration.

Fifteen deterministic readings—first/last/middle/length, all three Eye digits
from either end, digit sum, and label modulo word length—were tested with both
marker policies. Shuffling whole names over labels and reselecting the entire
family gives corrected upper tail `316/2001 = 0.157921`; the selected output is
gibberish. A second method-transfer test alphabetizes the names into an
83-card initial deck and applies the exact recursive shuffle learned from
practice cipher #5. Its best result places `560/1027` body values in `0..41`,
also ordinary under shuffled-name controls (`240/2001 = 0.119940`).

The exact lookup remains an eligible clue only if another authored object
selects how to consume it. Arbitrary per-occurrence letter choice and
unrestricted name ordering are closed as unfalsifiable. Reproduction is in
`scripts/scan_game_authored_tables.py` and
`scripts/analyze_gun_names_selector.py`; the full audit is
`docs/game-authored-table-audit.md`.

### Fifth wide fan-out: six unrelated bounded mechanisms

The next breadth cycle froze six tests before results: directed graph edge
reuse, top-to-bottom visual-row local rules, direct base-83 radix packets,
stable-sort inversion traces, nonlinear digitwise 3×3 operations, and native
direction turtle drawings. Each control reruns the complete within-lane model
selection and preserves the specific nuisance structures documented in
`docs/fifth-wide-fanout-2026-07-21.md`.

Five primary results are negative. Directed-edge reuse is 175 of 1,018
transitions (`87/2001 = 0.043478` upper tail). The best direct radix packet is
reversed base 128 with `714/938` printable values
(`1668/2001 = 0.833583`). The best of eight digitwise `F5`/min/max grid
operators matches only 3 of 216 pairwise-distinct aligned positions
(`1895/2001 = 0.947026`). Native turtle paths have selected bounding-area sum
10,152 (`1053/2001 = 0.526237` lower). The stable-sort statistic reaches
`6743/12408 = 0.543440` under component order `(1,2,0)`, but a separate
10,000-control refinement gives `147/10001 = 0.014699`, above the frozen
promotion threshold.

The visual local-rule primary statistic initially crosses its threshold:
radius three and shift minus one fit `1292/1298` cells, with
`1/2001 = 0.000500` upper tail. It does not survive its required predictive
audit. The model uses 1,149 context rules, and leave-one-row-pair-out validation
covers only 232 of 1,298 cells. Dropping every first row pair removes all
complete pairs carrying the family-prefix copies. The capacity-controlled
radius-at-most-one result then becomes ordinary (`458/1133`,
`197/2001 = 0.098451`), while the radius-three model covers only 46 of 1,001
held-out cells (`36/46` correct). Its remaining coverage is concentrated in
known later copied windows. The hit is another measurement of position
synchrony plus sparse lookup-table memorization, not a cellular decoder.

No fifth-fan-out lane promotes. Reproduction is in
`scripts/run_fifth_wide_fanout.py` and `src/eye_mystery/fifth_wide.py`.

### Practice cipher 3: corrected cycle arithmetic and bounded stop

The unresolved sdlwdr #3 progression hypothesis was audited before granting it
more solver time. Its Discord thread contains only the ciphertext attachment
and an A0 correction; the claim that its alphabet progresses with position is
our hypothesis, not an author hint found in that thread.

The first `C82+1` and `C41+C41+1` encodings also contained a real arithmetic
error: they reduced stream positions modulo 83 before applying the shorter
cycle modulus. The corrected implementation retains raw reset-relative
positions. This does not change the established `C83` UNSAT result. Corrected
ten-second checks make group A SAT at 42 symbols under both decompositions;
groups B, C, and the full corpus still time out.

A permutation annealer was then calibrated against A. In 400,000 swaps and two
restarts it finds 40 symbols for `C82+1` and 41 for `C41+C41+1`, confirming that
the diagnostic can enter the satisfiable basin. Its corresponding best bounds
for B are 65 and 64; for C, 77 and 78; for the full 18 streams, 83 and 83.
These are not exact lower bounds, but the large, monotone gap is enough for a
resource decision: stop deepening this unendorsed premise until a new invariant
or known plaintext arrives. The corrected model and calibration remain
reproducible in `scripts/solve_sdlwdr_cipher3_cycle.py` and
`scripts/optimize_sdlwdr_cipher3_cycle.py`.

### Sixth wide expansion: algebra, codebooks, and column phase

Another breadth cycle froze twelve representations before selecting six cheap
tests. Literal affine actions in the authored `F5^3` eye coordinates fit none
of seven strong context maps; the intentionally strange `F3^4+2` model also
fits none. Geometric rolling hashes and header-as-polynomial-root rules select
only the already-known forward additive checksum at base one, covering the
three diagonal East panels (`138/2001 = 0.068966` after complete-family
selection). Adjacent componentwise `k-x-y` completion lands in the 42 unused
trigrams 441 of 1,018 times, below its control median (`1325/2001` upper tail).

Treating centre as an empty generator makes 85 word classes in the full
five-direction cube, but the visible `0..82` subset occupies only 55 and shares
eight classes with the unused subset. Native inverse cancellation reduces the
full cube to 53 classes, not 83. The nearby 85 count is not a visible-alphabet
explanation.

The only primary hit is 26-column phase: all 34 complete records have
column/label MI 1.882712351 under intact-row rotation controls
(`1/2001 = 0.000500`). After every first row is removed, the tail remains
`11/2001 = 0.005497`. A family-held-out predictor closes it. Training
same-column label counts on two natural prefix families and scoring the third
gives parts 45, 46, and 49, total 140, versus control median 136 and
`856/2001 = 0.427786`. The primary effect is in-sample equality alignment,
not a predictive column channel. No sixth-expansion lane promotes.

The full portfolio and kill rules are in
`docs/sixth-wide-expansion-2026-07-21.md`; reproduction is in
`scripts/run_sixth_wide_expansion.py`.

### Read-only Discord delta: factoradic headers and a Paley negative

On 22 July, a read-only sweep of the recent `silmä-cryptography`,
`silmä-novel`, and `silmä-teollinan-älly` discussions recovered Lquid's
`noita_eye_header_audit.zip`. Its SHA-256 is
`ec9968c38c0816caba668a4cc73d78f0e8a89c2bba569b8729276d121d710fb8`;
every included manifest entry verifies. The supplied reproduction regenerates
its report and JSON byte-for-byte in a temporary directory.

The important finite core was then implemented independently from the local
canonical corpus. Ordinary lexicographic S6 unranking maps header ranks
`50,80,36` to `r,s,r^-1`, generating D4 and fixing center/newline. The six
remaining headers fix only center and generate S5. Newline preimages in case
order are `555343434`; East-Q occupies three right cosets of P and West-Q one.
The fixed center is partly automatic because ranks `0..82` lie below 120.

Freezing each named header's first two base-five graph digits and permuting the
observed third-digit multiset gives 22,680 assignments, 15,120 in range and
12,096 with distinct ranks. Counts are: typed newline word 6, P=D4 136, Q=S5
80, P=D4 plus Q=S5 4, and the full typed/coset system 2. The survivors are the
observation and the West2/West4 label exchange; those positions are the same
graph edge and type. This is one structural class modulo the graph's duplicate
edge. It promotes header metadata while leaving project-wide selection and the
missing body decoder explicit. Reproduction is in
`src/eye_mystery/factoradic_headers.py` and
`scripts/analyze_factoradic_headers.py`.

The same acquisition pass preserved “deck chaining” and merged-operation XGAK
as mechanism leads and treated `wmdwm.net/noita` only as an AI-generated
pattern viewer. The giant-dollar sprite is byte-identical in the current and
archived early-access assets, making it chronologically eligible, but the new
43-row mirror/XOR claim still lacks independently frozen masks.

The “Why 83?” discussion also motivated a distinct key-free Paley probe.
Quadratic character modulo 83 maps every adjacent nonzero difference to one
bit and complements under sign reversal. The 1,027-bit corpus has 485 ones.
Repeated contexts achieve only 134/221 best equal-or-complement matches, one
exact copy among thirteen, with global-label upper tail
`1004/2001 = 0.501749`. The best selected 7/8-bit ASCII form is gibberish and
has upper tail `738/2001 = 0.368816`. This lane is closed; implementation is in
`src/eye_mystery/paley_projection.py`.

The next S6 work begins wide: row/message products, adjacent quotients,
running actions, moving-delimiter tapes, D4 cosets, and conjugacy features each
receive one cheap necessity test before any body model is deepened. Details
and provenance are in `docs/discord-factoradic-audit-2026-07-22.md`.

That portfolio is now complete and entirely negative. Across 500 matched
global body-label permutations, the corrected tails are: product/header
`501/501`, quotient-support lower `501/501`, quotient-visible `396/501`,
quotient-in-D4 `164/501`, running-state compression `498/501`, header-coset
membership `482/501`, coset self-transition `164/501`, and cycle-type MI
`258/501`. Observed adjacent quotients occupy 119 of all 120 possible S5
elements. Literal newline movement turns 86 source rows into 327/456 fragments
with 30/75 empty rows. No direct S6/body lane promotes. Reproduction and scope
are in `docs/factoradic-wide-2026-07-22.md`.

### Giant-dollar mirror geometry: real defect, movable row number

The 21 July `silmä-novel` thread proposed the older
`boss_centipede/rewards/giant_dollar.png` as a diagram for a mirrored Gate
sieve. The current and archived early-access copies are byte-identical,
41x75 RGBA files with SHA-256
`0bc8284f0b915d73e350343faa4be2ff3d36f4e73e0edea59267a3d55a69e9c1`.
A September 2019 Discord message already describes the giant dollar-sign
reward, so it is chronologically eligible before the Eyes.

An independent raw-alpha audit finds three columns opaque for all 75 rows,
`x=19..21`. Contiguous runs outward from the stem produce a genuine reflected
near-symmetry: left rows `5..64` and reversed right rows `5..64` agree on
59/60 rows. The sole mismatch is left `y=34` width 11 against right `y=35`
width 12; these are zero-based PNG coordinates.

The reported 43-row statement is one subwindow of this relation. Left rows
`12..54` versus right rows `57..15` agree on 42/43 and place `11|12` at the
23rd row. Exhausting all `33*33*2=2,178` 43-row start/orientation choices finds
18 co-best alignments, all using `left_y+right_y=69` and the same defect. The
mismatch index ranges from 13 through 30 as the window slides. Therefore the
physical one-pixel asymmetry is real, while row 23 is not selected by the
centre-run rule alone. A separately defined void/divider mask may select it,
but the thread did not publish that mask; the raw widths also do not reproduce
the claimed transformed range `23..1`.

This promotes a mirror/compare construction vocabulary, not a dollar-to-Gate
or Gate-to-Eye decoder. Code, tests, and the exact falsification target are in
`docs/giant-dollar-audit-2026-07-22.md`.

### Seventh wide funnel: dynamic transforms all close

A new six-lane portfolio was frozen before implementation. It tested
header-ordered BWT→MTF on the exact six-symbol renderer tape, factoradic
six-token block transposition, `Z101` missing-interval crossings, sequential
three-eye change masks, equality-only next-occurrence pointers, and ordinal
six-value self-indexing. Global label relabelings preserve every body equality
and copied prefix for the absolute-label lanes; the two equality/position
lanes use the established prefix-tree-preserving positional shuffle.

Across 2,000 controls, corrected tails in lane order are `1101/2001`,
`1551/2001`, `1800/2001`, `1465/2001`, `71/2001`, and `1807/2001`. The
pointer lane was the only preliminary near miss (`10/501`); refinement moved
it to `71/2001 = 0.035482` without adding any convention. No lane crosses the
frozen `0.01` line.

The most informative negative is the first. A header supplies a complete
order of the five directions plus renderer newline, and the marker layer
independently supports BWT vocabulary. Nevertheless, a correctly terminated
header-collated BWT and ordinary move-to-front coding gives 2,523 runs over
3,176 symbols, exactly ordinary under matched relabelings (`0.550225`). The
headers also match none of the first-six-distinct body permutations and only
one of 873 eligible sliding ordinal windows. Factoradic metadata still lacks a
body consumer.

Full definitions, stop rules, results, and reproduction are in
`docs/seventh-wide-funnel-2026-07-22.md`.

### Ninth causal batch: six relational summaries close

The first six lanes of the frozen causal portfolio are complete. A global
assignment fits `108/209` partial-context edges with corrected tail `1/1001`,
but that score is dominated by the six literal prefix maps. Removing them
leaves `36/117`, null range `35..42`, and tail `0.818182`.

The five branch-reconvergence tapes occupy 54 columns, have maximum `GF(2)` and
Boolean rank five, and have zero nested row pairs. The excess columns are in
the opposite direction from the planned low-footprint test and restate known
isomorphic windows. Synchronization profiles are exactly functions of the
equality signatures that selected those windows, so they are non-identifying.

Both the full and common-98-coordinate equality skeletons have automorphism
group order one. The deduplicated 843-edge transition support gives an absent
matrix of binary rank 82 with 83 distinct rows; degree/no-loop controls are
indistinguishable. Finally, the factoradic header partition's invariant
transition model has held-out log gain `-3.408916`. Its superficially strong
`2/280` rank is invalid as promotion evidence because even the best tested
partition has negative gain.

Methods, controls, and the false-positive audit are in
`docs/ninth-causal-batch-2026-07-22.md`.

### Exact trailer-category acquisition

Read-only Discord context supplies the missing exact form of the recent XGAK
selector. Keying `A-Z0-9` with `A BAD MAGIC CARD TRICK` gives
`ABDMGICRTKEFHJLNOPQSUVWXYZ0123456789`. The annotated trailer diagram colors
the proposed categories as normal/front `ABKEFHJLNOPQ`, nonstandard/front
`DMGICRT`, and unseen/back `SUVWXYZ0123456789`; Q may move to the back set, and
a four-class variant splits back letters from digits. The full back side is
speculative even though it fits the available width.

This acquisition unblocks a finite category-level test but is not itself a
decoder. Its frozen test sits beside unrelated carry and worldline lanes in
`docs/ninth-second-wide-freeze-2026-07-22.md`.

### Ninth second slice: category, borrow, and worldline tests

The exact trailer categories put all nine candidate initial digits in one
class, satisfying the proposed common-start precondition. They do not preserve
any complete documented funny-obstacle pair: `EAST/WEST` mismatches at zero,
while `COPPER/SILVER` and `FROZEN/MOLTEN` mismatch at zero, one, and three.
This retains the partition as a possible start selector but rejects it as the
complete three/four-operation quotient.

The frozen borrow-state agreement initially scores `63/141` with arbitrary
global-label tail `3/2001`. A matched subgroup that preserves the East-1,
East-3, and East-5 sums exactly gives tail `0.007496` overall and `0.013493`
on the first-to-last held-out split. It therefore fails the frozen promotion
rule. Its Markov tail is `0.035482`.

A six-feature ablation rejects the arithmetic interpretation. The winning
order never emits the middle-eye step, and two independent high/low digit
comparisons reproduce `63/141` and held-out `35/82` without borrow
propagation. This simpler relation has checksum-preserving tails `0.005997`
and `0.006997`, but selection from six inspected variants raises them beyond
the familywise line. It remains a scoped out-of-sample prediction rather than
a result to deepen on the same contexts.

Finally, every directed panel pair has both literal and repeat-validated
isomorphic suffix/prefix overlap zero. All `9!` worldline orders tie at zero;
the strict checkpoint model is rejected. Code, full controls, and the
false-positive audit are in
`docs/ninth-second-wide-results-2026-07-22.md`.

### Tenth horizon: novelty audit before depth

A read-only Discord search prevents four broad ingredients from being
mislabelled as new. Faro shuffles appear in `silmä-cryptography` on 28 June
2025; an 84-card XGAK representation appears on 10 May and 17 July 2026; a
stable sort was suggested in `silmä-novel` on 25 January 2023; and Tuska
explicitly removed the middle eye and published outer-pair projections on
7 May 2026. The first-`N` cut and reversed-packet variants are likewise
documented community leads.

No searched message matched four exact diagnostics: an 84-card out-Faro whose
83 non-sentinel positions form the mod-83 orbit, riffle rising-sequence
complexity of the partial context maps, tie-aware ordinal-pattern recurrence,
or an exact graph-cover/bisimulation quotient. Absence from search is not proof
of global novelty.

Sixteen lanes are frozen before further Eye computation. The first cheap batch
tests ordinal patterns, riffle complexity, the pure 84/42 Faro algebra, graph
quotients, branch differentials, and context-loop obstructions. The outer-eye
lane is deliberately deferred so the seven windows that generated its residue
cannot validate their own interpretation. Definitions and prior-work
boundaries are in `docs/tenth-wide-horizon-2026-07-22.md`.

### Tenth horizon first batch: one screened anomaly fails validation

Tie-aware ordinal patterns have reselected family tail `0.594406` and
first-to-last-family tail `0.349650`. Partial context maps require 58 rising
sequences under their best shared base-five order, ordinary against matched
maps (`0.550450`); the held-out tail is `0.899101`.

An 84-card out-Faro fixes position 83 and acts as `x -> 2x mod 83` on all 83
other positions. Two has multiplicative order 82, and adding visible cuts
recovers the already-excluded affine `F83` family. In-Faro moves the sentinel
and therefore needs an independently specified output rule. Directed color
refinement individualizes all 83 transition labels after two iterations, even
with any one panel withheld. The observed context-window graph is a forest
with cycle rank zero, so it supplies no semantic holonomy loop.

The only initial positive is sibling-branch differential support. Mod-101
differences have repeated mass `3142/3611`, one support slot beyond 1,000
prefix/sum-preserving controls; selecting among four representations gives
`4/1001 = 0.003996`. A definition committed before validation fixes mod 101
and moves to the seven nonliteral context maps. Their repeated mass is 11,
controls span 2..21, and the tail is `874/2001 = 0.436782`. The clue fails.
Per the freeze, missing residues are not mined for semantic numbers. Full
methods and results are in
`docs/tenth-wide-batch-results-2026-07-22.md`.

### Eighth wide batch: structural and provenance lanes close

The six deferred sixth-expansion lanes were frozen as a second batch rather
than discarded. The literal 83-of-125 synchronizing/error code fails exactly:
its minimum Hamming distance is one, it has 415 distance-one pairs, and
9,746/13,778 cross-boundary length-three splices remain in `0..82`.

Without-replacement coverage is ordinary. The 34 complete 26-token records
sum to 750 distinct labels and the nine phase-zero 83-token body blocks sum to
474; the joint matched upper tail is `1214/2001 = 0.606697`.
Deterministic, net-positive RePair saves 68 symbols after charging two per
rule, with prefix-preserving upper tail `657/2001 = 0.328336`.

The reconvergence cocycle receives an exact stronger falsifier. Every repeated
bigram identifies its three path-boundary states. The quotient has 729 nodes,
786 distinct constraints, and one component. Solving
`potential(v)-potential(u)=label mod 101` yields 57 contradictory constraints;
there are only 58 surplus constraints beyond a spanning tree. The visible
labels are not a literal mod-101 gradient on this minimally merged equality
graph.

The two provenance-gated lanes cannot begin honestly. The archived/current
loose data contain 337/975 calls to engine random functions and zero definitions
of those generators. The known native placement RNG has no authored
header-to-body consumption rule. The exact table audit has no 42/101 table and
only duplicated 83-string `gun_names`, not a frequency model. Generic PRNG and
range-model fitting remain disallowed.

Definitions and reproduction are in
`docs/eighth-wide-deferred-2026-07-22.md`.

### Practice cipher 4 breadth pass: encoded formats close, quotients survive

The exact `22..78` action band was treated as a representation problem before
another mechanism was fitted. An injective map into all 95 printable ASCII
characters fails against a `99.9231%` planted control. The legal unpadded
Base64 lengths and close frequency profile motivated a stronger arbitrary
53-to-64 digit search; planted prose recovers cleanly, while the real best has
only `691/975` printable bytes and is more than 17,300 score units worse.

A frozen screen of every contiguous quotient width `2..28` finds two genuine
structural survivors. Width 2 produces a 29-state quotient with serial MI
`1.480049` plus a parity bit; width 3 produces a 19-state quotient with serial
MI `0.788949` plus a ternary stream whose serial MI `0.001320` is ordinary
under within-portion shuffles. The adjacent-pair grouping's quotient/parity
coordinate MI is unusually low under random assignments of the fixed label
frequencies (`98/10001 = 0.009799`). Width 3 ranks first and width 2 second by
remainder excess across the full width screen.

Neither quotient is plaintext yet. Exact 24-symbol equality signatures have
no match in the large English corpus; the 29-state version additionally has
no match in Finnish *Seven Brothers* or *Kalevala*. Injective English and
Finnish 29-character alphabets both recover planted controls exactly but leave
the real streams roughly 9,000–10,000 score units worse and unstable.
Successive mod-29 and mod-19 finite differences become more uniform, so the
un-differenced quotient is the uniquely useful layer.

The retained question is now mechanical: what bounded deck construction
lifts 29 or 19 payload states into consecutive pairs or triples? Static
language substitution and natural-phase Base64 are closed. Definitions,
full results, and boundaries are in
`docs/practice-cipher4-wide-codec-audit-2026-07-24.md`.

### Practice cipher 4 selector and route attribution

The frozen mechanical follow-up is complete. Widths 2 and 3 together define
206 direct, unsigned, signed-selector, Boolean-carry, direction-toggle, and
per-selector-lane laws. They were rendered on the plausible rings
`19,27,28,29,30,36,37,41,42` under two disclosed alphabet conventions. The
planted width-2 walk decodes cleanly; on every real run the untouched quotient
beats all 205 state/control alternatives. The Finnish 29-ring and shared-shift
checks agree.

A leave-one-portion-out selector predictor initially survives strongly.
After excluding centered quotient windows copied across portions, the best
previous-`q`/current-`q`/previous-`r` context gains `0.328318` bits per binary
selector and `0.551030` per ternary selector. All four 1,000-control nulls—
free selector shuffle, within-quotient shuffle, circular selector offsets, and
intact-rank shuffles—give corrected upper tail `1/1001`.

Exact carrier attribution reverses the interpretation. At width 2 the
predictor is correct on `304/322` seen contexts whose complete rank bigram
also occurs in training, but `0/23` seen contexts with a genuinely new rank
bigram. Width 3 gives `295/317` and `0/42`. Exact rank trigrams account for
`188/194` and `180/189` correct cases. Thus the effect detects the disclosed
shared plaintext's repeated transitions; it is not an executable selector
transducer.

Finally, a label-invariant eight-symbol equality-pattern model exhausts 396
fixed routes: reversal, global odd/even, ragged rectangular and snake reads,
rail fences, and fixed blocks. A planted seven-column route is identified and
inverted exactly. The real best improvements over identity have full-selection
tails `0.651741` and `0.179104` under 200 matched controls. No route survives.

Lanes A–G are therefore closed as specified, and the two-cycle lane is not
opened without an invariant. Cipher 4 remains unsolved. The broader lesson is
that statistical significance under several nulls is still insufficient when
the effect can be attributed completely to already repeated full symbols.
Definitions and reproduction are in
`docs/practice-cipher4-selector-route-results-2026-07-24.md`.

## 24 July 2026 — eleventh wide horizon and first mixed batch

The next Eye pass was frozen wide before choosing an implementation favorite.
Sixteen lanes cover direct numeric claims, unknown-plaintext GAK feasibility,
deck-action constraints, Finnish source structure, carrier attribution,
renderer confounds, chronology, and later in-game interfaces. The portfolio
and promotion gates are in
`docs/eleventh-wide-horizon-2026-07-24.md`.

The recent entropy/music PDF's exact assertion is false on the accepted
corpus. Across the first, middle, third, and sum-mod-five trigram projections,
none of 36 message/projection blocks at glyphs 25–49 is balanced or perfectly
lag-five periodic. Selecting the best projection and cut at fixed lag five
gives `62/180`, with corrected upper tail `402/1001`. Selecting lags 2–10 as
well gives `77/207`, tail `55/1001`. The PDF's plotted perfect payload is not
the real message data.

The community's ciphertext-orphan example reproduces under the precise
identity-reset ordinary-GAK convention. `BCBDBCDA` has the exact plaintext
schedule `aababaaa` with operations `(1,2,3,0)` and `(3,1,0,2)`;
`BCBDBCDAC` is UNSAT after all 108 decryptable two-operation sets, including
the ordinary requirement that the operations have distinct top-source
positions. The ninth symbol raises the minimum operation alphabet from two to
three. This is a real ciphertext-only falsifier, but pair enumeration grows
from 108 at four cards to 533,433,600 at eight. It is a calibration oracle, not
an Eye-scale solver.

The no-double capacity interpretation closes constructively. Repeating the
single 83-card rotation `(1,2,...,82,0)` produces an arbitrarily long
double-free ciphertext; a 1,028-symbol fixture has zero doubles. No-double
constrains top movement but does not bound length or plaintext alphabet.

A deterministic Finnish orthographic syllabifier was calibrated against
Kielitoimisto examples. The crafted Discord Kanteletar pair has aligned
syllable runs `24 same, 2 different, 6 same, 2 different, 14 same`, whereas
East 1/West 1 begin `24,4,4,4,13`. The example also edits the source and omits
a common line. It is not source evidence. Syllable search remains dependent on
finding an invariant that arbitrary GAK would expose.

Finally, the retained curiosities were assigned to their exact carriers.
Headers carry the factoradic classifier and `Fi!`; selected body sums and
markers carry the mod-101 checks; selected equality contexts carry the
isomorph and first/third-eye residues; the later Gate asset only
retrospectively matches an Eye-derived statistic. None predicts an unseen body
context. Full results and reproduction are in
`docs/eleventh-wide-first-batch-results-2026-07-24.md`.

## 24 July 2026 — symbolic GAK frontier and second mixed batch

The exact ciphertext-only ordinary-GAK primitive now has an SMT-LIB backend.
It independently reproduces the four-card parent/orphan pair, decides
constructed two-operation orphans at deck sizes five and six, and exactly
replays a planted SAT witness at deck size 12. This crosses the predeclared
calibration gates, although similar planted sizes 8 and 10 time out, so runtime
is not a useful monotone scale.

A lazy multi-message encoding shares unknown operations across all nine Eye
panels while resetting each to the identity deck. It represents only operation
values reached by the nested top-card compositions, extends the resulting
partial injections to full permutations, and rejects any SAT model that fails
exact replay. With nine operations it finds witnesses through three glyphs per
panel and times out at four; with 26 operations it finds witnesses through
four glyphs and times out at 5, 8, and 10. These short SAT prefixes are
underconstrained compatibility, not support for GAK, and timeouts are not
negative evidence. The lane is frozen until a new representation decides ten
glyphs per panel or an external clue constrains the operations.

The reset-regime and renderer-counterfactual lanes close by audit. Every direct
and equality-isomorphic panel overlap is already zero under all panel orders,
while fixed-base continuous and row-reset scans are negative. The 26-column
position effect fails family-held-out prediction, its edge controls are
null-typical, and the newer change-point searches select 42 or 55 rather than
25/26. Full results and reproduction are in
`docs/eleventh-wide-second-batch-results-2026-07-24.md`.

The remaining second-batch lanes also close. A six-card, one-hidden-swap XGAK
counterexample emits the same two no-double, prefix-sharing, visibly
reconvergent paths under two keys. In one key the tested operations and final
states are equal; in the other both are unequal. Thus ciphertext
reconvergence alone cannot reveal the withheld action relation.

A complete literal Lua arithmetic grammar over the current WAK finds no
mod-42/83/101, no 42/83-sized random domain or numeric loop, and no produced
9/42/83/101 value flowing into a table index. It finds 114 ordinary
101-outcome random domains, ten nine-outcome domains, one nine-step
clusterbomb loop, and the two known `Random(0,100)<83` wand branches. Semantic
inspection yields no state walk or Eye lookup. The practice-transfer backstop
also closes because none of these methods honestly applies to the disclosed
construction of unsolved sdlwdr ciphers 3 or 4; those puzzles remain active
separately.

## 24 July 2026 — twelfth wide novelty horizon

The next search begins with a sixteen-lane map rather than a single favored
theory. The frozen map is in
`docs/twelfth-wide-novel-horizon-2026-07-24.md`. It treats “novel” as an exact
test absent from the local record and targeted readable Discord searches, not
as a claim that nobody privately considered the broad ingredient.

The prior-art boundary matters. Projective groups occur in the recent
practice-cipher/GAK work, 9×9 and `81+2` layouts are old Eye suggestions,
overlapping trigrams are extensively explored, an Eye vector-field comment
dates to 2021, and Shamir/Reed–Solomon have been named. The targeted searches
found no Eye-specific fractional-linear `PGL(2,83)` context model, no
five-eye-to-adjacent-`S6`-generator construction, no 9×9
visible-symbol-as-directed-edge path test, and no discrete curl/Hodge audit.
Those narrower constructions are hypotheses, not results.

The first batch is intentionally mixed: projective context-map compatibility,
header-conditioned Coxeter words, a natural nine-state directed-edge code,
leave-one-panel-out polynomial shares, and exact-layout spatial Hodge defects.
Its stop rule requires all five cheap screens before depth unless one produces
a literal held-out prediction.

The first mixed batch is complete in
`docs/twelfth-wide-first-batch-results-2026-07-24.md`. Every lane is negative.
After removing copied-prefix identity contamination, the seven nonliteral
context maps have projective-fit tails `.781095` over `F83` and `.925373`
over `F101`, with no exact context. The complete 120-model
header-conditioned Coxeter scan has tail `.746269`; a training-selected
assignment scores only `4/148` heldout, tail `.830846`.

The natural 9×9 directed-edge path is the closest descriptive excess but is
still ordinary: the first four panels select row-major numbering and the
other five give `75/589` joins, tail `.149254`. Cross-panel interpolation
finds two degree-seven columns over `F83` and one over `F101`, tails `.213930`
and `.497512`, with no lower-degree column. The exact-layout triangular Hodge
stencil gives null-typical distinct, zero, and nontrivial-alignment statistics;
its best tail is `.248756`. No lane advances, so the next work remains lateral
rather than adding parameters to these failures.

The next five lateral tests are frozen before execution in
`docs/twelfth-wide-second-batch-freeze-2026-07-24.md`. They test an exact
line-digraph support closure, the two rejected raw trigram phases, a
train/heldout `AG(2,3)` line-sum design, a fixed dictionary of physical deck
actions, and an order-two raw-direction transducer controlled by the
independently established factoradic header classes.

The second lateral batch is complete in
`docs/twelfth-wide-second-batch-results-2026-07-24.md`. The exact line-digraph
closure collapses to one hidden state and forces 6,046 absent transitions.
The P-header triple nevertheless ranks first among 84 training triples by F1,
but only because its 5,377 novel guesses obtain high recall at 9.22%
precision; the exact support contradiction is decisive.

The rejected raw phases initially show a `.004975` occupancy tail under
within-row direction shuffles. That control destroys accepted trigrams. A
strict validation preserving every accepted glyph, row-pair multiset, and
triangle parity gives `.910448` at 200 controls and `.902020` at 5,000; marker
and row-boundary tests also fail. Train/heldout affine-plane line sums give
`.388060` over `F5` and `.094527` over `F83`. A 373-action physical shuffle
dictionary completes no nonliteral context and is worse than its null. The
order-two header-controlled raw transducer ranks `81/280` and scores
`626/2601`, below the unconditioned `628/2601`.

The remaining wide lanes are frozen in
`docs/twelfth-wide-third-batch-freeze-2026-07-24.md`. A read-only review of the
latest crypto/novel discussion finds no independently selected in-game deck
interface beyond the shared number 83. The batch gives new finite tests to
spectral concentration and five-ary convolutional syndromes, while storage
bitplanes, conventional modes, and executable clue paths must pass existing
selector and identifiability gates rather than receive another free scan.

### Twelfth wide horizon: final batch and restored lane G

The final batch is complete in
`docs/twelfth-wide-third-batch-results-2026-07-24.md`. A bookkeeping audit
caught that the signed-projective quotient G had been deferred rather than
executed. The restored complete scan quotients every nonliteral context into
`P1(F41)`, fits all Möbius maps, and reselects all 83 reflection centers inside
200 target-shuffle controls. Center 39 is best, with supports
`5,5,5,4,7,7,6`, zero exact contexts, and corrected tail `.109453`. All 40
primitive roots are coordinate-isomorphic and give the same support vector.

The 843-edge transition support has leading singular-energy fraction
`.1513166097198497`, ordinary under degree-preserving no-loop edge swaps
(`.149254`). Of all 124 normalized memory-one through memory-three parity
filters over `F5`, P selects `(1,2,2,1)` at `177/726`; it gives `385/1875` on
heldout Q, essentially the strict-control mean, tail `.457711`.

The remaining lanes close by stronger existing boundaries. Exact greedy
base-seven packing already reconstructs all 150 engine constants and its
forced 21/22 capacity tape is null (`.825817`); no authored bit index exists.
Unknown plaintext makes stream, CBC, and arbitrary keyed-permutation modes
constructively capable of realizing any observed ciphertext. The renderer,
83-of-101 wand branch, copied `gun_names`, Gate, and selected Lua arithmetic
paths supply no executable state walk or heldout Eye prediction. The Gate
remains possible later construction vocabulary, not a completely rejected
visual clue.

All sixteen A–P lanes now have a bounded result and none earns depth. The
step-back bottleneck is external identifiability: a known plaintext, selected
operation family, new authored interface, or a method learned from unsolved
practice cipher 3/4.

### Practice cipher 3: mechanism breadth restart

The first post-horizon method-acquisition target is sdlwdr cipher 3. The old
position-progressive permutation was a project hypothesis rather than a
located author hint, so increasing its SMT budget would not be a genuine new
lead. `docs/practice-cipher3-wide-freeze-2026-07-24.md` instead freezes seven
independent routes before scoring: transfer of the solved ciphers 1/2 wheel,
standard `C83` actions, fixed position drift, named physical deck updates,
cipher-5's exact recursive operation family, label-invariant isomorph maps,
and source closure only after mechanism selection. Group A is training; groups
B/C remain held out.

The first mixed batch is complete in
`docs/practice-cipher3-first-batch-results-2026-07-24.md`. The complete
ciphers-1/2 wheel/control family is ordinary on B/C (`.422886`) and produces
gibberish. Fixed drift selected on A expands from 78 to all 82 ordinary wheel
states in both heldout groups. Among 120,372 distinct physical
base/action/mode candidates, the A winner still emits 136 out-of-range ranks
and 946 more on B/C. Cipher 5's exact recursive operation family emits
159/351/581 outside-range ranks. These transfers close without weakening the
older scoped progression results. Standard-`C83` and label-invariant lanes
remain active.

## Crib observations

The strongest public alignment suggests a repeated plaintext region of roughly
17 characters in the first message family, with repeat spacings 28, 30, and 35.
`as above so below` is exactly 17 characters and appears explicitly in Noita's
lore, so it is a sensible crib to test. It is not unique: Hermetic source text
also contains local repeats at the relevant spacings. Exact checks against
multiple Emerald Tablet translations and the G. R. S. Mead *Corpus Hermeticum*
put the superficially promising repeats at the wrong message offsets or across
word boundaries. Also, a GAK isomorph is not a literal plaintext repetition
pattern. No result currently validates this crib.

## Sources

- [Noita Wiki: Eye Messages](https://noita.wiki.gg/wiki/Eye_Messages)
- [The Emerald Tablet research directory](https://docs.google.com/spreadsheets/d/1Aih_3v9BMbVI-MQQgWP51HTTplgRwXi2jRKYgyhPMao/edit)
- [Community Eye Glyph Timeline](https://docs.google.com/document/d/1q-4HnP8lPLQioG5h6fBb7BjVuF1EAOltO3gqn___Pp8/edit)
- [Noita 1.0 release notes, 15 October 2020](https://noitagame.com/release_notes/20201015/)
- [The solved Cessation Cipher Quest](https://noita.wiki.gg/wiki/The_Cessation_Cipher_Quest)
- [Official Noita Summit Q&A, Eye answer at 53:42](https://www.youtube.com/watch?v=5T_DBlXL0YQ&t=3222s)
- [Official interviews and videos index](https://noita.wiki.gg/wiki/Official_Interviews_and_Videos)
- [Nolla Games' 2019 developer AMA](https://www.reddit.com/r/Games/comments/d7cqjz/we_are_nolla_games_the_team_behind_the_upcoming/)
- [Profile of Petri Purho and his card magic](https://www.killscreen.com/profile-petri-purho/)
- [Datamined eye-rendering function](https://pastebin.com/rXNsPi47)
- [Noita data archive](https://github.com/vexx32/noita-data)
- [Earliest timestamped public `Random(0,100)<83` copy, 9 February 2021](https://github.com/vexx32/noita-data/commit/70696c9d62f9d95647b369c307dbecf1158d681c)
- [Noita early-access data archive](https://github.com/defektu/noita-early-access-data)
- [Lymm37's eye-message research wiki](https://github.com/Lymm37/eye-messages/wiki)
- [Noita Eye Glyphs on Puzzling Stack Exchange](https://puzzling.stackexchange.com/questions/119923/noita-eye-glyphs)
- [Aki's active eye-message experiments](https://git.ignore.pl/noita-eyes/)
- [Aki's experiment log](https://git.ignore.pl/noita-eyes/log/)
- [Aki's Noita depot manifest history](https://git.ignore.pl/noita-data-builder/plain/manifests)
- [Lymm's Binoculars](https://gitlab.com/realgonzogames/lymms-binoculars)
- [Preserved “Hidden Secret” email document](https://docs.google.com/document/d/1DZsFCcO5aRGVwF-spIPCJk1cbsBG0uNo3tMBusywTII/edit)
- [July 2026 opening-animation Eye proposal](https://www.reddit.com/r/noita/comments/1so4si9/state_of_the_cauldron_eyes_mystery_in_noita_2026/)
- [Generalized Cipher Clock, ePrint 2020/1492](https://eprint.iacr.org/2020/1492.pdf)
- [Tomster12's isomorph viewer](https://tomster12.github.io/isomorph-viewer/)
- [Noita Wiki: Game Lore](https://noita.wiki.gg/wiki/Game_Lore)
- [Corpus Hermeticum, G. R. S. Mead translation](https://www.gnosis.org/library/grs-mead/TGH-v2/th209.html)
- [Finnish Corpus Hermeticum XIII](https://www.azazel.fi/article/corpus-hermeticum-kolmastoista-kirja/)
- [Azazelin Tähti Finnish article sitemap](https://www.azazel.fi/wp-sitemap-posts-soa_page_article-1.xml)
- [Azazelin Tähti Finnish Emerald Tablet](https://www.azazel.fi/article/smaragditaulu/)
- [Finnish 2020 Corpus Hermeticum product record](https://www.suomalainen.com/products/corpus-hermeticum)
- [National Library record for the Finnish Corpus Hermeticum](https://kansalliskirjasto.finna.fi/Record/fikka.5440482)
- [Publisher/society Corpus Hermeticum listing](https://www.gnosis.fi/itseopiskelu/corpus-hermeticum/)
- [Publisher/society ebook listings](https://www.gnosis.fi/itseopiskelu/e-kirjoja/)
- [Project Gutenberg Finnish-text catalog](https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv)
- [Project Gutenberg: Kalevala](https://www.gutenberg.org/ebooks/7000)
- [Project Gutenberg: Seven Brothers](https://www.gutenberg.org/ebooks/11940)
- [Project Gutenberg: J. A. Hahnsson's Finnish Grimm translation](https://www.gutenberg.org/ebooks/45046)
- [Kotus modern Finnish word-list page](https://kotus.fi/sanakirjat/kielitoimiston-sanakirja/nykysuomen-sana-aineistot/nykysuomen-sanalista/)
- [Project Gutenberg: books about alchemy](https://www.gutenberg.org/ebooks/subject/563)
- [Alchemy Texts: all authors and books](https://www.alchemy-texts.com/all-authors/)
- [Waite, *A Demonstration of Nature*, exact candidate passage](https://sacred-texts.com/alc/hm1/hm107.htm)
- [Waite's *Hermetic Museum* index](https://www.sacred-texts.com/alc/hermmuse/index.htm)
- [Internet Archive OCR source, *Hermetic Museum* volume I](https://archive.org/details/b24927363_0001)
- [Internet Archive OCR source, *Hermetic Museum* volume II](https://archive.org/details/b24927363_0002)

## Highest-value next work

1. Obtain an external clue or a known plaintext fragment. A general `S_83`
   deck/GAK instance with arbitrary shuffles is underdetermined from this corpus.
2. Treat `A83` and `S83` as observationally tied until a nearly complete
   context permutation or another sign relation is found. All affine transitive
   groups are already excluded by the strong context certificate.
3. Test crib candidates only against a concrete state mechanism. Language-like
   prose alone is not validation.
4. Search confirmed Noita puzzle constructions for an external key or state
   walk rather than reusing their plaintext literally. Cessation's known
   calendar key and direct skip mechanism are now negative controls.
5. Search Petri Purho's likely construction vocabulary: small card/deck
   operations, Noita wand shuffling, and a 26-symbol plaintext alphabet. Keep
   each proposal falsifiable against shared prefixes, reconvergence, isomorphs,
   and the absolute no-double rule.
6. Classify the `LUMIKKI` constant historically. The installed build excludes
   CRC-32/BZIP2 as its runtime string hash; the remaining discriminator is a
   contemporaneous record of the reverse-hash search universe or construction
   evidence. Without one, do not promote Snow White associations into a key.
7. Continue separating three clocks: external construction material must
   predate internal cipher construction; developer-created ideas need not
   predate their public release; decoder clues may be introduced after the
   ciphertext. Record which clock every chronological claim uses.

### Practice cipher 3: the hidden reset-body prefix tree

The frozen label-invariant pass found a much stronger observable than the old
position-progression premise. Although no two relevant messages share their
first ciphertext symbol, A4 and A5 share the next 43 symbols exactly; A0
shares their first eight. A1/A3 also share three. Ten thousand independent
within-message multiset shuffles, rejecting every control with an adjacent
double, have maximum body-prefix lengths `0..4`; the 43-symbol observation has
corrected upper tail `1/10001`.

This makes a first-symbol predecessor/IV interpretation natural: different
predecessors enter one common state, after which common plaintext actions
trace one common path. The full transition graph stops that intuition from
becoming a claimed solve. Its 2,229 events contain 1,845 distinct directed
edges, maximum out/in degree `32/33`, and occupancy equivalent to
`69.041053` uniform outgoing choices. Thus 42 partial permutation colours can
interpolate the graph, but a predecessor-only, 42-action natural-language
machine would repeat far more edges. The distinction between edge-colouring
compatibility and generative evidence is the main transferable result.

The standard `C83` raw/difference/accumulation width screen is selected on A
and fails to replicate on B/C. A bounded static English homophone model remains
gibberish and scores roughly 2,966 log units below a matched planted control;
because that control reaches only 24.97% event accuracy, the run is not a
general exclusion. Raw/body/both-difference source fingerprints give zero
matches in Sherlock Holmes, English/Finnish Kalevala, and Finnish Seven
Brothers. An exact unknown-`C83`-order/42-difference test times out at 60
seconds and remains undecided.

The complete checkpoint is
`docs/practice-cipher3-second-batch-results-2026-07-24.md`; reproduction is in
`scripts/run_practice_cipher3_second_batch.py` and
`scripts/audit_sdlwdr_cipher3_homophones.py`.

Applied retrospectively to the Eye bodies, the same statistic gives 1,018
events, 843 distinct edges, maximum out/in degree `19/18`, and effective
uniform choice count `33.426694`. Thus the Eyes are compatible with a
42-action predecessor model whereas Cipher 3 is not. This is not new positive
evidence: the previously frozen, prefix-tree-preserving Eye edge-reuse test had
only `.043478` upper tail. The method distinguishes “not falsified” from
“selected,” and the Eye lane stays closed absent a predictive edge colouring.

### Practice cipher 3: reflection wheel separates key from geometry

The exact alphabet-size bridge `Z83/{±1}` was tested after freezing it.
Before quotienting directions, the real reciprocal-transition graph proves
that a single 42-step forward half-cycle is impossible: 253 unordered pairs
occur both ways and one raw state has 14 reciprocal partners; a directed
half-cycle allows at most two.

For the direction-free quotient, the displayed standard wheel and all 166
ways to insert exceptional `J` into both orientations of the solved
cipher-1/2 wheel were exhausted. Matched controls recover 100% plaintext at
`-7.178008` per trigram and select the planted `forward-17` insertion together
with its dihedral `reverse-65` equivalent. The real standard wheel scores
`-15.538194`; the best old-wheel insertion scores `-15.394573`. Both are
punctuation-heavy gibberish, closing those finite coordinate families.

The arbitrary hidden-wheel test stops at its positive control. With the true
wheel fixed, the substitution solver reaches 100% in 10,000 moves. With the
wheel unknown, 500,000 moves reach only `9.017497%` jointly (and about 9.47%
even with the true key fixed), with no dihedrally correct wheel. Circular
spectral initialization recovers at most 10 of 83 true adjacencies. Therefore
the real arbitrary-wheel corpus is not assigned a candidate score or text.
The result isolates wheel geometry—not language substitution—as the missing
method.

Freeze and results are
`docs/practice-cipher3-reflection-wheel-freeze-2026-07-24.md` and
`docs/practice-cipher3-reflection-wheel-results-2026-07-24.md`; implementation
is in `src/eye_mystery/practice_cipher3_reflection.py`.

### Wide freeze: recovering hidden geometry from Eye isomorphs

The Cipher-3 reflection-wheel failure identifies a transferable bottleneck:
language scoring could solve the substitution when the wheel was fixed, but
could not recover an arbitrary 83-point wheel even on planted data. The Eyes
have seven nonliteral equality-isomorphic windows that may constrain geometry
directly, so a new twelve-lane breadth map was frozen before optimization in
`docs/thirteenth-wide-hidden-geometry-horizon-2026-07-24.md`.

The prior-work boundary matters. Requiring every context map to be one
rotation or reflection is a dihedral subgroup of the already excluded
arbitrary-label affine action. The new first hypothesis instead equates only
the unsigned hidden-wheel lengths of corresponding textual steps, allowing
each step to choose its own orientation. Across the seven fixed contexts this
supplies 141 unique equations on 71 observed labels. Exact adjacent and
multi-lag satisfiability, planted recoverability, solution multiplicity, and
first-family/last-family prediction are specified before any candidate wheel
or plaintext may be scored.

### Hidden geometry result: multi-step rejection, adjacent case open

The exact lag ladder is complete enough to separate two mechanisms. Every one
of the seven nonliteral contexts is individually SAT even when all within-
window pairwise distances are imposed. They cannot share a wheel: the first
family is UNSAT at cumulative lags 1–6, the last and combined families at
1–3, and the last family is also UNSAT at lag 5 alone. The preceding first
1–5 and last 1–2 cases remain `UNKNOWN` after 120 seconds, so the reported
thresholds are proved boundaries rather than claimed minima.

The last-family proof shrinks to eight chord equalities from `last-east5` and
`last-east3`. Enumerating their 256 orientation choices and row-reducing over
`F83` forces two distinct labels to have the same coordinate in every branch.
The core is deletion-minimal; deleting its rows leaves
`3,5,8,8,8,8,2,2` collision-free sign branches. This dependency-free
certificate rejects a common multi-step metric without invoking language or
the authored numeric label order.

Lag 1 alone remains unresolved. Each context is SAT, but joint arithmetic and
Boolean Z3 encodings time out; an independent eight-worker CP-SAT run is still
`UNKNOWN` after 300 seconds; and one-sided searches reach only 61–65/141.
These are not negative evidence. The surviving hypothesis is specifically an
adjacent differential transducer whose immediate motion classes need not
compose into longer geometric chords. Full results and reproduction are in
`docs/thirteenth-wide-hidden-geometry-results-2026-07-24.md`.

### Practice cipher 4: homophone and fractionation checkpoint

The 200-symbol common action block was scanned by its exact equality
fingerprint against letters-only and space-preserving *Sherlock Holmes*,
English/Finnish *Kalevala*, and Finnish *Seven Brothers*. Unlimited
many-to-one homophones are allowed, but all 150 repeated-position constraints
must hold. Across 2,040,251 and 2,478,970 normalized characters respectively,
there are zero compatible windows. This is a concrete-source exclusion.

The frozen selector-demultiplex family then selected every width-2/3 lane
order and reversal on portions 1–2 and tested the fixed winner on portion 3.
A planted interleaving is recovered with corrected tail `1/201`; the real
winner has held-out improvement `-0.102488285` and tail `1080/2001`.

Typed coordinate reassociation required a calibration repair: the order-8
pattern model failed its positive control, so its real score was discarded.
Order 14 was the smallest model to recover the planted width-3, period-7
inverse and was frozen before the real run. The planted result has tail
`1/101`; the real winner has held-out improvement `-0.365859218` and tail
`77/101`.

Cipher 4 remains unsolved. The lesson is procedural: calibrate the statistic
before exposing it to real data, select transformations on training material,
and require the one fixed transform to survive held-out data. Full results and
reproduction are in
`docs/practice-cipher4-fractionation-results-2026-07-24.md`.

### Fourteenth wide horizon: transfer methods, not answers

After the Cipher 4 fractionation closure, prior Eye work was inventoried by
the *object* each test consumes. Direct `0..82` transforms, fixed routes,
small group actions, deck bases, ordinary language formats, visual stencils,
prefix tries, and generic checksums are heavily saturated. Typed fields inside
one trigram, shared automatic generators, canonical complete-dictionary
automata, label-invariant recurrence timing, checksum-algorithm selection, and
operation-interface archaeology remain materially less explored.

Fifteen lanes were frozen before scoring any of them in
`docs/fourteenth-wide-method-transfer-horizon-2026-07-24.md`. The first
experiment is a direct method transfer: use one raw eye as a five-way selector
that stably demultiplexes the other two eyes' `0..24` payload values. Every
selector position, payload order, lane order, and lane reversal is inside the
declared family. Selection occurs on P panels; the fixed winner is tested on Q
panels. Global permutations of all 83 accepted labels preserve the complete
equality/prefix nuisance structure, and a planted interleaving must be
recoverable before a real score is admissible.

This breadth freeze explicitly preserves the lag-1 hidden-geometry CSP and
recursive mod-101 trie checksum while preventing either from becoming an
unbounded favorite. If selector demultiplexing fails, the next tests are a
shared order-1..32 linear generator and canonical minimal/failure-link
automata, not fitted selector codebooks.

The inherited order-8 equality-pattern statistic then failed the selector
positive control by spuriously reversing one lane, so its real-data run was
blocked. Orders `8,10,12,14,16,20,24` were evaluated only on the planted
fixture. Order 14 is the smallest that exactly recovers the planted third-eye
selector, natural lane order, concatenation, and zero reversal mask; order 24
also succeeds. Order 14 is frozen before any real Eye selector score.

The real selector result is negative. P selects
`s1:concatenate:order=3,0,2,1,4:reverse=10111`, with train improvement only
`+0.009392391`; applied unchanged to Q it gives `-0.776995317`. Two of the
first three global-label controls exceed that held-out value. Even if none of
the remaining 197 did, the corrected tail would be
`3/201 = 0.014925373`, so the frozen `.01` promotion line is unreachable and
the run stops exactly.

This closes only the stable global five-lane selector family. Per-header
selectors and fitted lane codebooks are disallowed repairs. Full evidence is
in `docs/fourteenth-selector-results-2026-07-24.md`; the next lateral test is
the shared-linear-generator lane C.

Lane C then passes its own calibration and closes exactly. A planted order-3
`F83` recurrence with coefficients `(2,5,7)` is uniquely recovered from P and
predicts all `462/462` Q equations generated from independent seeds. The real
scan covers raw ranks and differences over `F83` plus all six within-trigram
component serializations over `F5`, at every order 1–32 after removing known
copied openings.

None is even consistent on P. At order 32, raw ranks give 146 equations,
differences 143, and each digit serialization 630; every coefficient matrix
has rank 32 and augmented rank 33. This is an exact contradiction, so no
Q-side coefficient fitting occurs. Full results are in
`docs/fourteenth-linear-results-2026-07-24.md`. The branch moves laterally to
the canonical minimal dictionary automaton rather than increasing recurrence
order toward interpolation.

Lane D is canonical but not independent. The nine marker-stripped bodies form
a 919-state/918-transition trie. Bottom-up right-language minimization gives
911 states and still 918 transitions. The sole non-singleton equivalence class
is the nine accepting terminal leaves; there are zero internal
suffix-equivalent merges.

Accordingly the transition labels still total `37,774 = 374*101`, with exactly
the existing trie multiplicity vector. Its diagonal-sum- and marker-preserving
zero count is the same
`8,174,134,656 / 825,564,856,320 = 0.009901263`, so it cannot be counted as a
second checksum. Full results are in
`docs/fourteenth-dictionary-automaton-results-2026-07-24.md`. Aho–Corasick
failure links remain a genuinely different next object because they can
capture internal phrase suffixes without identical complete continuations.

Before calculating lane E, its ambiguous “depth-change word” was resolved.
The nine bodies define one Aho–Corasick trie and numeric-label BFS. Retain
exactly nodes whose failure target is non-root; sum their incoming labels
modulo 101 and serialize `node depth - failure depth` in that BFS order. The
only word tested is independently fixed
`BEXIT=(2,5,24,9,20)`. Both closure and one contiguous word occurrence are
required. The freeze is
`docs/fourteenth-failure-link-freeze-2026-07-24.md`.

Lane E fails both gates. The canonical Aho–Corasick trie has twelve nodes whose
failure target is non-root, and all twelve targets have depth one. Their
incoming labels total `792`, residue `85 mod 101`. The exact
diagonal-check- and marker-preserving subgroup has zero closing relabelings
among `825,564,856,320`.

In numeric-label BFS order, the complete depth-drop tape is
`11,29,32,46,64,71,75,78,79,104,109,112`; it contains no
`BEXIT=(2,5,24,9,20)`. No joint control is required because neither observed
criterion passes. Full results are in
`docs/fourteenth-failure-link-results-2026-07-24.md`. This closes the
canonical cache/failure machine; a different record layout now requires an
authored consumer.

The recursive trie lane was then narrowed before calculation. On the ordinary
marker-stripped prefix trie, define
`R(v)=a*incoming+b*sum(children)+c*outdegree+d*depth mod101`, with nonzero
`a in {-1,+1}` and `b,c,d in {-1,0,+1}`: 54 rules total. Each of the five
outdegree-at-least-two nodes is held out while a rule is selected on the other
four. Promotion requires 5/5, root closure by the all-branch-selected rule, a
planted selection control, and a joint matched tail below `.01`.

This prevents the definitional `(1,1,0,0)` root sum from counting as its own
prediction and forbids coefficient expansion after seeing five residues. The
freeze is `docs/fourteenth-recursive-check-freeze-2026-07-24.md`.

The recursive selector passes its planted nested tree: all five held-out
branches are zero and the root closes. The Eye data gate then fails maximally.
Across all 54 rules and five canonical branch nodes—270 values total—not one
is zero. Every leave-one-out fold therefore scores zero; deterministic ties
select `(-1,-1,-1,-1)`, whose branch values are
`96,32,64,73,5` and whose root value is 62.

Since observed prediction is `0/5` and the root is nonzero, subgroup controls
are not run. Full results are in
`docs/fourteenth-recursive-check-results-2026-07-24.md`. The result preserves
the unexplained `37,774 mod101=0` root event while closing this compact uniform
recursive consumer and forbidding coefficient/node-type expansion without an
authored interface.

The remaining high-ranked method-transfer lane B then passes its positive
control before the Eyes are scored. Its 225 candidates move exactly one of
three typed eye components within periods 2–26 by left shift, right shift, or
reversal, rejecting any reconstruction outside `0..82`. An accepted-range
fixture encrypted by period-seven right shift of component 2 is recovered
exactly by `c2:p7:shift-left` under the already frozen order-14 pattern model.
Train and held-out improvements are `+5.842783471` and `+4.030816846`.

The real reassociation audit then fails before model selection. Zero of all
225 routes keeps every P-panel reconstruction in the accepted `0..82`
alphabet. The Q-side intersection and the all-nine intersection are also
empty; per-panel counts in message order are
`19,8,56,0,8,40,33,3,71`, so West 2 alone excludes the family.

No equality-pattern score or matched control is meaningful when no candidate
passes this necessary gate. Full results are in
`docs/fourteenth-reassociation-results-2026-07-24.md`. This exactly closes
short-block accepted-alphabet misalignment while leaving a deliberate
`0..124` intermediate code, externally selected routes, and other typed-field
roles as separate hypotheses. The next novelty choice must again begin wide
across the remaining portfolio rather than extending this failed family.

The next step therefore starts from objects, not parameters. A read-only
Discord audit of `silmä-cryptography` and `silmä-novel` found no exact prior
formulation matching header-ordered binary prefix trees, within-trigram
multiset/order factorization, five-adic glyph-tree isometries, reflected
base-five Gray traversal, or low-complexity symbolic dynamics. Exact search
terms and attribution limits are recorded in
`docs/fifteenth-wide-novel-horizon-2026-07-24.md`; no messages, reactions, or
calls were made.

Two Kantele documents were also inspected. They already map the five eye
directions to Kantele notes, try trigrams as note sequences/chords and sums,
and suggest playing Eye-derived sequences in game. Music conversion is
therefore prior art. Its useful method transfer is narrower: a chord naturally
splits an unordered pitch multiset from a voicing/inversion order. For visible
Eye ranks, that quotient has 31 realized multiset classes and four absent
classes `333,334,344,444`.

The fifteenth horizon freezes twelve mutually bounded lanes and selects four
for the first batch: a 42-shape header-ordered six-leaf prefix code, the
31-class multiset/order split, six possible authored five-adic coordinate
orders, and 96 canonical reflected-Gray geometries. Plants, first/last-family
held-out gates, complete controls, and forbidden repairs are specified before
any real result.

All four plants pass. The prefix-code selector recovers
`shape17:header`, aligned width-eight MSB, exactly. The multiset plant beats
200 relabelings on both P and Q (`1/201` each). A conditional five-adic tree
automorphism recovers hierarchy `(2,0,1)` and preserves `3120/3120` training
plus `2340/2340` held-out pairs. A translated reflected-Gray fixture preserves
`136/136` and `102/102` chords; two reflection masks are distance-equivalent.

The Eye results are all negative. The prefix-code winner
`shape11:inverse` has held-out score `-24.720305418` and exact rank
`5/120 = 0.041666667`. The multiset projection has P/Q corrected tails
`1410/2001 = 0.704647676` and `656/2001 = 0.327836082`; the order tape's
`343` compressed bytes and `684` runs give `89/2001 = 0.044477761`.

The geometric necessities fail exactly. The best five-adic order `(1,2,0)`
preserves `171/249` first-family and `573/831` last-family label pairs. Its
first contradictions change LCP depth from one to zero. The best 125-state
Gray candidate preserves only `3/59` and `3/82` aligned adjacent chords, with
an index-zero contradiction in both splits.

Full evidence is in
`docs/fifteenth-first-batch-results-2026-07-24.md`. This closes the four frozen
objects without altering arbitrary lag-one 83-wheel status or licensing
fitted code trees, multiset alphabets, hierarchies, or space-filling curves.
The branch returns laterally to E–H or acquisition lane K.

The next batch was narrowed against prior coverage before calculation.
Ordinary radix-five borrows, generic moments, geometric hashes, and RePair
were already tested, so they were excluded. Three distinct mechanisms were
then frozen in
`docs/fifteenth-second-batch-freeze-2026-07-24.md`: literal phase-zero uniform
productions of lengths 2–5, strict factoradic-class leave-one-out dispatch
over a standard checksum dictionary, and binary events produced when a
componentwise raw cube result enters `83..124` and is reduced by 83.

All positive controls pass. The morphism plant recovers
`0->01, 1->10` and exact heldout predictions. Three authored checksum classes
recover `9/9` withheld markers and their three rule types. A reduction plant
uniquely separates `sum-order201` from every rival and is exact at `6/6` plus
`5/5`.

All real-data necessities fail. For uniform lengths 2, 3, 4, and 5, East 1's
repeated label 40 already demands two different productions at source index
8. The deduplicated 32-vector checksum dictionary makes zero correct
factoradic-class predictions: eight folds have no compatible two-panel rule,
and the ninth is the known negative additive mod-101 rule trained on East 3
and East 5, which produces no visible East-4 marker.

The 18 missing-state event tables have no exact training convention. The
first-family winner is `sum-order012` at `45/59`; fixed on the last family it
scores `41/82`. Its first contradictions are `14->21` versus `25->64` in
`first-gap30`, and `22->60` versus `43->66` in `last-west4`.

Full evidence is in
`docs/fifteenth-second-batch-results-2026-07-24.md`; 493 tests pass with Z3
enabled. These results close only the frozen objects. The next novelty step
must again start wide; reset/synchronizing automata and predictive/Hankel
state are retained alongside other new candidates, while the original trie
checksum, lag-one wheel, Gate vocabulary, practice ciphers 3/4, and
source/chronology leads remain unchanged.

The next synthesis checkpoint again began wide. Projectivizing a nonzero raw
eye triple in `F5^3` yields one of the 31 points of `PG(2,5)`. A canonical
inventory shows that visible labels `1..82` cover all 31 points, with
multiplicities 17 twice, 8 three times, and 6 four times. The 42 excluded cube
states are exactly the missing scalar representatives. This differs from the
negative 31-class sorted-multiset quotient: it identifies scalar multiples,
not coordinate permutations.

The count structure suggests two further exact but unproven interfaces. A
projective line in `PG(2,5)` has six points. The exceptional outer
automorphism of `S6` sends a standard point-stabilizing `S5`—the abstract type
generated by the Q headers—to the transitive `PGL(2,5)` action on six
projective-line points. Separately, every complete record has length
`26=|P1(F25)|`, giving a precise within-row extended Reed–Solomon test rather
than the already-negative cross-panel share model.

Targeted read-only searches of `silmä-cryptography` and `silmä-novel` found no
exact hit for the projective-plane/outer-`S6` constructions or for the
unrelated Dyck, rotor-router, reset-word, Hankel, and Lyndon candidates. This
is a bounded attribution audit, not proof of universal novelty; older broad
Reed–Solomon suggestions remain acknowledged.

Fifteen lanes and their overlap boundaries are frozen in
`docs/sixteenth-wide-exceptional-structures-horizon-2026-07-24.md`. The first
batch deliberately spans four objects: canonical `PG(2,5)` ray homophony and
projective-context necessities, header-induced three-type Dyck syntax,
five-state raw-eye rotor schedules, and within-row `P1(F25)` low-degree
extended codes. No real score may be calculated before the freeze commit.

All four positive controls then pass before real scoring. A planted
projective map preserves `4495/4495` incidence triples, and a canonical ray
homophone beats 200 relabelings on both splits. The header-Dyck plant validates
all `977+2190` symbols. Five planted local rotors are recovered across
independent resets. The extended-row plant uniquely recovers
`x^2+2`, output eyes `0,2`, forward order, and degree 3, closing `10/10` P
plus `24/24` Q records.

The real projective action fails before matrix fitting. Every one of the seven
nonliteral contexts is nonfunctional or noninjective after ray projection.
The separate 31-point language tape also misses promotion: P/Q corrected
tails are `132/2001=.065967016` and `298/2001=.148925537`. Thus the
31-ray/42-complement inventory is exact but has no validated geometric or
homophonic consumer.

Typed stack syntax fails all panels. The P-selected `header-aligned`
convention reaches only `5/977` training and `26/2190` heldout symbols; East 1
first mismatches at renderer-tape index 5. The rotor model fails still
earlier: the first five successors of current direction zero in East 1 are
`1,1,2,0,1`, not a permutation of the five directions.

The exact `P1(F25)` row test is maximally negative. Across ten irreducible
quadratics, six ordered eye pairs, two directions, and degrees 0–5, all 720
candidates fit zero of ten P records. No candidate reaches Q selection.

Full evidence is in
`docs/sixteenth-first-batch-results-2026-07-24.md`; the Z3-enabled suite passes
504 tests. The result does not reject the factoradic headers or use the
abstract outer-`S6` identity as evidence. Outer-`S6`, reset/Hankel/Lyndon,
`GF(125)`, graph covering, finite-state coding, archaeology, and practice
transfer remain queued alongside the original durable leads.

The second sixteenth-horizon batch was then frozen without viewing real
scores. Its three objects are deliberately different. A canonical outer
automorphism of `S6` is built from duads, synthemes, and pentads; all 720
inner conjugates and header/inverse routes act on renderer tapes and must
preserve the exact newline mask. A word-combinatorics lane asks whether the
authored cut is already the least necklace rotation under header/inverse
alphabet order and forward/reverse tape direction. A complete-cube field lane
enumerates 40 irreducible cubic models of `GF(125)` and three Frobenius powers,
fitting only a local Möbius map per context while holding the representation
global.

All three plants must pass before any Eye score. The freeze and exact stop
rules are in `docs/sixteenth-second-batch-freeze-2026-07-24.md`.

The outer positive control first exposed a gauge ambiguity. With an arbitrary
planted conjugate, 96 P candidates preserved newline masks and the frozen
tie-break selected the wrong one for Q. Before any real scoring, only the
plant gauge was changed to canonical `c000`; the 1,440-model catalog, score,
split, and tie-break were untouched. The canonical plant then selects
`c000-header`, decodes `0/977` plus `0/2190` mismatches, and makes the
remaining 24-fold P ambiguity explicit. The necklace and `GF(125)` plants
also pass; the latter uniquely recovers `t^3+t+1`, Frobenius one, across all
seven independent Möbius contexts.

All real mechanisms fail. Outer action `c003-header` minimizes P errors but
still gives `53/977`, all from West 1; it then gives `364/2190` on Q. No
outer candidate is exact on P. Each of the four header/inverse and
forward/reverse necklace conventions has zero canonical P and Q panels. All
nine tapes are primitive and borderless; their least rotations are nonzero.
The three P Duval factor counts happen to equal seven, but that field was
diagnostic and Q is mixed, so it is not promoted.

The exhaustive `GF(125)` scan finds no exact context in any of 120 global
representations. The selected `t^3+2t^2+2t+3`, Frobenius-one representation
scores `8/18,6/18,9/18,6/9` on the four training contexts and
`7/30,7/30,7/25` heldout after maximizing each local map over every three-edge
fit. Three agreements are definitional, and every context has a further
contradiction.

Full evidence is in
`docs/sixteenth-second-batch-results-2026-07-24.md`. These results close the
direct outer renderer action, canonical header necklace cut, and fractional
`GF(125)` context action. They do not demote the original trie checksum,
lag-one wheel, factoradic metadata, Gate vocabulary, practice ciphers,
source ancestry, or chronology leads. The novelty portfolio returns to
reset/Hankel, graph-covering, finite-state-coding, archaeology, and
practice-transfer breadth.

### Practice cipher 3: conformance-vector breadth restart

The active method-acquisition pivot returns to unsolved sdlwdr cipher 3, but
does not grant more budget to the failed arbitrary-wheel optimizer. The
strongest positive evidence is architectural: six streams in each of three
length bands, plus a 43-symbol A4/A5 body copy behind unequal first symbols
and two shorter branches. This may be a deliberately selected conformance set
rather than eighteen ordinary literary excerpts.

A sixteen-lane wide horizon was therefore frozen in
`docs/practice-cipher3-third-wide-horizon-2026-07-24.md` before new scoring.
It spans master-tape excerpts, per-message affine masks over `F83`, low-order
generators, counter/PRNG modes, the exact `83=2*42-1` two-sheet architecture,
higher-order visible states, broader deck actions, compression/recoding,
polygraphic projections, six-stream route objects, variable-length token
codes, self-synchronizing codes, equality-only grammars, authored numeric
order, source conformance, and cross-puzzle construction genealogy.

The first cheap batch was A/B/C/H/M: cross-stream exact and affine factors,
order-1/2 recurrences and linear complexity, compression signatures, and
canonical equality-grammar structure. A is selection, B validation, and C
heldout wherever parameters are learned. The disclosed A prefix tree earns no
promotion by itself.

The renewed read-only Discord session then allowed the full Cipher 3 thread
to be checked. It contains the March 2025 attachment and A0 correction, then
only recent unsolved discussion. No mechanism, plaintext, IV/header, grouping,
or alphabet hint is present. In the preceding practice-cipher thread, sdlwdr
called the third one “a bit more unique”; in July 2026 they said its source
code had been lost. This is useful construction-genealogy evidence, not a
decoder clue.

The frozen first batch is completely negative. Outside the disclosed A tree,
the best affine relation has length five and all nine such maps occur once;
there is no exact factor of length four. The strongest equality-isomorph has
28 positions but only two repeated constraints. A-selected order-one/two
`F83` recurrences leave `77/75` residual values on A and all 83 on B/C.
All eighteen Berlekamp–Massey complexities are essentially half their body
lengths.

The 2,229 bodies have entropy `6.344283` bits/symbol, zero adjacent doubles,
and 1,588 direct LZ78 phrases. Direct numeric MTF still uses all 83 labels.
A2/A3/A5 cannot use their first value as a literal BWT primary index; the 15
valid inversions give 1,255 phrases. Under 1,000 multiset-preserving shuffles,
the direct and inverse lower tails are `.242757` and `.758242`.

A public Crawford *Kalevala* check found hundreds of matching `43/8`
prefix-tree hierarchies and thousands of repeated length-43 passages under
each tested normalization. The source remains possible, but the prefix shape
does not locate plaintext. Full evidence is in
`docs/practice-cipher3-third-wide-first-batch-results-2026-07-24.md`.

The next distinct construction-genealogy test is affine `AGL(1,83)` GAK/deck
state. It is not ruled out by random-like visible-symbol recurrence. Freeze
structured update families and a bounded exact 42-symbol solver, verify
planted recovery, select only on A, and transfer unchanged to B/C.

That batch is now frozen, before real scoring, in
`docs/practice-cipher3-affine-gak-freeze-2026-07-24.md`. It fixes the
standard visible coordinate `x=b/a`, five first-symbol modes, and four
structured global update families. The finite lane selects only on A and
requires at most 42 decoded values over A/B/C jointly. The exact lane gives
each realized nonzero action one arbitrary global multiplier and asks for a
decoded union of at most 42 states on A, B, C, and all messages. Positive
controls must recover a known structured family, exact planted
satisfiability, and forward ciphertext replay before real results count.

Both controls pass. The structured 42-action plant retains its true
`indicator-both`, `u(t)=2^t` family among the A-minimizers and transfers to
B/C. A separate four-state arbitrary-update plant is exact `SAT` and its model
replays the complete ciphertext. Direct round trips pass for all five modes.

The real finite result is far from the threshold. Of 35,675 candidates, 2,291
remain valid over A and zero decode A to at most 42 values. The unique
A-selected minimum is `skip`, `u(t)=70*t+60`, with 75 values and normalized
IoC `1.016215981`; it hits a zero multiplier on B/C.

The exact lane is inconclusive. With ten-second limits, all five group-A
queries at 42 states return `unknown: timeout`. All five all-message
diagnostics also time out even when the ceiling is relaxed to all 82 states.
The formulation is therefore not decisive on real data despite its passing
small plant. Per the frozen stop rule there is no structured survivor or exact
group result to justify blind depth.

`docs/practice-cipher3-affine-gak-results-2026-07-24.md` closes only the four
finite global update families in the five standard modes. Arbitrary update,
hidden coordinate permutation, two-sheet homophony, higher-order state, and
non-affine deck families remain open.

### Seventeenth wide synthesis: state reconstruction

A fresh read-only Discord delta was reconciled against the durable ledger
before generating new approaches. The recent entropy pivot, crafted Finnish
syllable pair, alternating renderer rotations, first-glyph checksum summary,
33,840-read audit, known-plaintext deck CNF, and ciphertext-only tiny GAK
examples are already preserved and bounded locally. No new solve or
operational hint was found.

The next novelty phase therefore starts wide around a different question:
whether the nine arrays are observations or conformance tests of a hidden
machine. Twelve lanes are frozen in
`docs/seventeenth-wide-state-reconstruction-horizon-2026-07-24.md`:
exact adjacent geometry, conformance-suite architecture, predictive Hankel
state, reset automata, directed graph fibrations, context bisimulation,
typed silent `Z101` events, maximum-entropy constraint generation,
mechanism-gated source tokens, version-differential clues, confirmed in-game
operation vocabulary, and noncommutative typed checksums.

Lane A ranks first because its hypothesis is already frozen and exactly open.
The new seven-bit/bit-vector formulation changes the solver rather than the
model. It must recover a planted wheel, solve every individual context, agree
with the integer encoding on small subsets, and then report only `SAT`,
`UNSAT`, or timeout on the first family, last family, and all seven. Lag two
and plaintext scoring remain forbidden.

The seven-bit formulation passes every gate. It agrees with the integer
solver on planted SAT/UNSAT fixtures and makes all seven individual Eye
contexts `SAT`; the complete test file passes in 1.802 seconds. On the three
real joint instances it returns only:

```text
first  59 constraints / 45 labels  unknown at 60.029 s
last   82 constraints / 62 labels  unknown at 60.032 s
all   141 constraints / 71 labels  unknown at 60.045 s
```

This is a solver result, not a cryptographic negative. Lane A remains open,
and the precommitted stop rule moves the portfolio laterally to directed graph
fibration and predictive Hankel state. Full evidence:
`docs/seventeenth-lane-a-bitvector-results-2026-07-24.md`.

Lane E then passes its planted-cover control and fails exactly on the Eyes.
Starting from one color, directed in/out block-count refinement recovers the
plant's five three-vertex fibers. P alone refines the real support and
multiplicity graphs to 77 blocks with copied openings, or 75 after trimming
them; only unseen/sparsely seen labels remain grouped. Adding Q makes all four
partitions discrete: 83 singleton blocks. No P partition remains equitable on
the complete graph.

This closes an exact observed-graph fibration into at most 42 fibers without
requiring random controls, because the model-independent cardinality gate
already fails. Details:
`docs/seventeenth-lane-e-fibration-results-2026-07-24.md`.

Before real Lane-C scoring, the empirical Hankel test is frozen separately in
`docs/seventeenth-lane-c-hankel-freeze-2026-07-24.md`. It removes known copied
openings, counts reset-local word occurrences, tests depth pairs
`(1,1),(2,1),(1,2)` over `F83,F101,F257`, selects only on P by the worst-prime
normalized rank deficit, and transfers to Q. Two hundred joint controls
shuffle each trimmed multiset under the no-double constraint and repeat the
whole selection. A deterministic low-state plant must beat 99% of heldout
controls before Eye ranks count.

The implementation audit catches an algebraic degeneracy before real scoring:
because `H(1,1)` is a submatrix of the two registered rectangular blocks and
all have the same smaller dimension, the nominal selector always chooses
`(1,1)`. The committed protocol retains that primary statistic, reports the
two deeper blocks, and freezes a continuation requirement that Q rank not
exceed P rank. A fixed 36-step hub/leaf plant passes unchanged: P and Q both
rank `20/28` in all three fields, no one of 200 shuffles matches its Q
deficit, corrected tail `1/201`, and rank excess zero.

The Eye result does not transfer. P's selected block ranks `72/75`, but Q
ranks a full `84/84` over all three fields. Both deeper blocks are full at
their limiting dimensions. Every control's nonnegative Q deficit is at least
the real zero, giving corrected tail `201/201 = 1`; Q rank exceeds P by 12.
This closes the registered shallow raw-label empirical-Hankel lane. Details:
`docs/seventeenth-lane-c-hankel-results-2026-07-24.md`.

A subsequent read-only sweep of recent `silmä-cryptography` and `silmä-novel`
adds no solve, but sharpens two directions. Historical cryptography messages
explicitly distinguish reversible GAK/permutation state from irreversible
state collapse and Alberti-style control symbols that override state and are
discarded on decryption. Those mechanisms can preserve long isomorphs and
break them at isolated events, so they strengthen seventeenth lanes D/G
without supplying a fitted reset map.

The newest controller/tutorial-stone glitch has a direct mundane explanation
in both the installed 14,745-entry WAK and the public 2021 asset history.
Mountain background scenes choose keyboard or gamepad art with
`GameGetIsGamepadConnected()` during scene initialization; individual control
emitters make a separate check when their spawn marker is processed, and
collision triggers later enable their components. Changing input mode during
loading can therefore mismatch the baked background and glowing overlay.
There is no Eye data path or cryptographic operation in these scripts.

One recent numerical observation was absent from the ledger and merits an
exact audit. After the final family's copied 20-symbol opening, the unique
clean gap-11 repeat anchors are `75,81,48`; their directed differences are
the marker values `27,77,33`. Because both the gap and presentation were
seen, a 50,000-control freeze lets every shuffle search gaps 2–30 and all
anchor orders. No control has been run yet. Protocol:
`docs/eighteenth-gap-anchor-freeze-2026-07-24.md`.

The frozen audit is positive. The detector recovers its plant, and the real
trimmed/full positions are respectively `16/37`, `18/39`, and `17/38`.
Exactly 1,616 of 50,000 nuisance-preserving shuffles have one clean gap-11
anchor in every final-row message; none also satisfies the exact formula, for
corrected tail `1/50001 = .0000199996`. The deliberately severe broad control
searches gaps 2–30, all six anchor orders, and ignores header-to-edge
assignment. Only 55 controls match, for corrected tail
`56/50001 = .0011199776`.

The relation is most compactly a telescoping checksum over the ordered anchor
path `E4 -> W4 -> E5`: headers W4 and E5 are the two modular decrements, while
header E4 is their sum and the endpoint difference. This promotes a genuine
marker/body construction link and gives the final factoradic row a concrete
consumer. It does not yet explain the landmark selector, the first two rows,
or plaintext. Full results:
`docs/eighteenth-gap-anchor-results-2026-07-24.md`.

Before deepening, two 50,000-permutation controls are frozen in
`docs/eighteenth-gap-anchor-label-freeze-2026-07-24.md`. The first globally
reassigns body labels while keeping markers fixed; the second permutes the
shared body/marker alphabet jointly. Both retain the exact equality skeleton
and charge all anchor orders/header-edge assignments. They test whether the
natural mod-83 coordinate, rather than only the selected positions, is
authored.

Both label nulls promote. With body labels permuted and markers fixed, the
exact/broad corrected tails are `9/50001 = .000179996` and
`100/50001 = .001999960`. With markers and bodies permuted jointly, preserving
their common abstract alphabet, the tails are `1/50001 = .000020000` and
`4/50001 = .000079998`. Thus the natural orthodox mod-83 coordinate is part
of the final-row construction link. Subtracting each anchor from its
12-symbol window does not align the interiors, so this is not evidence for a
simple running rotational cipher. Results:
`docs/eighteenth-gap-anchor-label-results-2026-07-24.md`.

The printed anchor positions expose a further pre-control fact:
`(16,18,17)=16+(0,2,1)`, exactly the W4 marker edge's independently defined
component order. A new matched-control protocol is frozen before counting. It
requires the broadened numeric match plus consecutive positions, reselects
gaps 2–30, and allows any of the three final header orders. Its result will
not be multiplied with the earlier tails because the anchors are shared.
Protocol: `docs/eighteenth-gap-anchor-position-freeze-2026-07-24.md`.

The position control passes. Of 50,000 new shuffles, 1,612 retain one clean
gap-11 anchor in all three messages. One has positions equal to a translated
`021`; a different one satisfies the exact numeric formula; none satisfies
both. After every control searches gaps 2–30 and allows any final header
order, none survives the joint numeric/position condition. The corrected
broad tail is `1/50001 = .0000199996`.

The promoted final-row record therefore has two interfaces: its full marker
values encode telescoping mod-83 differences, and W4's header edge order
`021` encodes the rank order of the three landmark positions. This is one
shared construction result, not two multiplicative p-values. Details:
`docs/eighteenth-gap-anchor-position-results-2026-07-24.md`.

The positive record triggers a deliberately wide follow-up in
`docs/eighteenth-wide-anchor-record-horizon-2026-07-24.md`. Its central new
abstraction is a rank-two K3 coboundary: the final anchors are vertex
potentials and the markers are all three pair differences. The first six
marker control edges independently enumerate both orientations of the
three-vertex cycle, while the final W4 edge supplies the observed `021`
position order.

This also sharpens, but does not wholesale validate, the later Gate lead.
The established Eye record has the exact binary interface
`77 + 33 -> 27 mod 83`: two path increments and their central telescoping
total. That matches the independently reconstructed two-side-input,
upper-control, center-result Gate topology at the level of arity and routing.
No Type4/Type6 execution, Seula residual mask, or fresh-value allocator has
appeared. Twelve lanes are ranked before depth; finite incidence conventions
go first, followed by row-typed records and the synchronizing 11-loop.

Lane A's finite slot audit gives a much cleaner exact description. For each
final order `(source,target,remaining)`, exactly one of six directed slot
differences reproduces all markers:
`h=a[source]-a[remaining] mod 83`. The output vectors for slot pairs
`01,02,10,12,20,21` are respectively
`(77,27,6)`, `(27,77,33)`, `(6,56,77)`, `(33,50,27)`, `(56,6,50)`, and
`(50,33,56)`.

The omitted target column of orders `012,021,102` is `(1,2,0)`, exactly the
ascending rank pattern of anchors `(75,81,48)`. Since this was seen
retrospectively, a new matched control is frozen before counting. It reselects
gaps 2–30, retains the broad numeric test, and allows both ascending and
descending rank directions. Protocol:
`docs/eighteenth-anchor-record-slot-freeze-2026-07-24.md`.

The slot/target control promotes. Of 50,000 new matched shuffles, 1,640 have
the target gap-11 structure and 253 also have ascending target ranks
`(1,2,0)`. None satisfies the exact numeric formula, so none has both exact
fields. The broad control reselects gaps 2–30, broadens numeric edge/order
assignment, and allows ascending or descending target ranks; 24 match, for
corrected tail `25/50001 = .000499990`.

The final marker orders now have three coherent consumers: slots 0 and 2
select source-minus-remaining operands; the omitted slot-1 column gives
anchor-value ranks; and W4's full order gives anchor-position ranks. This is a
compact self-describing record, though the base-16/gap-11 selector and
plaintext remain unknown. Details:
`docs/eighteenth-anchor-record-slot-results-2026-07-24.md`.

The closed slot record exposes a possible gauge-fixing pointer. E4 is the
unique self-edge panel; its selected repeat endpoint is trimmed index 27,
equal to `h_E4`. Adding the fixed one-marker plus 20-symbol opening frame gives
full-array index 48, equal to the E5 anchor selected as E4 identity order
`012`'s remaining component. The pointer sets `a_E5=48`; marker differences
then reconstruct `a_E4=75` and `a_W4=81`, while `h_E5=33` checks the final
edge.

Because index/value links are fertile post-hoc territory, a severe new
control is frozen before counting. Every shuffle may search gaps 2–30, any
panel, start or end, any marker and anchor, and coordinate offsets
`0,1,20,21`, after first satisfying the broad numeric record. Protocol:
`docs/eighteenth-anchor-pointer-freeze-2026-07-24.md`.

The pointer/gauge control promotes. Of 50,000 new matched shuffles, 1,747
retain one clean gap-11 anchor in all three panels. None also reproduces the
exact endpoint pointer; none reproduces the exact numeric slot rule. The
fully broadened family reselects gaps 2–30, any panel, either repeat boundary,
any marker and anchor, and independent offsets `0,1,20,21`; six controls
survive, for corrected tail `7/50001 = .000139997`.

The final row therefore fixes its own additive gauge. E4's trimmed endpoint
`27` is `h_E4`; adding the fixed full-array frame `21` gives `a_E5=48`.
The typed difference record reconstructs `a_E4=75` and `a_W4=81`, then
checks `h_E5=33`. This makes the final row a closed self-describing record,
not a checksum graph needing an external seed. It remains structural
metadata rather than a plaintext decode. Details:
`docs/eighteenth-anchor-pointer-results-2026-07-24.md`.

A read-only Discord reconciliation reopens the Earthquake/Holy-Mountain
magical circle in a more constrained form. The installed WAK routes
Earthquake and workshop collapse through `magical_symbol[_fast].xml` to
`animated_emitter[_large].png`. The two image SHA-256 values are respectively
`0e752d47688bfe88f196bf312c98e720f6391b5cf616e145ed2ee8ca15ba591d`
and
`7d839270f5abf0516faaa41d077f21181009a0a833cf2ab384dcf3a38475c9be`;
the early-access-data copies are byte-identical.

The five transcribed rows have lengths `32,24,20,17,24`, primitive periods
`5,1,2,17,6`, and the alternating 20-band has ten zeroes and ten ones. The
community already noted the `24/20` copied-opening match in 2021, added the
middle `5`/five-eye match explicitly in March 2026, and proposed a 17-position
wheel in 2023. These are prior art, not project discoveries.

The validated final anchor record now gives the loose numbers one compact
consumer: circumference 20 selects the final opening trim; ring length 17
gives one-based address 17 or zero-based 16; W4 order `021` gives starts
`16,18,17`; the balanced band supplies ten interior events, framed by an
equal state at gap 11; and rune periods five/six echo the visible-eye and
renderer/control alphabets. This recipe was assembled retrospectively and
gets no new p-value. Eight possible consumers are ranked before depth. The
first prospective test will use the still-unused actual 17-bit pattern;
independent acquisition of the reported `24,20,16` diamond geometry is next.
Horizon: `docs/nineteenth-earthquake-circle-wide-horizon-2026-07-24.md`.

The diamond acquisition overturns the reported-number premise. Naugam's
`24,20,16` “radii” are the shell sizes `4r` for `r=6,5,4`, and `85` is the
size `1+2r(r+1)` of the same radius-six Manhattan ball. The board was
constructed by assigning the three trigram eyes walk lengths `1,2,3`; these
are not counts measured from Noita's diamond sprite. Lane G is therefore
negative as independent Earthquake-circle corroboration.

The original defektu “Diamond Readings” document nevertheless exposes a
different exact asset-backed transform. In the installed WAK, blocks 01
(diamond), 05 (three ovals), and 07 (`¡!¡`) are precisely the three decorated
desert-ruin pieces sharing spawn weight `.6`. Pairing accepted trigrams as
`y,x`, reading orders `021,120`, and zero-padding odd endings reproduces every
published `5x+y` and `x²+y` value.

The squared output has 19 reachable symbols and a built-in uniform-input IoC
of `.0624`, so its raw `.069–.085` message IoCs are not direct language
evidence. It uniquely maximizes aggregate ordered collisions among the six
relative component alignments. Max-family controls give `384/20001=.019199`
for whole-x-trigram reassociation and `276/20001=.013799` for cyclic offsets.
Those controls still do not correct the historical formula search, and the
author later called similar high-IoC summed-eye effects coincidental. Preserve
the exact transform for a held-out isomorph test, but do not call it a decode.
Audit: `docs/twentieth-diamond-reading-audit-2026-07-24.md`.

The first prospective Earthquake-content test is now frozen without reading
the real slices. Apply `11110111011101110` only as forward/reverse
ones/zeros masks to 17-symbol slices at final trimmed starts `16,18,17`.
Offsets 0 and 11 are the already known anchor equality and are removed from
all scoring.

The four registered held-out metrics are nontrivial exact equality skeleton,
common repeat pairs, conflict-free supported partial bijection, and aligned
numeric equality. Fifty thousand controls condition on the full promoted
selector by preserving length, multiset, the fixed numeric anchors at
start/start+11, no adjacent doubles, and the unique clean gap-11 witness.
Variant maximization happens within each metric and the four metric tails are
Bonferroni corrected. Freeze:
`docs/twenty-first-earthquake-mask-freeze-2026-07-24.md`.

Before real evaluation, the positive-control wording needed one transparent
correction. Removing known offset 0 makes forward-one a strict subset of
reverse-one, so unique forward identification is impossible for every metric.
The plant must instead make all four registered fields nonzero in
forward-one; ties are allowed because both real and control scores already
maximize the same four-variant family. No real slice or score was inspected
before this correction.

The frozen Earthquake irregular-mask test is decisively negative. The
positive plant exercises all four fields. On real 17-symbol slices at
`16,18,17`, every forward/reverse and ones/zeros view scores zero for
nontrivial exact skeleton, common repeats, supported conflict-free partial
bijection, and aligned numeric equality after removing the known offsets
0/11.

All 50,000 controls condition on the complete promoted anchor witness. The
shuffler takes 1,305,953 attempts for 150,000 accepted streams, mean
8.706353. Since all observed metric maxima are zero, every control is at least
observed and the corrected tail is `1`. Close direct application of the
17-bit row to these final slices; do not rotate, shift, resize, or choose
panel-specific masks after the failure. Results:
`docs/twenty-first-earthquake-mask-results-2026-07-24.md`.

The next lateral step is frozen before evaluation in
`docs/twenty-second-cessation-wheel-transfer-freeze-2026-07-24.md`.
A 23 July Discord attachment records a solved practice cipher whose decisive
operation is line-reset traversal of a binary tape with distances `1..5` and
a one-position timing exception at each line terminal. Its archive SHA-256 is
`1c4a834e9722bf3287e008d973ff4eae914988c3a4129b8fcdcac13ad00c8e71`.
This is not an Eye clue; it is a concrete method transfer that distinguishes
physical wheel traversal from the failed static mask.

The frozen Eye test maps engine directions `0..4` naturally to distances
`1..5`, reconstructs the actual visual rows, samples the gap-fixed 17-bit
Earthquake band, and re-interleaves sampled bit triples. Forward/reverse is
selected only on the first four fixed nonliteral context pairs. The primary
score is equality on changed-label positions in the last three pairs. Its
exact matched null is all `C(17,4)=2,380` tapes with the authored bit
composition. No rotations, fitted direction maps, panel phases, or byte
searches are allowed after scoring.

The frozen Cessation-wheel transfer is strongly negative. The real irregular
tape selects forward from the four training contexts, with `19/63`
changed-label agreements. It then scores `17/85` on the three held-out
contexts, and no context matches exactly. Uniform endpoint timing is slightly
worse at `17/63` training and `16/85` held out.

Every one of the 2,380 composition-matched tapes underwent the same
training-only orientation selection. A total of 2,273 tie or exceed the real
held-out score, giving inclusive exact tail `.955042017`. The terminal-aware
practice method is executable and marginally changes the Eye output, but the
authored Earthquake tape is structurally unexceptional in the wrong
direction. Close this exact sampler under its stop rule. Results:
`docs/twenty-second-cessation-wheel-transfer-results-2026-07-24.md`.

The next novelty step again starts wide. The eight-lane map in
`docs/twenty-third-wide-post-wheel-horizon-2026-07-24.md` separates the
desert quotient, remaining marker rows, rune mapping, practice ciphers 3/4,
Gate topology, version archaeology, source ancestry, and coding-theoretic
anchor interpretations before selecting depth.

The cost-adjusted first discriminator is frozen in
`docs/twenty-third-diamond-context-freeze-2026-07-24.md`. It resets the exact
historical `y=021`, `x=120`, `x²+y` transform at each of the seven fixed
nonliteral context records. Fully copied input pairs are excluded; the first
four contexts are descriptive and only the final three form the primary
score. Fifty thousand global permutations of `0..82` preserve every corpus
equality and partial-isomorph structure while destroying the natural
base-five coordinates. No real score has been inspected.

The held-out desert quotient is decisively negative. The exact historical
`x²+y` transform scores `11/96` eligible output agreements on the first four
contexts and `6/129` on the final three, with no exact record. The lossless
`5x+y` sanity reading gives `4/96` and `3/129`.

All 50,000 controls preserve the complete equality skeleton through one global
`0..82` relabeling. A total of 48,175 tie or exceed the real held-out score,
for inclusive tail `48176/50001=.963500730`. With `y=021` fixed, the six
held-out scores for x orders are `(16,9,10,6,11,14)`; the historical `x=120`
order is uniquely last. Close this record-local transform under the frozen
stop rule and return to the twenty-third portfolio. Results:
`docs/twenty-third-diamond-context-results-2026-07-24.md`.

A new read-only Discord acquisition adds an unusually relevant practice
calibration without displacing the original five-puzzle obligation. Sdlwdr's
22 July “Practice Cipher #6” explicitly names a deck cipher incorporating the
Trailer Altar and Earthquake Circle. Both attachments were acquired; the
author-designated revised file has nine lines, 761 non-newline symbols, all 83
characters `!` through `s`, and SHA-256
`0b5e0a73e1cb8efc6090fa893fc4604195d2d85e884bfe2d39f35952974654c2`.

Its first characters `<=>?@ABCD` occupy natural deck ranks `27..35`, matching
plaintext digits `1..9` after A–Z and suggesting nine resets with known
numbered prefixes. The original and revised encodings share only those nine
starts plus twelve later cards, so the correction mutates the running state
almost immediately. Before testing language, seven distinct asset roles are
frozen: altar plaintext order, paired rotating decks, fixed circle cuts,
binary stable partitions, rune-index schedules, revision differential, and
the nine reset-prefix constraints. The finite paired-deck family is first.
Record: `practice-puzzles/12-sdlwdr-06-in-game-deck.md`.

The finite paired-deck screen is negative. Nine source-fixed initial orders
and six circle/natural nadirs produce 486 generalized-Chaocipher settings. All
retain the inferred numbered first symbols, but every decoded stream uses all
83 ranks and reaches rank 82. Low-rank counts span `370..419/761`, median 397;
the maximum uses outer-cycle counterclockwise on the left, natural on the
right, and nadir 20. Its `.550591` in-range fraction is not a plaintext
collapse and its rendering is gibberish.

Before the next score, a distinct circle-permutation test is frozen. The only
base permutations are signed cuts of `17,20,24,32`, stable partitions from
the exact alternating and irregular bit rows, and their displayed
outside-to-inside composition. Only two physical directions and two global
packet orders are allowed. Natural-reset decoding emits current card rank,
then applies `P`, `P^rank`, or `P^(rank+1)`. The altar fixes only the
alternative letter rendering. Details remain in the practice record.

The direct circle-permutation family is negative. After deduplication, 18
signed-cut, repeated-binary-partition, and outside-to-inside bases crossed
with three exponent schedules produce 54 candidates. Every result still uses
all 83 ranks through 82. The maximum low-rank count is fixed `cut+24` at
`428/761=.562418`; its natural and altar renderings are visibly mixed-rank
gibberish.

A sharper joint clue is now frozen before testing. The community phrase
`A BAD MAGIC CARD TRICK` is 22 characters with spaces, and the three
Earthquake binary rows total `24+20+17=61`; concatenating them gives exactly
83 positions. This is not literal altar text, so the identity may reflect the
practice author's choice rather than Noita's original asset.

Five consumers are separated before depth: stable ordering of the 83
positions, cyclic-rotation ordering, 13 tape-symbol operation classes,
literal per-rank steps, and a transformed instruction stream. Only the first
two are presently executable without fitted semantics. Their frozen test uses
two physical binary directions, natural or first-occurrence symbol collation,
stable versus cyclic order, and the already fixed `P`, `P^rank`,
`P^(rank+1)` schedules. No tape rotation or per-line selection is allowed.

The direct 83-slot position-order test is negative. Eight unique permutations
from binary direction, symbol collation, and stable/cyclic ordering cross with
three exponent schedules. Every one of the 24 settings uses all ranks through
82. The maximum is fixed cyclic clockwise order under first-occurrence
collation, `406/761=.533509` low ranks, with no coherent rendering.

The next tape consumer is frozen without fitting operations. The tape has 13
distinct symbols in first-occurrence order
`A,space,B,D,M,G,I,C,R,T,K,0,1`. After emitting current card rank, address the
tape by that plaintext rank, turn its symbol into a natural or
first-occurrence class rank, and rotate the deck by class or class-plus-one.
Two global cut directions and two binary readings give exactly 16 models.

The 13-class ordinal cut audit is negative. All 16 settings use every rank
through 82; the maximum, clockwise/first-occurrence/class-plus-one/right cut,
has only `407/761=.534823` low ranks.

One stricter asset-valued interpretation is frozen next. Map phrase letters
through either the proposed Trailer order
`BDMAGICKEFHJLNOPQRSTUVWXYZ` or the `A BAD MAGIC CARD TRICK` keyed order
`ABDMGICRTKEFHJLNOPQSUVWXYZ`. Treat bits either as appended alphabet
positions `26/27` with space 36, or literal `0/1` with zero-width spaces.
Address this value tape by recovered plaintext rank and cut by value or
value-plus-one, under two global directions and two binary readings. These
32 settings exhaust the admitted family.

The altar-valued plaintext-autokey family is negative. Every one of its 32
models uses all ranks through 82. The maximum is counterclockwise binary
reading, card-trick alphabet, appended nonletters, zero-based right cut:
`423/761=.555848`.

A read-only server-wide Discord search then recovers a decisive architecture
hint from the puzzle author. On 18 May 2023 in `#silmä-novel`, sdlwdr wrote
that the Earthquake symbol might be used for “some sort of alberti cipher.”
Later community discussion calls a custom 83-symbol form ciphertext autokey,
not classical Alberti. This is older than Practice #6 and therefore is not a
retrospective reaction to the puzzle.

The next family is frozen accordingly. Natural, Trailer-keyed, and
card-trick-keyed initial decks all preserve the digit positions. After current
rank emission, the observed ciphertext card supplies either its raw value or
its fixed 83-slot tape value. Update is cumulative rotation or absolute
realignment, with zero/one indexing and global direction; tape-valued models
also admit the two binary readings and two fixed nonletter conventions. The
complete family has 24 raw plus 192 tape-valued models. No line-specific
offsets or symbol-specific signs are admitted.

The 216-model custom-Alberti ciphertext-autokey rotation screen is negative.
Every candidate uses all ranks through 82. The maximum is a cumulative,
left-turning, one-based asset key from the clockwise tape and Trailer value
alphabet, starting from the Trailer-keyed deck: `418/761=.549277`. Raw-card
ciphertext autokey reaches only `409/761`.

All six fixed mechanism families were then replayed unchanged on the
superseded original ciphertext. Their maxima are respectively
`419,431,417,416,403,430/761`, and every stream again uses all 83 ranks.
Thus the author's correction is not one of the tested reset, timing, address,
or value conventions.

A final more faithful rotating-disk family is frozen before evaluation. In the
Trailer alphabet, outer `KMGIC` is `[7,2,4,5,6]` and inner `MAGICK` is
`[2,3,4,5,6,7]`. At time `t`, combine those 5/6-cycles and the 20/17 binary
cycles under eight fixed sum, difference, bit-select, and bit-sign schedules.
Two physical readings, cumulative/absolute alignment, zero/one-based step,
and three initial decks give 192 models with no fitted phase.

The full-circle clock is negative. Every model uses all 83 recovered ranks and
reaches 82. The best is the card-trick initial deck with the irregular row
signing the outer-plus-inner step, counterclockwise physical reading,
cumulative alignment, and one-based steps: `415/761=.545335` low ranks. This
closes the finite synchronous-clock interpretation.

Cipher #6 has now done useful methodological work without yielding its
plaintext: it exposed an exact 83-slot cross-asset construction, supplied a
known-reset prefix oracle, and showed how quickly plausible visual semantics
become underdetermined when no state transition is independently fixed. The
joint tape and sdlwdr's historical Alberti remark remain open evidence, but
additional directions/phases would be curve fitting. Practice effort returns
to unresolved #4/#3 unless a new author or source clue fixes a non-rotational
transition.

### Cipher 4 nonlinear restart: the omitted signed map closes, the GAK stays open

The new bigram heatmap is a visualization of the already recovered cyclic
geometry: every adjacent ciphertext step lies in `22..78`, leaving a diagonal
forbidden band. Its odd width motivated one genuinely omitted finite map.
Ranks `0..56` were interpreted by the standard signed zigzag
`0,-1,+1,...,-28,+28` and its reflection, alongside the direct centered
signed order. Accumulation on rings 19..83, including the standard
83-character plaintext wheel, produces no language. The asymmetric zigzag
was not present in the earlier selector-sign table, so this is a real closure
rather than a rerun.

The more important architecture is still the arbitrary cyclic-GAK recurrence
`p[i+1]=sign*delta[i]+q(p[selector]) mod83`. Exact all-message Z3 models were
augmented with equality over every maximal common action block of length at
least eight. Compact 27, natural-position 27, and natural 42 all return
`unknown` after 30 seconds in the primary current-symbol convention; no
impossibility is claimed.

A packed beam was then implemented to avoid copying full keys and paths before
selection. It passes a deliberately repetitive nonlinear plant, but that
control is too easy. At the real 200-action common block, a six-gram,
250,000-state natural-position search retains only thirteen candidates and
dies after transition 49. A matched 201-character natural-English plant from
the training corpus also dies after transition 49 and loses its known target.
Therefore the real failure is inadmissible. The surviving lead is now sharply
defined: solve or constrain nonlinear `q` with a crib, source passage, or
look-ahead/constraint search that first recovers the matched plant.

### Early-row transfer of the final anchor grammar

The next twenty-third-portfolio discriminator was frozen before evaluation:
apply only the final record's clean-loop selector, fixed
source-minus-remaining slot rule, and ascending target-rank field to the first
two marker rows. The required row-1 positive plant turns out not to exist.

Exact enumeration gives 83 numeric anchor solutions for row 1 because
`50+80+36=0 mod83`, but their rank patterns are only `021,102,210`; the fixed
target column is `120` and occurs zero times. Row 2 has zero numeric solutions
because `76+63+34=7 mod83`, whereas a closed gradient must sum to zero. The
same implementation accepts the known final anchors `75,81,48`, headers
`27,77,33`, and ranks `120`.

The calibration gate therefore stops the test before any earlier body or
matched shuffle is inspected. The universal three-row schema is rejected
without a p-value. Retain the exact row typing—zero circulation, residue
seven, and pointer-closed final difference—as a discriminator for a future
model, not as permission to invent a new operator per row. Freeze and result:
`docs/twenty-fourth-row-record-transfer-freeze-2026-07-24.md`;
`docs/twenty-fourth-row-record-transfer-results-2026-07-24.md`.

### Marker `!Fi` / `+358` conjunction

Stepping back to the complete first-trigram layer reveals a new exact spatial
reading. In canonical engine order, the header third digits are
`001/134/223`; their three column sums are `(3,5,8)`, Finland's international
calling code. This reuses the nine digits already decoded through the fixed
East-5-first marker trail, stable LF mapping, and primary-zero inverse BWT as
`!Fi`.

The discovery was retrospective, so a finite conditional audit was frozen
before enumeration. It keeps every first/second graph coordinate fixed,
permutes only the observed multiset `001122334`, retains ranks in `0..82` and
distinctness, and measures exact versus D4 `358`, exact versus
case-insensitive `Fi`, their intersections, and the unchanged full factoradic
predicate. No body value or language score is consulted.

The old range filters reproduce exactly: 22,680 assignments become 15,120
in-range and 12,096 distinct-rank cases. In that final universe, natural
ordered `358` occurs 224 times and D4-broadened `358` 855 times. The fixed BWT
route has 1,137 single-cycle assignments, 404 with three values in `0..82`,
two case-insensitive `Fi` suffixes, and one exact `!Fi`. Every registered
joint count is one: natural or D4 `358`, crossed with exact or
case-insensitive `Fi`, retains only the observed assignment. The other text
case is `%Fi` on assignment `100134223`, whose column sums are `457`.

The pre-existing full factoradic predicate remains untouched and again leaves
two survivors. The observed `001134223` has column sums `358` and BWT `!Fi`.
The West2/West4 scalar swap `001234213` has sums `448`, no D4 `358` view, and
no valid single-cycle BWT text. Thus the new layout resolves the factoradic
duplicate-edge ambiguity 1-of-2.

This is a positive structural discriminator but not a calibrated discovery
tail: both readings use the same digits, and the search space of recognizable
post-hoc grid facts is unknown. Do not multiply the counts. Promote only the
narrow claim that the markers likely contain designed, self-checking metadata
consistent with Finland/Finnish. It neither solves the bodies nor licenses
arbitrary `FI358` keys. The next prospective lane is an equality-derived
body-map holonomy test for the zero-circulation versus residue-seven row
typing. Freeze and full results:
`docs/twenty-fifth-wide-marker-country-horizon-2026-07-24.md`;
`docs/twenty-fifth-marker-country-results-2026-07-24.md`.

### Read-only delta and twenty-sixth routing

A read-only sweep of the restored Discord session found no prior `+358`
marker observation. The latest `#silmä-cryptography` content remains the
Kanteletar syllable-pattern proposal already audited. `#silmä-novel` adds a
tutorial-stone input-device rendering glitch; the author of the observation
reports that the background loads with the world while the highlight layer
loads on first input, making it likely an ordinary keyboard/controller state
split. Preserve tutorial-stone rendering as a low-priority in-game interface
lead, but do not treat this glitch as cipher evidence.

Ground-up review closes the proposed body-holonomy lane before body scoring.
The tenth pass already established that the seven independently observed
context windows form a forest with cycle rank zero. Completing a natural
three-panel triangle from the same aligned positions would make its composite
identity tautological, not a held-out observation.

The next clean marker-to-body interface is frozen instead. Interpret the
canonical column totals as fixed coefficients and test only
`3*x0+5*x1=8*x2 mod83` on the three natural panel rows after their known copied
openings. The total covers 263 aligned positions. Its exact null preserves
each truncated panel as a complete circle and exhausts both relative offsets
per row; the three row histograms are convolved. No sign, coefficient
permutation, intercept, lag, or panel selection is admitted. Protocol:
`docs/twenty-sixth-358-weighted-alignment-freeze-2026-07-24.md`.

The weighted interface is negative. Exact natural-row scores are `2/74`,
`1/96`, and `1/93`, totaling only `4/263`. Their independent cyclic-null
ranges are `0..6`, `0..7`, and `0..6`; the exact per-row tails are
`.228816654`, `.678385417`, and `.676494392`.

Convolving all three exact histograms gives null range `0..19` and inclusive
upper mass `171017439974/436487491584=.391803759`. The detector recovers a
perfect algebraic plant, every row histogram has mass `L²`, simultaneous
rotation is invariant, and the convolved mass is exact. Close direct
coefficient/sign/lag variants under the stop rule. The marker country tag is
unaffected, but it supplies no linear body consumer here. Results:
`docs/twenty-sixth-358-weighted-alignment-results-2026-07-24.md`.

### Three-plane locale checksum freeze

The marker country observation extends symmetrically across eye coordinates.
Summing down canonical columns separately in the first, middle, and third
digit planes gives `683`, `034`, and `358`. These are assigned E.164 calling
codes for Niue (`NU`), Spain (`ES`), and Finland/Åland (`FI`,`AX`). The fixed
BWT route on the scalar plane says `!Fi`.

The exact triple is post hoc and is not scored. A generic conditional audit is
frozen instead: in the same 12,096 graph-conditioned scalar assignments, parse
single-digit column sums as a padded decimal calling code and ask whether the
fixed-trail BWT's two-letter suffix is one of that code's assigned regions.
Natural geometry is primary; all D4 views are the one broadening. The first
BWT character is ignored for the generic event and `!` is reported
separately. The unchanged factoradic predicate is crossed only after all
events are counted.

Calling-code-to-region data is pinned to libphonenumber commit
`f7e3e88c92b905c8d6edb81f336dbe25edc05b52`; the generated map will be
vendored with provenance. This can corroborate a locale checksum, never body
language or a key. Protocol:
`docs/twenty-seventh-three-plane-locale-freeze-2026-07-24.md`.
