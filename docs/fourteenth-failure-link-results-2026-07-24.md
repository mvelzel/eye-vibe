# Fourteenth horizon: failure-link sieve result

## Outcome

The canonical Aho–Corasick failure-link lane is exactly negative.

Only twelve body-trie nodes have a non-root failure target. Every target is a
depth-one prefix. Their incoming labels sum to `792`, residue `85 mod 101`,
and their frozen numeric-BFS depth-drop tape does not contain the independently
fixed `BEXIT=(2,5,24,9,20)` word.

Both required conditions fail. No cache/failure decoder is promoted.

## Frozen construction

The exact serializer was committed before calculation in
[`fourteenth-failure-link-freeze-2026-07-24.md`](fourteenth-failure-link-freeze-2026-07-24.md):

1. build the prefix trie of the nine marker-stripped bodies;
2. construct standard Aho–Corasick links in numeric-label breadth-first order;
3. retain nodes whose longest proper suffix that is a trie prefix has positive
   length;
4. sum each retained node's incoming label once modulo 101;
5. write `node depth - failure-target depth` in the same BFS order;
6. require both checksum zero and one exact contiguous
   `(2,5,24,9,20)` occurrence.

No alternate traversal, failure-chain expansion, reverse word, or substring
was inspected.

## Eye result

```text
trie nodes:              919
retained failure nodes:   12
incoming-label total:    792
residue modulo 101:       85
failure-target depths:    twelve at depth 1
```

The complete depth-drop word is:

```text
11,29,32,46,64,71,75,78,79,104,109,112
```

It has no `BEXIT` occurrence.

The retained incoming-label multiplicities were also passed to the exact
subgroup control that preserves all three diagonal message sums and fixes all
nine markers:

```text
zero assignments:                 0
all subgroup assignments: 825,564,856,320
```

Thus this fixed 12-record checksum cannot close anywhere in that entire
matched subgroup. A joint Monte Carlo word/check control is unnecessary
because neither observed requirement passes.

## Interpretation

The bodies do contain twelve nontrivial suffix-to-prefix relations, but only
to one-symbol prefixes. They do not form the predeclared mod-101 failure-link
sieve or reproduce the independent branch/exit depth word.

This is a useful distinction from the minimal dictionary automaton:

- dictionary minimization found no internal equal continuation languages;
- failure links find twelve proper suffix-prefix matches;
- those links nevertheless fail both the numeric and structural consumer.

The result also sharpens the Gate boundary. “Cache,” “repeat,” or “failure”
vocabulary can inspire a canonical automaton, but the Eye corpus does not
execute this one. A different cache machine now needs an independently
authored interface; freely choosing failure-chain levels or record fields
would abandon the frozen test.

## Reproduction

```bash
PYTHONPATH=src python scripts/run_fourteenth_automata.py
PYTHONPATH=src python -m unittest tests.test_fourteenth_automata -v
```

Definitions are in
[`fourteenth_automata.py`](../src/eye_mystery/fourteenth_automata.py).
