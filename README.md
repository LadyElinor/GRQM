# GRQM (Governance-First Toy Proxy)

A scoped computational-physics workflow for testing **process reliability** and a narrow **WDW-inspired toy correction signal**.

Canonical status source: `CLAIM_STATUS_MATRIX.md`.

## Minimal mental model
- This repo is a **methodology + toy-model** stack.
- We run a tiny FRW-inspired ODE with/without a correction term.
- We treat outputs as **in-core evidence only** (not broad physical confirmation).
- Governance files track what is OPEN/PROVEN/BLOCKED and why.

## 60-second quickstart
```bash
cd Physics
python -m pip install -e .[dev]
python scripts/run_toy_model.py --out-dir outputs
pytest
```

Expected artifacts:
- `outputs/grqm_proxy_results_v1.json`
- `outputs/grqm_proxy_results_v1_summary.csv`

## Architecture sketch
```text
src/grqm/core.py
  ├─ integrate() + accel() + metrics
  └─ run_cycle()
       ├─ symbolic receipt call (src/grqm/symbolic.py)
       ├─ writes canonical JSON + summary CSV
       └─ returned dict consumed by tests/scripts

scripts/run_toy_model.py
  └─ thin CLI wrapper around run_cycle()

tests/
  ├─ toy-model invariants (refinement, signal persistence, determinism)
  └─ symbolic scaling checks

notebooks/
  └─ diagnostic/governance support scripts (non-canonical unless promoted)
```

## Canonical JSON example
From `grqm_proxy_results_v1.json`:

```json
{
  "metadata": {
    "seed": 42,
    "model": "FRW-inspired minisuperspace toy ODE",
    "params": {"omega_m": 0.3, "omega_l": 0.7, "alpha_qg": 1e-7},
    "symbolic_validation": {"derivation_ok": true}
  },
  "q1": {
    "delta_proxy_l2": 0.001,
    "baseline_refinement_error": 0.000001,
    "corrected_refinement_error": 0.000001
  },
  "q2": {
    "D_star": 0.002,
    "replication_rel_diff": 0.01
  }
}
```

(Values above are schema-shaped examples; run locally for exact values.)

## Artifact map + reproducibility
- Canonical vs archival map: `CANONICAL_ARTIFACTS.md`
- Dependency/repro tiers: `docs/REPRODUCIBILITY_TIERS.md`
- Strict lockfile path (for governed reruns): `requirements-lock.txt`

## Repository layout
- `src/grqm/` — core model, symbolic receipts, package CLI
- `scripts/` — stable entrypoints
- `tests/` — automated smoke/invariant tests
- `notebooks/` — exploratory + diagnostic scripts
- `docs/` — rationale, derivation, and reproducibility guidance
