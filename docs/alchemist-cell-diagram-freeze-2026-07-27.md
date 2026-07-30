# Alchemist cell diagram — frozen audit

## Question

Does `data/biome_impl/alchemist_secret_background.png` specify a small,
developer-feasible operation that has an exact consequence in the canonical
Eye Messages?

The asset is tested on its own. A partial fit will not be combined with Wall,
Gate, or other clue theories.

## Asset-only observations

The installed 512-by-512 RGBA image has SHA-256:

```text
545b4b57c9d046f8bb59828ae0d3669f3a1bde3f7d46419c79281677c905733a
```

Its only opaque content is one diagram with two aligned bands:

- the upper band has eight groups of two rows by eight cells;
- the lower band has eight groups of two rows by five cells;
- each group contains exactly one gold cell across its two rows;
- the eight upper gold columns form a permutation of `0..7`;
- upper and lower gold rows alternate, in opposite phases.

These facts will be recovered from pixels and asserted before any Eye test.
The authored colors, exact grid geometry, and every non-gold cell are part of
the parser checks.

## Frozen interpretations

Each aligned group is one record:

```text
(upper-band column in 0..7, lower-band column in 0..4, two row bits)
```

Only the following global ambiguities are admitted:

1. group order is left-to-right or right-to-left;
2. column numbering is left-to-right or right-to-left, applied to both bands;
3. if row is consumed, upper/lower may be globally complemented.

No independent group permutations, per-record reflections, arbitrary
rotations, fitted offsets, or arithmetic recodings are allowed.

Three primary outputs are declared:

- the eight lower-band columns in authored group order: a five-symbol tape;
- the function `f:{0..7}->{0..4}` obtained by sorting records by their
  upper-band column.
- the one-hot cell indices when each complete `2×8` and `2×5` group is
  linearized. Row-major order gives an eight-digit hexadecimal tape and an
  eight-digit decimal tape; column-major order is the only admitted alternate
  linearization.

The upper-band column sequence itself is retained as the independently
authored permutation of eight records. Row bits may therefore be binary
controls or the high part of the `0..15` / `0..9` cell indices; neither reading
is privileged before the source searches.

## Frozen canonical tests

Tests run in this order:

1. **Source constants.** Search the WAK, executable, and eligible source
   mirrors for each complete hex/decimal tape as text and as 32-bit
   little-/big-endian values. Test whether paired tapes are literal
   base-conversions under the frozen global orientations; do not scan fitted
   digit permutations.
2. **Literal tape.** Search each admitted five-symbol tape exactly in every
   canonical raw-direction stream, with and without its one-trigram header.
   Report every occurrence; do not score near matches.
3. **Header-cycle alignment.** Compare the authored eight-record permutation
   with the independently selected eight successful edges of the canonical
   first-digit cycle. Only cyclic origin and global reversal are allowed.
4. **Fixed-table consumers.** Apply only operations whose complete rule is
   specified by the diagram before seeing Eye output. A many-to-one table
   must retain the equality signatures of all six registered `THAT WHICH`
   windows if proposed as a visible decoder.
5. **Deck/state mechanism.** A GAK/XGAK interpretation is considered only if
   the diagram fixes the deck operation or selector, not merely eight labels.
   It must replay a planted fixture first and then satisfy a held-out
   canonical isomorph consequence.

The canonical reading remains fixed: accepted trigrams are
`25a+5b+c` in `0..82`. Alternative Eye orders are outside this audit.

## Decision rule

Promote the diagram as an Eye clue only if it selects a complete,
low-capacity mechanism and predicts a canonical fact not used to choose that
mechanism. A literal absence, a header mismatch, or destruction of the known
isomorphs closes the corresponding interpretation but not every possible use
of the asset.
