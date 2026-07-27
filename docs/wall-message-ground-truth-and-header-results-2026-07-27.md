# Wall Messages — asset ground truth and Eye-header audit

## Outcome

The Wall Messages are a chronologically eligible in-game clue source, and one
new correspondence is worth retaining:

```text
Wall: 50 periods, 61 literal YOU + 2 grammatical omissions, 33 question marks
Eye:  East1 header 50, East3 header 63, East5 header 33
```

Those are exactly the three messages whose full canonical sums are
`4040=40×101`, `5656=56×101`, and `4545=45×101`.

The match is intriguing but unpromoted. The `63` requires editorial repair,
the category order is not independently specified, and no complete decoder or
held-out consequence follows. A particularly readable context extraction,
`AND CREATED GOD`, is also fragile and fails as a literal 83-entry decoder.

## Chronology and source boundary

The Walls predate the Eye Messages. A
[27 September 2019 report](https://www.reddit.com/r/noita/comments/da32dp)
already shows and decodes G9, and an
[October 2019 thread](https://www.reddit.com/r/noita/comments/dfm8a1)
records that all texts were known. The Eyes arrived with 1.0. Wall information
therefore could have been used to construct the Eye cipher, not merely added
later as a solution hint.

The audit uses:

- the exact English surface text in
  [`../artifacts/noita-wall-messages-en.txt`](../artifacts/noita-wall-messages-en.txt);
- the 12 current installed PNGs and their `_pixel_scenes.xml` coordinates;
- the public [Game Lore](https://noita.wiki.gg/wiki/Game_Lore) transcription;
- Ciderhelm's public
  [Wall Messages research document](https://docs.google.com/document/d/1vuI_lK8gzSxIBfnCKjtEpfvcWesMTK0B8DSPyyv7fIo/edit);
- read-only Discord archaeology of Lymm's prior Baconian experiment.

The current PNGs are byte-identical to the public
[`noita-early-access-data`](https://github.com/defektu/noita-early-access-data)
mirror, but its sole commit is dated 2022. This supports payload continuity;
it is not a 2019 timestamp for all 12 files.

## Exact asset findings

All 12 images are static RGBA assets on a `5×7` cell grid. Each visible rune
is a `4×4` opaque bitmap. Exact alignment recovers every authored line
uniquely and gives a bijection between 29 used surface symbols and 29 rune
bitmaps. Case is not encoded; Q and Z are absent from the carrier.

For every symbol, every occurrence has the identical complete `5×7` pixel
template. There are no occurrence-level shape or invisible-RGB variants, and
the PNGs have no ancillary chunks. The English text is therefore authored
directly in the asset codebook rather than being a lossy translation of a
Finnish hidden layer.

The exact leading line offsets sum to 90, not the reported 83. Direct
per-message, per-line, clause, and word XOR overlays do not expose a second
rune stream. The separately named building `runes.png` is decorative and
supplies no shared Wall alphabet interface.

## Bounded steganography screens

The previously recovered practice-puzzle rule—punctuation/capital boundaries
plus word-length Morse—fails unchanged on the Walls: 46 of 98 groups are valid
Morse, 52 invalid, with no readable run longer than three.

A separate finite Baconian screen tested 1,120 models over 515 words:

- eight natural geographic/artifact orders;
- visible typography and punctuation;
- word-length thresholds and parity;
- `you*` membership;
- simple features of the authored `4×4` rune masks;
- bit order and inversion.

One hundred sixty models avoid Bacon values 26–31, but every output is
low-diversity gibberish. This rejects the declared visible-feature family, not
an arbitrary fitted partition of the vocabulary.

The Wall also supplies twelve source-selected 83-bit masks from
`50+33` punctuation records, `50+(19+14)` punctuation records, and 83 `you*`
tokens. None yields one common binary tape on the six canonical
`THAT WHICH` isomorph windows. The best family agreement is `101/150`;
100,000 independently shuffled family controls give corrected tail `.86040140`.

## The `50,63,33` and `AND CREATED GOD` candidate

Order the messages by world Y:

```text
G9 G7 G6 G10 G8 G11 G12 G1 G2 G3 G4 G5
```

There are exactly 83 tokens beginning with `you`: 61 `you`, 19 `your`, two
`you've`, and one `you're`. Number them zero-based. At indices `50,63,33`—the
odd-East headers—the immediately preceding words are:

```text
50 -> AND
63 -> CREATED
33 -> GOD
```

Among the 83 preceding words, the multiplicities are `AND=6`,
`CREATED=3`, and `GOD=3`. A fixed ordered triple under random permutation
would therefore have probability

```text
6×3×3 / (83×82×81) = 1/10209
```

This is descriptive only: the target phrase was noticed before it was frozen.
It is not a discovery p-value.

The result is unique in the frozen `4×2×2` sensitivity family of world-Y,
reverse-world-Y, XML, and reverse-XML orders; zero/one-based indexing; and
preceding/following words. But nearby conventions give unrelated phrases:

```text
world-Y, 0-based, following: FREE THINK DON'T
world-Y, 1-based, previous:  AND NOT GOD
XML,     0-based, previous:  ASK DO CREATED
```

Most importantly, the full literal consumer fails. Mapping all 83 canonical
Eye values to their preceding Wall words gives only 42 distinct outputs and
word salad. On the six fixed `THAT WHICH` windows, only two retain the
canonical equality signature `A.B.CB.AC.`; the six mapped signatures are not
equal. Following-word and `you`-form tables also fail (`40` and `4` distinct
outputs, with one and zero of six signatures preserved).

Thus the Wall table is not a direct substitution decoder compatible with the
canonical isomorph evidence. The count/header coincidence could still be a
selector or clue to a stateful/deck construction, but no such consumer is
currently specified.

## Reproduction and decision

The executable audits are:

- [`../scripts/audit_noita_wall_assets.py`](../scripts/audit_noita_wall_assets.py)
- [`../scripts/audit_wall_baconian.py`](../scripts/audit_wall_baconian.py)
- [`../scripts/audit_wall_83_masks.py`](../scripts/audit_wall_83_masks.py)
- [`../scripts/audit_wall_header_clue.py`](../scripts/audit_wall_header_clue.py)

Retain the exact `50,63,33` correspondence as a lead. Do not promote
`AND CREATED GOD`, use it as plaintext, or fit a Wall-keyed state machine
unless an independent in-game rule chooses the table order, context side, and
consumer while preserving the canonical Eye isomorphs.
