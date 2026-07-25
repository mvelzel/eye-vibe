# Thirty-eighth pass — terminal source-state return results

## Outcome

Promote a cyclic source-state return:

```text
row 2 selects late class 15 at positions 16 and 29

class 15 labels:
E4 loop         40
W4 source mate  67
E5 target mate  21

W4-E4 = 67-40 = 27 mod83 = E4 loop header
```

The header/phase machine now closes rather than terminating at an unexplained
body value.

## Fixed direction

The E4/W4 scope and subtraction direction were not selected from these
labels. The established control edges are:

```text
E4 0->0  loop
W4 0->2  source mate
```

The prior header-level source delta already used mate minus loop:

```text
77-27 = 50
```

Applying that same directed operation to the row-2-selected terminal state
gives `67-40=27`.

## Exact matched relabeling audit

The matched null preserves each panel's:

- complete late equality signature;
- class multiplicities;
- visible-label multiset;
- old/new label-reuse status.

Class 15 is fresh relative to the old phase and occurs twice. Compatible
classes are:

```text
E4: class 1,5,15
W4: class 0,1,5,15
```

The 12 compatible label pairs are:

```text
E4 labels 57,60,40
W4 labels 63,5,66,67
```

Exactly one pair has directed difference 27:

```text
E4 class15 label40
W4 class15 label67
```

Therefore:

```text
exact matched probability = 1/12 = .083333333
```

This is conditional specificity after inspection, not a prospective p-value.

## Broad repeat and marker inventory

With the fixed E4→W4 direction and target 27, the terminal class is the only
hit among all five repeated late classes.

Allowing both source-pair directions and any marker gives two hits:

```text
class 5   W4 66 -> E4 60   difference77  West4 marker
class15   E4 40 -> W4 67   difference27  East4 marker
```

Allowing every ordered panel pair, every repeated class, and any of the nine
markers gives only one additional hit:

```text
class20   E5 73 -> E4 26   difference36  East2 marker
```

Thus the complete broad inventory is three hits among 30 ordered
pair/repeated-class combinations. The primary terminal return is the only hit
with its independently selected class, pair, direction, and target.

Among all aligned fresh multiplicity-two classes in the fixed source pair,
the only marker differences are the class-5 reverse hit and class-15 primary
hit. This discloses the nearby alternative rather than hiding it.

## Conditional header cross

The body return value is fixed at 27. Across 12,096 conditional scalar
assignments:

```text
E4 marker equals returned27             2532
+ full phase/source-boundary topology      2
+ terminal row-2 pointer record            1
```

The unique joint survivor is the observed marker assignment. These are nested
conditions and are not multiplied with the `1/12` relabeling count.

## Executable cyclic sieve

The promoted control cycle is now:

```text
E4 loop header 27
      |
      | Gate +3
      v
late common phase length 30
      |
      | source-mate suffix +4
      v
E4/W4 source boundary 34
      |
      | row 2: +29, then +13
      v
terminal class15 at positions16,29
      |
      | W4_label - E4_label
      v
E4 loop header 27
```

The side path `old target boundary20 + late phase30 = row-1 self50`
simultaneously repairs the remaining first-row field. This is an executable
Eye-derived cyclical sieve using:

- typed header edges;
- equality-state boundaries;
- row-2 repeat pointers;
- directed body-label subtraction;
- the later Gate `+3` operator.

This does not validate the dossier's unreproduced Seula mask, eight-cache
allocator, or Type4 bit selection. It does show that “cyclical sieve” is a
productive description of the actual Eye control machine, not merely a visual
analogy.

## Interpretation boundary

The cycle explains how one selected body state feeds the control header. It
does not yet explain:

- why the visible class-15 labels are `40,67,21`;
- how fresh labels are allocated;
- the roles of the two other broad marker-return hits;
- whether the bodies encode natural-language plaintext.

## Next falsification target

The other two marker-return events are now a sharply bounded lead:

```text
position9  class5   distance4   -> West4 marker77
position26 class20  distance4   -> East2 marker36
```

Test whether header scopes and repeat direction predict those operations
without choosing among pairings after seeing their numeric differences. If
they form a scheduled cache/control sequence, it should predict a fourth
state or explain why the repeats at positions 18 and 27 are data-only.

## Reproduction

```bash
PYTHONPATH=src python scripts/audit_terminal_source_return.py
PYTHONPATH=src python -m unittest tests.test_terminal_source_return
```

Implementation:

- `src/eye_mystery/terminal_source_return.py`
- `tests/test_terminal_source_return.py`
- frozen protocol:
  `docs/thirty-eighth-terminal-source-return-freeze-2026-07-26.md`
