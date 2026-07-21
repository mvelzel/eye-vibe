#!/usr/bin/env python3
"""Print the exact last-family certificate against ``P**position``."""

from eye_mystery.progression_certificate import (
    last_family_commutation_contradiction,
    last_family_progression_contradictions,
)


def main() -> None:
    commuting = last_family_commutation_contradiction()
    print("model: cipher_i = P**(i + phase_m)(S[plain_i])")
    print("assumption: the two strong length-30 last-family alignments repeat plaintext")
    print("let A be East 4->East 5 and B be East 4->West 4")
    print("context edges: A(3)=44, B(3)=22, A(22)=23, B(59)=23")
    print("if A and B commute, B(44)=B(A(3))=A(B(3))=A(22)=23")
    print("but B(59)=23; injectivity of B would force 44=59")
    print("result with arbitrary per-message phases: UNSAT")
    print()

    contradictions = last_family_progression_contradictions()
    print("smaller common-phase specialization:")
    for contradiction in contradictions:
        chain = " -> ".join(map(str, contradiction.forced_chain))
        print(
            f"P-chain forced by the one-step context: {chain}; "
            f"three-step context requires {contradiction.start} -> "
            f"{contradiction.required_target}"
        )
    print(f"contradictions: {len(contradictions)}")
    print("result: UNSAT")


if __name__ == "__main__":
    main()
