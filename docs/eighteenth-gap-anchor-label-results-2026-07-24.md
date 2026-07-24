# Gap-anchor orthogonal label controls — results

## Result

Both preregistered global-label nulls pass the broad `.01` gate. The natural
orthodox `0..82 mod 83` coordinate is promoted as part of the final-row
header/body construction link.

```text
null                         exact tail              broad tail
body labels, markers fixed   9/50001 = .000179996   100/50001 = .001999960
joint body/marker labels      1/50001 = .000020000     4/50001 = .000079998
```

Counts before the plus-one correction are respectively `8,99,0,3`.

## What the nulls preserve

Both controls retain the exact complete equality skeleton. The three clean
gap-11 anchors remain unique and at positions `16,18,17`; only their numeric
labels change.

The body-only null leaves markers `27,77,33` fixed and applies one random
permutation of all 83 labels to every body anchor. Its broad statistic allows
all anchor orders and ignores header-to-edge assignment. The low tail shows
that the selected body labels are coupled to the marker values.

The joint null applies the same random permutation to both body anchors and
markers. It preserves their common abstract alphabet assignment while
destroying modular arithmetic in the natural base-5 rank coordinate. Its still
lower tail shows that the orthodox numeric coordinate is not replaceable by
an arbitrary shared relabeling.

## Boundary

This establishes three things under independent nuisance structures:

1. the equality landmark is positionally unusual under body shuffles;
2. its labels are coupled to the fixed headers;
3. the natural mod-83 coordinate carries the coupling.

It still does not establish that subtraction is the per-symbol encryption
operation. Directly subtracting the anchors from their 12-symbol windows
aligns only the two endpoints (and one incidental W4/E5 interior position),
so a simple rotational cipher does not follow.

The strongest current interpretation is therefore typed construction or
check metadata. The final marker row records two modular path differences and
their telescoping total over a label-invariant repeated-body landmark.
