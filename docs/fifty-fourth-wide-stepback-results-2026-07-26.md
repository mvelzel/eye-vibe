# Fifty-fourth pass — wide step-back and exact no-double signatures

## Outcome

One new metadata relation survives as construction corroboration, while two
literal decoder ideas are negative:

- the marker columns `3,5,8` also describe the visible alphabet cutoff exactly;
- the final-row header stagger does not transfer to the earlier rows;
- the Eyes contain no exact instance of sdlwdr's proposed arithmetic
  no-double replacement signatures.

None of these results is plaintext or a body decoder.

## 1. `358` is also an alphabet descriptor

The independently recovered renderer radix is five, the visible alphabet has
83 values, and the independently recovered marker columns are `3,5,8`. They
satisfy:

```text
83 = 3 × 5² + 8
```

Thus the ordered metadata describes the accepted base-five cube prefix as
three complete 25-symbol slabs plus an eight-symbol tail. It predicts the
maximum accepted glyph:

```text
83 - 1 = 82 = 312₅
```

Among the six orders of the distinct digits `3,5,8`, only `(3,5,8)` satisfies
`q × radix² + remainder = 83`.

This is a real cross-layer identity, but the interpretation was noticed after
both `+358` and alphabet size 83 were known. It cannot receive an independent
p-value. Retain it as a compact reason that the marker may self-describe
locale **and** serialization parameters; do not use `358` as a body key.

The marker trail `!Fi` also admits a mathematical pun: all six Q factoradic
headers are derangements after removing the automatically fixed center.
That fact was already part of the factoradic audit, and the `!Fi` parsing is
retrospective, so it adds no new evidence.

## 2. Literal header-controlled stagger is negative

The final clean gap-11 anchors have starts:

```text
(16,18,17) = 16 + (0,2,1)
```

and `(0,2,1)` is the middle panel W4's component order. The narrow
generalization was: each natural row's middle header supplies the consecutive
three-stream stagger.

After removing each row's established copied opening, scan gaps `2..30` for a
gap with exactly one clean anchor in every panel:

```text
row 1  middle order 120   no common unique gap
row 2  middle order 210   gap 3, starts (90,97,113), not consecutive
row 3  middle order 021   gap 11, starts (16,18,17), exact 021
```

Only the already promoted final record fits. This closes the literal
all-row stagger/interleave reading. An unconstrained multiplex remains
possible in the abstract but has no selector or payload statistic and should
not be searched.

## 3. Exact arithmetic no-double postprocessing is absent

In [this read-only Discord discussion](https://discord.com/channels/453998283174576133/817530812454010910/1420064399036514457),
sdlwdr proposed replacing a would-be double by functions of the preceding two
ciphertext symbols, illustrating:

```text
5,7,7,20 -> 5,7,2,12,35,20
```

The surrounding messages also give multiplier examples using `3,2,5` and
powers of three. One of the practice ciphers uses the simpler special-symbol
double event; that mechanism was already recovered independently in practice
ciphers 1/2 as the exceptional `J`.

The Eye audit searches every panel independently for:

- difference, sum, and product in all six orders;
- raw arithmetic and arithmetic modulo 83;
- original-value multipliers `3,2,5`;
- chained multipliers `3,6,30`;
- powers `3,9,27`.

Positive fixtures recover the exact function and multiplier signatures. The
1,036 Eye glyphs contain:

```text
exact witnesses = 0
```

Therefore this exact proposed postprocessor never visibly executes in the
Eyes. Zero hits do not exclude an untriggered rule or an arbitrary special
control symbol, but the explicit arithmetic variants cannot explain the
observed no-double corpus.

## 4. Practice Cipher 4 side check

Before the Discord context showed that the arithmetic suggestion concerned
the Eyes rather than Cipher 4, the complete small insertion family was also
tested on Cipher 4's recovered action stream. The audit covers:

```text
2 coordinates × 7 arithmetic relations × every period/phase through 32
= 7,392 supported candidates
```

Every control shuffles actions within each portion and reselects the complete
family. The best real cell has only two hits:

```text
coordinate       action83
relation         raw sum
period, phase    31,29
support, hits    40,2
best z           8.7737
corrected tail   177/501 = .353293
```

The high nominal z comes from a rare-event cell and is ordinary after family
selection. This does not advance Cipher 4 and is not an author hint for it.

## Reproduction

```text
PYTHONPATH=src python3 scripts/audit_novel_metadata.py
PYTHONPATH=src python3 scripts/audit_no_double_postprocess.py
PYTHONPATH=src python3 scripts/audit_sdlwdr_cipher4_insertions.py
```

The executable implementations are:

- `src/eye_mystery/novel_metadata.py`
- `src/eye_mystery/no_double_postprocess.py`
- `src/eye_mystery/practice_cipher4_insertion.py`

## Next consequence

The useful survivor is not “use 358 as a key.” It is that the header appears
capable of redundantly declaring the corpus's locale and alphabet boundary.
The next admissible metadata test must predict an unused serialization
parameter or boundary. The body attack remains focused on mechanisms that
explain the promoted state phases and context maps without freely assigning
83 labels.
