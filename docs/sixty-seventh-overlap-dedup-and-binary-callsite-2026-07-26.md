# Sixty-seventh pass: overlap deduplication and binary callsite

**Date:** 26 July 2026  
**Outcome:** two wide-horizon lanes closed; no decoder recovered

## 1. Parameterized-overlap work was already done

The sixty-sixth-pass horizon proposed treating the seven registered
equality-isomorphic factors as parameterized strings, composing their
renamings, and looking for overlap closure. A targeted project-history audit
shows that this is not a fresh unexecuted lane.

Three previous exact screens cover its useful forms:

1. `scripts/analyze_isomorph_group_closure.py` composed the seven partial
   renaming maps and their inverses through reduced-word depth five. With
   at least two forced edges per retained word, the untrimmed maps produced
   4,339 restrictions and a certified 109-element conflict clique.
2. The same calculation was ordinary under domain/image/fixed-point-matched
   null maps. At trim two, 9/10 nulls equaled or exceeded the observed
   85-element clique; at trim three, 11/40 equaled or exceeded 70.
3. `scripts/analyze_delayed_isomorph_groups.py` exhaustively grouped
   repeat-rich equality patterns at seed lengths 6 through 14, requiring at
   least three occurrences and two repeated labels. Every positive two-symbol
   delayed extension was a shifted or nested view of the same known episode;
   no independent group replicated it.

The stricter checkpoint form had also tested all 72 directed panel pairs:
literal and equality-isomorphic suffix/prefix overlap were both zero once two
repeat validations were required.

These negatives have a common reason. The strongest Eye factor maps only
25/83 visible labels, so partial-map composition rapidly loses observed
support and does not close as it did in solved practice cipher #2. Recasting
the same sparse maps as word equations does not add information.

**Decision:** close parameterized overlap until a new longer factor, an
independently authored label correspondence, or another source of missing
edges arrives. Do not rerun the historical group closure under new
terminology.

## 2. Frozen binary question

The verified function at `0x0061ed60` contains the nine packed Eye arrays.
The remaining binary-interface question was:

> Does its caller pass a key, state, seed, ordering object, or other value that
> could constrain decoding?

The installed executable remains:

```text
SHA-256
808d2a0ab51ea0b46e9ad2aeb3327a4b0ce3feae04f32ba26326bf585b5779bd
```

The audit scans the complete `.text` section for `E8 rel32` encodings
resolving to the initializer and verifies independent exact instruction
windows around both caller and callee. A planted fixture checks the relative
address arithmetic and full signature conjunction.

## 3. Exact caller interface

There is exactly one direct call:

```text
initializer       0x0061ed60
direct callsite   0x00620129
direct calls      1
```

The compiled calling convention is:

```text
ECX          world x coordinate
EDX          world y coordinate
[ESP]        panel index
```

At function entry, the initializer saves ECX and EDX and reads its sole stack
argument. The caller:

- initializes the panel index to zero;
- increments it until the fixed bound nine;
- pushes that index as the only stack argument;
- computes the two position coordinates immediately before the call.

Its input side selector is exactly a parity filter:

```text
selector +1  keeps indices 0,2,4,6,8   (five panels)
selector -1  keeps indices 1,3,5,7     (four panels)
```

This independently confirms the alternating compiled order:

```text
E1,W1,E2,W2,E3,W3,E4,W4,E5
```

The surrounding caller uses seeded randomness to choose valid placement
coordinates. That randomness does not enter the packed arrays or select their
values; it supplies only the location arguments.

## 4. Interpretation

The 2025 binary exposes no caller-supplied cipher key, seed, state machine, or
companion table. The only variable inputs are where to render an Eye message
and which of the nine precompiled messages to render. This is consistent with
the earlier finding that the initializer merely unpacks base-seven constants.

This result is narrower than claiming the executable contains no clue
anywhere. It closes the direct caller interface as a decoding source. Mining
the placement RNG constant as a key would be retrospective constant selection
with no data path into message content.

A 2020 executable could still verify chronology and release stability. It is
unlikely to decode the messages unless it contains a materially different
caller interface or adjacent authored object.

## Reproduction

```text
PYTHONPATH=src python3 scripts/verify_eye_callsite.py /path/to/noita.exe
PYTHONPATH=src python3 -m unittest tests.test_binary_initializer
```

Implementation:

- `src/eye_mystery/binary_initializer.py`
- `scripts/verify_eye_callsite.py`
- `tests/test_binary_initializer.py`
