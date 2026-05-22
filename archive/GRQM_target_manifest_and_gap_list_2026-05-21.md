# GRQM Target Manifest and Live Gap List (2026-05-21)

## Purpose
Convert the Phase 0 decisions and reconciliation analysis into:
1. an exact proposed target manifest for **T**
2. a comparison against current live working tree **L**
3. a first implementation batch for actual cleanup work

States:
- **L** = current live `repos/GRQM` working tree
- **T** = proposed target canonical state

## Proposed exact target manifest (T)

### Root files / dirs to keep in T
| Item | Status in L | Action |
|---|---|---|
| `README.md` | present | keep |
| `ARCHITECTURE.md` | present | keep |
| `MODEL-VALIDITY.md` | present | keep |
| `LICENSE` | absent | add |
| `.gitignore` | absent | restore |
| `pyproject.toml` | absent | restore |
| `requirements.txt` | absent | restore |
| `requirements-dev.txt` | absent | restore if still maintained |
| `.github/` | absent | restore minimal CI if active public code surface |
| `src/` | present | keep |
| `tests/` | present | keep |
| `docs/` | absent | create |
| `archive/` | present | keep |
| `outputs/` | present | keep, curate |
| `scripts/` | absent | restore selectively |
| `notebooks/` | present | keep only as residual/archive-oriented container if needed |

### `docs/` target set
| Item | Status in L | Proposed source | Action |
|---|---|---|---|
| `docs/CANONICAL_ARTIFACTS.md` | absent | restore from G/M or recreate | restore/create |
| `docs/CLAIM_STATUS_MATRIX.md` | absent | restore from G/M or recreate | restore/create |
| `docs/RESEARCH_ASSUMPTION_REGISTER.md` | absent | restore from G/M if still canonical | restore conditionally |
| `docs/GR_QM_TESTABILITY_BLUEPRINT.md` | absent | restore from G/M | restore |
| `docs/GR_QM_TOY_MODEL_SPEC.md` | absent | restore from G/M | restore |
| `docs/GR_QM_NUMERICS_PROTOCOL.md` | absent | restore from G/M | restore |
| `docs/GR_QM_REPLICATION_REPORT_V1.md` | absent | restore from G/M if still current | restore conditionally |
| `docs/AUDIT-NOTES.md` or `archive/governance/AUDIT-NOTES.md` | currently root file | move current live note after reconciliation | move later |
| `docs/WDW_INTEGRATION_PROTOCOL.md` | absent | restore only if wanted as historical context | optional archive/docs |
| `docs/PROXY_RATIONALE.md` | absent | restore from G | optional useful docs restore |
| `docs/REPRODUCIBILITY_TIERS.md` | absent | restore from G | optional useful docs restore |

### `outputs/` target set
| Item | Status in L | Action |
|---|---|---|
| `outputs/shoulder_causality_20260323T222400Z/` | present | keep as canonical shoulder bundle |
| `outputs/shoulder_causality_20260323T215813Z/` | present | archive as predecessor rerun unless immediate provenance link needed |
| `outputs/bohmian_adaptation_20260319_191614/` | absent in live L | recover/confirm before canonical inclusion |

### `scripts/` target set
| Item | Status in L | Proposed source | Action |
|---|---|---|---|
| `scripts/run_toy_model.py` | absent | G/M | likely restore |
| `scripts/run_schrodinger_newton.py` | absent | G/M | likely restore |
| `scripts/regenerate_golden_run.py` | absent | G/M | optional restore if benchmark preservation matters |

### `archive/` target policy
| Class | Status in L | Action |
|---|---|---|
| `archive/session-notes/2026-03/` | present (39 files) | keep as archive provenance layer |
| dated `GR_QM_*` governance notes | mostly absent from root, partly preserved in archive | keep archived, not root |
| prior reconciliation notes written on 2026-05-21 | present under `archive/` | keep as meta-governance audit trail |

### Keep only in cold archive M
| Class | Action |
|---|---|
| PDF/reference corpus | keep only in M |
| unrelated local workspace dirs | keep only in M |
| redundant old notebook/output clutter with no current claim role | prefer only in M unless specific archive need |

## Immediate live gap list (L vs T)

### Already correct in L
- `README.md`
- `ARCHITECTURE.md`
- `MODEL-VALIDITY.md`
- `src/`
- `tests/`
- `archive/`
- `outputs/` (needs curation, but class exists)

### Missing and should likely be restored/created next
- `LICENSE`
- `.gitignore`
- `pyproject.toml`
- `requirements.txt`
- `docs/`

### Missing but conditional / secondary
- `requirements-dev.txt`
- `.github/`
- `scripts/`
- selected curated docs from G/M
- possible recovered `bohmian_adaptation_20260319_191614/`

### Present but should later move or be reclassified
- root `AUDIT-NOTES.md` -> move to docs/archive after reconciliation
- `outputs/shoulder_causality_20260323T215813Z/` -> likely demote to archival rerun status
- `notebooks/` -> clarify whether residual provenance container remains or is thinned further

## First implementation batch (recommended)

### Batch 1A — root/repro stabilization
1. add `LICENSE`
2. restore `.gitignore`
3. restore `pyproject.toml`
4. restore `requirements.txt`
5. decide whether to restore `requirements-dev.txt`

### Batch 1B — docs scaffold
6. create `docs/`
7. restore the highest-value curated docs first:
   - `CANONICAL_ARTIFACTS.md`
   - `CLAIM_STATUS_MATRIX.md`
   - `GR_QM_TESTABILITY_BLUEPRINT.md`
   - `GR_QM_TOY_MODEL_SPEC.md`
   - `GR_QM_NUMERICS_PROTOCOL.md`
8. defer WDW-specific docs unless needed as historical context

### Batch 1C — outputs posture
9. mark `shoulder_causality_20260323T222400Z/` as canonical
10. mark `shoulder_causality_20260323T215813Z/` as predecessor/archive bundle
11. investigate whether `bohmian_adaptation_20260319_191614/` should be recovered into live T

## Recommended immediate execution order
1. Batch 1A
2. Batch 1B
3. output-bundle labeling/recovery
4. selective scripts restore
5. later CI restore
6. only after that, archive/demotion cleanup

## Success condition for this stage
This stage is complete when the live repo has:
- a stable root/repro surface
- a real curated `docs/` layer
- a named canonical output set
- no ambiguity about which missing items are intentional versus accidental
