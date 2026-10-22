# shor-factoring

A complete implementation of **Shor's factoring algorithm** for N = 15,
built with Qiskit: quantum phase estimation of a compiled
modular-multiplication unitary, continued-fraction post-processing of
the measured phases, and the classical gcd step that turns the order
into factors.

This is #20 in my portfolio and #6 in my quantum series (`quantum-circuits-implementation` was #1,
`bb84-qkd-implementation` was #2) — and the famous one: the algorithm
that broke RSA in theory. I love molecular engineering, and above all
QUANTUM.

## The two implementations

| # | Script | What it demonstrates |
|---|--------|----------------------|
| 1 | `01_shor_15.py` | **Full Shor pipeline** — 15 = 3 × 5, end to end |
| 2 | `02_order_finding.py` | **Order finding, standalone** — the quantum heart: r = 4 |

## Architecture

```
counting (4):  |+>──■────────■────────■────────■──[QFT†]── measure
                   │        │        │        │
work (4):      |0001>──U^(2^0)──U^(2^1)──U^(2^2)──U^(2^3)
                       ×7      ×7²      ×7⁴      ×7⁸  (mod 15)
```

The multiply-by-7-mod-15 gate is a compiled swap+X construction
(hardcoded for N = 15, a = 7 — that hardcoding is what "compiled"
means). Phase estimation returns the phases s/4; continued fractions
recover the order r = 4; gcds give the factors. See [docs/architecture.md](docs/architecture.md) for the honest
story on why this doesn't factor RSA-2048.

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

bash run_all.sh
```

## Validation

Measured on Qiskit Aer 2.6.0 (seeded simulator, 2048 shots), 2026-10-21:

| Implementation | Prediction | Measured |
|----------------|-----------|----------|
| Shor N=15 | phases 0, 1/4, 1/2, 3/4 (~25% each); factors {3, 5} | `0000`: 478, `0100`: 520, `1000`: 526, `1100`: 524 — order r = 4 (phase `1000` → 1/2 → r₀=2 → verified 7⁴ mod 15 = 1); 7² mod 15 = 4; p = gcd(3, 15) = **3**, q = gcd(5, 15) = **5** — assertion passed |
| Order finding | r = 4 | r = **4**, verified 7⁴ mod 15 = 1, matching brute force (7, 4, 13, 1) — assertion passed |

## Why this matters (the one-paragraph version)

RSA rests on factoring being hard; Shor factors in polynomial time on
a quantum computer. This implementation proves the *algorithm* works —
the order-finding subroutine genuinely extracts r = 4 from quantum
phases. Everything between 15 and RSA-2048 (estimates: ~20M physical
qubits with error correction) is hardware engineering, not algorithm
design — and that gap is what quantum engineering exists to close.

## Plain-language guide

[simplified-explanation.md](simplified-explanation.md) — Shor's
algorithm without scary math: the famous lock, the rhythm trick, and
the honest gap to RSA-2048 (Spanish).
