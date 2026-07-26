# Sixty-sixth pass: theory-isolated wide horizon and visible actions

**Date:** 26 July 2026  
**Status:** one cheap screen executed; no plaintext or decoder recovered

## Purpose

This pass steps away from the accumulated construction theories and starts
wide from the Eye corpus itself. Each lane below is a standalone hypothesis.
A partial fit in one lane cannot corroborate another. A useful operation or
negative result may transfer, but evidential weight does not.

The first executed lane transfers a technique learned from sdlwdr practice
cipher #3. That transfer is not claimed as a new cryptographic invention.
The parameterized-matching lanes appear new within this repository, but no
claim is made that the wider Noita community has never considered them.

## Wide horizon

| Lane | Independent hypothesis | Cheap necessity test | Capacity rule |
|---|---|---|---|
| A. Direct visible permutation actions | The visible rank is the complete state and each plaintext/action symbol selects one global permutation of the 83 ranks. | Find the exact minimum action cover while enforcing aligned actions in the registered isomorphic passages. | A cover is compatibility only. Require a forced action backbone or an independently selected permutation family before language scoring. |
| B. Parameterized-match closure | Repeated plaintext appears as factors equal up to a consistent renaming of state labels, rather than literal ciphertext equality. | Freeze a set of parameterized factors, close their overlaps as word equations, and ask whether they predict another occurrence or forced extension. | Charge every freely chosen factor, alignment, reversal, and renaming. A retrospective split is validation, not prospective evidence. |
| C. Parameterized source fingerprint | The plaintext or source has distinctive repetition geometry recoverable before symbol identities. | Compare equality-pattern factors and overlap graphs against fixed, chronologically eligible sources. | Select the source and normalization without reading candidate matches; require an unseen extension. |
| D. Minimum hidden-state lift | A small action alphabet exists, but one visible rank aliases multiple hidden states. | For fixed action counts such as 26 or 42, compute the minimum hidden multiplicity needed to remove transition conflicts. | Do not invent state splits after inspecting words. A useful bound must be followed by an authored rule that names the splits. |
| E. Prime-degree group fork | The 83 visible states are an orbit of a deliberately structured permutation group. | Use the degree-83 group classification to separate small affine candidates from high-capacity transitive groups, then test only fully specified small families. | `A83`, `S83`, or unrestricted generators explain almost anything and are rejected without an external selector. |
| F. Binary interface archaeology | The renderer's caller or a release delta supplies an input, ordering, or companion object not visible in the packed arrays. | Trace callers and arguments around the verified initializer; compare a pre-Eye or 2020 executable if acquired. | A later asset is a clue only if it independently specifies a complete Eye operation and predicts an uninspected consequence. |
| G. Non-prose protocol stream | The actions describe a program, construction trace, route, music, or other protocol rather than natural-language prose. | Test grammar only after actions have been selected independently of the desired output. | Never interpret an arbitrary graph coloring as opcodes or words. |
| H. Constraint-authored object | The arrays were generated to satisfy visible combinatorial constraints and may have no conventional plaintext. | Define a low-parameter generator from promoted facts and compare frozen unseen statistics. | Maximum-entropy or arbitrary constraint completion is not a solution; require a compact authored generator or payload. |

Lane A was the cheapest exact screen. Its outcome is below. The next
potentially informative pure-cryptographic lane is B, because it uses the
corpus's strongest invariant—equality and reconvergence—without assigning
meanings to the 83 labels.

## Frozen Lane-A model

Remove the nine structured first-trigram markers. For every remaining
adjacent pair, assume

```text
c[i+1] = P[action[i]](c[i]),
```

where each `P[a]` is one permutation of all 83 visible ranks.

Two observed transition events may share an action exactly when their directed
edges can coexist in one partial permutation:

- one source cannot map to two different targets;
- two different sources cannot map to one target.

Every compatible partial bijection can be completed to a full permutation by
bijecting the unused sources and targets. The resulting conflict graph
therefore gives an exact support-level test, not an approximation.

The seven registered nonliteral equality-isomorphic contexts add a conditional
constraint: if those passages represent repeated plaintext/action strings,
their aligned internal transitions must have the same action. The aligned
event variables are unioned before coloring. These passage interpretations
are not assumed proven; adding them makes the compatibility screen stricter.

## Exact result

The body corpus contains:

```text
transition events                       1018
unique directed edges                    843
repeated edge events                      175
maximum edge multiplicity                   9
maximum distinct outdegree                 19
maximum distinct indegree                  18
event classes after alignment unions      877
aligned classes                            54
internally conflicting aligned classes      0
conflict pairs                          12561
```

The maximum in/out degree is a lower bound of 19 actions. Deterministic DSATUR
constructs a valid 19-coloring, so the exact minimum is 19.

For comparison, inverting

```text
sum_s K * (1 - (1 - 1/K)^visits[s])
```

at 843 unique edges gives an effective uniform choice count of
`33.426694445`. Fixed uniform models predict:

```text
K=26    801.089446 unique edges
K=42    874.959727 unique edges
```

This occupancy calculation is descriptive only. The coloring was optimized
after seeing every transition and need not have uniform action frequencies.

Keeping the nine marker-to-body transitions does not create the result:
the marker-inclusive corpus has 1,027 events, 850 unique edges, 886 aligned
classes, and again an exact 19-action cover.

## Exact identifiability audit

Visible source rank 26 is unique: it is visited exactly 19 times and reaches
19 different targets:

```text
8,13,14,19,23,28,30,45,48,54,57,59,62,63,68,76,77,78,79
```

Those outgoing classes form a 19-clique. Naming their sorted targets as
actions 0 through 18 removes the global `19!` action-label symmetry.

The decisive follow-up does not require an expensive all-solutions search.
Start with the valid 19-color construction. For each of the other 858 event
classes, hold every other class fixed and ask whether one unused neighboring
color is available. Changing only that class then explicitly constructs a
second valid coloring.

Result:

```text
anchored pivot classes                    19
nonanchor classes                        858
one-step mutable nonanchors              858
forced nonanchors                          0
available colors per nonanchor          2..14
```

Available-color histogram:

```text
2:49, 3:114, 4:92, 5:83, 6:149, 7:101, 8:133,
9:95, 10:31, 11:6, 12:2, 13:2, 14:1
```

Thus every non-pivot class has at least two witnessed action assignments even
after action names are fixed. This proves that the construction has no
nontrivial unary coloring backbone. It does not rule out higher-order
relations shared by all colorings, but it prevents the graph coloring itself
from assigning a single plaintext/action symbol anywhere outside the naming
pivot.

The marker-inclusive robustness model has the same conclusion:
all 867 nonanchor classes are one-step mutable.

## Interpretation and decision

Lane A survives only as a support-capacity result:

- arbitrary global permutations can replay every observed one-step body
  transition without hidden state;
- the repeated-passage action constraints introduce no contradiction;
- exactly 19 arbitrary actions suffice.

It is not positive evidence for a 19-symbol plaintext alphabet or for this
being the authored machine. The entire coloring is fitted to the ciphertext,
and every nontrivial class can change action independently in a witnessed
valid completion. Generated color strings would therefore be manufactured
output, not decryption.

Stop this lane unless an independent in-game, binary, header, or source
interface selects a restricted family of permutations. Do not run word
optimization over the arbitrary colors.

## Reproduction

```text
PYTHONPATH=src python3 scripts/analyze_visible_action_coloring.py
PYTHONPATH=src python3 -m unittest tests.test_visible_action_coloring
```

Implementation:

- `src/eye_mystery/visible_action_coloring.py`
- `scripts/analyze_visible_action_coloring.py`
- `tests/test_visible_action_coloring.py`
