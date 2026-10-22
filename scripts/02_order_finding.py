"""
02 — Order finding, standalone: the quantum heart of Shor's algorithm.

Everything quantum in Shor's algorithm is right here: find the smallest
r with 7^r = 1 mod 15 using phase estimation. The rest of Shor (gcd
tricks to turn r into factors) is classical.

We show both sides:
  * classically, the answer by brute force: 7^1=7, 7^2=4, 7^3=13,
    7^4=1 (mod 15) — so r = 4;
  * quantumly, phase estimation of U|y> = |7y mod 15> yields the phases
    s/4, and continued fractions recover r = 4 from any nonzero one.

Expected result: r = 4.

Run:
    python3 scripts/02_order_finding.py [--shots 2048] [--seed 42]
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import build_qpe_circuit, find_order, phase_from_key, ascii_histogram

from qiskit import transpile
from qiskit_aer import AerSimulator

A, N = 7, 15


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", type=int, default=2048)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    print(f"Order finding: smallest r with {A}^r = 1 mod {N}")
    print()
    print("Classical check (brute force):")
    for r in range(1, 6):
        print(f"  7^{r} mod 15 = {pow(A, r, N)}")
    print("  -> the order is 4 (this took 4 multiplications;")
    print("     for RSA-2048 it would take longer than the age of the universe).")
    print()

    print("Quantum order finding via phase estimation ...")
    qc = build_qpe_circuit(n_count=4)
    sim = AerSimulator(seed_simulator=args.seed)
    counts = sim.run(transpile(qc, sim), shots=args.shots).result().get_counts()
    print(ascii_histogram(counts, args.shots))
    print()
    print("Measured phases and their continued-fraction readings:")
    for key in sorted(counts):
        print(f"  {key} -> phase {phase_from_key(key)}")
    print()

    r, detail = find_order(A, N, counts)
    print(f"Recovered order: r = {r}")
    print(f"  ({detail})")
    assert r == 4, f"expected order 4, got {r}"
    assert pow(A, r, N) == 1
    print()
    print("OK — the quantum subroutine found r = 4, matching brute force.")


if __name__ == "__main__":
    main()
