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

## Why this matters for the Eyes

This puzzle is the first practice example in the storehouse that explicitly
combines a hidden deck with Noita assets. A solution could therefore teach how
an author expects a solver to turn decorative ring content into executable
state transitions. It is method calibration, not evidence that the Eyes use
the same cipher. In particular, success may validate the workflow “identify a
deck architecture, assign each asset one unambiguous role, and use repeated
resets as a known-state oracle” without transferring the exact operation.
