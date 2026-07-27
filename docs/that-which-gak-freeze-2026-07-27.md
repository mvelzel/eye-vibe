# `THAT WHICH` ordinary-GAK stabilizer audit — freeze

## Question

Can the community's ten-character plaintext proposal

```text
THAT WHICH
```

occupy all six established first-family isomorph windows under ordinary GAK?
The windows use raw trigram offsets:

```text
East 1   40, 68
West 1   40, 70
East 2   45, 80
```

These zero-based offsets and the ten-character common extent are already
frozen by
[`../scripts/classify_that_which_windows.py`](../scripts/classify_that_which_windows.py).
The phrase was proposed retrospectively; this audit tests architecture, not
discovery likelihood.

## Frozen architecture

- orthodox trigram ranks are ciphertext cards;
- each literal plaintext character, including the space, selects one fixed
  permutation of deck positions;
- one update emits the new top card;
- every window may begin in an arbitrary deck state;
- operations are shared across all six windows;
- no XGAK selector, context memory, token merging, postprocessor, or alignment
  change.

The fixed-point test is independent of deck size and starting state. If equal
ciphertext cards occur at the endpoints of a plaintext word, that word's
composite position permutation fixes the top. Unequal cards mean it does not.
All permutations fixing the top form a subgroup.

## Frozen tests

For every nonempty contiguous operation word observable between two outputs:

1. collect its fixes/does-not-fix status in all six windows;
2. reject if the same word has both statuses;
3. for every observed factorization `uv`, reject any of the three subgroup
   violations:

   ```text
   u fixes, v fixes, uv does not
   u fixes, v does not, uv fixes
   u does not, v fixes, uv fixes
   ```

The current helper implements the last two cases; extend it to the first and
pass its existing planted contradiction and valid-random-GAK controls before
inspecting the Eye result.

If no certificate exists, run an exact arbitrary-state compatibility check.
It must first recover and replay a planted six-window fixture with the same
lengths and equality pattern. `SAT` establishes feasibility only; `UNSAT`
must yield a small observation core or independent subgroup certificate;
`unknown` leaves the architecture unresolved.

## Interpretation

A contradiction rejects only this literal phrase/alignment under ordinary
one-update-per-character GAK. Compatibility does not identify the plaintext.
XGAK or a context-dependent cipher remains outside scope.
