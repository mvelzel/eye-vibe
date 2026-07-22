# Practice cipher 4: case-sensitive bijection test — 22 July 2026

## Frozen question

The standard `C83` reduction of sdlwdr's fourth puzzle uses 53 values inside
the exact contiguous band `22..78`, a span of 57 positions.  Earlier attacks
case-folded those values and forced them into either fixed two-homophone slots
or an unrestricted many-to-one map.  They did **not** test the distinct
hypothesis suggested by the author's “very straightforward initial PTA” hint:

> the 57 positions are a conventional case-sensitive character alphabet, and
> the 53 observed actions are a one-to-one substitution of 53 distinct
> plaintext characters.

This is compatible with cyclic CTAK: adjacent ciphertext differences recover
the injective plaintext action map, after which only a monoalphabetic
substitution remains.

## Finite experiment

1. Preserve upper/lower case, ordinary word spaces, and punctuation while
   training a character four-gram model on the frozen English corpus already
   used for the other practice attacks.
2. Search injective maps from the 53 observed actions into each of these
   conventional character pools:
   - `A-Z`, `a-z`, and ` .,?!`;
   - `A-Z`, `a-z`, and ` .,'-`;
   - `A-Z`, `a-z`, and ` .;:-`;
   - `A-Z`, `a-z`, and ` .,:;`.
3. Allow observed symbols to swap with unused pool characters, so the four or
   five absent plaintext characters are not fixed in advance.
4. Run the identical optimizer on planted case-sensitive prose at the real
   total length.  Record recovered character accuracy and score.
5. Repeat the real search across independent seeds.  A solution must be
   readable across all three portions, preserve their exact shared blocks,
   and recur up to symbols that are genuinely underdetermined.

## Decision rule

- **Promote** only if several seeds converge to the same readable plaintext
  and the planted control verifies that the optimizer can recover this model.
- **Reject this family** if the control recovers while the real candidates
  remain seed-unstable gibberish with a large calibrated score gap.
- Do not reinterpret a best-scoring pseudo-word string as a partial solution.

This test does not cover a second transposition/encoding layer or a plaintext
alphabet outside the listed conventional families.  Those remain separate
hypotheses if this one fails.
