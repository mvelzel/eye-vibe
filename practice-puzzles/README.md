# Noita community practice puzzles

This folder keeps short, reproducible **attack records** for the practice
puzzles used while investigating the Eye Messages.  Each record explains the
observable that exposed the cipher, the search-space reduction, the final
decoding step, and the verification.  Construction details are included only
where the attack needs them.  A file is marked **solved** only when the method
has an exact ciphertext replay or the puzzle author has confirmed the intended
answer; merely plausible language output is not enough.

Every solved record must answer five distinct questions:

1. **What was actually given?**  Public rules, known plaintext, hints, and
   author feedback are inputs to the attack, not discoveries by the solver.
2. **What ciphertext observable exposed the route?**  Examples include a
   transition invariant, equality-pattern isomorphs, or an immediately visible
   component of a hidden state.
3. **How was the search reduced?**  The record gives the finite choices,
   constraints, staging, and any boundary controls that kept the real answer.
4. **How was ambiguity closed?**  Language ranking alone is not silently
   promoted to proof; author confirmation, a crib, or another independent
   constraint is stated explicitly.
5. **What verifies the result?**  Prefer full re-encryption/replay.  When the
   original generator is unavailable, say exactly where reproducibility stops.

This deliberately makes the *route to the solution* longer than the cipher
recipe.  A copied plaintext or a retrospective description of how the author
encrypted it is not, by itself, a useful practice-puzzle solution.

## Index

| Puzzle | Status | Main lesson for the eyes |
|---|---|---|
| [Practice 83 card GAK cipher](01-practice-83-card-gak.md) | Solved; exact replay | A plaintext-selected 83-card operation can be locally invertible when its action set is known. |
| [Another solvable GAK](02-another-solvable-gak.md) | Solved; exact replay | Examine transition laws before attacking visible symbols as substitutions. |
| [A solvable GAK](03-a-solvable-gak-cube-morse.md) | Solved; author-confirmed | Recover the small physical/group action first, then look for a second codec such as Morse. |
| [Known-plaintext S83 deck/swap cipher](04-known-plaintext-s83-deck-swap.md) | Solved; exact key recovery | Separate the emitted top-card substitution from delayed hidden-state effects. |
| [Practice `two`](05-practice-two-octal-hidden-group.md) | Solved; withheld-plaintext confirmation | Compose isomorph column maps into a group, trim dirty anchors, then finish the residual codec. |
| [sdlwdr #1 — two-cycle Wadsworth cipher](06-sdlwdr-01-wadsworth-kalevala.md) | Solved; author-confirmed | Chained isomorph maps can expose equal hidden cycles, unequal-wheel arithmetic, and a state-changing exceptional symbol. |
| [sdlwdr #2 — drifting/reversing Wadsworth cipher](07-sdlwdr-02-reversing-wadsworth.md) | Solved; deterministic full decode | Position bands expose slow drift; a rare marker can reverse both hidden traversals. |
| [sdlwdr #5 — recursive increasing-chunk shuffle](10-sdlwdr-05-recursive-chunks.md) | Solved; exact replay | Equality-pattern repetitions can select a recursive state-update law before plaintext letters are assigned. |

Additional files will be added as the remaining practice puzzles are either
solved or closed with a clearly scoped negative result.
