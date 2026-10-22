"""
01 — Shor's factoring of N = 15, end to end.

Pipeline:
  1. Pick a = 7 (a real Shor run picks a at random; here a is fixed
     because the quantum circuit is COMPILED for N=15, a=7 — the gate
     sequence hardcodes them instead of doing general modular
     arithmetic).
  2. Run quantum phase estimation of the multiply-by-7-mod-15 unitary.
  3. Classical post-processing: continued fractions on the measured
     phases -> candidate orders -> verify 7^r = 1 mod 15.
  4. From the order r: p = gcd(7^(r/2) - 1, 15), q = gcd(7^(r/2) + 1, 15).

Expected result: factors {3, 5}.

Run:
    python3 scripts/01_shor_15.py [--shots 2048] [--seed 42]
"""

import argparse
import os
import sys
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build_qpe_circuit, find_order, phase_from_key, ascii_histogram

from qiskit import transpile
from qiskit_aer import AerSimulator

N = 15
A = 7


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", type=int, default=2048)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    print(f"Factoring N = {N} with Shor's algorithm (a = {A}, compiled circuit)")
    print()

    # Step 0: classical easy case — does a share a factor with N already?
    g = gcd(A, N)
    print(f"Step 0 — gcd({A}, {N}) = {g} (1, so no trivial factor; continuing)")

    # Step 1: quantum order finding via phase estimation.
    print("Step 1 — quantum phase estimation of U|y> = |7y mod 15> ...")
    qc = build_qpe_circuit(n_count=4)
    sim = AerSimulator(seed_simulator=args.seed)
    counts = sim.run(transpile(qc, sim), shots=args.shots).result().get_counts()
    print(f"  measured phases ({args.shots} shots):")
    print(ascii_histogram(counts, args.shots))
    for key in sorted(counts):
        print(f"    {key} -> phase {phase_from_key(key)} "
              f"= {float(phase_from_key(key))}")

    # Step 2: continued fractions -> order.
    print("Step 2 — continued fractions on the measured phases ...")
    r, detail = find_order(A, N, counts)
    print(f"  order r = {r} ({detail})")
    assert pow(A, r, N) == 1

    # Step 3: classical post-processing -> factors.
    print("Step 3 — classical post-processing ...")
    assert r % 2 == 0, "odd order: restart with another a (did not happen here)"
    x = pow(A, r // 2, N)
    assert x != N - 1, "a^(r/2) = -1 mod N: restart (did not happen here)"
    p, q = gcd(x - 1, N), gcd(x + 1, N)
    print(f"  7^{r // 2} mod 15 = {x}")
    print(f"  p = gcd({x - 1}, 15) = {p}, q = gcd({x + 1}, 15) = {q}")
    print(f"  check: {p} x {q} = {p * q}")

    assert {p, q} == {3, 5}, f"wrong factors: {p}, {q}"
    print()
    print(f"OK — Shor factored 15 = {p} x {q}.")


if __name__ == "__main__":
    main()
