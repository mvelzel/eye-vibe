# Practice cipher 3 — hidden reflection-wheel freeze

## Why this family survives

The reset-body prefix tree makes adjacent transitions more natural than
absolute ciphertext labels. A fresh one-direction Wadsworth wheel is already
impossible, independently of language:

```text
unique directed transitions       1845
reciprocal unordered pairs         253
maximum reciprocal degree           14
```

If every transition were one of 42 consecutive forward steps on a hidden
83-cycle, both directions of one unordered pair could coexist only at the two
boundary distances 41 and 42. Each state could therefore have at most two
reciprocal partners. Raw state 82 has fourteen. The contradiction closes a
single global direction, not wheel arithmetic in general.

The natural direction-free quotient is different. For hidden coordinates
`z(a), z(b)` in `Z83`, define

```text
d(a,b) = min((z(b)-z(a)) mod 83, (z(a)-z(b)) mod 83).
```

Its nonzero values are exactly `1..41`; adding zero gives 42 classes. Thus the
visible 83-state alphabet and the known 42-position plaintext alphabet meet
without an arbitrary modulus, divisor, or discarded symbol. No displayed
numeric order is assumed.

## Frozen tests

### A. Authored standard order

Apply the unsigned distance above directly to raw labels `0..82`. Solve one
injective substitution from its 41 observed classes into the known
42-character plaintext alphabet. This is a cheap baseline, not evidence for
the authored order.

### B. Old-wheel insertions

Insert the exceptional `J` into every one of the 83 positions of the exact
82-wheel recovered from practice ciphers 1 and 2, in both orientations.
Apply the reflection quotient and select a single plaintext substitution.
This tests construction reuse more broadly than the first batch's directed
wheel/control transfer.

### C. Joint hidden wheel

Optimize one permutation of the 83 raw labels and one injective assignment of
the resulting 41 magnitudes to the 42 plaintext symbols. The allowed moves are
only:

- swap two raw labels' cyclic coordinates;
- swap two magnitude-to-plaintext assignments.

Every coordinate swap is rescored only at incident transitions and every key
swap only at windows containing its magnitude. The objective is a smoothed
English/Finnish trigram likelihood with message boundaries preserved.

### D. Positive and heldout controls

Plant a random hidden 83-wheel, a random injective plaintext-to-magnitude map,
and independently random direction choices at the exact real message lengths.
The optimizer must recover readable heldout plaintext and a wheel equivalent
up to the unavoidable dihedral symmetry.

For the real corpus, A/B/C are not all used for model repair. A first screen
may use the full corpus, but promotion requires leave-one-group-out fits whose
heldout text remains readable and whose recovered wheels agree up to
rotation/reflection. A full-corpus local optimum alone fails.

## Stop rules

- Close A and B after complete finite enumeration plus a calibrated
  substitution control.
- Do not interpret isolated words from C unless the planted control recovers
  the wheel at the same budget.
- A better real score than shuffled text is only a screen. Promotion needs
  readable multi-message plaintext, cross-fold wheel agreement, and exact
  re-encoding under the recovered magnitude/direction schedule.
- Failure of this quotient does not exclude a direction bit carried by a
  larger deck state, randomized homophones, or arbitrary `S83` operations.

## Transfer target

The Eyes already have a heavily tested literal `Z83/{±1}` quotient. This
practice pass is still useful if it yields a cracking method: joint recovery
of an unknown cyclic coordinate order and a small language alphabet. Only a
method that recovers the planted wheel and survives heldout data may be
transferred back.
