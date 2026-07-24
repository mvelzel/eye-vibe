# Fourteenth horizon: minimal dictionary automaton result

## Outcome

The canonical minimal dictionary automaton adds no structure beyond the
existing prefix trie.

Minimizing the nine marker-stripped bodies removes exactly eight states: the
nine terminal trie leaves become one accepting state. No internal states have
identical right languages, so no suffix continuation is shared and no
transition is removed. Consequently the automaton's transition-label sum is
literally the existing prefix-trie sum, not a second checksum:

```text
37,774 = 374 * 101
```

Lane D is closed as an independent corroboration.

## Construction

Start with the canonical trie of the nine complete bodies. Two trie states are
equivalent exactly when:

1. both are accepting or both are nonaccepting; and
2. their complete maps from outgoing label to child equivalence class are
   identical.

Interning these signatures bottom-up yields the unique minimal acyclic
deterministic automaton for the finite nine-word dictionary. There is no
traversal order, key, language score, or fitted state count.

Toy tests distinguish:

- the unavoidable merge of accepting terminal states;
- a genuine internal merge when two words share an identical suffix
  continuation;
- duplicate words, which already share one trie path.

## Eye result

```text
prefix-trie nodes:          919
prefix-trie transitions:    918
minimal states:             911
minimal transitions:        918
accepting classes:            1
internal merged nodes:        0
largest class sizes:          9, then 910 singletons
transition-label total:  37,774
residue modulo 101:           0
```

The sole non-singleton class contains the nine accepting leaves. Because their
incoming transitions originate at nine different predecessor states, merging
the leaves does not merge any transition.

The transition-label multiplicity vector is therefore identical to the
ordinary body prefix trie's vector. Under the exact subgroup that preserves
all three diagonal message sums and fixes all nine markers:

```text
zero assignments: 8,174,134,656
all assignments:  825,564,856,320
fraction:         0.009901263
```

That is the already reported prefix-trie calibration. It cannot be multiplied
with or counted as confirmation of itself.

## Interpretation

The bodies do not share complete suffix continuations beyond their common
empty continuation. Therefore minimizing the finite dictionary does not
expose a hidden suffix cache, smaller conformance automaton, new state count,
or independent mod-101 closure.

This does not close lane E's Aho–Corasick failure links. Failure links merge
the *longest proper suffix that is also any trie prefix* and can capture
internal repeated phrases even when complete remaining suffixes differ. That
is a different canonical automaton and remains the next lateral test.

## Reproduction

```bash
PYTHONPATH=src python scripts/run_fourteenth_automata.py
PYTHONPATH=src python -m unittest tests.test_fourteenth_automata -v
```

Definitions are in
[`fourteenth_automata.py`](../src/eye_mystery/fourteenth_automata.py).
