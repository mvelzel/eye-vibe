# Practice cipher 3 — prefix and action-graph batch

## Outcome

Cipher 3 contains a deliberate reset-body prefix tree that had not been
recorded:

```text
A4/A5  43 equal symbols after their unequal first symbols
A0/A4   8 equal symbols after their unequal first symbols
A0/A5   8 equal symbols after their unequal first symbols
A1/A3   3 equal symbols after their unequal first symbols
```

Ten thousand independent, no-double, within-message multiset shuffles have
maximum body-prefix lengths `0..4`; none reaches 43. The corrected upper tail
is `1/10001 = .000100`. The copy is authored structure, not a frequency
accident.

It does **not** by itself solve the mechanism. A natural interpretation is
that the first symbol is a predecessor/IV and the remaining values are a path:
once two paths enter the same state, shared plaintext actions make them
coincide. The complete transition graph rejects the simplest version of that
story. Its occupancy behaves as if each state had about 69 equiprobable
outgoing choices, not at most 42 plaintext-selected choices.

The frozen standard-`C83` width lane is also negative on heldout groups. A
static English homophone attack is weaker on the real corpus than on its
matched planted control and gives no text, but the control is only partially
recovered, so that family is not excluded.

The puzzle remains unsolved.

## 1. Literal prefix tree

The first symbol is different in every copied pair:

```text
A0/A4/A5 first symbols  24 / 8 / 77
A4/A5 copied body       positions 1..43 inclusive
A0 branch               after body position 7
A4/A5 branch            after body position 42
```

Two full-message one-symbol prefixes also occur: `A0/B0` begin with raw 24
and `A1/C0` begin with raw 42. There are 16 distinct first symbols among 18
messages, so those two collisions are ordinary under an 83-symbol alphabet;
the headers are not unique message identifiers.

For A4/A5, the equality pattern extends one symbol farther in each direction:
their full windows at position zero are isomorphic for 45 symbols. This is
mostly the literal 43-symbol copy: it contributes the identity part of the
partial map, plus `8->77` at the left endpoint and `73->41` at the right.
The next pair conflicts because A5's value 16 already occurred in the copied
region. No comparable nonliteral isomorph was found elsewhere; all other
cross-message candidates have only two repeated-equality constraints.

### Why the first-symbol-as-IV reading is plausible

If a plaintext action labels a transition

```text
c[i] --p[i]--> c[i+1],
```

then different predecessors can enter the same `c[1]`. From that point, equal
actions produce an equal ciphertext path. This explains exactly why the
unequal first values of A4 and A5 do not disturb their next 43 values.

It is an interpretation, not a deduction. A static cipher with a disposable
first symbol, a copied test vector, or a more complicated synchronized state
can produce the same observation.

## 2. Exact transition-graph necessities

Treat each of the 2,229 adjacent pairs as one directed edge. The corpus has:

```text
unique directed edges       1845
repeated edge events          384
maximum edge multiplicity       5
maximum distinct outdegree      32
maximum distinct indegree       33
```

If each plaintext character chooses a permutation action on the visible
83-state predecessor, edge labels form a bipartite edge colouring. By
Kőnig's line-colouring theorem, the observed support can be coloured with 33
partial permutation actions. Thus a 42-action model passes the bare degree
necessity. This is compatibility, not evidence: the colouring is extremely
non-unique and can assign singleton edges almost arbitrarily.

Occupancy is more discriminating. Conditional on the exact number of visits
to every source state, invert

```text
sum_s K * (1 - (1 - 1/K)^visits[s])
```

at the observed 1,845 distinct outgoing edges. The effective uniform choice
count is:

```text
K = 69.041053
```

For comparison, 42 uniform choices predict 1,644.81 distinct edges; natural
language's nonuniform character frequencies would predict fewer still. The
real graph is much closer to a high-entropy 82-choice walk. Therefore the
literal model “the previous ciphertext symbol is the whole state and one of
42 plaintext symbols uniquely selects the next symbol” is a poor explanation.
This does not exclude randomized/homophonic actions or a larger hidden state.

An exact extension asked whether an unknown cyclic labelling of the 83 visible
states could put every edge into at most 42 modular-difference classes. A
60-second `QF_LIA` run timed out. Spectral and swap heuristics improved
concentration but did not approach a 42-class witness. This hidden-order
extension remains undecided, not negative.

## 3. Frozen standard-`C83` lane

Five fixed standard-coordinate transforms were screened:

```text
raw
forward/backward adjacent difference
forward/backward cumulative sum
```

For every contiguous width `2..42`, both quotient and remainder streams were
scored by first-order mutual-information excess over within-message shuffles.
The model is selected on A and then read unchanged on B/C.

The strongest A result is not held out:

```text
raw, width 41 remainder       A +.265297  B +.052308  C -.011862
forward diff, width 31 rem.   A +.254819  B -.068010  C -.009808
raw, width 2 quotient         A +.244360  B +.045327  C +.027882
```

The A-only excess is explained naturally by the copied 43-symbol prefix. No
fixed transform/width gives a comparably strong B/C replication. This closes
the frozen standard-coordinate quotient/action lane; it does not close an
unknown ciphertext order.

## 4. Static homophone check

The nearly flat 83-symbol frequencies motivate a static many-to-one
substitution. A bounded model assigned all 83 raw labels to frequency-weighted
slots over `A-Z` plus space and optimized a smoothed English trigram score.
At eight deterministic 300,000-step restarts:

```text
matched planted control   best -19517.0, 24.97% event accuracy
real raw corpus           best -22483.4, uniform gibberish
control-real gap             2966.4
```

The optimizer is deliberately calibrated, and it does materially better on
the control. But 24.97% control recovery is not strong enough for a general
exclusion. The result is only negative for this fixed slot allocation,
English alphabet, score, and budget.

A key-free source fingerprint adds a precise scoped result. For the 215-symbol
C4 message, every repeat of a ciphertext token was required to align with the
same source character. Raw, first-symbol-stripped, forward-difference, and
backward-difference streams have zero matches in:

- English *Sherlock Holmes*;
- Crawford's English *Kalevala*;
- Finnish *Seven Brothers*;
- Finnish *Kalevala*.

That excludes those exact source passages under a static homophone mapping. It
does not exclude another source or a stateful cipher.

## Transfer to the Eyes

1. **Inspect prefixes after a possible IV.** A nonmatching first value can hide
   a far stronger copied body. Eye headers are already treated separately, but
   any new corpus should be checked both with and without its first record.
2. **Separate degree compatibility from action evidence.** A graph needing at
   most 42 edge colours merely says that 42 permutation actions can interpolate
   the observed edges. Occupancy and heldout prediction determine whether that
   interpolation resembles a real plaintext action stream.
3. **Use collision rate as an early model discriminator.** Cipher 3's effective
   69-choice graph rejects a tempting predecessor-only action model before a
   language optimizer can overfit it.
4. **Copied paths can be test vectors.** The A prefix tree may have been chosen
   to demonstrate synchronization or chaining rather than because a literary
   source repeats. For the Eyes, branch continuations should likewise be tested
   as conformance vectors, not assumed to be prose repetitions.
5. **Static homophone source scans are one-way.** Equal ciphertext must imply
   equal plaintext, but unequal ciphertext may still share plaintext. This is
   a cheap exact source test that does not require solving the mapping.

The direct retrospective Eye measurement is:

```text
events / distinct edges       1018 / 843
maximum out / indegree          19 / 18
effective uniform choices     33.426694
```

So the simple 42-action predecessor model is compatible with the Eyes even
though it is poor for Cipher 3. It is not selected: the already frozen
prefix-tree-preserving Eye edge-reuse test has only `.043478` upper tail.

## Reproduction

```bash
PYTHONPATH=src python3 scripts/run_practice_cipher3_second_batch.py \
  --prefix-controls 10000 --width-controls 200

PYTHONPATH=src python3 scripts/audit_sdlwdr_cipher3_homophones.py \
  --english-corpus /path/to/sherlock.txt \
  --source-corpora /path/to/sherlock.txt /path/to/kalevala-en.txt \
  /path/to/seven-brothers-fi.txt /path/to/kalevala-fi.txt

PYTHONPATH=src python3 -m unittest tests.test_practice_cipher3_wide -v
```
