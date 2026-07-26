# Practice cipher 3 — arbitrary two-sheet freeze

**Date:** 27 July 2026
**Status:** frozen before scoring the real corpus

## Motivation

Cipher 3 uses all 83 raw symbols, while sdlwdr's established plaintext
alphabet has 42 symbols and `83 = 2*42 - 1`. The complete affine pairing
family `x ~ a-x mod83` is negative, but that tested only 83 authored-coordinate
pairings. The earlier general homophone optimizer used 27 plaintext slots and
failed its own positive control.

This pass tests the exact unresolved static architecture:

```text
q : {0..82} -> {0..41}
```

where one plaintext symbol has one raw representative and each other plaintext
symbol has exactly two. The same `q` is used for every message. Decoding is
simply `p[i] = q(c[i])`; there is no position drift, wheel, state, or
per-message key.

This family is high-capacity but finite and semantically precise. A readable
full replay would solve the practice puzzle under this mechanism. Gibberish
does not exclude it unless the same solver first recovers a matched plant.

## Frozen language data

Train one 42-symbol trigram model on Project Gutenberg's *The Adventures of
Sherlock Holmes*:

```text
https://www.gutenberg.org/cache/epub/1661/pg1661.txt
SHA-256 922e2a12ccb43a4c9544c260b2166c6ad2097aeb5957faeee113f173bb857cd0
```

Use Project Gutenberg's *Moby-Dick* only for planted plaintext:

```text
https://www.gutenberg.org/cache/epub/2701/pg2701.txt
SHA-256 9a6844ac0703853720010787c7b6c70b0020f1ab1862dcd74452fa46474d1215
```

Normalize both with the already fixed alphabet:

```text
ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .-’?!
```

The plant retains the real 18 message lengths. Its six A passages are selected
from *Moby-Dick* solely to maximize 42-symbol coverage; B and C use disjoint
fixed passages. A random valid two-sheet key and deterministic balanced choice
between each pair generate the ciphertext. No real Cipher 3 value enters
plant construction.

## Frozen search protocol

The key always retains the exact `2,...,2,1` preimage-size multiset. Annealing
uses only:

1. swapping the plaintext assignments of two raw symbols;
2. moving the singleton role from one plaintext symbol to another.

Training objective and all key selection use group A only. Freeze the best A
key, then score and render B+C once. Run complete-stream and first-symbol-
stripped modes separately because the existing puzzle evidence does not
establish whether the first item is payload or an indicator. This two-mode
choice is disclosed; neither mode may tune on B or C.

Algorithm parameters may be tuned only on the planted control. Freeze the
final restart count, iteration count, and temperature schedule before the
first real run.

The first passing budget is now fixed:

```text
restarts              4
iterations/restart    300,000
temperature           18.0 -> 0.08 geometrically
seed                   20260727 (body mode xor 0xB0D1)
```

At that budget the matched plant scores:

```text
mode   A accuracy   untouched B+C accuracy
full    94.444444%       98.448368%
body    94.354839%       97.199785%
```

Both modes pass the frozen operational gate. No real result had been inspected
when these parameters were added.

## Promotion and stop gates

The solver is operational only if the planted key reaches:

```text
A event accuracy       >= 80%
B+C event accuracy     >= 60% with the frozen A key
```

If the plant fails, the real family remains unresolved and must not be scored.

If the plant passes, run the real corpus once. Promote only if the frozen key
produces coherent held-out plaintext and exact full replay. If real heldout
text is gibberish and separated sharply from the plant, close only this direct
static two-sheet family. Do not widen to an arbitrary stateful sheet schedule
or hidden coordinate permutation.
