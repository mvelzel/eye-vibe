# Non-WAK and raw-payload side-channel audit — 2026-07-30

## Scope

This was a read-only audit of places where the Eye renderer could have carried
an authored key, ordering, or decoder hint without appearing as an obvious
Eye-specific script: PNG chunks and palettes, font atlases, translation
tables, generated schemas, FMOD banks, the developer executable, and the raw
`data.wak` byte stream. It also checked the public data-history dates for the
cave Eye assets. The result is a set of negatives, not a claim that every
compressed or runtime-derived channel has been exhaustively understood.

## Reproduction and observations

### Canonical Eye PNGs

The six cave glyph files (`data/biome_impl/caves/eye.png` and
`eye_01.png`…`eye_05.png`) were parsed with a PNG chunk reader and Pillow.
They are ordinary 9×5 grayscale art. The directional files have only normal
colour/gamma chunks; the base file has an Adobe ImageReady software tag. There
is no text, XMP, custom payload, timestamp, palette ordering, or trailing data
that supplies an 83-entry alphabet or key.

Other matching assets do contain normal authoring metadata, but it is not an
Eye channel. For example, `evil_eye_iris.png` has a 2021 Photoshop/SuperPNG
XMP record, and several `room_gate_drop*` and `symbolroom` files have ordinary
Photoshop or GLDPNG timestamps. Those records describe export history and do
not occur on the six canonical glyphs.

### Font atlas

`data/fonts/font_pixel_runes.xml` maps exactly 240 unique Unicode IDs. The IDs
are ordinary runs (ASCII 32–122, selected Latin-1/Cyrillic, punctuation, and
U+221E), and the atlas rectangles are in normal increasing order. It is not a
custom 83-symbol alphabet, substitution table, or Eye-specific ordering. The
regular pixel font is likewise generic and is only referenced by the example
mod in the shipped data.

### Translation table

`data/translations/common.csv` contains 3,707 rows and 25 columns (3,631
unique keys and 72 ordinary duplicate keys); `common_dev.csv` has two rows.
There is no 83-row/83-column block, cipher key, glyph table, checksum table, or
Eye-message record. Keyword hits such as “All-seeing eye” and “Open your eyes”
are ordinary action/status/lore text. Field and line lengths have the natural
distribution of translations, not a hidden 83/101 structure.

### Generated schemas

The 159 XML files under `data/schemas` expose normal component fields such as
`eye_offset_x/y`, `SymbolAltarComponent.symbol_id`, and
`active_symbols`/`normal_symbols`/`endgame_symbols`. A keyword and numeric
scan found no Eye payload, 83/101 table, glyph alphabet, or checksum schema.

### FMOD banks and video directory

The 25 FMOD banks contain normal event names (`all_seeing_eye`, rune start/end
events, liquid and material events). No event, parameter, or bank string is
named for an Eye message, cipher, glyph table, or checksum. `tools_modding`'s
FMOD project metadata has the same result. `data/video` contains only its folder
descriptor and no video payload that could be an ordering source.

### Developer executable

`noita_dev.exe` was scanned in addition to the release binary. Its useful
strings are generic source/PDB paths and ordinary identifiers such as
`SecretsOfTheAllSeeing`, `ThreeEyesAreWatchingYou`, `eye_offset_x/y`, and the
Eye particle/font paths. There is no plaintext payload, key, decoder, or
Eye-specific table in the string or symbol surface. This does not exclude
constants hidden in optimized code; native disassembly already establishes
that the visible Eye initializer is a renderer-only unpacker. A raw scan of
both executables for the regenerated packed words found only the same
short-final-word accident (`0x8c`, index 149); all 149 substantive words and
the complete stream are absent.

### Raw WAK payload scan (new hard negative)

Using `src/eye_mystery/storage_serialization.py`, all 150 packed base-seven
64-bit words implied by the canonical visible corpus were regenerated. The
current `data/data.wak` was memory-mapped and searched for each word in both
endiannesses and for the complete 150-word stream.

* Of the 143 words with at least 21 symbols (and the 112 with at least 22),
  exact aligned or unaligned 64-bit hits were **zero**.
* The complete 150-word byte stream is absent.
* Obvious monotonic byte/16-bit/32-bit sequences for 0…82, 0…100, and 0…124
  are absent in both byte orders.
* The only hits when the short final records are admitted are two accidental
  occurrences of the final two-symbol word (`0x8c`) inside image/PSD bytes;
  they are not aligned or contextual and have no evidentiary value.

Therefore the current WAK does not carry the canonical serialized Eye corpus
as a raw key/table, nor an obvious contiguous integer alphabet. This is only a
negative for literal byte-presence; a compressed, transformed, or runtime
constructed source remains possible.

### Public data-history check

In the public data mirror, the cave Eye paths (and the Gate monster asset used
for comparison) appear in the initial 2021-02-09 commit and are unchanged by
later commits. This dates the mirror entry, not the private authoring time, and
does not reveal a hidden payload.

## Interpretation

No audited side channel supplies a plausible source-selected alphabet, key, or
decoder for the Eye cipher. The strongest new result is the raw-WAK negative:
the canonical 150 packed words are not simply embedded in the current archive.
The metadata, font, locale, schema, FMOD, and developer-binary negatives are
useful stop conditions, while leaving transformed/compressed runtime data and
non-file engine behaviour open for separately justified tests.
