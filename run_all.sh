#!/usr/bin/env bash
# Runs every implementation in the project, in order.
set -euo pipefail
cd "$(dirname "$0")"

# Prefer the project's venv (where qiskit lives); fall back to python3.
if [ -x ".venv/bin/python" ]; then
  PY=".venv/bin/python"
else
  PY="python3"
fi

echo "=== 01 — Shor's factoring of N=15 ==="
$PY scripts/01_shor_15.py
echo
echo "=== 02 — Order finding (the quantum heart of Shor) ==="
$PY scripts/02_order_finding.py
echo
echo "All implementations completed successfully."
