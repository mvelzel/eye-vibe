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

Canonical ranks:

```text
row 1: 50 80 36
row 2: 76 63 34
final: 27 77 33
```

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

The nine header scalar digits form:

```text
0 0 1
1 3 4
2 2 3
```

Natural column sums give `+358`; the fixed marker trail and inverse BWT give
`!Fi`. A generic calling-code/region audit finds the observed
`358 -> FI/AX` and `!Fi` match uniquely among the 12,096 admissible
assignments. The other coordinate planes sum to `683 -> NU` and `034 -> ES`.

Interpret this as a redundant Finnish/Finland locale marker. It does not by
itself establish Finnish body plaintext or authorize `FI358` as a key.

## Promoted final-row record

After removing each marker and its copied 20-symbol opening, the final three
messages contain unique clean gap-11 repeats:

```text
message  anchor  trimmed start
E4       75      16
W4       81      18
E5       48      17
```

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

## Later Gate/WAK corroboration

The Gate Guardian postdates the October 2020 Eye Messages and is eligible only
as a later decoding/construction hint.

Objectively measured Veska bands:

```text
upper components: 1,5,3 -> 153
lower pictogram:  +3
153 mod83       -> f
(153+3) mod83   -> i
```

The current-WAK chest RNG salts independently render as `+3` under the Eye
alphabet and repeat `683 -> NU`; they were introduced in March 2023.

The `+3` operator acts coherently on the two non-self fields of the final Eye
record:

```text
77+3=80
33+3=36
```

It is the only nonzero shift completing any natural non-self row transfer on
the observed grid. Under the fixed conditional scalar null, the exact event
occurs `372/12096`; any ordered row pair gives `492/12096`.

The two transfers have different left and right factoradic quotients. This
supports a narrow scalar/check-field restatement, not one Gate-derived
factoradic instruction and not a body-wide `+3` shift.

The dossier's Type4/Type6 cache machine remains unproved. In particular, the
Seula 70-pixel residual, exact `12+43+9+8` Veska partition, side-band scope
rules, and first-seen Type6 allocator are not independently executable.

## Other construction facts worth retaining

- The complete body prefix trie closes exactly modulo 101. Direct recursive,
  automaton, and failure-link consumers tested so far do not explain it.
- A procedural wand generator independently selects exactly ranks `0..82`
  from an underlying `0..100` range; this is evidence that 83-of-101 is
  authored game vocabulary, not an Eye decoder.
- Equality/reconvergence structure and copied openings are real and must be
  preserved by any decoder. Fixed substitutions that destroy them are poor
  models.
- Direct fixed `3,5,8` body weighting is negative.
- The existing equality-derived context graph is a forest, so a claimed
  holonomy around its derived triangles is tautological.

## Practice-puzzle calibration

sdlwdr status:

- #1 solved and author-confirmed;
- #2 solved;
- #3 unresolved; simple progression, old-wheel, reflection-wheel, recursion,
  and large fixed deck families are excluded;
- #4 outer 57-cycle layer recovered, inner plaintext/codec unresolved;
- #5 solved with exact replay;
- #6 unresolved; direct Trailer-Altar/Earthquake rotating, cut, and Alberti
  families are negative.

The transferable lesson is to recover an operation from equality structure,
use language-independent scoring, and demand exact replay. Do not import a
practice plaintext or in-game asset merely because both use 83 symbols.

## Interpretation boundary

The compact current model is:

1. orthodox trigrams are correct;
2. first trigrams are a typed, redundant locale/check header;
3. at least the final row contains an exact self-describing body landmark
   record;
4. later game assets plausibly restate some marker operations;
5. the body machine and plaintext remain unknown.

Do not collapse these layers into one cipher without a held-out prediction.

