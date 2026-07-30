# Public three-ring disk-mask screen (2026-07-30)

## Provenance and method

The public noita-eyes repository contains commit 0b0e028 (2024-11-02),
“Naive approach to disk-based masking directly on the trigrams.” It defines
three periodic masks (eyes1, eyes2, eyes3) and applies them independently to
the three raw direction digits. A mask bit of zero keeps the direction and a
one replaces it with zero; the resulting 25a+5b+c values are emitted as
ASCII32. The ring lengths are 17, 20, and 24.

Implementation: public_disk_mask.py and screen_public_disk_mask.py. The
current repository's stale Lua script has a post-refactor argument-order bug;
this audit ports the original rule directly and tests the source constants.
No ring, phase, order, or alphabet was fitted to Eye output.

## Verified output

The complete output is reproducible with:

    PYTHONPATH=src python scripts/screen_public_disk_mask.py

The nine output lengths and SHA-256 digests (of the UTF-8 output string) are:

    east1  99   463c936106837e95e7b12988dcb31beb77b6f2dcd494a75f7f467cc13bebe5fa
    west1 103   bbae56b39374798f494142e9c933f98cdac582f6d8fcd2590c6a11981016e51d
    east2 118   c3c74513e7b93dfa93829cc33f970d00d4ffc28e65dab1bb1b742f738db3bb1f
    west2 102   ca7d739b2140a38597f8b3d12d548e8a6e74bc4bfc2a2e14cd5c82a727c6bcb0
    east3 137   51406949e973c7ab3a7aebd606ecccac93f4e302e7e6324a195c3af37318358d
    west3 124   8c5b04b1d184e41c2cedfc46e0afb7b7463c77a92d2ed912cf9065c0e3455930
    east4 119   e88b982424e5f790dcf28d7686528d1aeddd5ca9283fa0857144b6d3eebb4273
    west4 120   241e6f67e4f1353995e20324b2812bdced5776cc5f5f4ce3365f883f08ca12dc
    east5 114   e565057b061f6b1d08893e5a7e478c30db99c960484786cd8b7aa1dbcd6b04b0

The first 60 characters of East1 are:

    R0 7T- $$]"4!^".!( #"=#8!%m/#&!3 /S/!.!4"3#J$7#O$8"? 8#K$1#8

All nine streams are punctuation-heavy ASCII, not Finnish or English. The
deterministic mask retains shared prefixes but does not turn the copied or
isomorphic regions into a readable stream.

## Disposition

This closes the exact three-ring mask proposed in the public source. It does
not reject an independently selected disk with a different mask, hidden phase,
or stateful operation; those remain the separate arbitrary-disk lane already
frozen in the project. The source supplies no evidence for such a variant, so
fitting one after this negative would be an unconstrained search.
