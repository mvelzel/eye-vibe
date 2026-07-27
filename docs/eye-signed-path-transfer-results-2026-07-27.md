# Eye corpus — signed 42-state path transfer results

**Date:** 27 July 2026
**Outcome:** exact finite negative; no decoder or plaintext

## Control

The same-length planted fixtures selected
`orientation=-1, offset=17`, exercised every displacement in `-41..+41`, and
replayed every state inside `0..41`:

```text
mode     result   surviving maps
full     sat           1
primer   sat           2
```

The two primer survivors are reflection-equivalent.

## Real Eye corpus

Using accepted trigram order and all nine original message boundaries:

```text
mode     surviving maps
full          0
primer        0
```

The primer test ignores each first trigram and exactly admits every possible
per-message start whose body walk stays inside the 42-state line.

## Decision

Close this complete finite family:

```text
d(v) = ((sign*v + offset) mod83) - 41
sign in {+1,-1}, offset in 0..82
```

The Eyes are not an authored-order signed-displacement walk on a natural
42-position plaintext line, whether the first trigram is payload or metadata.
This does not reject an arbitrary hidden permutation of the 83 displacement
labels, modular walks, or other state machines.

The result contributes a scoped exclusion only. It supplies no plaintext,
key, intended operation, or in-game clue.

## Reproduction

```text
PYTHONPATH=src python3 scripts/run_eye_signed_path.py --phase both
```
