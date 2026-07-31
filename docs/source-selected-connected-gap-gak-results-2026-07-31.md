# Source-selected connected-gap GAK — results

## Outcome

All 40 literal *Hermetic Museum* continuation triples are impossible under the
frozen ordinary-GAK model.

The rejection is stronger and simpler than finite-completion failure. Every
triple contains the same operation word with contradictory top-stabilizer
status, so no deck size, initial deck choice, or permutation completion can
repair it.

## Source census

The two fixed Internet Archive OCR volumes contain:

```text
gap 28 / East 1    5 source pairs
gap 30 / West 1    4 source pairs
gap 35 / East 2    2 source pairs
total triples      5 × 4 × 2 = 40
```

The literal intervals use 18–22 shared character actions depending on the
triple. The exact free-subgroup audit rejects every triple with one universal
forced nonmember:

```text
AT WHICH␠
```

## Direct certificate

Every source interval begins:

```text
THAT WHICH␠
```

Compare ciphertext outputs at zero-based segment positions 1 and 10. The
intervening plaintext actions are exactly `AT WHICH `:

```text
segment   output[1]   output[10]   AT WHICH␠ fixes top?
East 1       44           72       no
West 1       44           44       yes
East 2       13           13       yes
```

For an ordinary GAK, equal endpoint cards mean the intervening operation word
fixes top position zero; different cards mean it does not. This status depends
only on the shared operation word, not on card labels or the independent start
deck. The same `AT WHICH ` word therefore cannot realize all three segments.

This certificate appears twice as a direct fixed/nonfixed word-status conflict:

```text
East 2 positions 1->10 fixes; East 1 positions 1->10 does not
West 1 positions 1->10 fixes; East 1 positions 1->10 does not
```

No CP-SAT run is necessary.

## Interpretation

This closes the exact proposal that the three gaps are literal normalized
Waite continuations under one-update-per-character ordinary GAK. It does not
reject:

- the ten-character `THAT WHICH` core;
- different continuations after that core;
- a context-dependent/XGAK architecture;
- the anthology as a separate clue rather than plaintext.

The result is an application of the previously observed length-11 split, not a
new cryptographic property of the Eye messages. Its value is lane closure:
source selection does not rescue the random-gap compatibility witness.

## Reproduction

Download the public OCR files:

```text
https://archive.org/download/b24927363_0001/b24927363_0001_djvu.txt
https://archive.org/download/b24927363_0002/b24927363_0002_djvu.txt
```

Then run:

```bash
PYTHONPATH=src python scripts/run_source_selected_connected_gap_gak.py \
  b24927363_0001_djvu.txt b24927363_0002_djvu.txt
```
