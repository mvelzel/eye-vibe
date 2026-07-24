# Twentieth audit — desert glyphs and “Diamond Readings”

## Outcome

This audit separates two old ideas that had been conflated:

1. Naugam's `85`-cell weighted-walk diamond;
2. defektu's paired-trigram “Diamond Readings” transform.

The first does **not** provide independent `24,20,16,85` asset measurements.
Those numbers are consequences of an analyst-chosen Manhattan board. The
second is an exactly reproducible 19-symbol transform grounded in a real trio
of desert-ruin assets. Its elevated IoC survives simple matched controls, but
not strongly enough to promote after the visible choice family and historical
method search are considered.

So lane G's quoted-number premise is rejected, while the exact desert-glyph
transform remains a medium-low-priority intermediate representation.

## Primary material acquired

The original public document is:

- [Noita — Diamond Readings](https://docs.google.com/document/d/1sIvuJY-z1kuQWB4x46WHkNDb1H_Xc5YaTZq4h-ZBFHY/edit)

The installed WAK contains:

| glyph | asset | size | SHA-256 |
|---|---|---:|---|
| diamond | `desert_ruins_block_01_visual.png` | `23×20` | `a81400197542572d49092fa253a5a8d72301e15a3c2e0eb1d4c2bfa87b0bd608` |
| three ovals | `desert_ruins_block_05_visual.png` | `23×18` | `c89b5a36614303ce117bb3a802d4c5a913c9d0f92307e646868a005c9b49e209` |
| `¡!¡` strokes | `desert_ruins_block_07_visual.png` | `20×15` | `b8733c16e4b5de748ed01130482c0ba7950413288ddb2ec7aa60a1ce599b1e98` |

All three, and only these three decorated blocks, have weight `0.6` in:

```text
data/scripts/props/overworld_desert_ruins_spawner.lua
```

The spawner also avoids repeating one block within a stack. This validates
the document's observation that the three glyphs form an objectively selected
asset class. The
[Noita Wiki's desert-glyph entry](https://noita.wiki.gg/wiki/Mysteries_and_Oddities#Desert_Glyphs)
independently identifies the same trio.

The assets do **not** author the numbers `24,20,16,85`.

## Why the 85-cell claim is circular

The March–April 2023 proposal assigns the first, second, and third eye of a
trigram walk lengths `1,2,3`. Four directional eyes move on the square grid;
the centred eye does not move. All endpoints therefore lie in the Manhattan
ball of radius:

```text
1 + 2 + 3 = 6
```

A radius-`r` Manhattan shell has `4r` cells, giving:

```text
r=6 -> 24
r=5 -> 20
r=4 -> 16
```

The complete radius-six ball has:

```text
1 + 2r(r+1) = 1 + 2·6·7 = 85
```

Thus the apparent match to Earthquake-circle row lengths is produced once
the analyst chooses walk weights `1,2,3`; it is not a measurement of the
diamond sprite. The attached numbered-diamond image is a constructed
`0..84` board. The desert asset contributes only the broad idea “diamond.”

This also explains why the proposal cannot explain the accepted 83-symbol
alphabet by itself: 125 trigrams collapse onto 85 endpoints, with two board
cells then declared unused.

## Exact paired-trigram transform

The separate defektu document can be reconstructed exactly from the canonical
Eye streams.

Take accepted trigrams two at a time. The first is the `y` record, the second
the `x` record. Pad an odd final record with `000`. The asset-derived component
orders used by the document are:

```text
y order = 021
x order = 120
```

For East 1, the first two accepted trigrams are:

```text
y = 200
x = 231
```

They become:

```text
y[021] = 2,0,0
x[120] = 3,1,2
```

Method 1 emits:

```text
5x+y = 17,5,10
```

Method 2 emits:

```text
x²+y = 11,1,4
```

Across all nine messages, the implementation reproduces every published
output value, including the zero-padded final triples:

```text
east1  150 outputs
west1  156
east2  177
west2  153
east3  207
west3  186
east4  180
west4  180
east5  171
```

Implementation:

- `src/eye_mystery/diamond_reading.py`
- `scripts/analyze_diamond_reading.py`
- `tests/test_diamond_reading.py`

## IoC audit

The document's values are reproduced exactly:

| message | `5x+y` IoC | `x²+y` IoC |
|---|---:|---:|
| east1 | .04170022 | .06908277 |
| west1 | .04292804 | .06972705 |
| east2 | .04461993 | .07569337 |
| west2 | .04884761 | .08144135 |
| east3 | .04497913 | .08503354 |
| west3 | .04556815 | .08032549 |
| east4 | .04121664 | .07063935 |
| west4 | .04605835 | .08547486 |
| east5 | .04664603 | .08022016 |

The correct uniform-input baselines are:

```text
5x+y   .0400
x²+y  .0624
```

The squared baseline is not `1/21`. Of the nominal values `0..20`, `14` and
`15` are unreachable, and low values have multiple preimages:

```text
preimages(4)=3
preimages(1,2,3,5)=2
all other reachable values=1
```

The many-to-one map therefore creates high IoC before any language structure
is present.

The document alignment is the unique highest aggregate ordered-collision
score among the six relative component alignments:

```text
20272, 20206, 21234, 20224, 20590, 19674
                 ^
              document
```

That ordering was inspected historically, so it is not a prospective
one-in-six result. Two 20,000-control max-family tests compare the observed
`21234` against the best of all six alignments in every control:

```text
reassociate whole x trigrams, preserve y/x roles and zero padding
383 / 20000 at least observed
corrected empirical tail = 384 / 20001 = .01919904

cyclically shift each message's x-trigram tape against its y tape
275 / 20000 at least observed
corrected empirical tail = 276 / 20001 = .01379931
```

These controls correct the six geometric alignments, but not selection among
the many formulas tried before publication. In June 2023 the author also
characterised the high-IoC result as a coincidence and noted that summed eye
values often elevate IoC. The result is therefore suggestive structure, not
fresh evidence at the `.01` level and certainly not plaintext.

## Verdict and next use

Reject:

- `24,20,16` as measured radii of the Noita diamond sprite;
- `85` as an independently authored asset count;
- the old IoC values as language evidence without a matched transform null.

Retain:

- the three equally weighted decorated desert blocks as a deliberate class;
- the exact `021/120` paired-trigram geometry;
- `5x+y` as the lossless 25-symbol construction;
- `x²+y` as a lossy 19-symbol candidate representation with a modest,
  post-selected structural excess.

Do not launch an unconstrained substitution search on the 19-symbol output.
Its next useful test must predict an unused equality/isomorph field or
outperform the complete six-alignment family on held-out structure. The
prospective Earthquake 17-bit mask remains cleaner and stays ahead of this
branch.
