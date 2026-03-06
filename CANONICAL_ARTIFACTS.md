# Canonical vs Archival Artifacts

This map separates **governance/canonical artifacts** from **archival or exploratory outputs**.

## Canonical (source-of-truth / governance-facing)

### Status + governance
- `CLAIM_STATUS_MATRIX.md` — canonical claim state and scope boundaries.
- `GR_QM_MONTHLY_GATE_REPORT_01.md` — gate summary used for governance reporting.
- `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.md` (+ `.csv`) — promotion/continuation ledger.

### Model + protocol definitions
- `README.md` — project entrypoint and canonical runtime path.
- `GR_QM_TOY_MODEL_SPEC.md` — toy-model contract.
- `GR_QM_NUMERICS_PROTOCOL.md` — numerical protocol.
- `docs/C-WDW-001_CORRECTION_DERIVATION.md` — public derivation appendix scaffold/path.

### Canonical reproducible run outputs
- `notebooks/outputs/golden_run_20260302/grqm_proxy_results_v1.json`
- `notebooks/outputs/golden_run_20260302/grqm_proxy_results_v1_summary.csv`

## Archival / exploratory (non-canonical unless explicitly promoted)
- Timestamped folders under `notebooks/outputs/grqm_*`
- One-off diagnostics and probes (edge scans, microbatches, autopsies)
- Intermediate receipts produced during exploratory cycles

## Promotion rule (archival -> canonical)
An archival artifact becomes canonical only when all are true:
1. Referenced by a governance doc/decision note,
2. Reproducibility path is documented,
3. Claim matrix or gate report points to it explicitly.

Absent these conditions, treat it as historical context, not source-of-truth.
