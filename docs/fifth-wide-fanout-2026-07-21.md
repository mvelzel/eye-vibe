# Fifth wide fan-out — frozen before results

This cycle follows the explicit rule “start wide before going deep.” It does
not choose another attractive number or cipher family and elaborate it. Six
mechanically unrelated interpretations receive one cheap necessity test each;
the statistics, comparison families, and stop rules below are fixed before the
Eye results are calculated.

This is not a claim that nobody has ever mentioned any broad family. Novelty
is assessed only after a reproducible survivor exists. The purpose here is to
create genuinely different attack surfaces without silently refitting the same
deck, checksum, or prose model.

## Frozen inputs

- accepted `0..82` trigram reading and exact displayed row boundaries;
- first trigram retained as metadata where a test uses physical rows;
- first trigram omitted where a test explicitly targets bodies;
- natural 3×3 panel grid and independently known within-row shared body-prefix
  lengths `24,5,20`;
- full equality/prefix structure preserved by a null whenever that structure
  can directly affect the statistic.

No English score, crib, Gate number, or `BEXIT` residue is used to select these
six tests.

## Lane A — directed graph route rather than ciphertext

**Interpretation.** Each body is a route through a shared labeled graph. A
designed route should reuse directed edges more than a high-entropy symbolic
stream, even after accounting for copied prefixes.

**Statistic.** Across all nine bodies, count total adjacent transitions minus
the number of distinct directed transitions. This edge-reuse count is fixed as
the sole primary statistic.

**Null.** Shuffle positions jointly inside every exact prefix-tree edge and
independently inside singleton suffixes, preserving message lengths, symbol
multisets, position parity, and the complete copied-prefix hierarchy. The null
may create self-loops, which makes high reuse easier and is conservative for a
positive result.

**Promotion/stop.** Promote only for a corrected upper tail below `0.01`, then
inspect which repeated edges form cycles or predict endpoints. Otherwise close
the literal graph-route compression reading.

## Lane B — two-dimensional local rewrite sheet

**Interpretation.** The visual rows are successive states of a small cellular
or stencil rule rather than wrapped prose.

**Statistic.** Reconstruct authored top/bottom visual row pairs, deduplicate
identical pairs, and fit one global deterministic rule from a top-row
neighborhood to a shifted bottom-row cell. Search radii `0..3` and shifts
`-2..2`; select maximum majority accuracy over the 20 models.

**Null.** Independently cyclically rotate each unique bottom row and rerun the
complete search. This preserves each row's length, symbols, and local texture
while destroying its alignment to the top row. Exact duplicate row pairs are
counted once so copied message prefixes cannot multiply the evidence.

**Promotion/stop.** Promote only below family-corrected `0.01` and only if the
same rule predicts a held-out row pair. Otherwise reject this bounded local
rewrite family, not arbitrary 2D encodings.

## Lane C — direct mixed-radix packet

**Interpretation.** The `0..82` values are literal base-83 digits packing bytes
or seven-bit characters; plaintext need not be one symbol per trigram.

**Statistic.** Convert each body independently from base 83 to base 128 and
base 256 in both digit directions. Select the maximum fraction of ASCII
printable/whitespace output across the four variants.

**Null.** Use the same prefix-tree-preserving shuffles as lane A and reselect
all four variants. This keeps copied prefixes, lengths, and digit multisets.

**Promotion/stop.** Promote only below corrected `0.01`, followed by a strict
format signature or held-out parser. Otherwise reject direct radix packing;
do not optimize arbitrary bit offsets or compression dictionaries.

## Lane D — stable-sort/manual worksheet trace

**Interpretation.** The ciphertext was assembled by repeatedly sorting or
copying physical/spreadsheet records. Numeric/base-five order should then leave
unusually monotone displayed records.

**Statistic.** For each of the six component-priority orders, count inversions
inside every exact displayed trigram row. Select one global order and one
global ascending/descending orientation, not a separate orientation per row.
The score is the fraction of pair relations agreeing with the better global
orientation.

**Null.** Apply a uniform global permutation of labels `0..82`, which preserves
every equality, prefix, message, and row boundary, then reselect the six
component orders and global orientation.

**Promotion/stop.** Promote below corrected `0.01` only if the selected order
also predicts branch or marker order. Otherwise close the literal stable-sort
trace.

## Lane E — nonlinear digitwise 3×3 operator

**Interpretation.** Each grid row is a two-input operation with its diagonal
panel as output. The prior determinant test covers only linear value-level
relations; base-five componentwise arithmetic is a distinct family.

**Statistic.** After each row's known copied prefix, retain only reference
positions where the three panel values are pairwise distinct. Test one global
componentwise operation from the fixed family: sum, both differences,
negative sum, product, half-sum in `F5`, minimum, or maximum. Select the maximum
number of exact three-digit outputs over all three rows.

**Null.** Independently rotate each post-prefix tail, keep the eligible
reference positions fixed, and reselect all eight operations. This preserves
each tail's length and local cyclic texture but breaks cross-panel alignment.

**Promotion/stop.** Promote below corrected `0.01` only if a single operator
predicts a held-out row/segment. Otherwise reject this finite nonlinear suite.

## Lane F — raw-direction turtle drawing

**Interpretation.** Native eye directions are pen motions—centre pauses,
cardinals step—and the body encodes compact paths or glyphs before numeric
trigram conversion.

**Statistic.** Sum path bounding-box areas over all panels and select the more
compact of canonical stream order and actual visual-row scan order. Direction
semantics are fixed by the renderer; no rotations or remapped directions are
searched.

**Null.** Shuffle raw direction positions within the exact prefix hierarchy,
leaving the three-direction markers fixed, and reselect both read orders. This
preserves direction counts, message lengths, and copied prefixes. Because path
endpoints depend only on counts, endpoint closure is deliberately not scored.

**Promotion/stop.** Promote only for a corrected lower tail below `0.01`, then
render the independently selected paths. Otherwise reject literal compact
turtle drawings.

## Selection rule after the fan-out

No lane deepens merely for being the smallest of six ordinary p-values. A lane
must cross its own `0.01` threshold and retain a meaningful effect after its
documented nuisance structure is preserved. If none survives, all six bounded
forms close and the next cycle widens again or returns to unresolved practice
cipher #4; it does not rescue a favourite lane by adding parameters.

## Results

The six primary tests use 2,000 fixed-seed controls. Lane D additionally uses
a separately seeded 10,000-control refinement because its first estimate lay
close to the frozen threshold.

| Lane | Observed selected statistic | Corrected tail | Decision |
|---|---:|---:|---|
| A graph route | `175` reused of `1,018` directed transitions | `87/2001 = 0.043478` upper | stop |
| B local rewrite | `1292/1298 = 0.995378`, radius 3, shift -1 | `1/2001 = 0.000500` upper | nuisance audit required |
| C radix packet | `714/938 = 0.761194` printable, reversed base 128 | `1668/2001 = 0.833583` upper | stop |
| D stable sort | `6743/12408 = 0.543440`, order `(1,2,0)` | `147/10001 = 0.014699` upper | stop |
| E digitwise grid | `3/216`, left minus right | `1895/2001 = 0.947026` upper | stop |
| F turtle path | bounding-area sum `10152`, canonical order | `1053/2001 = 0.526237` lower | stop |

### Why lane B does not promote

The apparent cellular result is a capacity/copy artifact. The selected
radius-three model creates 1,149 arbitrary context rules for only 1,298 cells.
Leave-one-row-pair-out prediction covers just `232/1298 = 17.87%` of cells;
most coverage comes from the first row pairs containing the already-known
copied family prefixes.

A stricter nuisance audit drops the first visual row pair from every message,
so all complete retained pairs begin after every deepest shared body prefix.
Two consequences are decisive:

- the capacity-controlled radius-at-most-one family falls to
  `458/1133 = 0.404237`, with corrected upper tail
  `197/2001 = 0.098451`;
- the radius-three lookup covers only 46 of 1,001 cells under
  leave-one-pair-out validation (`36/46` correct), with almost all remaining
  coverage concentrated in two row pairs containing known later copied
  windows.

Thus the low primary tail rediscovers position synchrony and memorizes sparse
seven-cell contexts. It does not provide a compact row-update law or a
held-out row prediction, so it fails its predeclared promotion condition.

### Outcome

No lane survives. The bounded graph-route, direct radix, stable-sort,
digitwise-grid, and turtle forms close on their primary controls. The local
rewrite form closes after the required held-out/copy audit. This is useful
negative breadth: none should be reopened by adding arbitrary graph labels,
bit offsets, per-row sort directions, larger operator tables, remapped turtle
directions, or still wider cellular neighborhoods.

Reproduction is in `scripts/run_fifth_wide_fanout.py` and
`src/eye_mystery/fifth_wide.py`.
