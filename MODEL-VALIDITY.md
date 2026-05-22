# GRQM Model Validity Notes

This repository contains toy and proxy models. The most important enhancement is to make their validity boundaries explicit.

## Bohmian minisuperspace lane

Files:
- `src/grqm/bohmian_probe/guidance.py`
- `src/grqm/bohmian_probe/symbolic_core.py`

### Interpretable as
- a reduced FRW minisuperspace toy lane
- a bounded Bohmian guidance experiment
- a symbolic receipt scaffold for phase/decomposition sanity checks

### Not interpretable as
- a full Wheeler-DeWitt solver
- a full GR cosmology implementation
- a validated LQC model
- evidence for physical conclusions without additional derivation and falsifier work

### Important explicit assumptions
- `a > 0` domain with floor regularization
- scalar potential approximated locally by `V(phi) = Omega_L + 0.5 m_phi^2 phi^2`
- factor-ordering encoded by a tunable `nu`
- phase decomposition uses a principal-branch argument
- quantum acceleration is bounded relative to classical acceleration by `max_quantum_accel_ratio`

### Audit concern
The floor/reflective guard keeps trajectories numerically contained, but it can also mask physically important failure or boundary-crossing behavior unless reported explicitly.

## Schrödinger-Newton lane

Files:
- `src/grqm/models/schrodinger_newton.py`
- `src/grqm/solvers/pde_splitstep.py`

### Interpretable as
- a 1D toy Schrödinger-Newton probe
- a diagnostic sandbox for free-vs-self-coupled evolution and refinement checks

### Not interpretable as
- a full relativistic gravity-quantum unification model
- a direct empirical prediction engine
- a validated production numerics package

### Important explicit assumptions
- periodic 1D domain for the Poisson solve
- zero-mean gauge fix in Fourier space
- nondimensionalized or toy-unit settings unless otherwise stated
- optional dynamic-vacuum branch is diagnostic, not yet a validated physical sector

### Audit concern
Current refinement logic is more meaningful than interpolation-only checks, but it still needs documented tolerances, invariants, and regime statements before strong interpretation.

## Repository-wide non-goal

GRQM should not currently be described as a solved GR/QM theory project. It is better described as a receipts-first exploratory probe bench for adjacent toy models.
