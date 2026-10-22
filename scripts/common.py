"""
Shared Shor internals: compiled modular-multiplication circuit for N=15,
a=7, QPE assembly, and classical continued-fraction post-processing.

Compiled-circuit note (be honest about this): the gate sequence below
hardcodes N=15 and a=7 into swaps and X gates instead of implementing
general modular arithmetic. That is what "compiled" means — it
demonstrates the quantum subroutine (order finding via phase
estimation) while skipping the hard part (an efficient general modular
multiplier). Factoring 15 this way does NOT imply factoring RSA-2048.

The multiply-by-7 block implements |x> -> |7x mod 15> for 1 <= x <= 14
(verified by exhaustive statevector check); it swaps |0> <-> |15>, but
the orbit of |1> under x -> 7x mod 15 is {1, 7, 4, 13}, which never
visits 0 or 15 — so order finding is unaffected.
"""

import math
from fractions import Fraction
from math import gcd

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT


def c_mult7_power(power: int):
    """Controlled (multiply-by-7 mod 15)^power on 4 work qubits.

    One iteration = swap(0,1); swap(1,2); swap(2,3); X on all four,
    which maps |x> -> |7x mod 15> (x = 1..14). Repeating `power` times
    gives multiplication by 7^power mod 15. Returned as a controlled
    gate: control qubit first, then the 4 work qubits (index 0 = LSB).
    """
    qc = QuantumCircuit(4, name=f"mult7^{power} mod 15")
    for _ in range(power):
        qc.swap(0, 1)
        qc.swap(1, 2)
        qc.swap(2, 3)
        for q in range(4):
            qc.x(q)
    return qc.to_gate().control(1)


def build_qpe_circuit(n_count: int = 4) -> QuantumCircuit:
    """Phase-estimation circuit for the order of 7 mod 15.

    Layout: qubits 0..n_count-1 are counting qubits, qubits
    n_count..n_count+3 are the work register (qubit n_count = LSB),
    initialized to |0001> = 1. Counting qubit j controls
    U^(2^j) = multiply-by-7^(2^j) mod 15.
    """
    n_work = 4
    qr_count = list(range(n_count))
    qr_work = list(range(n_count, n_count + n_work))
    qc = QuantumCircuit(n_count + n_work, n_count)

    for q in qr_count:
        qc.h(q)
    qc.x(qr_work[0])  # work register = |1>

    for j in qr_count:
        c_u = c_mult7_power(2 ** j)
        qc.append(c_u, [j] + qr_work)

    qft_dag = QFT(num_qubits=n_count, inverse=True, do_swaps=True).to_gate()
    qft_dag.name = "QFT†"
    qc.append(qft_dag, qr_count)

    qc.measure(qr_count, list(range(n_count)))
    return qc


def phase_from_key(key: str) -> Fraction:
    """Convert a counts key to the measured phase as an exact Fraction.

    The inverse QFT here is Qiskit's library QFT with do_swaps=True,
    which leaves the most significant phase bit in the highest-index
    counting qubit — so the key string (highest classical bit leftmost)
    reads directly as phase * 2^n. No bit reversal needed.
    (Verified empirically: the four peaks land exactly on
    0, 1/4, 1/2, 3/4.)
    """
    return Fraction(int(key, 2), 2 ** len(key))


def find_order(a: int, n: int, counts: dict) -> tuple:
    """Recover the order r (a^r = 1 mod n) from QPE measurement counts.

    For each observed phase, in order of frequency: take the continued-
    fraction convergent (via Fraction.limit_denominator), then test the
    denominator and its small multiples until a^r = 1 mod n.
    Returns (r, detail_string).
    """
    n_count = len(next(iter(counts)))
    for key, c in sorted(counts.items(), key=lambda kv: -kv[1]):
        frac = phase_from_key(key).limit_denominator(n)
        r0 = frac.denominator
        if r0 == 0:
            continue
        for mult in range(1, n + 1):
            r = mult * r0
            if pow(a, r, n) == 1:
                return r, (
                    f"phase {key} -> {frac} -> r0={r0}, "
                    f"verified 7^{r} mod 15 = 1 ({c} shots)"
                )
    raise RuntimeError("order not found in measurement data")


def ascii_histogram(counts: dict, shots: int) -> str:
    lines = []
    for outcome in sorted(counts):
        bar = "#" * int(40 * counts[outcome] / shots)
        lines.append(f"  {outcome}  {counts[outcome]:>5}  {bar}")
    return "\n".join(lines)
