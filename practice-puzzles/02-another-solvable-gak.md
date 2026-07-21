# Another solvable GAK — solved

Source: [Discord thread](https://discord.com/channels/453998283174576133/1227024108286644284/threads/1498805023931633744), posted by `Lymm` on 28 April 2026.  An independent public workbench records the same exact solution in its [practice-puzzle results](https://github.com/hansborr/noita-eye-puzzle-scratchpad/blob/main/research/data/practice-puzzles/CODEC-RESULTS.md).

## Cracking method

The decisive observation comes before any language attack: every one of the
265 adjacent transitions is exactly `+1` or `-1` modulo 5.  The five visible
symbols are therefore a running state on `C5`; their signed directions carry a
binary stream.  Replace `+1` with one and `-1` with zero.

That raw bitstream still has a conspicuous parity alternation rather than ASCII.
Testing the two phases of the shortest possible periodic correction shows that
XOR with `0,1,0,1,...` removes it.  Scan the seven possible bit offsets and both
bit orders as a finite framing problem.  MSB-first at offset six produces valid
7-bit ASCII throughout and readable text.  The one unobserved bit before the
first transition is then forced by the opening `P`.

This reduces the puzzle in stages: five symbols → signed cycle steps → one bit
per step → period-two demasking → finite ASCII framing.  No substitution or
general-purpose English optimizer is needed.

## Plaintext

```text
Permutation Representation Destination
```

## Verification and transfer

The full construction has an exact 266/266 round trip in the public reference
implementation.  Locally, `tests/test_walk_mask.py` independently recovers
`ermutation Representation Destination` from all 265 observable transitions.
The main lesson is to attack the **transition law** before the symbol labels,
then test tiny masks and framings exhaustively.  Applying that exact attack to
the Eye Messages fails: their adjacent values are not a signed constant-step
walk on `C83` (nor on the natural base-three projections tested so far).
