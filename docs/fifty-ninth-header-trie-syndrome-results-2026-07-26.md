# Fifty-ninth pass — header-ordered trie syndrome

## Question

Lane E of the frozen order-ideal horizon proposed using each factoradic header
as the sibling collation of the fixed, marker-stripped body trie. An upper
branch would select a traversal and a lower branch would test its syndrome.

## Structural audit

The corpus gives one header per message, not one header per shared trie node.
At each non-singleton node I counted the distinct five-eye collations supplied
by its member messages:

```text
shared depth  members                    header  inverse
2             all nine                       9        7
24            E1,W1,E2                       3        3
5             W2,E3,W3,E4,W4,E5              6        5
9             E3,E4,W4,E5                    4        4
20            E4,W4,E5                       3        3
```

No shared node has a unique collation under either frozen route. In
particular, choosing a representative message, majority order, composition,
or aggregate would introduce a new rule that is absent from both the header
construction and the trie. Selecting that rule by the proposed lower-branch
syndrome would let the target define its own traversal.

## Decision

The exact header-ordered trie-syndrome lane is **non-identifying before any
body score is calculated**. It is closed without trying aggregators.

This does not reject the exact modulo-101 trie checksum, the factoradic
headers, or a future in-game object that independently assigns one collation
to each shared node. It rejects only the claim that the current message
headers already define that traversal.

Reproduction:

```text
PYTHONPATH=src python3 -m unittest tests.test_header_trie_syndrome
PYTHONPATH=src python3 scripts/audit_header_trie_syndrome.py
```
