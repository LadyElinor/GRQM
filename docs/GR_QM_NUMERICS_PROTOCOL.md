# GR_QM Numerics Protocol (v1)

Date: 2026-03-01

---

## 1) Solvers and implementation

Language: Python (plain NumPy, no exotic dependencies).  
Equation type: deterministic coupled first-order ODE for \((a,v)\).

Implemented steppers:
- **RK4** (primary production integrator)
- **Euler** (intentionally low-order comparator for divergence stress test)

File:
- `notebooks/grqm_proxy_toymodel_v1.py`

---

## 2) Discretization choices (v1 lock)

- Main step: \(\Delta t_{main}=10^{-3}\)
- Refinement step: \(\Delta t_{ref}=5\times10^{-4}\)
- Exact-reference proxy step: \(\Delta t_{exact}=2.5\times10^{-4}\)
- Alternate replication path step: \(\Delta t_{coarse}=2\times10^{-3}\)

Time window: \([0,3]\)

---

## 3) Convergence / consistency checks

For both baseline and corrected models:
1. Run RK4 at main grid.
2. Run RK4 at refinement grid.
3. Interpolate main-grid trajectory to refinement grid.
4. Compute relative L2 refinement residual
\[
\epsilon_{ref}=\frac{\|a_{main\to ref}-a_{ref}\|_2}{\|a_{ref}\|_2}
\]

Pass threshold (predeclared):
\[
\epsilon_{ref} < 5\times10^{-3}
\]

Observed (v1):
- Baseline: \(2.80\times10^{-7}\)
- Corrected: \(2.76\times10^{-7}\)
- Both pass.
