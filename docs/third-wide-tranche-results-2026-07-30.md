# Third wide-search tranche — 2026-07-30

This tranche kept four hypotheses independent: native renderer payloads,
historical authoring, source-selected deck families, and non-WAK side channels.
It produced no decoder or plaintext.

## Native executable

The release binary contains more than the packed rows: a neighboring method
builds five 11×7 direction-glyph frames from obfuscated 64-bit constants.  A
separate parser maps `'0'..'4'` directly to those five frames and `'5'` to a
row separator.  The method is a renderer atlas with an explicit numeric order,
not an 83-card key or decryptor.  The dev build retains generic debug and
achievement strings but neither this atlas nor the substantive packed words.
See [`compiled-eye-atlas-results-2026-07-30.md`](compiled-eye-atlas-results-2026-07-30.md).

## Historical stability

An independently dated April 2021 decompilation reproduces all 150 packed
words and all nine storage streams exactly, including the newline marker, with
only reverse/divide-by-seven/base-seven decoding.  It exposes no key or state.
The public data mirror dates separate eyespot/book machinery to February 2021
and shows it never consumes the Eye arrays.  Pre-1.0 executable comparison is
still blocked by the entitled historical depot.

## Developer-sized deck families

Twenty-one source-selected 83-card orders (ASCII, BDMAGICK/trailer, runic,
periodic-table, Noita lore/books, Wall text, and translation order) were paired
with fourteen reversible small deck updates in both directions.  Every model
passed a planted exact replay before Eye scoring.  No nontrivial model
preserved all seven registered isomorph contexts or literal resynchronizations.
The best rank-instruction swap-front result was 5/6 training plus the withheld
context, but failed the first-cross-late check; the result was identical for
all initial orders and therefore says nothing about alphabet choice.

## Literal side channels

The six canonical cave-eye PNGs have ordinary metadata only; the runic font is
a generic 240-ID atlas; translations, schemas, FMOD banks, video, and the dev
string surface contain no 83/101 table or Eye-message event.  A memory-mapped
scan of `data.wak` finds zero hits for every substantive packed word and no
complete stream; the only admitted hit is the two-symbol terminal word
`0x8c` accidentally occurring in image/PSD bytes.

## Boundary

The native binary is therefore confirmed as a storage/renderer implementation,
not a runtime cipher.  The corpus was already fixed by April 2021, so a key
must be an offline authoring input or a transformed/runtime-constructed source
not present literally in the current files.  The remaining historical delta
and any new operation must be tested with an independently selected rule and a
held-out Eye consequence; no partial match from these lanes is promoted.
