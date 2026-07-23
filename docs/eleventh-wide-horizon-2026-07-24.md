# Eleventh wide horizon — frozen 24 July 2026

## Purpose

This horizon starts wide before it goes deep.  It does not promote the newest
Discord idea, the Gate construction vocabulary, GAK, Finnish source matching,
or any earlier residue merely because it is vivid.  It places independently
falsifiable questions from six different domains beside one another:

1. direct numerical claims;
2. unknown-plaintext model feasibility;
3. deck-action constraints;
4. source-language structure;
5. evidence attribution;
6. renderer and in-game construction clues.

Global novelty cannot be proved.  “Project-original” below means only that the
exact discriminator was not found in this repository or in the broad read-only
searches of the accessible `silmä-cryptography`, `silmä-novel`, and related
Discord history.  Community ingredients and messages are credited even when
the bounded test is new.

## New evidence entering this horizon

- Henry supplied a small ordinary-GAK example in which `BCBDBCDA` has a
  two-operation, four-card parent but `BCBDBCDAC` does not.  This proves an
  important point of principle: an arbitrary-looking ciphertext need not have
  any parent for fixed plaintext and ciphertext alphabet sizes.  Existing
  project SAT work assumes known plaintext; it does not implement this
  ciphertext-only question.
- Cararasu reported a Finnish verse whose first syllable-token equality pattern
  tracks the proposed first-family pattern for several runs.  Literal
  ciphertext equality is not generally plaintext equality under GAK, so this
  is a source-fingerprint lead rather than a decryption.
- A recent PDF claims a universal entropy/variance pivot at glyph index 25 and
  a perfect lag-five payload related to a five-note Kantele motif.  Direct
  inspection already contradicts the exact claim: the real post-25 residue
  blocks are neither five-periodic nor uniformly distributed.  The broader
  change-point family still deserves one reproducible, selection-aware audit.
- A recent summary restates the already recorded fact that complete glyph sums
  for East 1, East 3, and East 5 are respectively `4040`, `5656`, and `4545`,
  all multiples of 101.  The other six messages are not multiples of 101, so
  any stronger checksum interpretation must predict its scope rather than
  select those three after seeing the sums.
- The cipher-4 selector experiment supplied a transferable warning: extremely
  significant held-out prediction can be carried entirely by repeated full
  plaintext transitions.  Exact carrier attribution turned the apparent
  mechanism into `0/23` and `0/42` success on new contexts.

## Frozen wide portfolio

| Lane | Hypothesis or question | First bounded discriminator | Provenance / boundary |
|---|---|---|---|
| **A. Universal change point** | The streams divide into a 25-glyph header and a five-periodic or distributionally distinct payload. | Test the exact index-25 assertions on every natural five-valued projection, then scan all eligible cuts, lags, and component orders with the whole family reselected in each control. | Prompted by the recent entropy/music PDF. Exact claims can be rejected without a null; a weaker phase-change claim cannot. |
| **B. First-glyph checksum field** | The first glyph is an ordering/check byte that makes a body statistic vanish modulo 83, 101, or another authored modulus. | Remove each first glyph and ask whether one fixed formula predicts all nine held-out first glyphs. Formula, modulus, family grouping, and sign are selected inside controls. | The three East odd-index multiples of 101 are community-observed; choosing only those three after inspection is not a prediction. |
| **C. Ciphertext-only GAK orphans** | The Eye equality sequence has no parent under an ordinary GAK with a bounded plaintext alphabet. | Reproduce the reported four-card SAT/UNSAT pair, calibrate on planted and random tiny cases, and only then measure the longest Eye prefix the exact solver can decide. | Henry's community result; distinct from the repository's known-plaintext SAT solver. SAT is feasibility, not a recovered plaintext. |
| **D. Minimum GAK operation curve** | Even where a parent exists, the smallest number of plaintext-selected operations grows too quickly or has message-family discontinuities. | For each decidable prefix length compute the minimum operation-alphabet size and compare it with planted GAK and equality/no-double-matched controls. | Project extension of lane C. No extrapolation from tiny prefixes without a calibrated scaling law. |
| **E. Reconvergence action collisions** | Divergent plaintext symbols can reconverge only when their composed deck actions agree on the relevant hidden state or visible card. | On planted one- through four-swap XGAK, infer collision constraints from divergence/rejoin events without plaintext labels; require recovery of withheld operation pairs before applying unchanged logic to Eyes. | Motivated by Tuska and Sam's recent composite-action discussion; overlaps deck chaining in theme, not in this test. |
| **F. No-double capacity bound** | The complete absence of adjacent ciphertext doubles constrains the number or support of possible plaintext operations more strongly than frequency statistics do. | Derive exact small-deck counts or SAT bounds for how long a fixed operation set can avoid top-card repetition, then compare the observed 1,027 transitions with reset-aware controls. | Project-original formulation. The observed no-double fact is old; a post-hoc probability under independent labels is insufficient. |
| **G. Gauge-invariant operation complexity** | Unknown initial deck order contributes an arbitrary substitution gauge; useful GAK complexity lives in conjugacy-invariant properties of the operations. | On known-plaintext fixtures, quotient recovered witnesses by simultaneous conjugation and test whether cycle types, generated subgroup, or commutators are stable across models. | Project-original exact audit of a known identifiability problem. It needs multiple SAT witnesses, not one attractive key. |
| **H. Finnish syllable-token fingerprints** | A borrowed Finnish source preserves word/syllable repetition or meter even if character equality is obscured. | Freeze a deterministic Finnish syllabifier, validate it on a small hand-labelled set, canonicalize token equality patterns, and search chronologically eligible corpora with planted-source controls. | Cararasu's verse comparison is community prior art. Literal ciphertext-equality matching is not justified by arbitrary GAK. |
| **I. Finnish phonotactic constraint lattice** | Vowel harmony, long-vowel/consonant quantity, and legal syllable boundaries constrain possible plaintext segmentation even without a source text. | Encode only independently documented Finnish constraints and ask whether any word-boundary lattice survives a fixed substitution/GAK-visible invariant; compare with matched pseudo-Finnish. | Project-original formulation; not permission to score arbitrary Finnish-looking decodes. |
| **J. Carrier-attribution matrix** | Existing near-hits may all be explained by copied prefixes, repeated full labels, renderer phase, or checksum selection rather than the proposed mechanism. | Re-score every retained positive/residue after partitioning test events into exact-label reuse, equality-only reuse, copied-prefix positions, row boundaries, and genuinely new contexts. | Project-original generalization of the cipher-4 audit. This is an evidence filter, not a decoder by itself. |
| **K. Equality-versus-source discriminator** | Shared ciphertext patterns arise either from repeated plaintext phrases or from state-machine dynamics; the two causes make different predictions after a repeated window exits. | On planted substitution, GAK, grouped-XGAK, and shared-source fixtures, classify only the first unseen transition after each isomorph and demand leave-one-family-out discrimination. | Project-original synthesis of the source and causal tracks. Existing isomorph scans did not train a calibrated cause classifier. |
| **L. Reset-state identifiability** | All nine panels reset one machine, continue one stream, or use family-specific reset states. | Derive label-invariant prefix/suffix likelihoods under planted reset/continuation models and require recovery of reset regime before fitting Eye parameters. | Earlier work tested direct concatenations and common base maps; this model-comparison gate is narrower and held out. |
| **M. Renderer-boundary counterfactual** | Apparent positions 25/26, row effects, or header lengths are consequences of 26-glyph rendering rather than cryptographic fields. | Rewrap the unchanged streams at every width in a frozen range and measure whether the same statistic follows glyph index, row end, or neither; reselect width and statistic in controls. | Project-original confound audit. It cannot establish that width 26 is a key merely because the renderer uses it. |
| **N. Later-clue interface signatures** | A later asset deliberately exposes an operation already used to construct the Eyes, as the Cessation quest later exposes its intended cycle. | Search decompiled handlers and assets for an executable interface with exactly the required arity/cardinality—such as 9 selectors, 83 states, 42 pairs, or mod 101—and demand one held-out Eye prediction. | Retained in-game track. The Gate topology and 70-pixel correspondence are inspiration, not accepted premises. |
| **O. Construction chronology and depot delta** | A decoder clue may be newer than the Eyes, while any borrowed construction material must predate their internal creation. | Build a dated asset/code delta for candidate mechanisms and label each as construction input, possible later clue, or chronologically impossible external source. | User-supplied chronology rule. Internal developer ideas are not dated by public release. |
| **P. Practice-cipher transfer test** | A method learned from sdlwdr ciphers 3 or 4 exposes a representation class missed on Eyes. | A method must solve or materially predict a held-out part of the practice puzzle before its unchanged invariant is evaluated on Eyes. | Retained calibration track. Merely fitting the disclosed plaintext or looking up a solution does not qualify. |

## First mixed batch

The first batch is **A, B, C, H, J, and F**, in that order only for engineering
convenience:

1. falsify or retain the exact entropy/change-point claim;
2. reuse and audit the existing finite first-glyph checksum controls rather
   than duplicate them;
3. reproduce the tiny GAK orphan result and establish a scaling gate;
4. calibrate syllable-token fingerprints before any large source search;
5. attribute the carriers of already retained statistical residues;
6. derive a tiny exact no-double capacity table before contemplating Eye scale.

These tests deliberately span direct arithmetic, model feasibility,
linguistics, meta-evidence, and combinatorics.  Lane C is not allowed to delay
the others if exact solving scales poorly.

## Promotion discipline

- Planted positives must be recovered before a new inference primitive touches
  the Eye data.
- Every choice of cut, lag, modulus, message subset, projection, direction, and
  family partition is repeated inside the null or held out.
- An exact contradiction closes the exact claim even when a looser relative
  remains possible.
- A SAT witness proves only existence; UNSAT is interpreted only for the exact
  frozen model and alphabet bounds.
- A source hit must reproduce a predeclared structural fingerprint and pass a
  chronology check.  The source need not have been publicly released if the
  developers could have possessed it, but an external text that did not yet
  exist cannot be construction material.
- In-game correspondences require executable directionality: the candidate
  clue must predict an Eye quantity that was not used to select it.
- No lane receives a deep search merely because all other cheap screens fail.

## First-batch result

The mixed batch is complete in
[`eleventh-wide-first-batch-results-2026-07-24.md`](eleventh-wide-first-batch-results-2026-07-24.md).
The exact entropy pivot and crafted syllable example close; no-double capacity
is unbounded.  The small ciphertext-only GAK orphan reproduces exactly and
becomes a useful calibration oracle, but factorial growth prevents an Eye-scale
claim.  Carrier attribution finds no retained result that predicts a genuinely
new body context.
