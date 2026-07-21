# Known-plaintext S83 deck/swap cipher — solved

Source: [Discord thread](https://discord.com/channels/453998283174576133/1227024108286644284/threads/1522526192400470056), posted by `Torben` from a cipher by `Lymm` on 3 July 2026.  The independently implemented attack and fixtures are public in the [Noita eye scratchpad](https://github.com/hansborr/noita-eye-puzzle-scratchpad/tree/main/research/data/practice-puzzles/deck-swap).

## Cracking method

The exercise supplies eight plaintexts, their ciphertexts, the 83-card group,
and the base permutation

```text
base[i] = 3(i + 26) mod 83.
```

Each letter applies `base` followed by exactly one, two, or three swaps between
the top position and another position.  The deck starts at identity for each
message, updates as `new_state[i] = state[perm_L[i]]`, and emits
`new_state[0]`.

Naively, each letter has up to 541,406 three-swap permutations and every wrong
choice corrupts all later deck states.  The successful attack notices that the
current emission depends most directly on only `perm_L[0]`; the remaining
entries are delayed effects.  It therefore separates two coupled unknowns:

1. Message-initial letters act on the identity deck, so their first ciphertext
   symbols reveal `perm_L[0]` exactly.  For every other letter, score the 83
   possible top values by re-simulating a short prefix of all eight known
   messages.  Coordinate descent quickly settles this substitution layer.
2. Pre-enumerate the allowed swap words and bucket them by `perm_L[0]`.  Once a
   letter's top value is fixed, search only its much smaller bucket.  Additional
   coordinate-descent passes on the full corpus recover the far swaps.
3. Accept only zero residual: re-encrypt all known plaintext from fresh identity
   states and require byte-for-byte equality.

This ordering prevents weakly observed far-swap choices from poisoning the
strong substitution signal.  Deterministic basin hopping was available for
local minima, but these three instances converged without it.

## Solution

The plaintext was supplied, so recognizing it is **not** the solution.  The
solution is a complete candidate permutation key for every letter that the
corpus can identify, separately for each of the one-, two-, and three-swap
instances.  In all three instances the recovered mappings cover the 24 letters
that occur.  `J` and `Z` never occur, so no ciphertext observation can constrain
their permutations; they are correctly reported as `UNRECOVERED`, rather than
filled with arbitrary values.

The exact per-letter arrays and their canonical top-swap words are emitted by
the reproducible `gak-swap-recover` implementation linked above.  They are
witness keys rather than a claimed proof of uniqueness: the cryptanalytically
important result is that an independently recovered observed-letter mapping
exists in the allowed key family and has zero residual on every supplied
known-plaintext pair.

## Verification and transfer

For every swap count, a fresh encryption with the recovered key reproduces all
eight ciphertexts exactly: **2,439/2,439 emitted symbols**.  This is key
recovery, not plaintext recognition and not merely a restatement of the public
encryption recipe; the three-swap result searches a 541,406-permutation
candidate surface per letter before exact verification.

The transferable tactic is to isolate the immediately observable substitution
layer from delayed hidden-state effects.  The result is not a direct eye solve:
the Eye Messages lack both the known plaintext and the public base permutation
that make this practice attack identifiable.
