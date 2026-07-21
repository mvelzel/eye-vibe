# Procedural-wand 83+18 architecture

## Result

Noita's procedural-wand generator contains a much tighter identity than “the
number 83 appears in the game.” It makes one inclusive integer draw from
`0..100` and partitions that exact 101-state domain as follows:

```text
rolls  0..82   (83 states) -> ACTION_TYPE_MODIFIER
rolls 83..100  (18 states) -> ACTION_TYPE_DRAW_MANY
```

The Eye data independently has a visible alphabet `0..82` and, under the
prefix-trie/mod-101 architecture, exactly 18 absent states `83..100`. Its
compressed body trie contains five branch instructions with fan-outs

```text
2, 3, 3, 2, 3
```

and thirteen outgoing compressed edges. Counting each branch instruction and
each edge gives `5+13=18` hypothetical structural records. The game code does
not, however, serialize a separate card for a node and for each edge. A tree
with five internal nodes and nine leaves executes fourteen card nodes; its
thirteen edges are relationships between those nodes. The 18-record count is
therefore an exploratory representation, not an execution-level identity.

The exact 83-of-101 selector remains an independently authored numerical clue.
Its complement being typed as draw-many is suggestive, but it no longer
qualifies as independent corroboration for the proposed 18-record trie model.
It is not a decoder.

There is also a real execution-level match. `draw_actions(n)` loops over `n`
cards; each drawn card is executed immediately, and a draw-many card can call
`draw_actions` recursively before its parent returns. Noita therefore executes
an ordered depth-first action tree. Ordinary modifiers continue with one draw;
draw-many cards create internal nodes. The Eye topology is a legal abstract
tree: five internal degrees `(2,3,3,2,3)` give
`1 + sum(degree-1) = 9` leaves. But the corresponding execution contains
`5+9=14` card actions, not 18.

## Raw-source audit

The installed sources contain the branch twice, in the standard procedural
generator and the special `wand_petri` sibling:

```lua
if( Random(0,100) < 83 ) then
    card = GetRandomActionWithType(..., ACTION_TYPE_MODIFIER, ...)
else
    card = GetRandomActionWithType(..., ACTION_TYPE_DRAW_MANY, ...)
end
```

The installed `gun_enums.lua` defines `MODIFIER=2` and `DRAW_MANY=3`.
`gun_actions.lua` currently contains 179 modifier definitions and 14 draw-many
definitions, so the 83 and 18 are random-roll ranges—not counts of available
spell cards. Draw-many cards include arities two and three, matching every Eye
branch fan-out, but also larger and variable arities; the fan-out compatibility
is supportive rather than selective.

Across the current WAK, 74 direct `Random(0,100)` comparisons use 22 distinct
operator/threshold pairs. `<83` occurs only in the two duplicated procedural-
wand sources. The loose repository labelled early access has 25 such
comparisons, ten distinct pairs, and the same two copies.

The same standard generator also contains two previously noted dimensions:

```text
ordinary generated deck capacity clamps to 26
unshuffled deck eligibility requires capacity <= 9
```

The Eye display has nine panels, and every complete visual row-pair is 26
trigrams. All four constants—9, 26, 83, and the implicit 101—therefore coexist
in one authored wand/deck mechanism. This is a convergence worth testing, not
a calibrated probability: the constants were assembled retrospectively and
have ordinary gameplay explanations.

Every Eye branching depth is inside the first 26-symbol row. In the
independently decoded East-5-first breadth order those depths are
`(2,5,24,9,20)`, whose A1Z26 readout is `BEXIT`. The wand interpretation gives
that old word a coherent operational reading—branch/exit structure inside one
deck-width record—but the word and the 26 correspondence were known before the
wand synthesis, so this is corroboration rather than a new probability.

## Chronology

The public `defektu/noita-early-access-data` tree contains the 9, 26, and 83
rules, but its single Git commit was uploaded on 2 October 2022. Its label is
archival evidence, not an independently timestamped pre-Eye source.

The earliest independently timestamped copy found in
`vexx32/noita-data` is the initial data commit of 9 February 2021. It contains
the same 83/18 branch, 26 clamp, and unshuffle-9 condition. This is after the
October 2020 Eye release. Under the correct chronology rule it remains fully
eligible as a later decoder clue; it does not prove the developers used this
public game code to construct the original ciphertext.

## Concrete machine hypothesis

A falsifiable reading is now available:

1. Work in a 101-state record space.
2. Values `0..82` are visible modifier/payload records.
3. Values `83..100` are hidden draw-many/control records.
4. A draw-many record opens a two- or three-way continuation.
5. Serializing only visible records yields the nine prefix-related Eye bodies;
   restoring controls yields one execution tree.
6. A complete visual row is one 26-slot deck record.

The source supplies an exact numerical/type analogy for statements one through
three, but no evidence that the Eye values are records in that domain.
Statements four through six are hypotheses. In particular, the real generator
uses the roll only to choose an action **type** and then separately chooses an
action ID; it does not emit the integer roll as a card label. The Eye mechanism
could borrow the vocabulary without literally replaying this Lua.

A literal one-Eye-symbol/one-card execution is already impossible: the merged
body trie has 918 labeled edges, while an ordinary generated wand has at most
26 deck slots. Any surviving model must use the wand as a control machine over
encrypted payload, treat rows as repeated casts, or explain another level of
serialization. This prevents the attractive topology from silently becoming
an unfalsifiable card metaphor.

## Scope-consistency falsification

The strongest-looking checksum connection does not survive local accounting.
The five compressed subtrees have these descendant residues and hypothetical
node-plus-edge record counts:

```text
members   visible residue   local records
all 9          30               18
upper 3        19                4
lower 6        70               11
nested 4       89                7
last 3         13                4
```

The full missing set `83..100` has residue 31. Its attractive closure
`70+31=101` therefore combines the lower-six payload with controls counted
over the entire nine-message tree. The lower-six subtree owns 11, not 18, of
the proposed records. Conversely, the only scope owning all 18 records has
visible descendant residue 30, and `30+31` does not close.

There are five unordered 11-label subsets of `83..100` whose sum is 31 modulo
101, so a local lower-six completion is mathematically possible. Nothing in
the Lua or Eye data selects one of those five subsets or orders it. Searching
them for readable output would be post-hoc fitting.

This rejects the current **local recursive-checksum version** of the model. It
does not prove that the developers never reused the 83/101 partition as a
later clue, but a replacement must independently explain why nodes and edges
are separate records and how controls cross subtree boundaries.

## What remains missing

- There is no canonical bijection from `83..100` to the five branch nodes and
  thirteen continuations.
- Actual recursive execution has fourteen card nodes, not eighteen records;
  `5+13` double-counts the four non-root internal nodes as both cards and
  incoming edges.
- The `70+31` checksum combines a six-message subtree with the entire tree's
  hypothetical control set.
- `DRAW_MANY` types the 18 states collectively but does not order them.
- No Eye marker has yet been shown to encode a specific draw-many card or
  branch arity without fitting.
- The 26-wide rows have failed literal deck-reset tests in previously audited
  shuffle families.
- No renderer or placement code calls the wand generator.
- The natural non-mystery explanation is that 83 approximates a desired
  modifier probability while 26 and 9 are UI/balance limits.

## Next bounded tests

1. Search only for an authored format that explicitly serializes node and edge
   records separately. Without that missing rule, stop treating `5+13` as the
   runtime's record count and do not enumerate 18! assignments.
2. Test whether the five marker/header-selected records predict the branch
   arities `(2,3,3,2,3)` under one fixed, source-derived mapping.
3. Treat each 26-trigram row as a deck trace only under the actual Noita draw,
   modifier, and draw-many semantics; require the model to reproduce copied
   prefixes and the no-adjacent-double property before language scoring.
4. Search later authored assets for an explicit modifier/draw-many or
   83/18 partition near Eyes, Gate, Cauldron, or Cessation. A second independent
   occurrence would distinguish deliberate decoder vocabulary from wand
   balancing.

Reproduction is in `scripts/audit_noita_random_thresholds.py` and
`scripts/analyze_wand_selector.py`.
