# Earthquake-gear Wadsworth audit — results

## Outcome

The fully specified visible/arithmetic-progression ciphertext disk is
rejected, including **every fixed choice of the three gear weights**, for both
26- and 29-symbol plaintext disks.

Lymm's broader original proposal is not rejected because it explicitly allows
an arbitrary hidden permutation of the 83 ciphertext symbols. That hidden
relaxation remained solver-indeterminate in bounded runs.

## Equal weights in visible ranks

For weights `(1,1,1)`, all 82 nonzero rank scales and both irregular-tape
directions were exhausted. The best one global configuration fits no complete
context and only one of 141 consecutive transitions:

| plaintext disk | complete contexts | best total prefix | best configuration |
|---:|---:|---:|---|
| 26 | `0/7` | `1/141` | direction `-1`, scale `5` |
| 29 | `0/7` | `1/141` | direction `-1`, scale `5` |

Maximizing each context separately over the same configuration family gives:

| context | best prefix |
|---|---:|
| `first-gap30` | `0/17` |
| `first-cross` | `1/17` |
| `first-cross-late` | `1/17` |
| `first-gap28` | `1/8` |
| `last-west4` | `1/29` |
| `last-east5` | `1/29` |
| `last-east3` | `1/24` |

This is an exact failure, not a language score.

## Arbitrary fixed weights in visible ranks

The stronger independent-phase screen began with all
`82×83×83 = 564,698` normalized parameter triples. On the first three
transitions of `first-gap30`, survivor counts were:

| plaintext disk | transition 0 | transition 1 | transition 2 |
|---:|---:|---:|---:|
| 26 | `12,269` | `171` | **`0`** |
| 29 | `13,888` | `248` | **`0`** |

This screen grants fresh phases and a fresh distance at every transition,
discarding the real gear machine's state continuity. Therefore the empty
intersection rejects every fixed-weight Earthquake-gear Wadsworth model whose
hidden ciphertext order is an arithmetic progression of the visible
base-five ranks.

The planted detector retains its generating triple `(scale,w20,w17)`.

## Arbitrary hidden ciphertext disk

For equal weights, the phase-independent same-distance relaxation has:

```text
m=26: 159 allowed increment pairs
m=29: 181 allowed increment pairs
```

All seven individual `m=26` contexts are SAT under this highly permissive
model. The first-family combination is also SAT:

| subset | status | elapsed |
|---|---|---:|
| each individual context | SAT | `0.04–0.96 s` |
| first three contexts | SAT | `3.49 s` |
| all four first-family contexts | SAT | `37.64 s` |
| last two contexts | unknown | `60.04 s` |
| all three last-family contexts | unknown | `60.22 s` |

On all seven contexts, two independent encodings reached the same bounded
outcome:

| disk | encoding | status | timeout | formula bytes |
|---:|---|---|---:|---:|
| 26 | linear integer | unknown | `120 s` | `819,734` |
| 26 | seven-bit | unknown | `120 s` | `992,730` |
| 29 | linear integer | unknown | `120 s` | `911,190` |
| 29 | seven-bit | unknown | `120 s` | `1,102,234` |

Both encodings pass planted positive controls. `unknown` is not evidence for
or against the hidden-disk construction.

## Interpretation

The Earthquake circle remains interesting as an eligible in-game vocabulary:
the authored `24/20/17` bands, the broken inner periodicity, and the already
known Eye `24/20/17` quantities are real. The community gear proposal is also
a legitimate stateful cipher and not an Easter-egg substitution guess.

What is now closed is the tempting numeric shortcut that the orthodox
base-five ranks, or any arithmetic progression of them, are the Wadsworth
ciphertext disk. The failure is weight-independent and occurs within three
transitions of one accepted repeated passage.

What remains open is the expensive part Lymm allowed from the beginning: an
arbitrary 83-symbol disk order. Without an independent order, that model has
71 observed coordinate variables and enough capacity that SAT would not
decode anything. Reopen it only with:

1. an in-game or developer-authored disk ordering;
2. a stronger exact solver that resolves the registered hidden relaxation;
3. a new invariant that removes the arbitrary permutation; or
4. a complete phase-continuous witness that replays all accepted contexts and
   survives a matched relabeling control.

Lymm's later imperfection plots give an additional qualitative warning: this
specific machine makes isomorphs, but apparently not with the Eye corpus's
long, frequently recurring stability. That observation is not multiplied
with the exact direct-disk rejection.

## Reproduction

```bash
PYTHONPATH=src python scripts/audit_earthquake_gears.py \
  --alphabet-sizes 26 29 --skip-hidden
PYTHONPATH=src python scripts/audit_earthquake_gears.py \
  --alphabet-sizes 26 29 --relaxed-only --timeout-ms 120000
PYTHONPATH=src python -m unittest tests.test_earthquake_gears
```
