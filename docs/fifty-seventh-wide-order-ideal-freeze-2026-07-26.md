# Fifty-seventh horizon — header-ordered codebook boundary

**Frozen:** 26 July 2026, before any real output was calculated.

## Why widen here

The Kantele/header interface is closed. The remaining compact facts suggest
that the markers may describe serialization rather than directly permute body
symbols:

```text
full eye cube       5^3 = 125
visible codebook          83
omitted codewords         42
83 = 3*5^2+8
```

Each marker also supplies an independently reconstructed permutation of the
five eye symbols plus newline. Existing tests used that permutation as a
substitution, group element, BWT collation, prefix-code leaf order, block
transposition, or Kantele operation. None ranked the *fixed 83-word order
ideal* under the marker's eye collation.

## Wide candidate set

| Lane | Mechanism | First exact discriminator |
|---|---|---|
| A. Visible-codebook rerank | Sort the canonical `0..82` glyph set under each marker's five-eye order and replace each glyph by its rank. | Ask whether the seven fixed nonliteral contexts become literal without fitting a substitution. |
| B. Omission-count channel | Subtract visible rank from full-cube rank. The result counts excluded words preceding the glyph and lies in `0..42`. | Select header/inverse on four contexts and score three held-out contexts under equality-preserving controls. |
| C. Header-orbit projection | Treat the nine headers as an `S6` representation; equal header images of one coordinate predict aligned panel equality classes. | Remove all copied openings and test each of six coordinates with the coordinate selected on row 1 and rows 2–3 held out. |
| D. Conditional no-repeat rank | Rank each next glyph in the 82-word codebook excluding the previous glyph, under header collation, then split `82=2*41`. | Require one fixed sign/magnitude convention to replicate across message rows. |
| E. Prefix-trie ordered syndrome | Use the header collation only to order siblings of the fixed merged trie, then compute subtree omission counts. | A syndrome trained on upper branches must predict the lower-six residue without changing traversal. |
| F. Rejection-transcript model | Interpret `0..82` as accepted states of an authored larger domain and the missing interval as unobserved delay/control states. | Advance only if an in-game sampler fixes the larger domain and predicts a stored boundary or skip count. |

Lane B ranks first because its output cardinality is forced by the exact
codebook complement, it consumes the factoradic header without a learned key,
and it makes a literal held-out equality prediction. Lanes C–F remain ideas,
not evidence.

## Frozen lane-B transform

For a message marker:

1. lexicographically unrank its real `S6` permutation;
2. use either that permutation or its inverse;
3. delete newline from the resulting order, leaving one order of eye digits
   `0..4`;
4. rank a body trigram in the complete 125-word cube under that order;
5. rank the same trigram among only the canonical visible words `0..82`;
6. output

```text
omission = full_cube_rank - visible_codebook_rank
```

This is exactly the number of omitted words before the glyph in that
collation, hence `0 <= omission <= 42`. No letter assignment, modulus, offset,
component permutation, or per-message route is admitted.

## Train/holdout boundary

Use the seven established nonliteral partial-bijection contexts unchanged.
The first four select one global route:

```text
first-gap30
first-cross
first-cross-late
first-gap28
```

The last three are untouched holdout:

```text
last-west4
last-east5
last-east3
```

The score is the number of aligned omission outputs that are literally equal.
Route selection uses training agreement only; a tie chooses `header`.

## Exact matched control

For every affine permutation of the visible labels,

```text
x -> a*x+b mod83
a in 1..82, b in 0..82
```

relabel every occurrence globally, preserve the real headers, reselect the
route on training, and score holdout once. These 6,806 controls preserve:

- every equality and inequality;
- all copied prefixes and nonliteral equality isomorphs;
- all message lengths and no-double structure;
- the complete marker/type system.

They break only the proposed relation between absolute base-five geometry and
the header-ordered codebook.

## Promotion and stop rules

Promote only if:

1. the exact heldout upper tail is below `.01`;
2. improvement is present in more than one heldout context;
3. the output supplies a second exact consequence, such as a stable
   42-symbol support or a marker/boundary prediction.

Training fit or a readable rendering selected afterward is insufficient.
Failure closes this exact static omission-count decoder. It does not reject a
stateful order-ideal code or lanes C–F.
