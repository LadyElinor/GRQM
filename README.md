# GRQM

GRQM is a receipts-first research workspace for toy general-relativity / quantum-mechanics-adjacent probes, currently centered on:

- Bohmian minisuperspace proxy experiments in `src/grqm/bohmian_probe/`
- 1D Schrödinger-Newton toy experiments in `src/grqm/models/` and `src/grqm/solvers/`
- archived run artifacts and notes under `notebooks/outputs/`, `outputs/`, and `archive/session-notes/`

## Current posture

This repository should be treated as an exploratory research sandbox, not a validated physical theory implementation.

The codebase contains useful probes and receipts, but several model-validity and simulation-audit boundaries should be made explicit:

- toy models are not interchangeable with full GR, Wheeler-DeWitt, LQC, or quantum-gravity claims
- dimensional conventions are largely implicit and often effectively nondimensionalized
- some guardrails prioritize numerical containment over physically transparent failure
- generated outputs and archived notes are substantial parts of the evidence trail

## Structure

- `src/grqm/bohmian_probe/`
  - symbolic minisuperspace receipts
  - Bohmian guidance toy dynamics
  - phase runners
- `src/grqm/models/`
  - Schrödinger-Newton toy model wrappers
- `src/grqm/solvers/`
  - numerical solver implementations
- `tests/`
  - currently sparse as checked-in source; cached pytest artifacts exist
- `notebooks/outputs/`, `outputs/`
  - run products and receipts
- `archive/session-notes/`
  - historical research notes and decision artifacts

## Recommended operating discipline

Use the operator-family standards when extending this repo:

- `physics-operator`: state regime, units, and validity boundaries before interpretation
- `math-operator`: keep symbolic claims receipt-backed
- `programming-operator`: make the smallest safe code changes and verify them
- `simulation-audit-operator`: treat diagnostics, clipping, convergence, and invariants as first-class audit targets

## Immediate enhancement targets

1. restore visible source tests and entrypoint documentation
2. document model assumptions and non-goals for each toy lane
3. add explicit audit notes for floor/guard behavior and validity boundaries
4. separate research claims from probe capabilities in maintainer docs

## Status

This README was created to give the repo a canonical maintainer-facing entrypoint before deeper physics or code changes.
