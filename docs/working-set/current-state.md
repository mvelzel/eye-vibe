# Current Eye-mystery state

**Snapshot:** 26 July 2026  
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
- The renderer stores packed base-seven rows and renders nine precomputed
  arrays; it does not decrypt at spawn time.

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

Direct factoradic body consumers tested so far are negative. The structure is
a header type system, not yet a decoder.

## Promoted locale field

The nine scalar digits form rows `(0,0,1)`, `(1,3,4)`, `(2,2,3)`.

Natural column sums give `+358`; the fixed marker trail and inverse BWT give
`!Fi`. A generic calling-code/region audit finds the observed
`358 -> FI/AX` and `!Fi` match uniquely among the 12,096 admissible
assignments. The other coordinate planes sum to `683 -> NU` and `034 -> ES`.

Interpret this as a redundant Finnish/Finland locale marker. It does not by
itself establish Finnish body plaintext or authorize `FI358` as a key.

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
multiplicity/reuse relabeling gives `1/12`. Thus the control cycle is
`27 ->(+3) 30 ->(+4) 34 ->(+29,+13) class15 ->(W4-E4) 27`.

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
`002+040=003+031+3`, echoing Gate `+3`. Prospective visible-label transfer
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

## Later Gate/WAK corroboration

The Gate Guardian postdates the October 2020 Eye Messages and is eligible only
as a later decoding/construction hint. Veska objectively supplies upper
`1,5,3 ->153`, lower `+3`, and `153,(153+3) mod83 -> f,i`.

The current-WAK chest RNG salts independently render as `+3` under the Eye
alphabet and repeat `683 -> NU`; they were introduced in March 2023.

Veska `1,5,3` has one valid late-state/suffix parse under all class, split,
width, and component-permutation controls: terminal class `15`, E4 loop width
`3`. Its lower `+3` then executes the closed restart `27+3=30`, while the same
marks redundantly retain `153,+3 -> fi`.

The previously missing self-field result closes through measured phases:

```text
final row +3             (27,77,33) -> (30,80,36)
E4 bridge repair +20                  (50,80,36) = row 1
```

Here `30` is the late common-phase length and `20+30=50`. The fixed full
closure occurs in `22/12096` conditional scalar assignments; allowing every
row pair, self slot, bridge length, and target permutation gives `34/12096`.
Scanning all 82 shifts leaves only this `+3` construction. It selects the
observed of two factoradic survivors. The source-pair delta and phase sum both
equal `50`; the late source-pair boundary `34` is exactly the West3 marker.

The dossier's Type4/Type6 cache machine remains unproved. In particular, the
Seula 70-pixel residual, exact `12+43+9+8` Veska partition, side-band scope
rules, and first-seen Type6 allocator are not independently executable.
The two non-self transfers still have different factoradic quotients, so this
is a header/state repair—not a body-wide shift or complete Gate decoder.

## Other construction facts worth retaining

- The complete body prefix trie closes exactly modulo 101. Direct recursive,
  automaton, and failure-link consumers tested so far do not explain it.
- NollaArvi directly attributed the Eye secret to Petri Purho in April 2021.
  Petri's 2015 triangle renderer predates the Eyes, but its polygon windings
  conflict with the accepted order. It corroborates only alternating-triangle
  topology, not the cipher; Gate and cauldron authorship remain unproved.
- Equality/reconvergence structure and copied openings are real and must be
  preserved by any decoder. Fixed substitutions that destroy them are poor
  models.
- Direct fixed `3,5,8` body weighting is negative.
- The existing equality-derived context graph is a forest, so a claimed
  holonomy around its derived triangles is tautological.

## Practice-puzzle calibration

sdlwdr #1, #2, and #5 are solved; #3 is unresolved after broad progression,
wheel, recursion, and deck negatives; #4 has a recovered outer 57-cycle but
unresolved codec. Its low aligned-symbol count is a weak phase-selection clue
(`.012627`), while high bigram IoC is null-ordinary (`.314659`). #6's direct
asset-driven families are negative. Transfer only a recovered operation and
demand exact replay.

## Interpretation boundary

The compact current model is:

1. orthodox trigrams are correct;
2. first trigrams are a typed, redundant locale/check header;
3. the final row contains an exact self-describing body landmark record;
4. later game assets plausibly restate some marker operations;
5. the body machine and plaintext remain unknown.

Do not collapse these layers into one cipher without a held-out prediction.
