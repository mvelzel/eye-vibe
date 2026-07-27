# Current Eye-mystery state

**Snapshot:** 27 July 2026
**Outcome:** unsolved; no validated plaintext or complete body decoder.

This file contains only the facts needed to resume reasoning. Exact evidence
and reproduction paths are in [`evidence-map.md`](evidence-map.md).

## Canonical object

- Nine messages are rendered as triples of five eye directions.
- The orthodox trigram rank is `25a+5b+c`.
- Only ranks `0..82` occur, although three base-five digits could represent
  `0..124`.
- The normal trigram reading is strongly selected among geometric reading
  variants and preserves the shared openings and known isomorphs.
- The installed 2025 binary's nine-way initializer contains all 150
  independently packed base-seven corpus words exactly. It unpacks them for
  rendering and performs no runtime decryption.
- Its sole direct caller passes only `(x,y,panel 0..8)`; a side-parity filter
  routes the five East and four West panels. No caller-supplied key exists.

## Promoted marker/header structure

The first trigram of each message is structured metadata, not an ordinary body
symbol.

Canonical rows are `(50,80,36)`, `(76,63,34)`, and final
`(27,77,33)`.

Treating each rank as a lexicographic permutation of the five eye codes plus
newline gives:

- row 1 as named `r,s,r^-1`, generating D4;
- the six remaining Q headers generating S5 on the noncenter symbols;
- the side-specific newline/coset classifier;
- two scalar assignments among 12,096 graph-conditioned assignments, one
  class after the only duplicate-edge swap.

Direct factoradic body consumers are negative: this is a header type system, not
yet a decoder. No source-, target-, or relative-header element can induce all
five nonliteral cross-panel maps; West4's seven-vertex path exceeds every header order.

## Promoted locale field

The nine scalar digits form rows `(0,0,1)`, `(1,3,4)`, `(2,2,3)`.

Natural column sums give `+358`; the fixed marker trail and inverse BWT give
`!Fi`, while the same digits describe the alphabet cut `83=3×5²+8`. A generic calling-code/region audit finds the observed
`358 -> FI/AX` and `!Fi` match uniquely among the 12,096 admissible
assignments. The other coordinate planes sum to `683 -> NU` and `034 -> ES`.

Interpret this as a Finnish/Finland locale marker with a retrospective
serialization echo; it does not establish Finnish plaintext or a `FI358` key.

## Promoted final-row record

After removing each marker and copied 20-symbol opening, the final messages
have unique gap-11 `(anchor,start)` records: E4 `(75,16)`, W4 `(81,18)`,
E5 `(48,17)`.

Their marker values are exact mod-83 differences:

```text
27 = 75-48
77 = 75-81
33 = 81-48
27 = 77+33 mod83
```

The starts are `16+(0,2,1)`, matching W4's independently defined component
order `021`. E4's repeat endpoint is trimmed position 27, equal to its marker;
converting frames fixes anchor 48 and closes the additive gauge.

This is a self-describing typed checksum/pointer record. It is the strongest
body-facing construction fact, but it is metadata rather than plaintext.

The exact final grammar does not transfer to earlier rows:

- row 1 has zero circulation but an incompatible target-rank field;
- row 2 has nonzero circulation residue `7`;
- only the final row satisfies the complete grammar.

## Promoted two-phase state trace

From each gap-11 endpoint to the independently known late-context entry, the
final bridges have lengths `(20,21,20)`. Their equality signatures share an
exact 17-position prefix. E4/E5 then share a complete 20-position bridge;
the first next pair conflicts and begins the known common 30-position phase.
W4 follows the shared trace through 17, then has a four-position suffix.
No matched, East-conditioned, or broadened control recurs in 50,000 trials
(`1/50001`). This promotes a reset, shared phase, typed suffix, exact map
switch, and second shared phase.

The final header control edges are E4 `0->0`, W4 `0->2`, E5 `1->0`.
Before the switch, the longest pair is the common-target E4/E5 scope:
`17+3=20`. After it, the longest pair is the common-source E4/W4 scope:
`30+4=34`. The E4 loop is the pivot, and the extensions match the target- and
source-mate suffix widths. This promotes a target-to-source scope switch.

The typed suffixes `(3,4,3)` consume two header fields:

```text
suffix + factoradic newline preimage = row-2 circulation
(3,4,3) + (4,3,4) = (7,7,7)
```

The generic ledger holds in 159/12,096 scalar assignments. All exact-suffix
matches use newline; any symbol/suffix placement gives 694/12,096. It selects
only the observed of two full factoradic survivors. Treat seven as a
phase-width budget and newline preimage as a schedule field; the state update
and body-label semantics remain unknown.

Literal transfer to row 2's copied-opening exit remains negative (`.0215`
exact, `.4000` broad). Row 2 instead encodes the terminal repeat of the late
common phase. From the source-pair boundary 34, the terminal zero-based
position is 29 and its back-reference distance is 13:

```text
34+29=63
63+13=76
```

This is the reverse-cycle order West3 -> East3 -> West2. It is the only hit
after allowing every row, order, repeat event, and increment sign. The fixed
record occurs in `126/12096`; combined with the phase topology it leaves only
the observed scalar assignment.

The selected terminal class15 labels are E4 `40`, W4 `67`, E5 `21`. The
already fixed source direction returns `67-40=27 mod83`, exactly the E4 loop
header. It is the only fixed-direction repeat returning 27; a matched
multiplicity/reuse relabeling gives `1/12`. This closes an Eye-only return to
header27. No Eye-derived operation currently selects the transition from 27
to phase boundary30; the earlier Gate-`+3` completion is unpromoted.

The positive middle-eye-only classes `5,10,15,20 = 010,020,030,040_5`
all repeat by boundary34; the other single-coordinate axes do not. Their
repeat order is directions `1,4,3,2`, exactly counterclockwise from up.
Class10 completes the missing right direction at the E4/W4 conflict, and its
cached W4->E4 label difference returns West4 marker77. Direct D4 transforms
of the `5×5` coordinates or visible eye trigrams are negative; even 18,432
independent-eye models fit at most 3/25 cells and fail the class10 holdout.
Adaptive cache policies also fail: a 55,360,004-model affine-deck family fits
at most 7/30 training symbols. Equality alone leaves `P(83,25)`, about 153.6
bits, of fresh-label choice and therefore cannot be the allocator input.
Cross-panel mod-83 models fit at most 7/23 and three-eye arithmetic 4/23;
all co-best models fail withheld control class10 and phase class24.

The third-eye classes `1..4` have scoped roles
`common,source,target,absent`, clockwise from up. Headers
`102,302,113_5` type source scalar2 and target scalar3; the two closed E4/E5
branch checks return `(3,2)` in reciprocal order. The first is the carry
`002+040=003+031+3`. Prospective visible-label transfer
scores `0/2`; strict stack/queue/deque and static `5×5` code models are also
negative. Direct transfer to six other registered contexts scores `0/4`.

Across the promoted final map switch, the same visible value links independently
canonicalized old/new classes. The only edge shared by any panel pair is
`7->24`, present in both East panels with different labels and absent West.
It was independently selected by `7+17=24`; East's newline preimage then puts
class 24's unique first occurrence at `24+4=28`. Under a null preserving both
equality signatures and all overlap multiplicity types, the exact East-pair
probability is `3/33800` (`.000088757`); any shared edge is common (`.1010`),
but any pair sharing an offset-17 edge has matched-control rate `.00136`.
Promote one preserved state/cache correspondence, not a general update map.

## Later-asset hypotheses (unpromoted)

Gate and current-WAK could be later clues, but Veska/WAK numerical matches
supply neither a complete asset-to-Eye mechanism nor a holdout and cannot
corroborate one another. Veska's raw marks give total72 and 9/8 bands, while
the objective remainder is 11/44, not the dossier's 12/43.

A frozen census also closes the reported 1.0 companion shortlist: its current
assets are binary, decorative, unordered, or passive rather than an Eye
interface. The historical fingerprint and `1402/145/980` WAK census remain
external reports because the paid historical depot requires authentication.

## Quotient-addressed table hypothesis

The checksum quotient can address each panel's first83 values as a functional
table. Nine orbit sizes total72; closing E1/E3/E5 give tail/cycle `8/12`,
multiplicity/union `20/17`, and cycles `1,4,7`; the union omits32 labels, E4's
remainder. These are dependent outputs of one retrospectively found operation.

Eye-only checks bound it. Source digit2 selects both tail-free walks, but any
simple header class does so in `.1740` of controls. Physical-row totals are
`(13,23,36)`, with `13+23=36=E2 header`; the broad rate is `.000896`. Retain
the anomaly, not a construction mechanism. No honest internal holdout remains;
reopen only if an authored Eye interface independently selects the operation.

## Other construction facts worth retaining

The body prefix trie closes modulo101, though direct consumers fail. Natural-trim
recurrence minima are `333|222|444` with tail `.00073`; Petri's renderer fails.

Waite's East-2 suffix is impossible under ordinary GAK. Distinct-selector XGAK
replays it but admits a frozen wrong next card. Local `THAT WHICH` fits GAK;
574/1,000 connected fills survive. Fixed-disk Wadsworth also fails.

A direct visible-state permutation-action model has exact support minimum19,
even after aligning the registered isomorphic passages. It is non-identifying:
after the unique source26 pivot names all actions, every one of 858 other
classes can change color alone. This is capacity, not a decoder. Adjacent
hidden-cycle pair geometry remains `18 SAT / 0 UNSAT / 3 UNKNOWN`.

## Wall-message lead and practice calibration

The 12 exact Wall PNGs contain one static 29-symbol `4x4` codebook: no
per-occurrence pixel channel or metadata survives. Visible-feature Baconian,
practice-Morse, XOR, and direct 83-bit/isomorph consumers are negative.
Chronology is eligible. Wall counts `(50 periods, 61 literal YOU + two explicit
omissions, 33 questions)` equal the three odd-East checksum headers
`(50,63,33)`. World-Y, zero-based indices into the 83 `you*` contexts select
preceding words `AND CREATED GOD`, uniquely in a frozen 16-convention family,
but the target is post hoc and the literal 83-entry table destroys four of six
canonical `THAT WHICH` signatures. Retain the count match, not a decoder.
sdlwdr #1/#2/#5 are solved; #3/#4 remain unresolved; #6's assets are negative.

## Interpretation boundary

The compact current model is:

1. orthodox trigrams are correct;
2. first trigrams are a typed, redundant locale/check header;
3. the final row contains an exact self-describing body landmark record;
4. later-asset clue theories remain unvalidated and separate;
5. the body machine and plaintext remain unknown.

Do not collapse these layers into one cipher without a held-out prediction.
