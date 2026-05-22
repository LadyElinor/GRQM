# GRQM Architecture

## Scope

GRQM is currently a mixed research workspace containing symbolic, dynamical, and archival layers. It is best understood as a receipts-bearing probe bench rather than a unified theory engine.

## Main code lanes

### 1. `src/grqm/bohmian_probe/`
Purpose:
- toy FRW minisuperspace symbolic and numerical experiments
- bounded Bohmian guidance-law probes
- phase-oriented runners for exploratory sweeps

Current notable files:
- `symbolic_core.py`
- `guidance.py`
- `runner_phase1.py`
- `runner_phase2.py`

Key architectural characteristics:
- symbolic and numerical receipts are partially separated
- dynamics include explicit floor/guard logic
- regime semantics are only partly encoded in docs/comments

### 2. `src/grqm/models/`
Purpose:
- higher-level physical model wrappers

Current notable files:
- `schrodinger_newton.py`

Key architectural characteristics:
- computes Q1/Q2/Q3-style diagnostics
- includes free-vs-coupled comparisons
- stores time series directly in result payloads, which is good for auditability

### 3. `src/grqm/solvers/`
Purpose:
- reusable numerical kernels

Current notable files:
- `pde_splitstep.py`

Key architectural characteristics:
- FFT-based periodic Poisson solve
- Strang split-step evolution
- optional dynamic-vacuum diagnostic branch

## Evidence layers

### `notebooks/outputs/`
Run-specific output directories, summaries, manifests, and receipts.

### `outputs/`
Later packaged output bundles, including shoulder-causality artifacts.

### `archive/session-notes/`
Historical narrative / governance / closure notes. These are important provenance artifacts and should not be casually rewritten.

## Current gaps

1. No canonical repo-level maintainer docs were present before this pass.
2. Visible checked-in source tests appear sparse relative to cached pytest artifacts.
3. Model validity boundaries are mostly implicit.
4. Numerical guard behavior is present but not yet centrally documented as an audit concern.
5. The repo needs clearer separation between:
   - toy probe infrastructure
   - symbolic receipts
   - physical interpretation
   - historical archive artifacts

## Recommended next hardening steps

1. add a `MODEL-VALIDITY.md` describing each lane's assumptions, regime, and non-goals
2. add an `AUDIT-NOTES.md` for simulation-risk patterns and known guard behaviors
3. restore or recreate visible source tests to match the observed cached test lineage
4. add simple package entry docs or a lightweight project config if active execution will continue
