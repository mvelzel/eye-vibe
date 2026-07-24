# Practice cipher 3 — third wide mechanism horizon

## Why widen again

Cipher 3 is not solved. The established results exclude a single hidden
`C83` position progression, several concrete deck-update families, the
recovered ciphers-1/2 wheel, a direct reuse of cipher 5's recursion, the
standard numeric `C83` quotient family, and two finite reflection-wheel
coordinate families. They do not identify what the author intended.

The strongest positive observation is the reset-body prefix tree:

```text
A4/A5  43 identical body symbols after unequal first symbols
A0      8 symbols on the same body branch
A1/A3   3 symbols on another branch
```

The three named groups contain six streams each, with distinct length bands:

```text
A  57..67
B  111..126
C  185..215
```

This looks at least as much like a collection of deliberately selected
conformance vectors as eighteen arbitrary prose excerpts. The next pass starts
from that architecture. It does not assume that the first symbol is an IV,
that the bodies are language, or that the displayed `0..82` labels are
arbitrary.

## Wide horizon

| Lane | Mechanism class | First falsifiable screen | Promotion gate |
|---|---|---|---|
| **A. Master-stream excerpts** | Streams are cuts, continuations, or edited versions of one longer generated tape. | Find maximal exact, reversed, and cyclic-label-shifted substrings at all offsets; compare their incidence graph with length/frequency-preserving controls. | A match outside the known A prefix must predict an unused continuation or stream boundary. |
| **B. Per-message affine keys over `F83`** | A common underlying tape is masked by `a*x+b`, possibly with linear counter drift. | Exhaust all `a != 0`, `b`, directions, and bounded position drifts between every stream pair; score held-out run extension rather than fit length alone. | One relation must extend past the construction window and recur in another independent pair. |
| **C. Low-order field generator** | Bodies are affine/LFSR-like output, or plaintext is added to such a generator. | Measure every order-1/2 affine recurrence over `F83`, Berlekamp–Massey complexity, and residual support under reset/body conventions. | A globally shared recurrence must reduce held-out residuals to at most the known 42-symbol plaintext alphabet and pass a planted control. |
| **D. Counter/PRNG masking** | The first symbol selects a seed while a deterministic keystream masks plaintext. | Test named small generators and counter modes only where equal/copy windows make seed or keystream relations observable without guessing words. | A seed law selected on A must predict B/C relations and replay all bodies; an in-sample language score is insufficient. |
| **E. Two-sheet homophony (`83 = 2*42-1`)** | Plaintext symbols have two ciphertext representatives, with one exceptional shared state and a deterministic sheet schedule. | Separate the unknown pairing problem from the schedule: screen numeric antipodes, affine involutions, parity/toggle schedules, and equality constraints from copied bodies. | Recover one pairing and schedule on A that maps B/C into at most 42 values and yields stable language or source compatibility. |
| **F. Higher-order visible state** | A ciphertext symbol represents a plaintext bigram, transition, or `(plain, hidden-bit)` state rather than an action from the preceding ciphertext. | Test de Bruijn/line-graph necessities, deterministic overlap constraints, and bounded 42-state colourings on ordered ciphertext pairs/triples. | The inferred state map must predict withheld transitions; merely colouring the observed graph fails. |
| **G. Output-rank deck families** | The visible value is a card/rank output from a state update not covered by the seven named updates or cipher-5 recursion. | Enumerate small algebraic deck actions: powers/cuts determined by current rank, perfect faros, packet reversals, Josephus steps, and emit/update timing. | A family must be planted-recoverable and keep every held-out decoded rank in `0..41` under one global convention. |
| **H. Compression and recoding** | Bodies are BWT/MTF, LZW-like, arithmetic/range-coded, or base-83-packed data rather than direct ciphertext characters. | Test signature-level invariants first: MTF low-rank skew, BWT run structure, dictionary-code growth, byte/base packing lengths, and reset headers. | Only a codec with the expected signature is decoded; promotion requires a valid complete stream and readable or independently recognizable output. |
| **I. Polygraphic/fractionated symbols** | One or more ciphertext values jointly encode a smaller alphabet. | Exhaust pair/triple arithmetic projections over `F83`, quotient/remainder widths, alternating coordinates, and phase choices with A selection/B-C holdout. | The same phase/map must reduce all groups and strengthen copied/equality structure, not only frequency score. |
| **J. Route/transposition layer** | The six streams per group are rows/columns or ragged blocks of one group object. | Test all six permutations, column reads, snakes, reversals, and bounded rectangles using equality-pattern and transition statistics. | A route must be uniquely recovered on a planted fixture and improve both B and C without route refitting. |
| **K. Variable-length token code** | Each visible symbol names a word, digram, source position, or dictionary event; ciphertext length need not equal plaintext length. | Check whether lengths, first symbols, and repeated windows fit prefix-code, phrase-table, or source-index constraints; do not force character-frequency English. | A finite dictionary must decode multiple streams consistently and explain all boundaries. |
| **L. Self-synchronizing/error-correcting code** | The long A4/A5 copy demonstrates resynchronization after a one-symbol disturbance. | Measure edit propagation under candidate convolutional, differential, and finite-state synchronizing codes; locate reset words and synchronizing lengths. | The model must predict another convergence/divergence event not used to select it. |
| **M. Equality-only/relabelled object** | Numeric symbols are deliberately random labels and only partitions/repetition patterns carry meaning. | Canonicalize restricted-growth strings, compare repeated factors, grammar compressibility, and cross-stream edit scripts under label renaming. | A grammar or map must generate held-out equality events with fewer degrees of freedom than the events predicted. |
| **N. Authored numeric order** | Original printable-character order or raw `0..82` arithmetic carries the key. | Audit differences, sums, products, inverses, Legendre classes, small intervals, ASCII classes, and `F83` projective maps under a complete-family correction. | A numeric projection must replicate across A/B/C and survive global-label controls. |
| **O. Source-conformance set** | The plaintexts are selected test sentences, lists, or templated passages rather than unrelated prose. | Search public-source equality fingerprints and length/equality trees after a mechanism supplies the correct equality implication. | Source identity must predict unseen text and be compatible with exact re-encryption; length coincidence alone fails. |
| **P. Cross-puzzle construction genealogy** | Ciphers 1–4 share implementation primitives even when their keys differ. | Compare reset conventions, standard printable order, exceptional-symbol treatment, cycle/rank arithmetic, and output/update timing—not recovered plaintext. | A reused primitive must expose a new invariant in Cipher 3 and pass a held-out test; authorship or theme alone fails. |

## First cheap batch

The first batch is A, B, C, H, and M.

These lanes ask whether the corpus is generated tape, simple field masking,
low-complexity recurrence, compressed/recoded data, or an equality-only
grammar. They need no language optimizer and no arbitrary hidden permutation.
They also directly test the conformance-vector interpretation of the 43-symbol
copy.

The batch will report:

1. all cross-stream maximal exact and affine-related factors, with the known
   A tree separated from newly discovered structure;
2. best order-1/2 `F83` recurrence residual supports and linear complexities;
3. MTF/BWT/dictionary-code signature statistics against matched controls;
4. restricted-growth-string factor and grammar measurements;
5. planted recovery for every statistic used to reject or promote a family.

## Controls and stop rules

- A is selection, B is validation, and C is final heldout whenever a parameter
  is learned. A pairwise discovery involving B or C must predict unused
  positions in the same pair or an independent pair.
- Controls preserve all eighteen lengths, each stream's symbol multiset, the
  no-adjacent-double constraint, and the known first-symbol/body split.
- The literal A4/A5 copy is treated as disclosed training structure. A model
  receives no credit for rediscovering only those 43 symbols.
- `UNSAT`, exhausted finite failure, failed planted recovery, and bounded
  heuristic failure remain separate outcomes.
- Language scoring may rank a finite structural survivor; it may not select an
  unrestricted geometry, transducer, or dictionary.

## Discord evidence boundary

The authorized browser profile currently opens Discord at a fresh login
screen. No new author hint was available for this freeze. The locally
preserved evidence remains the ciphertext attachment, the A0 correction, and
the absence of a recorded mechanism hint in the original thread. When the
session is available again, the author history should be audited for wording
about the A/B/C grouping, intended plaintext type, alphabet order, resets, and
whether the first symbol is data or setup. Those facts may reprioritize this
horizon but will not be silently read into it.
