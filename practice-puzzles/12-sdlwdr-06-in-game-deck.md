# sdlwdr #6 — in-game-keyed deck cipher

**Status:** Unsolved; exact revised ciphertext and a frozen wide mechanism map
are preserved.

**Thread:** [Practice Cipher #6 (one for the bots)](https://discord.com/channels/453998283174576133/1227024108286644284/threads/1529398055898447973)

## What was given

On 22 July 2026, sdlwdr described this as a deliberately difficult practice
puzzle with three positive hints:

- it is a deck cipher;
- it incorporates the Trailer Altar;
- it incorporates the Earthquake Circle.

The author also disclosed three differences from the Eyes: adjacent doubles
exist, the second and third characters are not consistent across messages,
and the ciphertext does not appear to contain isomorphs. A first ciphertext
was replaced 84 minutes later because one aspect of the mechanism was not as
intended. The replacement is harder, uses the same plaintext, and is the
version to solve. The author says some plaintext punctuation was removed and
explicitly discourages identifying the source by a length search.

The two exact attachments are preserved as
[`cipher6-original.txt`](../artifacts/practice-sdlwdr/cipher6-original.txt) and
[`cipher6-revised.txt`](../artifacts/practice-sdlwdr/cipher6-revised.txt).
Their SHA-256 hashes are:

```text
original  6e125aa8c3e845e94d9f8c90b8d131ca936439d3db87442f110900a28a2c1111
revised   0b5e0a73e1cb8efc6090fa893fc4604195d2d85e884bfe2d39f35952974654c2
```

## Immediate observables

The revised file has nine independently printed lines of lengths:

```text
57,53,77,99,108,72,111,110,74
```

It uses every one of the 83 consecutive printable characters from `!`
(code point 33) through `s` (115). There are twelve within-line adjacent
doubles. The nine first characters are:

```text
<=>?@ABCD
```

Their zero-based positions in that 83-character alphabet are `27..35`, the
ordinary positions of plaintext digits `1..9` after A–Z. This is strong
evidence that each line begins with its line number and resets an initially
natural deck. It is an observable rather than a supplied hint, but it remains
a hypothesis until a complete replay proves the plaintext convention.

Only 21 of 761 non-newline positions are equal between the original and
revised files: all nine initial characters and twelve later coincidences. The
correction therefore changes the running state almost immediately; the old
file is useful as a differential oracle, not as a second independent
plaintext.

## Wide mechanism map before depth

The clues admit several materially different uses of the two assets. They
must be separated before language scoring:

| Lane | Asset role | First bounded test | Stop rule |
|---|---|---|---|
| A. Plaintext alphabet | Trailer Altar fixes the keyed letter order `BDMAGICKEFHJLNOPQRSTUVWXYZ`; digits and punctuation follow normally. | Apply only after a mechanism recovers a concentrated low-rank stream; compare natural and altar letter renderings without selecting per line. | Readable output from a fitted deck is not evidence for the alphabet. |
| B. Paired rotating decks | The altar alphabet and the Earthquake outer/inner words initialize a generalized Chaocipher-like pair. | Enumerate the finite natural/keyed initial pairs and independently authored nadirs `17,20,24,32,41,42`; require all nine lines to decode under one setting. | Reject if no candidate sharply concentrates in a plausible plaintext rank range or language score. |
| C. Fixed physical cuts | Circle row lengths `32,24,20,17,24` are sequential cut, rotate, or packet widths. | Enumerate order-preserving cut/packet operations and update timing, with the same rule for every line and plaintext symbol. | No arbitrary reorderings of the five widths. |
| D. Binary stable partitions | The `20`-alternating and `17`-irregular bands define stable two-packet shuffles of the 83-card deck by repetition. | Test the two authored directions and zero/one packet order, alone and in the displayed outer-to-inner sequence. | No rotations after failure; the small gap fixes phase. |
| E. Rune-index operations | `KMGIC` and `MAGICK`, interpreted in the altar alphabet, select deck positions or operation classes. | Test the exact cyclic sequences and their two physical directions as cut amounts or operation schedules. | Do not permute rune-to-number mappings; the altar order must fix them. |
| F. Revision differential | The original and revised encodings differ by one corrected state-update aspect. | Compare first divergence, equality positions, and candidate update traces to determine whether the correction is timing, direction, reset, or mutation scope. | The old file may reject candidates but cannot choose an arbitrary edit. |
| G. Known numbered prefixes | The inferred plaintext prefixes `1..9` expose the first update from a common reset state. | For every candidate family, require the observed first two cards for all nine lines before inspecting later language. | Do not infer later plaintext from source-length search. |

The first cost-adjusted discriminator is lane B because it is finite, directly
uses “deck cipher” vocabulary, and can be rejected without knowing the
plaintext source. Lanes C–G remain recorded if B fails.

## First result: paired rotating decks are negative

The frozen generalized-Chaocipher screen used nine source-fixed initial
orders—natural, Trailer Altar, card-trick phrase, both physical readings of
the outer gap/cycle, and both readings of the inner cycle—and the six nadirs
`17,20,24,32,41,42`. All `9×9×6=486` left/right/nadir settings reset on every
line.

All 486 settings reproduce the numbered first-character oracle because the
candidate keys rearrange letters while leaving digit positions fixed. None
then concentrates into a plausible plaintext alphabet. Every candidate uses
all 83 recovered ranks and reaches rank 82. Counts in the fixed low range
`0..41` run from 370 to 419, with median 397. The maximum is:

```text
left=outer-cycle-ccw  right=natural  nadir=20
low ranks = 419/761 = .550591
```

Its rendered first line is visibly mixed with out-of-range symbols, and the
other lines behave the same way. With a uniform wrong mapping the expected
low count is `761×42/83≈385`; maximizing 486 correlated settings readily
explains this modest excess. Close the historical paired-rotation lane. This
does not reject every possible two-deck cipher, but further nadir or arbitrary
keyword scans would violate the lane's stop rule.

Executable audit:
[`audit_sdlwdr_cipher6_paired_decks.py`](../scripts/audit_sdlwdr_cipher6_paired_decks.py).

## Second freeze: circle-authored base permutation

The next test is not another two-deck variant. It asks whether the circle
defines one base permutation `P` and the plaintext rank generates a family of
83 deck operations, as in a group-autokey cipher.

The admitted base permutations are fixed before scoring:

- signed rotations by the displayed nontrivial row sizes `17,20,24,32`;
- stable zero/one partitions produced by repeating the displayed alternating
  20-bit and irregular 17-bit rows across 83 deck positions;
- the displayed outside-to-inside composition of those two partitions;
- only clockwise/counterclockwise tape reading and global zero-first versus
  one-first packet order.

At every character, emit the current rank of the observed card, then update
the deck under exactly one of `P`, `P^rank`, or `P^(rank+1)`. Every line resets
to natural order. The Trailer Altar is used only as the alternative fixed
letter rendering, not as a fitted deck. Promotion requires a dramatic
concentration in `0..41` across all nine lines, followed by coherent language;
otherwise close these physical cut/partition implementations without rotating
the bit rows or choosing rules per line.

## Second result: direct circle permutations are negative

Deduplicating the displayed cuts, repeated alternating/irregular partitions,
and their outside-to-inside compositions leaves 18 base permutations. The
three registered exponent schedules give 54 candidates. All preserve the
known numbered prefixes, but all recover all 83 ranks and reach 82. The best
candidate is:

```text
base=cut+24  update=P
low ranks = 428/761 = .562418
```

Its output is mixed-rank gibberish under both natural and altar alphabets.
The next candidates fall to `424/761` and `422/761`; no candidate approaches
the near-total low-rank collapse required of the presumed 42-symbol
plaintext. Close direct signed cuts, repeated binary stable partitions, and
their fixed/rank-power forms.

Executable audit:
[`audit_sdlwdr_cipher6_circle_permutations.py`](../scripts/audit_sdlwdr_cipher6_circle_permutations.py).

## New exact identity: one 83-slot asset tape

A more constrained joint use of the two clues appears only after keeping
spaces in the community's proposed Trailer-Altar phrase:

```text
len("A BAD MAGIC CARD TRICK") = 22
Earthquake binary rows       = 24 + 20 + 17 = 61
total                        = 83
```

Thus the phrase followed by the zero, alternating, and irregular rows is an
exact 83-position string:

```text
A BAD MAGIC CARD TRICK
000000000000000000000000
10101010101010101010
11110111011101110
```

This identity is exact given its inputs, but one input is a community keyed
phrase associated with the altar—not literal text displayed by the asset.
The author may have chosen the phrase precisely because this puzzle has 83
cards, or the equality may be incidental. It earns a bounded test, not an
assumption of intent.

### Wide consumers before selecting one

| Consumer | Meaning | Falsifier |
|---|---|---|
| Stable position order | Stable-sort the 83 card positions by their tape symbols, using either natural character order or the tape's first-occurrence order. | No low-rank collapse under the three already frozen update schedules. |
| Cyclic-rotation order | Because the binary source is circular, lexicographically order all 83 cyclic rotations; their starting positions form a full deck permutation. | Same; only natural and first-occurrence symbol orders, with the physical binary direction ambiguity. |
| Thirteen operation classes | The tape's 13 distinct symbols select 13 shared deck operations. | Deferred until an operation family is independently specified; do not fit 13 arbitrary permutations. |
| Literal per-rank steps | The symbol at plaintext rank selects a cut/distance. | Deferred because symbol-to-distance semantics are not yet fixed. |
| BWT/instruction stream | The 83-slot cycle is serialized after a transform and consumed over time. | Deferred unless the position-order tests reveal a related invariant. |

The first test admits two binary directions while keeping the phrase readable,
two fixed symbol orders, stable versus cyclic-rotation ordering, and the same
`P`, `P^rank`, `P^(rank+1)` updates. No tape rotation, per-line order, or
language-fitted symbol collation is allowed.

## Third result: direct tape orderings are negative

The two binary directions, two symbol collations, and stable/cyclic orderings
produce eight unique permutations and 24 update candidates. All again use all
83 recovered ranks through 82. The best result is:

```text
base=cyclic-cw-first-occurrence  update=P
low ranks = 406/761 = .533509
```

This is weaker than both prior maxima and is mixed-rank gibberish. Close stable
sorting and cyclic-rotation sorting as direct base permutations. Preserve the
exact `22+61=83` identity while moving to a different consumer.

Executable audit:
[`audit_sdlwdr_cipher6_asset_tape.py`](../scripts/audit_sdlwdr_cipher6_asset_tape.py).

## Fourth freeze: thirteen tape-symbol operation classes

The exact tape contains thirteen distinct symbols, in first-occurrence order:

```text
A, space, B, D, M, G, I, C, R, T, K, 0, 1
```

This admits a small operation quotient without inventing thirteen arbitrary
permutations. At each step:

1. find the observed ciphertext card's current rank and emit it as plaintext;
2. use that plaintext rank to address the 83-slot tape;
3. map the addressed tape symbol to its natural or first-occurrence class
   rank;
4. move the first `N` cards to the back, with `N=class` or `class+1`.

Test both global cut directions and the two physical readings of the binary
rows. Every line resets naturally. These `2×2×2×2=16` settings are the whole
family. Promotion requires the same near-total collapse into `0..41`; no
per-symbol direction, distance table, or arbitrary class permutation may be
fit afterward.

## Fourth result: thirteen ordinal cut classes are negative

All 16 pre-registered settings preserve the numbered first symbols, but every
one uses all 83 ranks through 82. The maximum is:

```text
binary=cw  class-order=first-occurrence  N=class+1  cut=right
low ranks = 407/761 = .534823
```

This is another ordinary mixed-rank stream. Close ordinal `0..12` class
numbers as direct cut distances.

Executable audit:
[`audit_sdlwdr_cipher6_tape_classes.py`](../scripts/audit_sdlwdr_cipher6_tape_classes.py).

## Fifth freeze: altar-valued per-rank cuts

The ordinal test discarded a meaningful part of the altar clue: its proposed
alphabet assigns actual positions to the letters. The next family maps the
tape symbols through one of only two documented keyed letter orders:

```text
trailer runes:  BDMAGICKEFHJLNOPQRSTUVWXYZ
card-trick key: ABDMGICRTKEFHJLNOPQSUVWXYZ
```

For each, admit two ways to incorporate the nonletters:

1. append digits and space, so `0=26`, `1=27`, `space=36`;
2. take the circle bits literally as `0/1` and make phrase spaces zero-width.

The resulting tape value at recovered plaintext rank selects a first-`N` cut.
Test value versus value-plus-one, left/right globally, and the two physical
binary readings: `2×2×2×2×2=32` models. Reset naturally per line. No ASCII
values, arbitrary space distance, symbol-specific signs, or rotations of the
83-slot address tape are admitted.

## Fifth result: altar-valued plaintext-autokey cuts are negative

All 32 admitted value maps and directions again preserve the numbered starts
but use every recovered rank through 82. The maximum is:

```text
binary=ccw  alphabet=card-trick  symbols=appended
distance=value  cut=right
low ranks = 423/761 = .555848
```

No setting produces coherent output. Close the 83-slot tape as a
*plaintext-rank-addressed* cut schedule under ordinal and altar-valued
semantics.

Executable audit:
[`audit_sdlwdr_cipher6_tape_values.py`](../scripts/audit_sdlwdr_cipher6_tape_values.py).

## Author-side clue: custom Alberti/ciphertext autokey

A read-only server-wide Discord search supplies a stronger architecture clue.
On 18 May 2023 in `#silmä-novel`, sdlwdr wrote:

> So I was thinking maybe the earthquake symbol could be used for some sort of
> alberti cipher.

The surrounding historical discussion later distinguishes classical Alberti
from a custom 83-symbol ciphertext-autokey variant. This predates Practice #6
by more than three years and comes from its author. It does not reveal the
puzzle mechanism, but it changes the next selector: the observed ciphertext
card, rather than recovered plaintext rank, should be allowed to turn the
disk/deck.

## Sixth freeze: 83-card ciphertext-autokey disk

The first custom-Alberti family uses natural line resets and the three
letter-only initial orders that leave digit positions fixed:

```text
natural
BDMAGICKEFHJLNOPQRSTUVWXYZ...
ABDMGICRTKEFHJLNOPQSUVWXYZ...
```

After emitting the observed card's current rank, update the disk from that
card's fixed label in one of two ways:

1. cumulative: advance the current alignment by the key value;
2. absolute: set the next alignment to the key value relative to the initial
   deck.

Two key sources are admitted:

- raw ciphertext card label, zero- or one-based;
- the already frozen 83-slot asset tape at that ciphertext label, under the
  two altar alphabets and literal/appended nonletter conventions.

Test both global directions and both binary readings where the asset tape is
used. This gives 24 raw-card and 192 asset-valued settings, 216 total. No
per-line initial offset, ciphertext substitution, tape rotation, or
symbol-specific direction is permitted. A correct model must collapse almost
entirely into the low plaintext ranks and then replay under one fixed
rendering.

## Sixth result: direct ciphertext-autokey rotations are negative

All 216 raw and asset-valued custom-Alberti settings preserve the known first
symbols but recover all ranks through 82. The maximum is:

```text
initial=trailer  key=asset-tape  alignment=cumulative
binary=cw  value-alphabet=trailer  nonletters=appended
distance=value+1  cut=left
low ranks = 418/761 = .549277
```

The best raw-card key is only `409/761`. This closes simple cumulative and
absolute ciphertext-keyed *rotations*. It does not reject a custom Alberti
whose disks use non-rotational permutations or several coupled rings.

Executable audit:
[`audit_sdlwdr_cipher6_ciphertext_autokey.py`](../scripts/audit_sdlwdr_cipher6_ciphertext_autokey.py).

## Revision differential

Every already fixed family was replayed unchanged against the author's
superseded original ciphertext:

| family | revised best | original best |
|---|---:|---:|
| paired rotating decks | 419 | 419 |
| direct circle base | 428 | 431 |
| 83-slot order | 406 | 417 |
| ordinal class cuts | 407 | 416 |
| altar-valued cuts | 423 | 403 |
| ciphertext autokey | 418 | 430 |

Every original maximum also uses all 83 ranks through 82. The revision does
not expose a near-solution under any tested reset, timing, address, or value
convention. Preserve the old file as an oracle, but do not use the vague
“one aspect” wording to multiply variants.

## Seventh freeze: full-circle rotating clock

The prior models barely used the authored outer and inner rune sequences as
sequences. In the Trailer alphabet they are:

```text
outer KMGIC  -> 7,2,4,5,6
inner MAGICK -> 2,3,4,5,6,7
```

At character time `t`, index those cycles at `t mod 5` and `t mod 6`; index
the alternating and irregular binary rows at `t mod 20` and `t mod 17`.
Eight source-fixed step schedules are admitted:

1. outer + inner;
2. outer - inner;
3. inner - outer;
4. alternating bit chooses outer versus inner;
5. irregular bit chooses outer versus inner;
6. alternating bit signs outer + inner;
7. irregular bit signs outer + inner;
8. alternating signs outer while irregular signs inner.

Test the two physical readings of every circle row, cumulative versus
absolute alignment, step versus step-plus-one, and the three digit-preserving
initial decks: `8×2×2×2×3=192` models. The schedule resets per line; no
rotations/phases, per-line direction, fitted rune values, or mixed timing are
allowed. Promotion again requires near-total low-rank collapse.

## Seventh result: the full rotating clock is negative

Every one of the 192 models still recovers all 83 ranks and reaches rank 82.
The best setting is:

```text
initial=card-trick
schedule=irregular-sign-sum
physical direction=counterclockwise
alignment=cumulative
step indexing=one-based
low ranks=415/761=.545335
```

This closes the finite interpretation in which the four authored Circle rows
are synchronous clocks controlling a rotating 83-card disk. Together with the
six earlier screens, it leaves no asset-backed preference among the simple
rotation, stable-partition, fixed-cut, or paired-Chaocipher interpretations.
The historical Alberti remark and exact 83-slot joint tape remain valuable,
but a further Cipher #6 attack now needs a new independently fixed state
transition—not additional phases, signs, or line-specific choices.

Executable audit:
[`audit_sdlwdr_cipher6_full_circle_clock.py`](../scripts/audit_sdlwdr_cipher6_full_circle_clock.py).

## Why this matters for the Eyes

This puzzle is the first practice example in the storehouse that explicitly
combines a hidden deck with Noita assets. A solution could therefore teach how
an author expects a solver to turn decorative ring content into executable
state transitions. It is method calibration, not evidence that the Eyes use
the same cipher. In particular, success may validate the workflow “identify a
deck architecture, assign each asset one unambiguous role, and use repeated
resets as a known-state oracle” without transferring the exact operation.
