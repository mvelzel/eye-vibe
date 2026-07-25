# Thirty-ninth pass — Veska state-selector freeze

## Question

Does Veska's objective `1,5,3` upper tape identify the terminal Eye state as
class 15 with loop-panel suffix width 3, while its lower `+3` executes the
cycle restart?

The independently derived Eye machine now has:

```text
terminal late equality class   15
E4 loop bridge suffix           3
terminal source subtraction    -> header27
next operation                 27+3 -> phase30
```

Veska's authored components are:

```text
upper  1,5,3
lower  +3
```

The inspected parsing is:

```text
upper  15 | 3 = terminal class | loop suffix
lower  +3     = returned-header restart operator
```

This was noticed after the Eye cycle and Gate measurements were known. Treat
it as retrospective later-clue corroboration, not a discovery p-value.

## Fixed inputs

Freeze:

- connected-component lengths `1,5,3` in natural left-to-right Veska order;
- the independently measured lower plus followed by three singleton marks;
- canonical late equality classes by first occurrence;
- repeat events in the promoted common 30-symbol phase;
- typed bridge suffixes `(3,4,3)`;
- E4 as the control-edge loop;
- the closed terminal return `27`;
- ordinary decimal concatenation, with no base conversion or padding.

Do not reorder sprite components, move the phase boundary, relabel equality
classes, or choose another arithmetic operation in the primary parse.

## Primary inventory

Split the fixed upper string `153` after its second digit:

```text
class = 15
width = 3
```

Report whether:

1. class 15 is a repeated late class;
2. it is the terminal repeat selected by row 2;
3. width 3 is the typed E4 loop suffix;
4. the lower `+3` maps the returned header 27 to late phase length 30.

## Broad parsing controls

Report every valid parse under:

1. all repeated late classes crossed with distinct suffix widths `{3,4}`;
2. all late classes `0..24` crossed with `{3,4}`;
3. both possible nonempty splits of the fixed string `153`;
4. every permutation of component lengths `1,5,3` and every split.

A valid split requires its left integer to be an observed class ID and its
right integer to be a typed suffix width. Preserve leading digits literally;
do not invent separators or multi-field arithmetic.

Also report panel-specific matches against suffixes `(3,4,3)`, distinguishing
the independently selected E4 loop from the second width-3 panel.

## Locale double reading

Retain the already reproduced locale interpretation:

```text
153 mod83 + ASCII32       = f
(153+3) mod83 + ASCII32   = i
```

Do not count the locale and state-selector readings as independent
probabilities. They reuse the same authored `153,+3` marks.

## Calibration and promotion gate

Tests must recover:

- the exact component order and value 153;
- primary parse `(15,3)`;
- all valid broad parses;
- terminal class and E4 suffix membership;
- restart `27+3=30`;
- failure after changing the class or suffix.

Promote Veska as a later state-selector diagram only if:

- `(15,3)` is the unique fixed-string domain-valid split;
- no component permutation supplies an equally valid alternative;
- the lower `+3` executes the already closed cycle without a new convention.

This cannot establish that the Gate existed when the Eyes were constructed.
It is eligible as a later decoding hint and remains separate from the
unreproduced Type4/Type6 claims.
