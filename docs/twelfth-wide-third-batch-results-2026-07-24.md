# Twelfth wide horizon — final batch results

## Outcome

The final batch promotes no decoder. It also repairs one scheduling omission:
the signed-projective quotient, lane G in the original sixteen-lane map, had
been deferred with its failed parent rather than executed. Its complete finite
test is included here, so every lane A–P now has a result or a documented
identifiability/selector closure.

The two new numerical mechanisms are ordinary under controls:

```text
G signed P1(F41) quotient       corrected selected tail  .109453
L transition spectral energy   degree-preserving tail    .149254
M F5 convolutional syndrome    heldout refitted tail      .457711
```

The exact-storage, conventional-mode, and executable-clue lanes fail their
predeclared gates without an arbitrary scan.

## G. Signed projective quotient

### Construction

For each global center `c` in `F83`, identify

```text
c+d  ~  c-d.
```

The center is the point at infinity. The remaining 41 signed orbits are
labelled by the discrete logarithm of `d`, modulo sign, and are the finite
points of `P1(F41)`. For each of the seven nonliteral context relations:

1. quotient every observed source/target edge;
2. deduplicate identical quotient edges but retain conflicting edges;
3. fit every nonsingular Möbius transformation through three edges;
4. record its maximum support on the complete relation.

The complete pre-existing family of 83 reflection centers is selected inside
every control. Controls independently shuffle each context's targets, exactly
as in parent lane A. The score first maximizes the number of exact contexts,
then support beyond the three fitted edges.

Changing among the 40 primitive roots of `F83*` only rescales the finite
projective coordinate. The implementation nevertheless checks all 40: they
give one and the same support vector.

### Result

```text
selected center       39
relation sizes        13,13,13,6,25,25,22
maximum supports      5,5,5,4,7,7,6
exact contexts        0 / 7
support beyond fits   18
matched controls      21 / 200 at least as strong
corrected tail        22 / 201 = .109453
primitive-root forms  1 distinct support vector
```

The quotient repairs no failed projective context and predicts no complete
withheld relation. **Decision:** close lane G.

## L. Directed-transition spectrum

The binary `83×83` adjacency matrix contains the 843 distinct body-transition
edges. Deterministic matrix-free power iteration computes

```text
sigma_1(A)^2 / ||A||_F^2 = 0.1513166097198497.
```

Each control performs 20 attempted directed edge swaps per observed edge.
Every accepted swap preserves all in-degrees, out-degrees, the simple-graph
constraint, and the no-loop constraint. With 200 controls:

```text
degree-null range   0.148206 .. 0.153653
degree-null mean    0.150496
corrected tail      30 / 201 = .149254
```

The observed concentration is normal for its degree sequence and does not
reach the `.01` screen, let alone replicate in a second panel operator.
**Decision:** close lane L.

## M. Five-ary convolutional syndrome

Scoring begins at each panel's independently fixed deepest-prefix exit.
Every normalized linear filter over `F5` with memory one through three is
enumerated:

```text
(1, a1, ..., ak),  k=1..3, oldest tap nonzero
4 + 20 + 100 = 124 filters.
```

The best zero-syndrome rate is selected on the three P-header panels. It is
then scored once on all six Q panels. Every control shuffles accepted trigrams
within the same authored row-pair and triangle parity, preserving every
visible glyph, row-pair multiset, and parity lane; the complete 124-filter
family is refitted on P.

```text
selected taps       (1,2,2,1)
P training          177 / 726 = .243801653
Q heldout           385 / 1875 = .205333333
heldout null mean   .205272
corrected tail      92 / 201 = .457711
```

The heldout rate is essentially the null mean. **Decision:** close lane M.

## N. Packed-storage bitplanes

The exact audit already supplies a stronger answer than another bit scan:

- appending renderer newline `5`, translating to base-seven digits `1..6`,
  adding the zero pad, and greedily filling unsigned 64-bit words reproduces
  all 150 engine constants;
- their verified little-endian digest is
  `5de6ccb3a045218827b7ddaad0f1493254f501b08addd1929495ce060242de94`;
- all 141 nonfinal chunks are forced to length 21 or 22 by overflow;
- reading those capacity choices under the natural reversal, inversion,
  offset, and byte-order family has corrected tail `.825817`.

No renderer instruction, asset, or game handler selects one of the 64 machine
bit positions. Scanning them now would add 64 retrospective choices to a
representation already proved to contain only the visible tape and forced
capacity boundaries. **Decision:** close lane N until an authored bit selector
exists; a future selected bitplane must still predict a heldout panel fact.

## O. Conventional-mode identifiability

Shared prefixes and later visible rejoins do not by themselves contradict a
conventional mode when every plaintext symbol/block is unknown.

For an additive stream/CTR/OFB view over any alphabetic group, choose any
keystream `K_i` and define

```text
P_i = C_i - K_i.
```

Every ciphertext corpus is therefore realizable. Ciphertext equalities simply
become equalities or known offsets among the chosen unknown plaintexts when
the same keystream positions are reused.

For CBC with any fixed invertible block permutation `E_K`, define

```text
P_i = D_K(C_i) xor C_(i-1).
```

Again, every ciphertext path is realizable for unknown plaintext. The same
argument applies to a keyed symbol permutation: choose
`P_i = pi^-1(C_i)`, which preserves the complete equality skeleton.
Unrestricted hidden sponge/CFB state is at least as underdetermined without a
known input, nonce rule, or selected primitive.

Thus naming CTR, CBC, OFB, CFB, or a sponge produces no key-free ciphertext
contradiction here. Testable conditions begin only with a known plaintext,
known nonce/IV reuse, or independently selected primitive. **Decision:** close
the ciphertext-only conventional-mode lane; do not search arbitrary keys.

## P. Executable clue interface

The selected game-side interfaces now have ground-up results:

| Candidate | Exact authored fact | Missing prediction |
|---|---|---|
| Eye renderer | nine hardcoded base-seven-packed arrays; no runtime decryptor; exact five masks plus newline | no decoder state or second channel |
| procedural wand branch | two known `Random(0,100) < 83` branches choose modifier versus draw-many actions | selected integer is not retained, walked, or used to index the 83-name table |
| `gun_names` | one 83-entry adjective list copied four times | direct readings `.157921`; practice-#5 shuffle transfer `.119940`; no consumption rule |
| Gate Guardian | paired panels, activation marks, Q-C successor edges, and later construction vocabulary are real | raw code does not execute the dossier's record machine; eight first-seen Type6 values remain ungenerated |
| current WAK arithmetic | complete selected Lua grammar finds no modulo/range 42/83/101 state walk or target-derived table flow | only the known two 83 thresholds remain |
| recent Discord deck discussion | the only independently stated in-game deck link is the shared number 83 | no selected handler, operation schedule, or heldout Eye prediction |

This does **not** reject the Gate as a possible later hint. It closes the
current proposed executable route and keeps its visual construction vocabulary
at a lower evidential tier. The number 83 is a valid clue candidate but cannot
both select an interface and count as that interface's prediction.

**Decision:** pause lane P until a named authored call path, asset operation,
or game event predicts a frozen Eye quantity beyond the cardinality used to
find it.

## Step-back result

The breadth-first exercise did its job: sixteen substantially different
objects were tested without letting any one become an unfalsifiable theory.
None earns depth. The recurring bottleneck is now sharper:

- the ciphertext equality structure is real, but arbitrary GAK/XGAK and
  conventional hidden-state machines can absorb it;
- factoradic headers are real metadata, but every bounded direct body consumer
  has failed;
- mod-101/trie, marker-BWT `!Fi`, Gate, renderer width, and 83-of-101 facts are
  retrospective structural vocabulary, not a selected decoder;
- further representation scans are unlikely to become identifiable without
  one external anchor.

The next rational depth choices are therefore method acquisition from unsolved
practice ciphers 3/4, or acquisition of an independently selected plaintext,
operation family, or in-game interface. Another unconstrained Eye-only
coordinate transform is not warranted by this horizon.

## Reproduction

```bash
PYTHONPATH=src python3 scripts/run_twelfth_third_batch.py \
  --controls 200 --seed 236851715 --workers 8
PYTHONPATH=src python3 -m unittest tests.test_twelfth_third -v
```

The default seed is the hexadecimal value `0xE1E1203`; the decimal spelling in
the first command is equivalent.
