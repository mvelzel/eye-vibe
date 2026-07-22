# Eighth wide batch — deferred structural and provenance lanes

## Scope

The first six lanes of the seventh funnel all missed their frozen promotion
line. This batch now executes the six qualitatively different lanes preserved
behind them; it does not add parameters to any failed transform.

Four lanes have exact corpus tests. Two are provenance gates: a PRNG or range
decoder is inadmissible until the game supplies the implementation or model it
would use. Failing that prerequisite is a useful bounded result, not a reason
to fit generic generators or arbitrary frequency tables.

## Frozen portfolio

| Lane | Concrete interpretation | Cheap necessity or selector gate |
|---|---|---|
| **G. Synchronizing/error codebook** | The visible 83 of 125 base-five trigrams are valid symbols; the unused 42 detect errors or token boundaries. | Compute exact minimum Hamming distance and both length-three cross-boundary splice closures. A literal correcting/comma-free code requires distance above one or near-zero valid cross-splices. |
| **H. Without-replacement packets** | Complete 26-wide authored records and the first 83-body-token deals are partial/full card packets rather than outputs with replacement. | Sum distinct labels in the 34 complete records and nine phase-zero 83-token body blocks. Require both to be at least as depleted as observed under prefix-tree-preserving positional controls. |
| **I. Reconvergence cocycle** | Repeated exact passages identify the same hidden graph states; a visible value is a mod-101 potential difference along an edge. | Identify boundary states forced by every repeated exact bigram, quotient the nine body paths, and solve `potential(v)-potential(u)=label mod 101`. One contradiction rejects the literal cocycle before fitting potentials. |
| **J. Straight-line phrase grammar** | Copied regions and reconvergences are reusable subroutines in a compact conformance program. | Run one deterministic RePair grammar independently across the nine bodies and compare net dictionary-plus-stream savings with prefix-tree-preserving positional controls. Do not choose grammar rules by language. |
| **K. Eligible Noita RNG trajectory** | A developer-generated random stream was pasted into the arrays, with headers as seeds/selectors. | Inventory eligible code for an explicit reproducible PRNG implementation. Engine calls such as `Random`, `ProceduralRandomi`, and `math.random` do not specify a trajectory. Test headers only if an implementation and output reduction are independently frozen. |
| **L. Authored range/arithmetic model** | Base-83 digits are an entropy-coded packet under a developer-authored symbol-frequency model. | Require an eligible 83-entry frequency/cumulative table or an explicit game rule generating one. The previously rejected `gun_names` strings are not frequencies. Without a model, do not optimize probability tables against the ciphertext. |

## Controls and stop rules

- G is an exact static code property and needs no Monte Carlo. A code with
  minimum distance one and abundant valid cross-splices fails this literal
  error/synchronization reading, even if some smaller subset could be chosen.
- H uses the established prefix-tree-preserving parity shuffle on body
  positions, keeps headers and record lengths fixed, and requires the joint
  event `unique26 >= observed26 AND unique83 >= observed83`. A high score in
  only one inspected packet size does not promote.
- I uses no selected substring length: repeated bigrams are the minimal exact
  path fragments, and overlapping bigrams automatically include every longer
  exact copy. Edge direction reversal negates every equation and cannot repair
  a nonzero cycle.
- J replaces the globally most frequent non-overlapping pair, with
  lexicographic tie-breaking, only while at least three replacements pay for
  the two-symbol dictionary rule. The sole score is original length minus
  final stream length minus twice the rule count. The same algorithm runs
  inside every positional control.
- K and L do not receive statistical tests unless their provenance gates pass.
  Generic LCG/xorshift families and fitted arithmetic models are expressly
  outside scope.

As before, promotion requires an exact necessity pass or a corrected matched
tail below `0.01`, plus a held-out consequence. If G–L close, the search widens
again across genuinely new formats or returns to practice-cipher calibration;
it does not recycle the closest numerical miss.

## Results

All six lanes close in their frozen forms.

| Lane | Result | Decision |
|---|---:|---|
| G. synchronizing/error codebook | minimum Hamming distance 1; 415 distance-one pairs; 9,746/13,778 valid cross-splices | exact reject |
| H. without-replacement packets | unique-count totals `750` in 34×26 and `474` in 9×83 | joint upper tail `1214/2001 = 0.606697`; stop |
| I. repeated-bigram cocycle | 729 quotient nodes, 786 constraints, one component, 57 contradictions | exact reject |
| J. deterministic RePair | 46 rules, stream 1,027→867, dictionary-adjusted savings 68 | upper tail `657/2001 = 0.328336`; stop |
| K. eligible Noita RNG | early/current Lua: 337/975 engine calls, zero engine-generator definitions | provenance gate fails |
| L. authored range model | no 42/101 table; four 83-entry tables are duplicate `gun_names` strings | provenance gate fails |

### G: the visible interval is not a literal synchronizing code

Among values `0..82`, 415 unordered pairs differ in exactly one of the three
base-five eyes. Across every ordered pair of codewords, the two length-three
windows that straddle their concatenation boundary give 13,778 splices;
9,746, or 70.74%, are themselves visible values. The splices reach 115 of all
125 possible words. This codebook neither corrects one-coordinate errors nor
marks concatenation boundaries in the literal comma-free sense.

This is a rejection of the complete visible set as the code. Choosing a
smaller optimized subset after seeing the result would abandon the exact
83-symbol premise and is not permitted.

### H: the authored packet sizes behave like replacement streams

The 34 complete accepted-order records contain 750 distinct-label slots in
total; the first 83 body values of each panel contain 474. A joint control must
meet or exceed both. It does so in 1,213 of 2,000 prefix-tree- and
parity-preserving shuffles. Control ranges are `738..791` and `454..493`.
There is no without-replacement depletion at either frozen size.

### I: almost every quotient cycle contradicts a potential

There are 104 repeated bigram types with 279 occurrences. Identifying the
three boundary states of every repeated occurrence reduces the nine paths to
729 nodes and 786 unique equations

```text
potential(v) - potential(u) = visible_label  (mod 101).
```

The quotient is connected, so it has 58 independent surplus constraints.
Fifty-seven equations contradict the potential assigned along a spanning
tree. Reversing every edge merely negates every equation and cannot repair a
nonzero cycle. The literal reconvergence cocycle is therefore decisively
false; no fitted potentials were needed.

### J: phrase reuse is explained by the preserved prefix structure

Deterministic RePair introduces 46 rules and shortens the live streams from
1,027 to 867 symbols. Charging two symbols for every rule leaves encoded size
959 and savings 68. Prefix-tree-preserving positional controls have savings
range `60..77`; 656 of 2,000 do at least as well. The bodies do not have an
exceptionally compact straight-line phrase grammar beyond the copied-prefix
architecture already in the null.

### K–L: the selectors are absent

The archived early loose tree contains 358 Lua files and 337 calls to
`math.random`, `Random`, or `ProceduralRandom*`; the current extracted tree has
1,016 files and 975 calls. Neither contains a definition of those engine
generators. Wrappers such as `random_next` only advance coordinates passed to
`ProceduralRandomf`; they do not specify its implementation. The native Eye
placement RNG is known to exist, but no independently authored rule says to
seed it with header ranks and reduce its outputs to body labels. That missing
consumer is precisely the selector gate, so generic PRNG fitting remains
disallowed.

The earlier exhaustive game-table audit found no 42- or 101-entry Lua table
and only four identical copies of the 83 adjective strings called
`gun_names`. Those strings have already failed direct lookup and dynamic-deck
tests and are not a probability model. With no authored cumulative/frequency
table or rule generating one, range coding has no finite decoder to test.

## Outcome

The two-stage wide funnel has now tested twelve additional mechanism families
without promoting one. That is useful compression of the search space: the
body does not currently expose a direct factoradic consumer, a low-capacity
derivative channel, a structural packet/code/grammar, or an authored random or
range model.

The next synthesis should start wide again, but it should change *question*
rather than representation. High-value directions are method calibration on
the unresolved practice ciphers, read-only acquisition of a concrete external
selector from recent discussion, and a fresh causal analysis of what equality
and prefix features an unknown state machine would have to generate. A new
numeric transform without an independent selector is now low value.

Reproduction:

```bash
PYTHONPATH=src python3 scripts/run_eighth_wide_batch.py \
  --controls 2000 --seed 20260722 \
  --data-root /path/to/current/data \
  --early-data-root /path/to/early-access/data
```
