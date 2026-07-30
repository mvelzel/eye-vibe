# Wide-net Eye investigation — results (2026-07-30)

## Scope and rule

This pass deliberately cast a wide net across three independent lanes:

1. developer-feasible readings of the later Alchemist diagram;
2. installed-game asset, WAK, and runtime/source archaeology;
3. current public/Discord-adjacent cryptanalytic proposals and prior art.

Each proposed clue was tested in isolation. A partial match was not allowed to
borrow evidential weight from another theory. The canonical Eye reading stayed
fixed: direction trigrams are `25a+5b+c` in the observed `0..82` alphabet, and
the six registered `THAT WHICH` windows must retain equality pattern
`A.B.CB.AC.` under a direct symbol decoder.

## 1. Alchemist cell diagram

### Recovered asset

The installed `data/biome_impl/alchemist_secret_background.png` is a 512×512
RGBA image with SHA-256
`545b4b57c9d046f8bb59828ae0d3669f3a1bde3f7d46419c79281677c905733a`.
Its opaque geometry is exact and small: eight one-hot records in a 2×8 upper
band and eight one-hot records in a 2×5 lower band. The upper columns are the
permutation `(4,2,1,6,5,7,0,3)`; the lower columns are
`(4,2,4,3,0,2,4,1)`; rows alternate in opposite phases.

The parser and pixel assertions are in
[`src/eye_mystery/alchemist_cell_diagram.py`](../src/eye_mystery/alchemist_cell_diagram.py),
with the raw asset under
[`artifacts/alchemist-cell-diagram/raw/`](../artifacts/alchemist-cell-diagram/raw/).

### Pre-registered readings

Allowing only global group reversal, common column reversal, and global row
complement gives the following distinct direct outputs:

| reading | authored orientation | reflected orientation |
|---|---:|---:|
| lower five-symbol tape | `4 2 4 3 0 2 4 1` | `3 0 2 4 1 0 2 0` |
| upper-column-sorted 8→5 table | `4 4 2 1 4 0 3 2` | `2 1 4 0 3 2 0 0` |
| row-major upper one-hot hex | `4A1E5F0B` | `C78296D3` |
| column-major upper one-hot hex | `852DAF07` | `9E143CB6` |
| row-major lower one-hot decimal | `92935291` | `35291525` |
| column-major lower one-hot decimal | `94961492` | `61492141` |

The complete orientation table is reproducible with:

```bash
PYTHONPATH=src python scripts/audit_alchemist_cell_diagram.py \
  artifacts/alchemist-cell-diagram/raw/alchemist_secret_background.png \
  --source /path/to/noita.exe --source /path/to/data.wak
```

### Screens and result

- None of the admitted five-symbol tapes occurs exactly in any canonical raw
  direction stream.
- None of the 16 hex/decimal tapes occurs as ASCII or as a 32-bit little- or
  big-endian integer in the installed `noita.exe` or `data.wak`.
- The upper permutation is not dihedrally equivalent to the eight successful
  edges of the independent first-digit header cycle. The canonical edge ranks
  are `(7,0,1,2,3,4,5,6)`; no admitted diagram orientation matches them.
- The direct sorted 8→5 table gives `0/6` exact `THAT WHICH` equality
  signatures in every admitted orientation. This has a simple cardinality
  obstruction: a direct 8→5 map can create at most five output classes, while
  the target signature contains six classes.
- An independent finite screen of the predeclared binary/base-five feature
  variants (rank bits, digit parity, high/low digit flags, order and polarity)
  also found `0` all-window models. Full 2×5/2×8 state readings reached only
  the duplicated East1/West1 window, never an independent holdout. Fixed
  checksum/selector families produced only isolated header coincidences and no
  all-nine rule.

**Disposition:** the diagram is a real structured later asset, but no direct
Eye decoder, selector, or held-out consequence survived. It remains a binary
standalone hypothesis only if a future investigation finds an authored
external state operation; it does not corroborate Gate, Wall, or locale lanes.

## 2. Installed-game and engine archaeology

The current WAK contains 14,745 entries. Targeted path/text searches found no
file named for an Eye message, cipher, checksum, glyph language, or Finnish
key. Textual scans found no relevant `cipher`, `checksum`, `true god`,
Kalevala, `83`, or `101` declaration. The only cryptic-looking string was the
credits heading `CRYPTIC HIGHSCORES`, unrelated to the Eye data. The orb-room
plan contains ordinary Hermetic lore, not a decoder specification.

The installed Eye-related Lua scripts are ordinary interaction/mechanics:
`eye_check.lua` toggles an evil-eye particle emitter, while the snowcave and
eyespot scripts handle teleports, books, or boss effects. The binary initializer
contains the packed Eye rows but its caller supplies only coordinates/panel; no
runtime decryption key or message handler was found.

The broad asset sweep checked cave-eye textures, Gate symbols and ornaments,
rune strips, symbol-room layouts, temporary symbols, music/kantele/runestone
sequences, and hidden text. These are either decorative or have explicit
gameplay consumers with no Eye selector. One apparent survivor,
`data/biome_impl/hidden/mountain_text.png`, is already identified in the
public lore documentation as the ordinary message “Devoted seeker after true
wisdom / know this we are watching you”; it is not an unknown Eye interface.

**Disposition:** no in-game asset or current runtime path supplied a complete
Eye key/operation. This is a broad negative, not proof that no secret code is
present in native code or an unrecovered historical build.

## 3. Orb-lore indexed-sum proposal

A recent public proposal indexes Finnish Orb-room lore by the sum of each raw
three-eye direction group. Reproduction confirms a real mechanical feature:
the first 15 sums of West4 are
`5,6,1,9,3,6,2,4,5,4,2,3,5,3,7`, or
`561936245423537`. East4 has the same body suffix with a different first
header digit (`361936...`), and East5 shares the `561936...` prefix.

That repeat is expected from the already-known shared ciphertext body; it is
not an independent language clue. Applying the repository’s explicit Finnish
Orb-lore key walk to West4 yields the reproducible output
`KEENKESIKISKKKS`, not Finnish plaintext. The public proposer later described
their Google-Translate result as non-reproducible; a native-Finnish response
also rejected it as gibberish.

**Disposition:** useful as a clean example of how a visually plausible
numeric/lore index can be generated by shared body structure, but not a decoder
or an Eye connection.

## 4. Public prior art and live proposals

The recent [`Null-H3x/Eyes`](https://github.com/Null-H3x/Eyes) repository is a
valuable independent consolidation, not a solved plaintext. Its latest
documentation reports a 13-class isomorph atlas, including a high-confidence
`A.B..B.A` class that the repository’s stricter repeat threshold misses, and
keeps the static-vs-dynamic deck fork open. Those are external claims/tooling;
they do not become evidence for a clue theory merely by appearing in another
repository.

The public Steam discussion records a concrete but incomplete “Holdswap Array”
idea: a used ciphertext symbol swaps with a per-plaintext hold box to explain
minimal side effects, no doubles, and the near-duplicate E4/E5 isomorph. The
proposal does not specify output timing, the swap partner, initial state, or a
complete reversible transition, so it cannot yet be simulated or falsified.
Its reported repeat constraints are observations of the existing isomorph
data, not a successful replay.

Other public wheel, 5×5 automaton, Rubik/cube, and cutscene-state proposals
either conflict with the fixed 0–82 trigram corpus or have published gibberish
outputs. They remain separate low-priority hypotheses, not combined support.

## Bottom line

The wide net produced no complete Eye solution and no new plaintext. It did
produce three useful boundaries:

1. the Alchemist diagram’s most natural developer-sized readings are directly
   incompatible with the six canonical isomorph signatures;
2. the installed game exposes no plain-text Eye key, decoder, or selector in
   its current WAK/runtime interface, and the strongest apparent hidden-text
   candidate is ordinary lore;
3. the current live cryptanalytic frontier is still an ordered dynamic
   permutation/deck model. The Holdswap idea is the clearest newly formalizable
   public proposal, but it first needs a complete state transition and planted
   fixture before it deserves an Eye run.

No fringe lane should be promoted until it supplies that complete chain plus a
held-out Eye consequence.
