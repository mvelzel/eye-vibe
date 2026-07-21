# sdlwdr #5 — recursive increasing-chunk shuffle

**Status:** Solved; exact replay of all 2,212 revised ciphertext symbols.

**Thread:** [Practice cipher #5](https://discord.com/channels/453998283174576133/1227024108286644284/threads/1446258502107533604)

## Solution

The nine independently encoded sections are the nine numbered passages of Dr.
Seuss's *Green Eggs and Ham*, in story order.  The recovered text runs from
`DO YOU LIKE GREEN EGGS AND HAM?` through `THANK YOU, THANK YOU. SAM-I-AM`.
The complete text is 2,212 characters.  Because the book remains copyrighted,
this record cannot reproduce all 2,212 characters verbatim; the following is
the fullest self-contained inventory of the recovered result that does not
substitute “run the script” for stating what was found:

| Section | Characters | Recovered content and boundary | SHA-256 of exact recovered text |
|---:|---:|---|---|
| 1 | 98 | Number `1`; the opening question; Sam-I-Am's first refusal | `c58e1976a553e32677e0cc62ecea0804893463f501bb0c49f018d350baa7ce0d` |
| 2 | 170 | Number `2`; the here-or-there offer; refusal anywhere and to Sam-I-Am | `c64ee65ca2920e19ab6f639568897314c8b0ae59c007d4aaf7de18dd7a6e9892` |
| 3 | 259 | Number `3`; house and mouse offers; cumulative refusals through anywhere | `36a2bb24ff52afc495dd1f054e622c6e7d32b370dea97dd84b3d931690e594a8` |
| 4 | 259 | Number `4`; box and fox offers; cumulative refusal ending with Sam-I-Am | `66c7be50362f695c7ab68524de27444cc8f0671af954a6c40bd9318a974bf023` |
| 5 | 228 | Number `5`; car and tree sequence; plea to be left alone | `57291e34bb8fe80922c06ce53b3efc851fbf3ffb633234bd24884a046ea89cdf` |
| 6 | 73 | Number `6`; the complete goat offer and refusal, ending in a comma | `de8e6fd73ee59a5eb39d1523a27a335c85e43f6981bf4b6eb6dd72ecb53a9543` |
| 7 | 451 | Number `7`; boat, rain, dark, and accumulated settings; renewed refusal | `e25b7e3f04cfa1507f04afeda023f137d5b7297a1d613d559f06a7f1c192bb62` |
| 8 | 152 | Number `8`; Sam asks for one trial; the other speaker agrees to try | `0614493184b9cc4bd7338a3113e38176371a04af6fa33780fe79ade843bd32ca` |
| 9 | 522 | Number `9`; acceptance, full setting-by-setting recapitulation, and thanks | `929a8d03e6fd435580e91c4ae213978c1fe78a3ab4610c7bb616837d81aa2217` |

These are hashes of the rendered plaintext—including the section number,
line breaks, spaces, punctuation, and final newline—not hashes of the source
book or ciphertext.  Together with the exact algorithm below and exact
ciphertext replay, they fix every recovered character without disclosing the
copyrighted passage itself.

The recovered plaintext ordering is:

```text
ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .<newline>,?-
```

Only its first 42 indices occur.  The ciphertext alphabet consists of the 83
consecutive characters with code points 33 through 115.

## How it was cracked

### 1. Turn the hints into falsifiable operation families

The author disclosed that the plaintext-character index selects a recursive
shuffle of the ciphertext alphabet, described as two stacks of sizes `index`
and `n-index`; smaller indices produce deeper recursion.  That establishes the
state architecture but not the recursion, its off-by-one convention, packet
collection order, or whether output occurs before or after the update.

I enumerated those finite choices rather than assuming one interpretation:
fixed-size peeling, increasing splits, doubling layers, interleaving versus
concatenation, reversed packets or packet order, zero- versus one-based widths,
and emission before versus after the shuffle.

### 2. Score candidates without guessing words

The nine sections contain long ciphertext windows with identical equality
patterns.  For each candidate shuffle family I decoded those paired windows
and counted equality at aligned plaintext positions.  This is a key-free
oracle: it rewards preservation of repeated plaintext structure without first
assigning any symbol to a letter.

One family separated sharply from the others.  It starts with width
`plaintext_index + 1`, peels consecutive packets whose widths increase by one,
and concatenates them in reverse order as recursion unwinds.  Equivalently:

```text
shuffle(deck, width):
    if len(deck) <= width: return deck
    return shuffle(deck[width:], width + 1) + deck[:width]
```

Internal order within every packet is preserved.  For index 2, for example,
the deck is split into widths 3, 4, 5, ... and those packets are collected
last-to-first.  Lower indices create more packets and therefore greater
recursion depth, matching the hint precisely.

### 3. Decode by current rank, then update

Each section resets the ciphertext deck to the standard order.  At each step:

1. Find the observed ciphertext card's current deck rank; that rank is the
   plaintext index.
2. Emit that index.
3. Apply the permutation selected by the same plaintext index.

The indices immediately collapsed to 36 used values, all in `0..41`.
Assigning the straightforward A–Z, digits, and punctuation order exposed the
source.  In particular, index 38 is a newline—not a punctuation mark—which
resolved the only apparent formatting anomaly in an early rough rendering.

## Verification

The recovered indices, rendered with the stated alphabet, re-encode to every
one of the 2,212 revised ciphertext characters exactly.  There are 83 distinct
shuffle operations, each a valid permutation of all 83 cards.  The nine
section hashes above independently pin the formatting and plaintext content;
the automated checks also pin the opening, permutation validity, and operation
uniqueness.  `scripts/solve_sdlwdr_cipher5.py` is an executable verification of
these stated results, rather than the only place where the solution is shown.

The author's original version is outside this claim: the thread explicitly
replaced it with a revised encoding intended to be solvable.  This record
solves and replays that revision.

## Transfer to the Eyes

- Translate prose hints into a family of small, explicit implementation
  choices and score the whole family against invariants.
- Equality-pattern repetitions can identify a hidden update law before any
  alphabet mapping or language model is introduced.
- Off-by-one conventions and update timing are structural variables, not
  cleanup details.
- A small recovered plaintext alphabet can sit inside a much larger dynamic
  ciphertext alphabet; unused plaintext ranks do not imply a wrong model.
- Formatting controls such as newline can masquerade as odd punctuation and
  should be inferred from repeated structural positions.
