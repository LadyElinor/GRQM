# Canonical vs Archival Artifacts

This map separates **canonical public artifacts** from **archival or exploratory outputs** for the reconciled GRQM target state.

## Canonical (source-of-truth / public-facing)

### Orientation / model-boundary docs
- `README.md` — project entrypoint and canonical runtime path.
- `ARCHITECTURE.md` — current code/evidence-layer structure.
- `MODEL-VALIDITY.md` — explicit interpretation boundaries and non-goals.
- `docs/CANONICAL_ARTIFACTS.md` — this artifact map.
- `docs/CLAIM_STATUS_MATRIX.md` — claim state and scope boundaries.
- `docs/GR_QM_TESTABILITY_BLUEPRINT.md` — testability/governance blueprint.
- `docs/GR_QM_TOY_MODEL_SPEC.md` — toy-model contract.
- `docs/GR_QM_NUMERICS_PROTOCOL.md` — numerical protocol.

### Canonical reproducibility surface
- `pyproject.toml`
- `requirements.txt`
- `requirements-dev.txt` (if maintained)
- `requirements-lock.txt`
- `src/`
- `tests/`

### Canonical output bundles
- `outputs/shoulder_causality_20260323T222400Z/` — current canonical shoulder-causality bundle.

## Archival / exploratory (non-canonical unless explicitly promoted)
- `outputs/shoulder_causality_20260323T215813Z/` — predecessor rerun / near-duplicate shoulder bundle retained for provenance.
- timestamped folders under historical `notebooks/outputs/grqm_*`
- one-off diagnostics and probes (edge scans, microbatches, autopsies)
- intermediate receipts produced during exploratory cycles
- WDW/LQC side-lane materials unless explicitly reactivated

## Currently missing / conditional canonical artifact
- `outputs/bohmian_adaptation_20260319_191614/` was identified during reconciliation as a likely canonical bundle candidate, but it is **not currently present in the live working tree** and is **not present in `origin/main`**. Treat it as conditional pending recovery/confirmation from archival sources.

## Reconciliation note (2026-05-21)
Some historical governance artifacts, especially in `docs/CLAIM_STATUS_MATRIX.md`, still reference evidence bundles from the richer predecessor workspace that are not all shipped in the reduced public GRQM tree. That mismatch is currently tracked as an honesty/governance limitation of the reduced public surface rather than silently papered over.

## Promotion rule (archival -> canonical)
An archival artifact becomes canonical only when all are true:
1. Referenced by a governance doc or explicit decision note,
2. Reproducibility path is documented,
3. Claim/status docs point to it explicitly,
4. It still matches the target canonical scientific identity of GRQM.

Absent these conditions, treat it as historical context, not source-of-truth.
