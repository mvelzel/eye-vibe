# Wall-context deck matched-control results

## Outcome

The frozen Wall-context deck survivors are not exceptional under a matched
shuffle of the proposed Wall-occurrence-to-Eye-label assignment.

Across the original and crossed-index families (`480` models), the real Wall
assignment gives:

```text
all seven registered isomorphs       30 models
plus the final bridge joint          25 models
```

In `500` fixed-seed controls, every control had an all-seven model and
`499/500` had a model that also retained the bridge joint. The control means
were `24.01` all-seven and `19.79` bridge-joint models. Counts at least as
large as observed occurred:

```text
all-seven count >= 30                110/500
bridge-joint count >= 25             121/500
```

Their plus-one rates are `.22156` and `.24351`. The family-wide result is
negative.

## Matched null

Each control applies one random permutation to the 83 Wall context rows. The
same permutation is used for all ten parameter tables. This preserves:

- every table's exact multiset;
- each raw/zero-based relationship;
- all five word-length fields belonging to one occurrence;
- the frozen decks, operations, directions, Eye streams, and gates.

It changes only which Wall occurrence supplies the parameter for an Eye
label. This directly tests the proposed source interface without randomizing
the Eye evidence.

## Strongest active candidate

The most active crossed-index survivor is:

```text
previous-length/zero-based
reverse initial deck
reverse-distance-prefix
label-decode / decoded-rank update
```

It is genuinely stateful: relative to the initial reverse relabel it has `72`
departures over the corpus, eight input labels with history-dependent output,
six departures in the old final bridges, and nine in the new 30-symbol phase.
It retains all seven isomorphs and the bridge joint.

That activity does not make its source assignment exceptional. In `20,000`
additional controls of this exact fixed model:

```text
all seven                            1,922/20,000
all seven plus bridge                  702/20,000
```

The latter plus-one rate is `.035148`. Because this model was selected from
the 480-model screen, this is not promotable evidence.

The original `following-length/raw`, identity, top-swap label decoder has a
lower all-seven null rate (`271/20,000`, plus-one `.013599`) but the observed
model fails the bridge gate.

## Degeneracy audit

No observed survivor is an exact static relabel over the whole corpus, and
none preserves the corpus-wide equality partition. However:

- six of the 30 survivors are static relabels on the registered gate cells;
- every survivor makes only `4..9` of the 83 input labels
  history-dependent;
- many bridge survivors alter zero or one old-bridge positions.

This explains why the label-invariant gates are easy to preserve. The active
previous-length candidate avoids the narrow no-op diagnosis, but its matched
rate independently rejects it as exceptional.

## Conclusion

Do not promote any Wall-context parameterized-deck candidate. The complete
frozen family is a clean negative for this source interface unless a new
authored clue independently selects one exact table, deck, update, and index
semantics before Eye scoring.

## Reproduction

```text
PYTHONPATH=src .venv/bin/python scripts/audit_wall_context_deck_controls.py \
  --controls 500 --specific-controls 20000 --seed 0x83a11

PYTHONPATH=src .venv/bin/python -m unittest \
  tests.test_wall_context_deck_controls
```
