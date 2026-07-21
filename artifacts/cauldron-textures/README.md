# Cauldron Room sand-texture audit

Source discussion: [Sand Pattern in Cauldron Room](https://discord.com/channels/453998283174576133/1227024108286644284/threads/1396453208079073370).
The accompanying world image was linked to [Noita Map at the Cauldron
Room](https://noitamap.com/?x=3821&y=5342&zoom=985&map=regular-main-branch).

The small material textures in `data/materials_gfx/` were extracted from the
user's installed `data.wak`. `earth.png` is the texture named by the
`sand_static` material. Its properties are:

```text
dimensions: 48 x 45 = 2160 = 83*26 + 2
palette:    (70,65,40) x1957; (95,87,49) x203
sha256:     22d0ec83c6ea7d12778284f90413b8edc0abbf07fba623cb38fba55796db79ad
```

`earth_bright.png` and `earth_bright_red.png` contain the identical binary
203-pixel mask under different palettes. The installed archive contains 14
48-by-45 material PNGs, so the near-`83x26` area is a material-tile convention,
not unique to this texture.

The reproducible direct test is
[`scripts/analyze_cauldron_texture.py`](../../scripts/analyze_cauldron_texture.py).
It enumerates the eight image orientations and only the three ways to remove
two boundary pixels before reshaping to 26 by 83. Its matched-null results are
recorded in `docs/research-log.md`; no plaintext or significant static signal
survives.
