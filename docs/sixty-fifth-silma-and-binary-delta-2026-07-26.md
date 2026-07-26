# Sixty-fifth pass — read-only Silmä and binary-initializer delta

## Scope and theory firewall

This pass read recent `silmä-cryptography`, `silmä-novel`, and
`silmä-teollinan-älly` discussion and linked public sources. Discord access was
strictly read-only. No message, reaction, call, or follow action was sent.

Every proposal below is judged independently. A failed visual theory cannot
lend its surviving patterns to a deck theory, and neither can corroborate
Veska. Only raw observations or reusable methods may transfer, without
transferring evidential weight.

## Recent channel delta

The recent cryptography discussion adds no selected decoder:

- the normal trigram reading remains the only tested reading preserving the
  alphabet, shared opening, and six later patterns;
- the XGAK discussion proposes broad representation/capacity claims but no
  independently selected Eye operation, key, or held-out prediction;
- the reported `C5 x C3 ~= C15` nontransitive construction has two disjoint
  chaining components and is a mathematical example, not an Eye decoder.

The recent novel discussion mostly revisited a 2023 octahedron/diamond drawing
proposal. It is audited below as its own theory.

The public
[Noita Eye Messages Research Hub](https://app.notion.com/p/Noita-Eye-Messages-Research-Hub-3a9b74fbf6e3811db688c569addf7d0e)
states a sound solution threshold: demand either deterministic full-corpus
decryption or a complete generator with frozen predictions. Its current
binary candidate is useful, but the local executable resolves its role more
directly than the hub currently does.

## Standalone Frosthaven visual-theory audit

### Reconstructed proposal

The original
[Frosthaven document](https://docs.google.com/document/d/1orFAVxP5LemIRlf1RMnXa8KI0vtSKP8UHQ4xFEkrBFw/edit?usp=sharing)
places the six eyes from two trigrams at fixed vertices of two joined
pyramids. Eye directions trace lines from four planar viewing angles. The
center-eye positions are swapped according to the `i!i` stone. Candidate
lines are then matched to in-game or Finnish-style runes.

The linked
[isomorph sheet](https://docs.google.com/spreadsheets/d/1wyxQ1frHkVfY4_8293lg6f_vy4gC30B7PtmYVSdOg9E/edit#gid=0)
shows that the construction reduces to a 14-segment-style display for the
currently treated odd trigrams. The
[known-rune catalogue](https://docs.google.com/document/d/1fcfUsJOmJ7dzHEwH45hXCDTX9DSgeWSrDkn4DIQZ4g8/edit)
supplies candidate glyph readings.

### Capacity and reproducibility failure

The proposal does not pass its own standalone gate:

- it was tuned using expected `HS` and C-like shapes;
- any orientation may count;
- one drawing may contain one rune or several merged runes;
- support lines may be ignored, while missing strokes may be tolerated;
- multiple in-game and external character sets are admitted;
- a human then selects letters and words from the candidate set;
- even trigrams do not have a completed fixed treatment;
- the isomorph sheet explicitly retains a Z-like candidate that fails the
  stated perspective rule “just in case”;
- no unique, deterministic, complete replay of all nine messages is given.

The method is therefore a high-capacity glyph-candidate generator, not a
decoder. It is rejected without reference to Gate, WAK, XGAK, or any other
theory. It can reopen only with fixed orientation, exact stroke tolerance,
complete odd/even handling, and a blind full-corpus decode.

## The highlighted binary function is the Eye initializer

The hub identifies 2025 function `FUN_0061ed60` as a candidate that constructs
nine arrays but describes the value-level result as unresolved. The installed
Windows executable settles that question.

Frozen local binary:

```text
PE timestamp: 2025-01-25 14:59:24
SHA-256:
808d2a0ab51ea0b46e9ad2aeb3327a4b0ce3feae04f32ba26326bf585b5779bd
```

The visible corpus independently packs into 150 unsigned 64-bit base-seven
words with SHA-256:

```text
5de6ccb3a045218827b7ddaad0f1493254f501b08addd1929495ce060242de94
```

In the frozen interval `0x0061ed60..0x0061fcdc`, the function contains:

```text
150/150 low 32-bit halves in exact corpus order
146/146 nonzero high 32-bit halves in exact corpus order
4 expected zero high halves
1 shared exact zero-high store at 0x0061fcdc
```

Changing one planted immediate causes the verifier to reject. The following
code then repeatedly performs division/remainder by seven before passing the
unpacked result onward. This is the compiled implementation of the already
reconstructed base-seven storage layer.

Consequently:

1. `FUN_0061ed60` is positively identified as the nine-way Eye-row
   initializer.
2. All 150 authored packed words match the accepted visible corpus.
3. The function stores and unpacks precomputed ciphertext; it contains no
   runtime decryption step.
4. Decompiling farther along this function is unlikely to reveal the cipher
   construction, because the construction occurred before these constants
   were compiled.

The claimed 2020 counterpart `FUN_005a7c20` remains unchecked because no
matching 2020 executable is locally available. Verifying it would strengthen
binary chronology, not supply a decoder.

Reproduction:

```text
python scripts/verify_eye_initializer.py /path/to/noita.exe
```

Implementation and planted control:

```text
src/eye_mystery/binary_initializer.py
tests/test_binary_initializer.py
```

## Practice cipher #4 source check

The live practice thread still contains the known author disclosures:
deck-based, much shared plaintext, identical straightforward initial
plaintext-alphabet order. A solver identified a cyclic effective group and
standard equivalent ciphertext order.

A read-only search of sdlwdr's messages after 22 July 2026 found no newer
author hint answering the request in the thread. The pure-cryptographic stop
rule therefore remains: do not widen the failed language beam; reopen only
for a source/crib, a qualitatively different deck invariant, or an author
hint.

## Decision

- Close Frosthaven's visual method as a standalone decoder.
- Promote the binary identification as a storage/renderer fact only.
- Do not treat the binary initializer as evidence for any cipher family.
- Do not aggregate any of these results with Veska or other fringe theories.
- Return cryptographic effort to mechanisms that can constrain the body
  before language fitting.
