# Discord delta and independent factoradic-header audit — 22 July 2026

## Outcome

The proposed six-symbol/factoradic reading of the nine first trigrams is a
real, reproducible header structure. It is promoted as metadata and as a
possible state-machine clue, not as plaintext and not yet as a body decoder.

The strongest finite result survives an implementation written from the local
canonical corpus rather than imported from the Discord attachment. Freeze the
known first-two-digit graph coordinates of every named header, preserve the
observed multiset of third digits, and permute only those third digits. Of
12,096 in-range assignments retaining nine distinct ranks, exactly two retain
all of:

- newline-preimage word `555343434`;
- P messages as the named `r,s,r^-1` generators of a D4 group;
- all Q messages fixing only center and generating S5;
- three East-Q right cosets versus one West-Q right coset of P's D4.

The two assignments are the observation and the exchange of West2 with West4.
Those messages have the same frozen graph edge and the same West-Q type, so
they form one class under the graph model's only relevant duplicate-edge swap.

Reproduction:

```text
PYTHONPATH=src python3 scripts/analyze_factoradic_headers.py
```

The independent implementation is
`src/eye_mystery/factoradic_headers.py`; exact fixtures are in
`tests/test_factoradic_headers.py`.

## Provenance and integrity

Lquid posted `noita_eye_header_audit.zip` read-only in
`silmä-teollinan-älly`. The downloaded 376.98 KiB attachment has SHA-256:

```text
ec9968c38c0816caba668a4cc73d78f0e8a89c2bba569b8729276d121d710fb8
```

Every member passes its included `MANIFEST.sha256`. In a temporary directory,
the archive's top-level reproduction command regenerated its shipped JSON and
Markdown byte-for-byte. Their hashes are:

```text
07a18ce78722d434aa0ca7ba64bf2443f39478ea20d893220d1e5f919c428d5a  JSON
893512dca51157c02b49d21568a380489ca55c2b78a21e21a4a48f22f552c323  report
```

The archive is evidence and a source of hypotheses. It is not vendored here;
the compact local implementation prevents its larger analysis stack from
becoming an unexamined dependency.

## Deterministic reconstruction

Use ordinary lexicographic unranking of each orthodox header rank as a
permutation of:

```text
[center, up, right, down, left, newline]
```

The table below comes directly from the local accepted corpus.

| message | rank | permutation | order | fixed inputs | input mapped to newline |
|---|---:|---|---:|---|---:|
| East1 | 50 | `0,3,1,4,2,5` | 4 | `0,5` | 5 |
| West1 | 80 | `0,4,2,3,1,5` | 2 | `0,2,3,5` | 5 |
| East2 | 36 | `0,2,4,1,3,5` | 4 | `0,5` | 5 |
| West2 | 76 | `0,4,1,5,2,3` | 6 | `0` | 3 |
| East3 | 63 | `0,3,4,2,5,1` | 5 | `0` | 4 |
| West3 | 34 | `0,2,3,5,1,4` | 5 | `0` | 3 |
| East4 | 27 | `0,2,1,4,5,3` | 6 | `0` | 4 |
| West4 | 77 | `0,4,1,5,3,2` | 5 | `0` | 3 |
| East5 | 33 | `0,2,3,4,5,1` | 5 | `0` | 4 |

East1, West1, and East2 are exactly `r,s,r^-1`; their generated group has
order eight and rank set `0,6,26,36,50,60,80,86`. The six Q permutations
generate all 120 permutations of the five noncenter symbols. East-Q occupies
three right cosets of P while West-Q occupies one.

## What is forced and what is not

Because all visible ranks are below `5! = 120`, lexicographic S6 unranking
automatically puts symbol zero first. Therefore the shared fixed center is not
independent evidence. The nontrivial observations are the exact P inverse and
reflection relations, the additional fixed newline in P, Q's side-specific
newline preimages, the full generated group orders, and the right-coset split.

The exact `2/12,096` conditional is local. It does not charge the entire
project for the many representations investigated before factoradics were
noticed, and it does not prove that newline is semantically part of the
cipher. The larger attachment reports strong leave-one-out classification,
but the current repository has independently reproduced only the deterministic
group facts and graph-conditioned enumeration. That is enough to promote the
lead while keeping its selection caveat visible.

The most obvious decoder is already bad: applying one P header permutation as
a fixed substitution destroys the bodies' independently observed aligned
equalities. No plaintext follows from the header table.

## Separate wide probe: Paley transition bit

The “Why 83?” discussion motivated a key-free construction not found in the
local prior logs: map each adjacent nonzero difference modulo 83 to its
quadratic character. Since `83 mod 4 = 3`, reversing a difference complements
its bit. That makes repeated windows under affine relabeling equal or bitwise
complementary without selecting a primitive root.

The corpus supplies 1,027 bits, 485 of them one. Across the frozen repeated
contexts, the best equal-or-complement fit is 134/221 comparisons with only
one exact copy among thirteen. Under 2,000 global label permutations its
upper tail is `1004/2001 = 0.501749`. The best selected 7/8-bit ASCII rendering
has 124/145 conservatively printable values but is gibberish; its corrected
upper tail is `738/2001 = 0.368816`. This Paley lane is closed.

Reproduction is in `src/eye_mystery/paley_projection.py` and
`scripts/analyze_paley_projection.py`.

## Read-only Discord delta worth retaining

- Henry's public SAT implementation is already covered by the local
  arbitrary-GAK audit; the fresh chat adds no stronger scaling result.
- Lymm proposes an undiscovered extension of graph chaining from GCTAK to GAK,
  informally “deck chaining.” This is a useful mechanism search target, not a
  specified algorithm yet.
- The XGAK discussion suggests quotienting or merging plaintext-selected
  permutations. If numbers share a permutation, the common starts and later
  reconvergence may reflect a small operation quotient rather than identical
  plaintext. This deserves a finite partition test; “trailer altar” is only an
  unverified possible selector.
- The public “Why 83?” document gives a plausible design argument: among the
  candidate maxima of three base-five digits, modulus 83 is the largest prime
  that preserves the digit/read-order diagnostics. Its additional primitive-
  root and asset numerology is exploratory.
- `wmdwm.net/noita` is useful as an interactive pattern viewer but labels more
  than 95% of its own text as AI-generated. It is navigation, not evidence.
- The giant-dollar sprite is present byte-identically in the current and
  archived early-access assets, so it is chronologically eligible as an
  original-construction clue. The recently claimed 43-row fold/XOR arithmetic
  still needs independent masks and a held-out prediction before promotion.

## Wide factoradic body portfolio before depth

The header result earns a new breadth pass, not immediate commitment to one
decoder. Run one cheap necessity test in each distinct family first:

| lane | mechanism | first falsifier |
|---|---|---|
| A | nonabelian message/row checksum | test whether forward/reverse S6 body products predict the header or identity against equality-preserving relabel controls |
| B | adjacent quotient walk | test whether `p_i^-1 p_(i+1)` uses unusually few generators or stays unusually often inside ranks `0..82` |
| C | running S6 transducer | use header as initial state and expose only fixed renderer coordinates; require a small output alphabet or held-out repeat consequence before language scoring |
| D | moving-delimiter tape | apply the Q permutation to the genuine six-symbol visual tape, including authored row breaks; require coherent retokenization rather than post-hoc text |
| E | D4 coset channel | quotient body permutations by the independently recovered P group and test whether side/family structure predicts coset transitions |
| F | conjugacy/cycle channel | reduce absolute permutations to cycle type or conjugacy differences; require predictive context alignment, not a fitted symbol mapping |
| G | deck-chaining quotient | search for a label-invariant way to merge operation classes from reconvergence, calibrated first on solvable GCTAK/practice instances |

Only a survivor with an independent consequence should receive a large solver
or plaintext search. In particular, direct per-message unshuffling and an
arbitrary mapping from S6 features to letters remain disallowed.

## Completed portfolio result

Lanes A–F have now been run and none promotes. Message products match none of
the nine headers/identity targets; adjacent quotients cover 119 of the complete
120-element S5 rather than a small generator set; running states do not
compress; P-coset and cycle-type channels are ordinary. Moving newline expands
the 86 authored rows to 327 or 456 fragments, including 30 or 75 empty rows.
Full matched-control results are in
[`factoradic-wide-2026-07-22.md`](factoradic-wide-2026-07-22.md). Lane G remains
a separate method-calibration lead.
