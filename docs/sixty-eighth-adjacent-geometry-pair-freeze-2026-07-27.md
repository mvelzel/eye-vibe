# Sixty-eighth pass — adjacent hidden-geometry pair census freeze

## Question

The frozen lag-one hidden-cycle model assigns distinct coordinates
`z[label] in F83` and requires every aligned adjacent chord pair to have equal
unsigned circular length:

```text
z[b]-z[a] = ±(z[d]-z[c]) mod 83
```

Every one of the seven registered nonliteral contexts is satisfiable alone.
The first-family, last-family, and all-context unions previously timed out.
The 21 unordered two-context unions were not reported.

This pass asks the exact necessary question:

> Is any pair of individually satisfiable contexts jointly inconsistent?

One UNSAT pair rejects the global adjacent-cycle hypothesis. SAT for all pairs
does not prove a common wheel.

## Frozen census

- Use the existing seven `NONLITERAL_CONTEXT_SPECS`, unchanged.
- Enumerate all `C(7,2)=21` unordered pairs in canonical context order.
- Use lag one only. No additional geometry, label ordering, or fitted distance
  class is admitted.
- Preserve the existing translation/scaling normalization on the first
  constrained edge.
- Run the bit-vector solver for 15 seconds per pair.
- For each bit-vector timeout, run the independent integer solver for another
  15 seconds.
- `SAT` and `UNSAT` are exact. A double timeout remains `UNKNOWN`.

## Controls before Eye scoring

1. **Jointly SAT pair:** split a small planted wheel across two context names;
   each half and their union must replay exactly.
2. **Jointly UNSAT pair:** split an equidistant triangle over `F5` so that each
   named half is SAT but their union is UNSAT.
3. Both integer and bit-vector encodings must agree on the controls.

## Branching and stop rules

- If any real pair is UNSAT, confirm it with both encodings, minimize its
  constraint set, and attempt a solver-independent finite orientation
  certificate. Do not inspect other model families first.
- If every pair is SAT, report only pairwise compatibility and return to a
  genuinely higher-order exact decomposition.
- If some pairs remain UNKNOWN and none is UNSAT, report the complete
  SAT/UNKNOWN census. Do not reinterpret timeout as evidence.
- No pair result licenses a fitted wheel, plaintext search, or lag-two repair.
