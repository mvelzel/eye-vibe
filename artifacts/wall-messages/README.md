# Noita Wall Message assets

The files under `raw/` were extracted from the user's installed `data.wak` on
27 July 2026. They are retained as the smallest source set needed to reproduce
the Wall-message geometry and rune-font audit:

- the 12 `data/biome_impl/hidden/*.png` message images;
- `data/biome/_pixel_scenes.xml`, which supplies their world coordinates;
- the separately named `runes` building sprite and XML files, inspected as a
  possible but ultimately unrelated alphabet asset.

Every message PNG has only `IHDR`, `IDAT`, and `IEND` chunks. The 12 current
PNGs are byte-identical to the files in
[`defektu/noita-early-access-data`](https://github.com/defektu/noita-early-access-data),
commit `a3937039fbdb2b743672bebe11088e4c694c4b4a`. That repository commit is dated
2 October 2022, so it establishes payload continuity with a public
early-access-labelled mirror, not a contemporaneous 2019 file timestamp.

The exact decoder and alignment checks are in
`src/eye_mystery/noita_wall_assets.py`.
