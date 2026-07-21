# sdlwdr #3 — unresolved progression cipher

**Status:** Unsolved.  One exact mechanism family is excluded; two broader
cycle decompositions remain undecided because their solvers timed out.

## What was tested

The working hint was that the ciphertext alphabet progresses with position.
That can be stated without guessing letters.  Let `P` be one permutation of
the 83 ciphertext symbols.  At zero-based position `i`, decode symbol `c[i]`
as

```text
P^-i(c[i])
```

and require all 2,247 decoded events to lie in at most 42 plaintext symbols.
The exact solver assigns every ciphertext symbol to one cycle coordinate and
counts every coordinate reached by its observed positions.  It therefore
tests arbitrary symbol labellings, not only the displayed `0..82` order.

## Exact result

For one 83-cycle, both the complete streams and the marker-stripped bodies are
inconsistent with a 42-symbol plaintext alphabet:

```text
full: events=2247, distinct-position constraints=1870, C83 -> UNSAT
body: events=2229, distinct-position constraints=1858, C83 -> UNSAT
```

This is a real exclusion: no rotation, initial coordinate assignment, or
substitution alphabet can repair that particular `C83` progression model.

Two natural relaxations were also encoded:

```text
C82 + fixed point
C41 + C41 + fixed point
```

Both returned `unknown: timeout` in fresh bounded runs.  They are **not**
excluded.  A separate scan of standard physical/near-size initial shuffles
followed by selected-card deck updates did not collapse a representative
message to a plausible small alphabet, but that scan is a finite negative,
not a proof about arbitrary deck operations.

## Solution

No verified plaintext has been recovered, so there is no solution text to
state.  The complete result is the scoped negative above: the proposed
position-progressive mechanism cannot be one 83-cycle with at most 42 decoded
symbols.  The supplied scripts retain the unresolved alternatives explicitly
instead of presenting a timeout as an impossibility proof.

## Transfer to the Eyes

- Translate a verbal mechanism into a label-independent constraint system.
- Use exact contradictions to discard whole key spaces before language search.
- Record `UNSAT`, finite scan failure, and timeout as three different outcomes.
- Do not infer that a family is wrong merely because its more symmetric
  one-cycle member is wrong.

The exact checks are implemented in
`scripts/solve_sdlwdr_cipher3_cycle.py` and
`scripts/solve_sdlwdr_cipher3_progression.py`; the bounded deck scan is
`scripts/search_sdlwdr_cipher3_decks.py`.
