# Architecture

## What this is

A working implementation of **Shor's factoring algorithm** for N = 15
in Python/Qiskit: quantum phase estimation of a compiled
modular-multiplication unitary, continued-fraction post-processing,
and the classical gcd step that turns the order into factors.

This is #3 in my quantum series (`quantum-circuits-implementation` was #1,
`bb84-qkd-implementation` was #2) — and the famous one: the algorithm
that broke RSA in theory.

## Layout

```
shor-factoring/
├── README.md
├── requirements.txt           # qiskit + qiskit-aer + numpy
├── run_all.sh
├── scripts/
│   ├── common.py              # compiled multiplier, QPE assembly,
│   │                          # continued fractions, histogram printer
│   ├── 01_shor_15.py          # full Shor pipeline: 15 = 3 x 5
│   └── 02_order_finding.py    # the quantum subroutine, standalone (r = 4)
├── docs/
│   ├── architecture.md        # this file
│   └── interview-answers.md
└── simplified-explanation.md  # plain-language guide (Spanish)
```

## Circuit

```
counting (4):  |+>──■────────■────────■────────■──[QFT†]── measure
                   │        │        │        │
work (4):      |0001>──U^(2^0)──U^(2^1)──U^(2^2)──U^(2^3)
                       ×7      ×7²      ×7⁴      ×7⁸  (mod 15)
```

- 4 counting qubits + 4 work qubits, 8 total. The work register starts
  in |0001⟩ = 1.
- Counting qubit j controls U^(2^j), where U|y⟩ = |7y mod 15⟩.
- The inverse QFT (Qiskit's library QFT, `inverse=True, do_swaps=True`)
  converts the phase kickback into a readable 4-bit phase.
- The custom controlled gates are transpiled to basis gates before
  simulation (Aer cannot run named custom gates directly).

## The compiled multiplier

`c_mult7_power(power)` builds controlled-(×7^power mod 15). One
multiply-by-7 iteration is:

```
swap(0,1); swap(1,2); swap(2,3); X on all four qubits
```

which maps |x⟩ → |7x mod 15⟩ for 1 ≤ x ≤ 14 (verified exhaustively by
statevector simulation). Repeating it `power` times gives ×7^power.
Counting qubit j uses power = 2^j, i.e. U^(2^j). The gate hardcodes
N = 15 and a = 7 — that hardcoding is exactly what "compiled" means
(see interview-answers.md).

## Why the measured phases are s/4

|1⟩ is an equal superposition of the four eigenstates of U, with
eigenvalues e^{2πi·s/4} for s = 0, 1, 2, 3 (the orbit of 1 under ×7 mod
15 is {1, 7, 4, 13}, period 4). Phase estimation therefore returns
0, 1/4, 1/2, 3/4 with ~25% probability each — exactly what the
histogram shows.

## Classical post-processing

For each observed phase (most frequent first):
1. `Fraction(phase).limit_denominator(15)` — the continued-fraction
   convergent, giving a candidate denominator r₀.
2. Test r₀, 2r₀, 3r₀, … until 7^r = 1 mod 15. (The phase-0 peak carries
   no information but its multiples still resolve to r = 4.)
3. With r = 4: x = 7² mod 15 = 4; p = gcd(x−1, 15) = 3,
   q = gcd(x+1, 15) = 5.

All arithmetic uses exact `Fraction`s — no floating-point phase
guessing.

## Design choices

- **Seeded simulator + transpiled circuit**: bit-for-bit reproducible;
  the README numbers regenerate exactly.
- **Exact rational arithmetic** for continued fractions: the phases are
  dyadic rationals, so floats would only add noise.
- **Assertions as the verdict**: script 01 asserts {p, q} == {3, 5};
  script 02 asserts r == 4. The conclusion is a passing check.
- **Honest scope**: no claim beyond N = 15 — see interview-answers.md
  for the RSA-2048 gap.
