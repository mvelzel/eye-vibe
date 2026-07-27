# Eye corpus — signed 42-state path transfer freeze

**Date:** 27 July 2026
**Status:** frozen before the Eye corpus is checked

## Motivation

The practice-cipher pass validated a cheap exact discriminator for:

```text
83 = 2*42 - 1
```

The Eye messages also use the accepted `0..82` trigram alphabet. This transfer
asks whether those values are signed displacements on the same natural
42-position plaintext line under the authored numeric order.

## Frozen catalog and modes

Exhaust:

```text
d(v) = ((sign*v + offset) mod 83) - 41
sign in {+1,-1}, offset in 0..82
166 maps
```

Use accepted trigram order and unchanged message boundaries. Test:

1. **full** — the first trigram is the initial absolute state;
2. **primer** — the first trigram is metadata/primer and is ignored, with any
   legal initial state allowed for the remaining body.

No panel-specific cut, modular wrap, alternate trigram order, hidden label
permutation, or language score is admitted.

## Controls and decision

A same-length planted fixture must select a hidden catalog map and exercise
every signed displacement. Both modes must replay inside `0..41` before the
real corpus is opened.

- zero real survivors exactly rejects this finite family;
- a survivor is only structural compatibility and must produce stable
  language before promotion;
- failure does not reject an arbitrary hidden signed-step permutation.
