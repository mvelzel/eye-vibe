# Noita eye-mystery workbench

This repository is a reproducible cryptanalysis workbench for Noita's nine Eye
Messages. It does **not** claim a plaintext. As of 21 July 2026 the mystery is
still publicly unsolved, and the experiments here deliberately distinguish a
statistical curiosity from a validated decryption.

The current queue is maintained in [`docs/open-leads.md`](docs/open-leads.md);
the chronological evidence and negative results remain in
[`docs/research-log.md`](docs/research-log.md).  A lead entering the queue does
not replace the others.  The breadth-first assumption audit and novel mechanism
map are in
[`docs/novel-synthesis-2026-07-21.md`](docs/novel-synthesis-2026-07-21.md).
The subsequent deliberately wide architecture map and its frozen cheap probes
are in
[`docs/wide-approach-map-2026-07-21.md`](docs/wide-approach-map-2026-07-21.md).
Its second fan-out tests eighteen additional representation and construction
families before deepening any one of them.  The longstanding community
`125=83+42` complement motivates two explicit 42-class constructions here,
but both canonical decoders are language-negative; the post-hoc `34x27` trie
layout also loses selectivity once record phase is admitted.

The canonical interpretation is implemented in `src/eye_mystery/corpus.py`:
three base-five eyes form one value, the accepted reading produces exactly the
contiguous alphabet `0..82`, and the nine messages contain 1,036 values. The
corpus tests also lock in the published lengths, shared prefixes, complete lack
of adjacent repeated values, and alphabet coverage.

## Current result

The strongest new concrete result is in the nine distinct initial markers.
Put their third digits in the independently decoded East-5-first trail order:
`300113422`. This is a valid cyclic Burrows-Wheeler last column. Stable sorting
it produces the independently decoded trie-compatible order, its LF map is one
nine-cycle, and inverse BWT at the independently selected East 5 row gives
`001123243`. Regrouping in the established base-five trigrams gives
`1,38,73`, or `!Fi` in the established ASCII+32 display—cyclically, `Fi!`.
It is the only exact `!Fi` result among all 22,680 distinct orderings of the
observed payload multiset and among the 168 observed-marker assignments that
retain the fixed trail. The natural reading is a Finnish-language hint, but it
does not by itself decrypt a body.

An exhaustive source-structure check now covers every Finnish text in the
Project Gutenberg catalog: 3,648 books, 2,631,331 letter-normalized candidate
passages, and 2,772,407 space-preserving candidates. It finds no complete
message tree and not even one 24-character upper-branch partial. The remaining
repeat-only hits are bibliography and song-refrain artifacts. The leading
non-Gutenberg check covers 100 publicly dated Finnish occult articles from
Azazelin Tähti: about 1.09 million normalized letters and 2,278 candidate
passages produce no fingerprint, complete tree, or partial subtree. The leading
source gap is therefore the unavailable 2020 Finnish print translation of
*Corpus Hermeticum*, not another unsearched public-domain Gutenberg text. It
appeared on 26 March 2020, 203 days before Noita 1.0 and 206 days before the
first recorded Eye sighting. This clears the public-release chronology check,
but the cipher's internal construction date is unknown: if the text was
borrowed, it must have existed before that internal act of construction. The
dates therefore preserve the lead rather than support it. No authorized PDF or EPUB edition has
been located; current publisher, library, and retailer records describe a
paperback, so acquisition is deferred while source-independent leads remain.

The reported `LUMIKKI` storage-word clue is exact but was previously
misidentified. `0xacf68674`, the high half of the first packed 64-bit constant,
is not the standard reflected CRC-32b of `lumikki` (`0x5bfc21b9`); it is
CRC-32/BZIP2. A scan of 103,834 modern Finnish dictionary words against every
Eye 32-bit constant and eight CRC variants finds no other match, but that does
not calibrate the unknown reverse-dictionary search that found `LUMIKKI`.
The installed January 2025 release binary contains the target exactly once,
only as that immediate Eye half-word. It has no BZIP2 CRC polynomial, table, or
string. Its only CRC implementation is standard reflected CRC-32, called three
times by its `IHDR`/`IDAT`/`IEND` PNG writer. This rejects an ordinary runtime
Noita string-hash explanation in the current build, not an offline construction
choice or deliberate easter egg.
The 1876 Finnish Snow White story was publicly downloadable by 2014 and is
chronologically eligible. It supplies neither the exact message tree nor the
first-family source fingerprint, and 1,940 direct Cessation-style walks through
it produce gibberish. No evidence has yet been found that Noita's engine uses
CRC-32/BZIP2 as an internal string hash. The clue remains live but unclassified.

The strongest remaining body-cipher model is a group-autokey cipher with hidden
state, plausibly equivalent to shuffling an 83-card deck and emitting the top
card. This explains the flat distribution, causal isomorphs, chaining conflicts,
and lack of doubles, but it is a cipher class rather than a key or plaintext.

A breadth-first mechanism audit has also found a clean new header fact.  The
first six marker edges enumerate all six elements of `S3`: the first natural
row is the three even permutations and the second is the three odd
permutations; the final row is identity plus the two adjacent generators.  A
retrospective boundary operation on body trigrams exactly echoes the complete
marker-BWT output `!Fi`, but a held-out test rejects the obvious decoder: the
two strong last-family body-context maps are not involutions and violate the
`ABA=BAB` braid relation.  The `S3` layout is therefore retained as a possible
global sieve or conformance clue, not claimed as a body transform.  An
independent exhaustive five-direction `S3` transducer produces a unique
eight-of-nine near-fit, but `98.353%` of exact intact-body reassignments do as
well or better, so that alternative is rejected too.

The breadth pass's strongest positive is simpler: strip the nine markers,
merge every copied body prefix into one trie, and count each distinct edge
once.  Its 918 labels sum to `37,774 = 374 * 101`.  The result is traversal
invariant, fails suffix/raw/nearby-offset/row-family controls, and adds a tenth
independent label-count equation to the nine message sums over `F101`.
An exact 132-trillion-member relabeling subgroup that preserves all three
diagonal checksum equations closes in `0.990113%` of cases; freezing all nine
markers changes that only to `0.990126%`.  This is a concrete construction lead
rather than a decryption or definitive p-value.  It motivates testing whether
the Eye bodies are a checksum-protected prefix-tree object intended to be
merged or sieved before any cipher step.

A more speculative synthesis gives that object a possible hidden state space:
the 18 labels missing between the visible `0..82` and modulus 101 match the
compressed trie's five branch nodes plus thirteen exits.  Values `83..100` sum
to 31, exactly complementing the lower-six descendant residue 70.  The joint
full/lower closure has exact marker-fixed conditional rate `0.0098015%`, but no
rule yet assigns the 18 values to the 18 records.  It is an architecture to
falsify, not permission to brute-force an 18! plaintext fit.

There is now an exact independent in-game selector for the numbers themselves.
The installed procedural-wand Lua uses `Random(0,100) < 83` to choose a modifier
card over a draw-many card. With Noita's inclusive integer bounds, that is
literally the successful set `0..82` inside a 101-value domain. Across 74
direct `Random(0,100)` comparisons in the current WAK, 83 occurs only in the
two duplicated procedural-wand sources. The earliest independently timestamped
public copy found is February 2021, so it may be a later decoder clue; it is
not proof of pre-Eye construction. More sharply, all 18 complementary rolls
`83..100` select `ACTION_TYPE_DRAW_MANY`. The compressed Eye trie has five
branch nodes of degrees `(2,3,3,2,3)` and thirteen continuations—exactly 18
retrospective node-plus-edge records. The literal machine interpretation is
now rejected: an executed tree has fourteen card nodes rather than eighteen,
and the lower-six checksum branch owns only eleven node-plus-edge records while
the complement contains all eighteen values. The raw 83-of-101 selector remains
an independently authored later-clue candidate, but it neither types nor orders
the proposed hidden states. The bounded audit is documented in
[`docs/procedural-wand-architecture.md`](docs/procedural-wand-architecture.md).

This work has ruled out or failed to support these concrete subclasses:

- direct arithmetic, projective, and positional transforms over `F_83`;
- common adaptive-deck transforms with ascending or descending initial decks;
- fixed physical/near-size shuffles followed by selected-card cuts,
  move-to-front/back, or prefix/suffix reversals (103,188 candidates);
- the same card families with state reset on every 26-trigram visual row-pair;
- 676 constrained 83-symbol generalizations of the historical Chaocipher;
- a 25-position five-operation automaton;
- simple affine field walks derived from the five eye directions;
- natural Gaussian direction walks using `0, +/-1, +/-i` over `F_83^2`;
- affine/common deck shuffles followed by one or two structured swaps;
- staged common-base deck searches with up to three formulaic hidden swaps
  after the output-making top swap;
- the one- and five-active-rule neighborhoods of the best structured common
  base, with an arbitrary non-top transposition learned exhaustively for each
  plaintext-selected rule;
- 8,430 standard physical/near-size deck bases, including interleaves,
  Mongean shuffles, Josephus deals, and affine shuffles on 82 or 84 positions;
- a common arbitrary base followed by a plaintext-selected top swap, under
  calibrated but non-exhaustive optimization;
- the published position-progressive model
  `cipher_i = P^i(S[plain_i])`, even with arbitrary per-message starting
  phases, by a short exact contradiction;
- a classical Wadsworth/cipher clock with a 29-letter Finnish plaintext ring,
  or a 30-position letters-plus-space ring, under every output-ring ordering;
- raw-eye inverse move-to-front followed by marker-indexed cyclic BWT, over all
  2,160 natural initial-list, marker-orientation, and index-offset choices;
- a two-alphabet substitution interpretation of the best field-walk anomaly.

The numeric affine scans above use the displayed glyph values as field
coordinates. General GAK permits an arbitrary relabeling of the 83 ciphertext
symbols, so those scans alone do not rule out either affine transitive group.

For move-to-front and move-to-back, an initial-order-independent invariant
strengthens the earlier deck scan: repeated cards alone force 59 distinct rank
instructions, whether or not the first trigram is skipped. Those models cannot
encode a conventional 26-symbol plaintext alphabet under any card labeling.

The public Aki disk candidate uses 114 physical input positions and is not
covered by the 42-position Wadsworth exclusion. It was tested separately with
all 6,806 affine orderings of the 83-position output ring, resetting each
message, both with and without markers. Its best transliterated-Finnish
tetragram scores are `-15.3843` and `-15.4314`, versus `-8.8862` for the
training corpus, and the displayed outputs are digit-heavy gibberish. This
rejects that concrete ring plus affine-output subclass, not an arbitrary
114-position cipher clock.

The field-walk anomaly collapses to 25 states with normalized IoC 1.693. After
the marker payload supplied `Fi!`, matched language tests did favor Finnish
over English. With Finnish diacritics kept distinct, the full-stream alternating
walk scores about `-11.47` per tetragram versus ten prefix-tree-preserving nulls
at `-13.05..-13.19`; English has a smaller matched advantage. This does not
validate the walk: it incorrectly lets headers alter the copied body prefixes.
Omitting the headers and resetting state restores the exact prefix tree, but
both best 25/26-state variants remain stable Finnish-looking gibberish around
`-11.89`, and the 16-state odd-East walk lies inside its shuffle null. An
unconstrained homophonic relaxation degenerates to `SISISISI...`; adding a
Finnish unigram constraint merely replaces it with a few `ISI/ATA/NEN` cycles.
These are language-hint controls, not plaintext.

Two independent, label-invariant SMT encodings test the strongest published
isomorph contexts without assuming those numeric coordinates. They prove that
the last-family contexts cannot all embed in `C83:C41`, and conditionally reject
`C83:C82 = AGL(1,83)` when a weaker nested East 3 context is included.

A stronger dependency-free certificate no longer needs that East 3 assumption.
For `C83:C41`, it enumerates all 1,681 multiplier pairs: 1,664 make the field
equations inconsistent and the other 17 force coordinate collisions. For full
`AGL(1,83)`, the two 30-character last-family contexts leave only four of 6,724
multiplier pairs linearly open; adding West 1's independent 18-character
self-repeat makes all 328 possible multiplier extensions inconsistent. Thus
both affine transitive groups are excluded under the two strongest repeated-
plaintext identifications, with no numeric glyph labeling and no weak East 3
context.

The arbitrary position-progressive permutation has an even smaller
label-independent certificate. Call the two last-family context maps `A` and
`B`. They include `A(3)=44`, `B(3)=22`, `A(22)=23`, and `B(59)=23`. Powers of
one permutation commute, so `B(44)=B(A(3))=A(B(3))=23`; injectivity of `B`
would then force `44=59`. This excludes every permutation, substitution
alphabet, and choice of per-message starting phases, conditional only on the
same strong last-family repeated-plaintext identification used by the group
analysis.

The observed context permutations still cannot distinguish `A83` from `S83`.
Every strong map leaves at least two sources and targets unassigned, so an
explicit completion can be made even or odd by exchanging two unobserved
assignments. The two length-30 last-family maps force at least 25
transpositions overall (26 for an even completion) and support sizes of at
least 42 and 43, but both remain compatible with either sign.

The first trigrams are now strongly identified as metadata rather than ordinary
encrypted prose. Subtracting one from each first digit turns the first/middle
pair into a directed edge on three states. Rotating the canonical order to
begin with East 5 produces an exact eight-edge trail through all nine messages,
and East 5 is the unique perfect cyclic start. The exact fixed-rule,
without-replacement null is `1.9864e-6`; a seeded one-million-trial scan allowing
any pair of digit positions and any integer offset found a comparable post-hoc
rule in 248 trials (`2.48e-4`).

Removing the distinct markers reveals a complete nested prefix hierarchy, not
just the three previously documented families: all nine messages share two
values; East 1/West 1/East 2 share 24; the other six share five; East 3/East
4/West 4/East 5 share nine; and East 4/West 4/East 5 share 20. This tree is
exact corpus structure and should constrain any proposed message semantics.

A snapshot/delta audit sharpens that constraint.  For the two deepest sibling
trios, fixed-coordinate substitution/truncation alignments lose only 12 edits
to unrestricted Levenshtein alignments; only 5 of 2,000 suffix shuffles that
preserve the complete prefix tree do as well (`6/2001 = 0.0029985`).  The
later equalities are not concentrated in the displayed 26-column geometry,
so this supports position-synchronous copying or encryption, not a visual row
edit scheme.  Compressing the three-way equality relation produces a natural
five-state tape, but direct base-five and two-tape Polybius decoders are
selection-corrected negatives.

The remaining marker digit supplies a second order. Its sorted multiset is
exactly `0,0,1,1,2,2,3,3,4`; sorting messages by ascending `(third, first)`
gives `E1,W1,E2,W2,E4,W4,E5,E3,W3`, in which every non-singleton prefix-tree
cluster is contiguous. The two roles compose rigidly: among all `9!`
assignments of the observed marker multiset to the fixed messages, the observed
assignment is the only one satisfying both the fixed East-5-first trail and
the fixed trie-compatible sort. Even allowing any trail rotation and any
signed two-digit lexicographic key leaves only `22/9! = 6.06e-5`. This decodes
two message orders, not the body cipher.

Those two orders are precisely the two columns needed for a cyclic BWT. In
East-5-first trail order the remaining digits form last column `300113422`;
stable sorting gives first column `001122334` and the trie-compatible message
order. The LF map `(6,0,1,2,3,7,8,4,5)` is one cycle. Inversion from row zero
(East 5) restores `001123243`, whose base-five values are `(1,38,73)` and whose
ASCII+32 rendering is `!Fi`, or `Fi!` up to cyclic rotation. Exact enumeration
gives:

| Conditional universe | Total | One LF cycle | Valid `0..82` trigrams | Exact `!Fi` |
|---|---:|---:|---:|---:|
| distinct observed payload orderings | 22,680 | 2,520 | 1,031 | **1** |
| observed-marker assignments retaining the fixed trail | 168 | 37 | 14 | **1** |

The LF traversal also fixes a body order
`E5,W3,W4,E3,E4,W2,E2,W1,E1`; associating message identities with the restored
digits fixes the reverse order `E1,W1,E2,W2,E4,E3,W4,W3,E5`. Neither acts as a
usable continuous-state key in the tested deck family: both orders, with and
without markers, over all 6,806 affine and 8,430 standard bases produce 60,944
candidates, bottoming out at 81 decoded instructions and 177 of 230 repeated-
context mismatches.

The result composes discoveries made independently of BWT, but `Fi` still has
interpretive ambiguity. The Finnish reading is supported by matched n-gram
controls; simple Fibonacci differencing, all 6,889 two-lag linear recurrences
over `F_83`, and `FI`/`FINNISH`/`FIBONACCI` keyed initial-deck scans all fail.
Treating each body itself as a BWT last column also fails the LF-cycle and exact
round-trip checks. A stronger raw-eye composition also fails exhaustively:
inverse MTF on the individual `0..4` eyes followed by cyclic BWT, with all 120
initial lists, six marker-digit orientations, and three index adjustments,
rejects all 2,160 candidates on the first message's exact round-trip test.

Concatenating the nine marker-free bodies in canonical order has LF cycles
`(1026,1)` over 1,027 values. Deleting any of three individual values makes one
cycle, but all three primary-row-zero inverses are visible gibberish. This is a
calibrated near miss: 10 of 10,000 seeded prefix-tree-preserving parity shuffles
have the exact same `(1026,1)` pattern, while five are even one-cycle BWTs. It
does not provide a plaintext.

There is a striking, but not yet calibrated, way in which the two metadata
discoveries compose. Put East 5 first as required by the marker chain, traverse
the non-singleton prefix trie breadth-first, and read its cumulative depths by
A1Z26: `2,5,24,9,20` becomes `BEXIT`. Dropping the universal root gives the
literal word `EXIT`; alternatively the leading `B` can specify the
breadth-first traversal. If the three marker eyes are treated as directions on
the canonical 3x3 message grid, all three fields starting at East 5 do exit:
the first and middle fields follow East 5→West 3→East 2 and leave north and
east, while the third leaves south immediately. East 5 is not unique: East 3
and West 3 also have the complete north/east/south signature. Exactly 312 of
the `9!` assignments of the observed marker multiset to this grid produce
three such starts; a one-million-trial uniform-marker simulation found 75.
These are exact or reproducible facts, but the A1Z26/traversal/grid target was
selected after inspection and has not yielded plaintext. Using `EXIT`, `NES`,
or their concatenation literally as an ASCII+32 keyed deck also fails: the simple
adaptive transforms retain 82 symbols, and 30,472 full/reset candidates over
15,236 unique affine and standard bases bottom out at 81 instructions and 89
of 230 equality mismatches, no better than the unkeyed structured searches.

The depths also suggest concrete English cribs. `THAT WHICH IS ABOVE IS LIKE
TO` is exactly 24 normalized letters, but completing the opposite branch as
`THAT WHICH IS BELOW...` creates a key-free perfect-isomorphism contradiction
on repeated `HICHI`: its ciphertext patterns are `.....` and `A...A`. That
obvious Emerald Tablet plaintext is rejected under the public GAK model. A
different lower-branch prefix, `THERE IS NO GOOD THAT CAN` (exactly 20 letters
and verbatim from Mead's *Corpus Hermeticum VI*), survives the same test across
East 4/West 4/East 5, with East 3 sharing `THERE IS NO`. It remains a crib,
not a recovered plaintext; a three-volume Mead sentence scan does not reproduce
the complete nine-message prefix tree. The upper and lower assignments also
survive the key-free test when combined. In the concrete identity-base sparse
deck model, the lower 20 letters have an explicit verified two-transposition
key. Requiring the first ten upper letters and all 20 lower letters to share
that one-hidden-swap construction is exactly unsatisfiable, but two and then
three hidden swaps give shared witnesses. An exhaustive coordinate descent
from the independently solved 14-letter seed extends the
four-transposition-scale construction to the full 24 upper plus 20 lower
letters in seven rounds; a materialized-deck regression test verifies the
result. It immediately fails the held-out lower continuation `BEGOT` at all
five positions. Greedy refitting stalls with two mismatches and three exact
solver seeds time out. The full witness therefore demonstrates flexibility,
not a recovered plaintext; the best nontrivial base and general GAK remain
open.

A distinct `THAT WHICH` lead survives its first audit. Waite's 81-character
sentence `SUBLIME THAT WHICH IS THE LOWEST, AND MAKE THAT WHICH IS THE HIGHEST,
THE LOWEST.` fills East 2 exactly from raw offset 37 and aligns its repeated
phrase with the message's raw 45/80 isomorph. Every repeated substring in the
candidate passes the necessary perfect-isomorphism check; the longest is
`E THAT WHICH IS THE ` at length 20. The game's byte-identical early-access
and current `orb_plan.txt` explicitly cite the *Hermetic Museum*, which contains
the source tract. This makes the crib source-backed and chronologically
plausible, though the archive was uploaded in 2022 rather than timestamped
contemporaneously; it is still not a decryption or a held-out prediction.
An OCR scan of both Waite volumes finds source pairs at all three observed
`THAT WHICH` gaps (`28,30,35`).  Complete-message alignment is stricter:
several windows pass separately, but no three-message combination passes the
cross-message perfect-isomorphism condition (the best has eight conflicts).
Thus the phrase/suffix lead remains open while the hypothesis that all three
complete plaintexts are contiguous Waite excerpts is rejected under exact
GAK/XGAK.

The complete East-2 body candidate also fails a finite reset-deck search:
8,598 distinct standard bases times 26 top/anchor/ring/mirror variants give
223,548 models and zero exact fits.  The best breaks 517 of 542 required
same-character relations.  This rejects that small physical-deck family, not
arbitrary plaintext-selected permutations.

The exact six-window boundary is now certified.  All six ciphertext windows
share one equality-pattern class through length 10 and split into two classes
at length 11.  In Waite's corpus, meanwhile, the unique longest string repeated
at all three gaps is ` THAT WHICH IS ` (15 characters).  Consequently the
ten-character `THAT WHICH` core remains possible, but a common `IS …`
continuation across all three messages is impossible under perfect GAK/XGAK.
East 2 may still use Waite's longer suffix independently.

A bounded higher-order variant changes that conclusion without solving the
cipher.  The two-symbol memory length came from an intentionally artificial
community counterexample, not an independent prediction from the Eyes.  If the
update remembers the two preceding plaintext symbols, the first two ciphertext
outputs of a repeated phrase may differ; after trimming those two, all six
windows remain isomorphic through raw end 17.  This makes
the shared 17-character `THAT WHICH IS THE` compatible with a two-symbol-memory
model.  In a conditioned no-adjacent-double null that freezes the selected
ten-symbol isomorph, 2,634 of 200,000 trials extend seven more symbols
(`1.317%`).  A corpus-wide scan over repeat-rich seeds of lengths 6–14 finds no
independent replication: every positive gain is a shifted view of this same
six-window episode.  The extension is therefore a useful model constraint,
not independent plaintext evidence or a recovered key.

A limited matched-text calibration makes the source fingerprint non-routine:
Waite reaches length 15, while none of 17 Project Gutenberg alchemy controls
or nine non-overlapping controls matched to Waite's 1,318,231 normalized
characters exceeds length 12.  This is not a discovery p-value because the
source, gaps, and candidate were selected retrospectively.

The East-5-first order does not behave like a persistent state for the concrete
deck construction tested here. Continuous scans over all 6,806 affine bases
and all 8,430 non-duplicate standard physical/near-size bases, at every cyclic
start, have a minimum decoded alphabet of 81 instructions; the best such
candidates miss 176 and 177 of 230 equality comparisons respectively. East 5
is not the best start in either scan. The order clue is therefore metadata
under these models, not a continuous-state key. Concatenating messages in the
new trie-compatible marker order does not help: affine and standard scans still
need at least 82 and 81 ranks; with markers removed the best standard candidate
misses 178 of 230 equality constraints.

The sparse hidden shuffles were also made non-formulaic. Starting from the best
full-stream standard base, each coordinate round exhausts all 3,321 non-top
transpositions for every currently decoded instruction and commits the single
best rule. The calibration has a sharp boundary: on synthetic messages made
with that same base, it exactly recovers one active rule in one round
(`9/230` equality misses and 48 body ranks to `0/230` and 26), and all five
active rules in five rounds (`44/230`, 66 ranks to `0/230`, 26). With 26
simultaneously active rules the greedy search does not enter the planted basin.
On the real corpus, ten exhaustive rounds improve the base from `87/230` to
`65/230` misses but leave all 82 body ranks. This rejects a key only a handful
of arbitrary sparse-rule changes away from that particular base; it does not
exclude a dense 26-rule key, multiple hidden swaps per action, or an unknown
base.

There is now a second, independent marker clue. The complete ciphertext sums
of East 1, East 3, and East 5 are `4040`, `5656`, and `4545`, with common gcd
101; equivalently, their initial values `50`, `63`, and `33` are exact mod-101
check digits for their respective message bodies. They are the unique
three-message subset with a gcd this large. Under independent uniform values,
the fixed odd-East event has exact probability `4.1178e-5`; allowing any
post-hoc triple raises the estimated probability to `0.00342`. Among all 36
parity-aware triangle reading orders, only the accepted order has this checksum
and the canonical `0..82` range. This strongly supports intentional metadata
and the numeric reading, but still does not identify the cipher key.

Two conditional checks sharpen, but do not turn, that clue into a solution. If
the observed body sums and marker multiset are held fixed, exactly
`720/362880 = 1/504` marker assignments put the checksum on all three natural
family representatives. Shuffling the observed values into the fixed message
lengths gives fixed-diagonal rates of `2e-5` (whole stream) and `4e-5` (markers
held fixed) in 100,000 seeded trials. These are related conditional views, not
independent p-values to multiply.

All nine complete sums also avoid divisibility by every two-digit prime
(`11..97`). The exact independent-uniform-sum baseline at the nine observed
lengths is `0.004699414767`. Holding the bodies and marker multiset fixed,
`938/362880` assignments retain that avoidance, `720/362880` retain the
odd-East mod-101 checksum, and only `18/362880` retain both. This makes the
marker-as-check-data interpretation more plausible, but the divisor set was
noticed after inspection and these overlapping statistics must not be
multiplied as independent evidence.

The engine trail was also audited. The public decompilation and installed
release executable contain no
plaintext or runtime encryption: it selects nine hardcoded arrays of 64-bit
constants, removes a base-7 padding digit, subtracts one from the remaining
digits, reverses them, and hands the resulting `0..5` stream to the renderer.
The paired `noita_dev.exe` contains none of the first twelve 32-bit halves of
the Eye payload, indicating that the secret payload is release-build-specific.
The storage boundaries themselves are now closed as an independent channel:
greedily packing the longest prefix of visible row symbols plus newline that
fits in an unsigned 64-bit word reproduces all 150 published engine constants
exactly (fixture SHA-256
`5de6ccb3a045218827b7ddaad0f1493254f501b08addd1929495ce060242de94`).
The 21/22-symbol capacity choices are forced by overflow, and a literal binary
reading of them is ordinary under fixed-weight controls.
The installed `data.wak` has 14,745 indexed files but no named or textual link
from the Eyes to the candidate ciphers or sources. Its five `eyespot` objects
are explicitly the Evil-Eye/tripping reveal mechanism for the Sun-seed books.
A semantic diff against the March 2023 data snapshot isolates 481 additions and
225 modifications through the January 2025 build; the eye-, secret-, music-,
book-, cauldron-, and puzzle-named subset supplies Cessation and other known
quest mechanics, but no Eye-message handler or decoder key. This cannot exclude
a clue encoded only in visuals, native code, or an innocuously named mechanic.

Native-code reconstruction closes two more bounded visual branches. The Eye
renderer has exactly five 11x7 solid-colour glyph masks plus newline—centre,
up, right, down, and left—with no hidden sixth glyph. An exhaustive scan of all
9,028 real PNGs in the installed archive finds no exact copy of any mask at
nearest-neighbour scales 1 through 4; the only two `.png` decode failures are
two-byte CR/LF placeholders. This excludes literal asset reuse, not a redrawn,
rotated, antialiased, procedural, or compositional clue.

The placement code also explains the known overlap world seed exactly. It XORs
the world seed with `0x0e4bc7e0` (`239847392`); choosing that same world seed
feeds zero into the RNG normalizer, which maps it to the modulus
`2147483647`, a fixed point. Consequently all five East messages occupy the
same coordinates and all four West messages occupy their mirrored coordinates.
Unioning the native direction marks yields all 31 nonempty five-bit masks in
the East composite and masks 1 through 30 in the four-layer West composite.
Direct base-32/letter/byte readings are gibberish, and the East best-printable
byte count is ordinary under a 1,000-trial position-shuffle null
(`118`, median `117`, `p=0.4296`; West is worse than its null median). The seed
is intentional placement behavior, but the literal overlaid mask stream is not
a decoder under these natural readings.

The most concrete passive in-game coincidence is the layout width. Every
complete interleaved visual row-pair contains exactly 26 trigrams, and both the
archived early-access and current procedural-wand scripts clamp ordinary wand
deck capacity to 26. That makes wand/deck vocabulary worth retaining even
though rare or special wands can exceed it. A direct implication is now
negative: resetting the leading common-base/top-swap deck at each row-pair
misses at least 100 of 230 repeated-context equalities and still needs all 83
instructions; selected-card variants miss at least 109 and need 82. Thus 26 may
hint at a plaintext alphabet or deck concept, but is not a row-reset rule in
these mechanisms.

Noita's current English localization was checked as a possible built-in crib.
Among 3,413 strings, seven happen to equal an Eye-message length under each of
two normalizations, but none has the complete first-family repeat fingerprint.
The exact-length matches are therefore unsupported coincidences.

The complete Finnish Project Gutenberg catalog was also checked, book by book,
under both letters-only and space-preserving normalization. All 3,648 texts
loaded successfully. Among 2,631,331 and 2,772,407 candidate passages in the
Eye length range, respectively, there are zero complete exact-length
`2/24/5/9/20` prefix trees. Letters-only normalization has no upper-24 partial,
five lower-20 partials, one nested-9 partial, and no lower-6 or joined root;
space-preserving normalization has `0/2/1/0/0`. Seven letters-only repeat
fingerprints are rotations of the bibliography abbreviation `Pipp. l. N:o` in
book 53047; three space-preserving hits are rotations of the repeated line
`Ooppee Mikko Hetta` in book 57770. None is a literal source candidate.

## Running the workbench

Python 3.11 or newer is sufficient for the dependency-free experiments:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 scripts/report_isomorphs.py
PYTHONPATH=src python3 scripts/search_field_models.py
PYTHONPATH=src python3 scripts/search_gaussian_walks.py
PYTHONPATH=src python3 scripts/search_deck_models.py
PYTHONPATH=src python3 scripts/search_affine_base_decks.py
PYTHONPATH=src python3 scripts/search_standard_base_decks.py
PYTHONPATH=src python3 scripts/search_row_reset_decks.py
PYTHONPATH=src python3 scripts/scan_chaocipher.py
PYTHONPATH=src python3 scripts/search_hidden_swap_decks.py
PYTHONPATH=src python3 scripts/search_multi_hidden_swap_decks.py
PYTHONPATH=src python3 scripts/optimize_sparse_deck.py --base affine-82-fixed82-15-17 --rounds 1
PYTHONPATH=src python3 scripts/search_continuous_affine_decks.py
PYTHONPATH=src python3 scripts/search_continuous_standard_decks.py
PYTHONPATH=src python3 scripts/search_keyword_initial_decks.py EXIT
PYTHONPATH=src python3 scripts/check_metadata_plaintext_cribs.py
PYTHONPATH=src python3 scripts/analyze_initial_markers.py
PYTHONPATH=src python3 scripts/analyze_marker_orders.py
PYTHONPATH=src python3 scripts/decode_marker_bwt.py
PYTHONPATH=src python3 scripts/search_bwt_order_decks.py
PYTHONPATH=src python3 scripts/search_raw_bwt_mtf.py
PYTHONPATH=src python3 scripts/audit_lumikki_hash.py
PYTHONPATH=src python3 scripts/audit_noita_binary.py /path/to/noita.exe /path/to/noita_dev.exe
PYTHONPATH=src python3 scripts/scan_noita_wak.py /path/to/data.wak --path-regex 'eye|glyph'
PYTHONPATH=src python3 scripts/analyze_overlap_seed.py --null-trials 1000
PYTHONPATH=src python3 scripts/scan_azazel_corpus.py --cutoff 2020-10-15
PYTHONPATH=src python3 scripts/analyze_body_bwt.py
PYTHONPATH=src python3 scripts/analyze_cipher_clock.py
PYTHONPATH=src python3 scripts/search_cipher_clock_ring.py --language-corpus /path/to/finnish.txt
PYTHONPATH=src python3 scripts/report_prefix_hierarchy.py
PYTHONPATH=src python3 scripts/analyze_context_completions.py
PYTHONPATH=src python3 scripts/checksum_null.py
PYTHONPATH=src python3 scripts/scan_reading_order_checksums.py
PYTHONPATH=src python3 scripts/prove_c41_last_contexts.py
PYTHONPATH=src python3 scripts/prove_c82_combined_contexts.py
PYTHONPATH=src python3 scripts/prove_permutation_progression_unsat.py
PYTHONPATH=src python3 scripts/scan_noita_localization.py /path/to/common.csv
PYTHONPATH=src python3 scripts/check_known_plaintext.py /path/to/lines.txt
PYTHONPATH=src python3 scripts/report_deck_invariants.py
PYTHONPATH=src python3 scripts/optimize_base_deck.py --reset-marker
PYTHONPATH=src python3 scripts/optimize_permutation_progression.py
PYTHONPATH=src python3 scripts/optimize_hermetic_crib_key.py --rounds 8
PYTHONPATH=src python3 scripts/search_lumikki_source.py
PYTHONPATH=src python3 scripts/test_two_symbol_memory.py
PYTHONPATH=src python3 scripts/analyze_delayed_isomorph_groups.py --base-length 6 --maximum-base-length 14
PYTHONPATH=src python3 scripts/analyze_suffix_row_hypothesis.py
PYTHONPATH=src python3 scripts/analyze_conformance_grid.py
PYTHONPATH=src python3 scripts/analyze_breadth_probes.py
PYTHONPATH=src python3 scripts/test_s3_context_relations.py
PYTHONPATH=src python3 scripts/analyze_s3_direction_transducer.py
PYTHONPATH=src python3 scripts/analyze_trie_checksum.py --samples 200000
```

The vectorized selected-card scan additionally requires NumPy:

```sh
PYTHONPATH=src python3 scripts/search_selected_card_shuffles.py
```

The exhaustive native-glyph asset scan additionally requires Pillow and NumPy:

```sh
PYTHONPATH=src python3 scripts/scan_noita_eye_bitmaps.py /path/to/data.wak --max-scale 4
```

The exact solver scripts additionally require the `solver` extra (equivalent to
installing `z3-solver`):

```sh
python3 -m pip install -e '.[solver]'
PYTHONPATH=src python3 scripts/solve_affine_gak_enum.py --mode skip --max-symbols 27
PYTHONPATH=src python3 scripts/test_affine_isomorph_embedding.py --families last
PYTHONPATH=src python3 scripts/solve_common_base_swap.py --contexts combined
PYTHONPATH=src python3 scripts/solve_sparse_crib_z3.py --messages east1,east4 --omit-markers --top-length 10 --lower-length 20 --timeout-ms 120000
PYTHONPATH=src python3 scripts/calibrate_arbitrary_gak_sat.py --deck-size 14 --messages 3 --length 18 --timeout-ms 30000
```

The alternating-substitution experiment accepts a local public-domain language
corpus rather than bundling one:

```sh
PYTHONPATH=src python3 scripts/solve_affine_substitution.py --language-corpus /path/to/english.txt
PYTHONPATH=src python3 scripts/solve_affine_substitution.py --language-corpus /path/to/finnish.txt --encode-finnish-diacritics --omit-markers --center-mode reflection --translation-pair 3 1 --up-order 312 --down-order 231
PYTHONPATH=src python3 scripts/fingerprint_source_corpus.py '/path/to/texts/*'
PYTHONPATH=src python3 scripts/scan_gutendex_fingerprints.py --search noita
PYTHONPATH=src python3 scripts/scan_gutendex_message_tree.py --search noita
PYTHONPATH=src python3 scripts/scan_gutendex_message_tree.py --catalog-csv /path/to/pg_catalog.csv --max-books 5000 --same-book --repeat-fingerprint --workers 16 --normalization both
```

See `docs/research-log.md` for measured outputs, null tests, sources, and the
next tractable questions.
