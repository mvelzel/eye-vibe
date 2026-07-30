# Compiled Eye glyph atlas — 2026-07-30

## Question

Does the native binary contain only the packed Eye message rows, or does it
also contain the renderer's direction glyphs and their ordering?  This is an
engine audit, not a claim that the renderer's glyph table is the cipher key.

## Frozen observation

In the installed release executable (`noita.exe`, SHA-256
`808d2a0ab51ea0b46e9ad2aeb3327a4b0ce3feae04f32ba26326bf585b5779bd`), the
method at `0x61e880` constructs five 64-bit words, applies the same fixed
XOR/add-with-carry transform to each, and writes five 11×7 image records.  The
exact immediate values are reproduced in
`src/eye_mystery/compiled_eye_atlas.py`.

The neighboring parser at `0x61eaf0` is important: it treats byte `'5'` as a
row separator and maps bytes `'0'` through `'4'` directly to numeric values
`0` through `4`, then indexes records by `value << 5`.  The known initializer at
`0x61ed60` calls into this same renderer family.  Thus this is a five-frame
direction atlas, not an independent 83-symbol table.

Undoing the compiled transform gives:

```text
0031888a38a22318
0031880a10a72358
0031890a70a42318
003589ca10a02318
0031884a1ca12318
```

With the allocator-zeroed buffer and the three compiled top-row pixels, the
frames are reproducibly rendered by `scripts/audit_compiled_eye_atlas.py`.
They are five visually distinct eye glyphs; their order is the direct numeric
direction order already exposed by the parser.  No permutation, key, or
plaintext operation is present in this path.

## Dev-build control

The installed `noita_dev.exe` (SHA-256
`d2f7dbeff72b785bdadd068870343d2821cf4bd2f6c58125fe6a90a1b0900285`) retains
generic debug/source strings and the achievement names
`SecretsOfTheAllSeeing` and `ThreeEyesAreWatchingYou`, but contains neither
the 150 packed message words nor the five atlas immediate signatures.  The
strings therefore identify statistics/assets, not a hidden dev-only decoder.

## Interpretation

This extends the binary boundary in a useful way: the executable contains a
hardcoded renderer atlas whose five-value order is explicit and whose image
bits are not a concealed alphabet/deck.  It strengthens the negative result
for “the native call hides a runtime decryptor,” while preserving the only
plausible binary route—a missing historical/offline construction source—as an
open provenance question.  It does not solve the body machine or plaintext.

Reproduction:

```text
PYTHONPATH=src python scripts/audit_compiled_eye_atlas.py /path/to/noita.exe
PYTHONPATH=src python -m unittest tests.test_compiled_eye_atlas
```
