# Historical Eye authoring audit — 2026-07-30

## Scope and provenance

This lane checked the public `vexx32/noita-data` history, the public Noita
Wayback Machine manifest/release-note index, and a dated independent
decompilation of the Eye renderer.  The historical depot payloads themselves
were not downloaded: the public downloader reports that the paid depot needs
an entitled Steam session.

## Independent 2021 binary reconstruction

Xkeeper's public gist was created 28 April 2021 and contains a decompiled
renderer initializer plus a small decoder:
[noita-eyes.php](https://gist.github.com/Xkeeper0/a6eda18571ef889be291822c400cc6c8).
It stores nine branches of 64-bit words as two 32-bit halves.  Its only data
operation is to reverse the words, divide by seven once (the zero padding
digit), read base-seven remainders, subtract one to recover symbols `0..5`,
and reverse the resulting stream.  There is no key, plaintext, state update,
or external input in this routine.

I parsed all 150 word pairs from the gist and compared them with the
repository's independently reconstructed `corpus_packed_words()` output:

```text
word count:       150 == 150
all 150 words:    exact equality
SHA-256 (u64 LE): 5de6ccb3a045218827b7ddaad0f1493254f501b08addd1929495ce060242de94
```

Decoding all nine branches reproduces `storage_stream(name)` byte-for-byte;
the branch stream lengths including row separators are
`305,317,364,314,423,382,367,370,352`.  After removing row-separator symbol
`5`, these are `297,309,354,306,411,372,357,360,342`, exactly the nine
canonical streams.
The public decompilation therefore independently reproduces the same static
ciphertext corpus found in the installed 2025 executable.  This is a strong
historical stability result, but the gist does not identify its exact game
build and is not an authoring source.

## Public data-history chronology

The earliest `vexx32/noita-data` commit (9 February 2021) already contains
the cave-eye terrain stamps, gate symbols, temporary symbol sprites, intro
assets, hidden mountain text, and ordinary book/lore assets.  Their history
does not contain a source-side Eye key or decoder.  The separate
`eyespot_a`–`eyespot_e` entities and `eye_check.lua`/`eyespot_check.lua` first
appear in commit `a1cf190` (22 February 2021).  The patch places five eye
spots at fixed coordinates and, only when the player is tagged
`tripping_extreme`, loads `book_s_a`–`book_s_e`; these scripts toggle particles,
load books, and teleport/secret-check, but never consume the Eye-message
arrays or a direction/rank stream.  This is a later, separate eye-themed
secret, not an Eye cipher mechanism.

The Wayback index exposes a pre-1.0 manifest (27 July 2020) and the 1.0
manifest (15 October 2020).  The corresponding [pre-1.0
notes](https://raw.githubusercontent.com/acidflow-noita/noita-wayback-machine/main/NOITA_BUILDS_RELEASE_NOTES/5246750520913292821/_release_notes.txt)
and [1.0 notes](https://raw.githubusercontent.com/acidflow-noita/noita-wayback-machine/main/NOITA_BUILDS_RELEASE_NOTES/2326595580679356504/_release_notes.txt)
only say `FEATURE: New secrets..`; neither names an Eye message, key, or
decoder.
Without the entitled depot payloads, this establishes chronology only, not a
byte-level pre-release delta.

## Result

The dated independent decompilation closes a major historical uncertainty:
the 150-word payload and base-seven renderer serialization were already fixed
by April 2021 and exactly match today's corpus.  It gives no developer-sized
ordering or key and no evidence that the later eyespot/book machinery decodes
the Eye Messages.  A pre-1.0 payload comparison remains blocked on an entitled
historical depot download; no speculative key is promoted.
