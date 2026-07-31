# Wall-context deck index extension — freeze

## Why this extension exists

The initial 240-model Wall-context deck freeze coupled each direction to one
update index:

- label decoding used the emitted Eye label;
- rank encoding used the supplied Eye rank.

The round-trip implementation already distinguished label-indexed and
rank-indexed updates, but the screen omitted the crossed semantics. In
particular, the ordinary GAK-like interpretation is:

1. locate the emitted label's current rank;
2. emit that rank as plaintext;
3. let the decoded plaintext rank select its Wall operation parameter.

This omission was identified after the initial structural screen but before
running or inspecting any crossed-index Eye score.

## Fixed extension

Retain without change:

- the exact Wall text and world-Y ordering;
- the ten raw/zero-based parameter tables;
- identity and reverse initial decks;
- the six reversible update families;
- the seven registered nonliteral contexts and final-row phase gate.

Add exactly two directions:

1. label-decode with the decoded rank indexing the parameter table;
2. rank-encode with the emitted label indexing the parameter table.

This adds `10×2×6×2 = 240` models. No new table, initial order, update
operation, reset schedule, or output scoring rule may be added after seeing
the results.

Every model must round-trip its paired inverse before touching Eye data.

## Gates

Use the same gates as the original freeze:

1. six registered training isomorphs;
2. held-out `last-east3`;
3. the independently promoted final-row bridge;
4. actual stateful deviation inside that bridge, so a static relabel or
   untouched holdout cannot qualify;
5. planted exact replay.

Record literal re-synchronization, but do not use language score.

