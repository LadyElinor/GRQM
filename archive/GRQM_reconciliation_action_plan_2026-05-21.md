# GRQM Reconciliation Action Plan (2026-05-21)

## Purpose
Translate the three-state reconciliation analysis into an execution-ready cleanup plan.

States:
- **L** = local `repos/GRQM` working tree
- **G** = public `origin/main`
- **M** = `Molt\workspace\Physics`
- **T** = target canonical GRQM state to converge toward

This plan assumes the strongest current reading from Pass 1 and Pass 2:
- T should be neither current G nor current L exactly
- T should be a **hybrid**: small public root, curated docs/archive, restored minimal reproducibility surfaces, selected canonical evidence bundles, and cold-archive separation for the rest

## Target shape (proposed)

### Root of T
Keep or add:
- `README.md`
- `LICENSE`
- `ARCHITECTURE.md`
- `MODEL-VALIDITY.md`
- `.gitignore`
- `pyproject.toml`
- `requirements.txt`
- optionally `requirements-dev.txt`
- `src/`
- `tests/`
- `docs/`
- `archive/`
- optionally `scripts/`

Do not restore root sprawl from G.
In particular, most dated `GR_QM_*` governance files should **not** return to root.

### Curated `docs/` in T
Likely residents:
- `CANONICAL_ARTIFACTS.md`
- `CLAIM_STATUS_MATRIX.md`
- `RESEARCH_ASSUMPTION_REGISTER.md` (if still part of canonical posture)
- `GR_QM_TESTABILITY_BLUEPRINT.md`
- `GR_QM_TOY_MODEL_SPEC.md`
- `GR_QM_NUMERICS_PROTOCOL.md`
- `GR_QM_REPLICATION_REPORT_V1.md` (if still current)
- `WDW_INTEGRATION_PROTOCOL.md` only if WDW remains active scientific identity
- `AUDIT-NOTES.md` only during reconciliation, then possibly move to `archive/governance/`

### `archive/` in T
Keep as secondary provenance layer:
- `archive/session-notes/2026-03/`
- ledger / prereg / cycle / gate / execution notes
- dated historical governance material
- most notebook-era output families if preserved in-repo at all

### `outputs/` in T
Keep only canonical evidence bundles:
- `outputs/bohmian_adaptation_20260319_191614/`
- `outputs/shoulder_causality_20260323T215813Z/`
- `outputs/shoulder_causality_20260323T222400Z/` pending redundancy decision

### Leave outside T
Keep in M or other cold archive only:
- broad PDF/reference corpus
- unrelated local workspace directories
- historical sweep clutter not needed for public canonical repo
- exploratory side-lane material with no current claim relevance

## Execution sequence

### Phase 0 — decision gates (must be explicit)
Before physical cleanup, decide and record:
1. **Canonical identity gate**
   - Is GRQM a public research sandbox with bounded receipts?
   - Or a fuller provenance repository?
2. **M role gate**
   - Is `Molt\workspace\Physics` the cold archive of record?
3. **WDW/LQC gate**
   - Are WDW/LQC lanes still canonical scientific identity or historical exploratory lanes?
4. **Evidence-bundle gate**
   - Are both shoulder-causality bundles canonical, or is one a superseding rerun?

Without these gates, cleanup risks baking in ambiguity.

### Phase 1 — stabilize public root and reproducibility surfaces
Actions:
1. keep current rewritten `README.md`
2. add `LICENSE`
3. restore `.gitignore`
4. restore `pyproject.toml`
5. restore `requirements.txt`
6. decide whether `requirements-dev.txt` is still maintained; restore only if real
7. decide whether `requirements-lock.txt` is maintained; restore only if curated
8. restore minimal CI (`.github/workflows/ci.yml`) if repo remains an actively public code surface

Rationale:
This repairs the repo’s basic trust/reproducibility posture without reintroducing root clutter.

### Phase 2 — establish curated docs layer
Actions:
1. create or restore `docs/`
2. move or recreate high-value scientific/governance surfaces there:
   - `CANONICAL_ARTIFACTS.md`
   - `CLAIM_STATUS_MATRIX.md`
   - `RESEARCH_ASSUMPTION_REGISTER.md` if still canonical
   - `GR_QM_TESTABILITY_BLUEPRINT.md`
   - `GR_QM_TOY_MODEL_SPEC.md`
   - `GR_QM_NUMERICS_PROTOCOL.md`
   - `GR_QM_REPLICATION_REPORT_V1.md` if current
3. place `WDW_INTEGRATION_PROTOCOL.md` in docs only if identity gate keeps WDW active
4. keep `AUDIT-NOTES.md` visible during reconciliation, then relocate to `docs/` or `archive/governance/`

Rationale:
This preserves important scientific/governance structure while preventing root sprawl.

### Phase 3 — formalize canonical output bundles
Actions:
1. confirm `outputs/bohmian_adaptation_20260319_191614/` as canonical or not
2. compare the two shoulder-causality bundles and decide:
   - both retained
   - older retained + newer as rerun
   - newer supersedes older
3. ensure canonical output bundles are referenced from README/docs
4. demote older notebook-era output families to archive or remove from T

Rationale:
Outputs now appear to be part of GRQM’s public truth surface, so they need explicit curation.

### Phase 4 — resolve notebooks by policy, not file churn
Actions:
1. do **not** wholesale restore historical runnable notebooks from G/M
2. choose one of two notebook policies:
   - **code-first policy:** keep no active notebooks except preserved provenance outputs
   - **exemplar policy:** retain only a tiny number of notebooks that regenerate canonical bundles
3. archive or exclude old families:
   - `grqm_batch_*`
   - `grqm_batch_tiered_*`
   - `grqm_q2_*`
   - `grqm_delta_autopsy_*`
   - `grqm_cycle*`
   - `grqm_a001*`
   - `grqm_a002*`
   - `grqm_boo*`
   - most `grqm_edge*`
   - most `wdw*`, `lqc*`, `nonlinear*` unless identity gates restore them

Rationale:
The local reduction already implies a move away from notebook-first canonical structure.

### Phase 5 — demote historical governance material
Actions:
1. move root-level dated `GR_QM_*` governance docs out of target root
2. preserve them in `archive/` if they still matter as provenance
3. leave low-value or duplicative historical materials only in cold archive M when in-repo preservation is unnecessary
4. keep archive orientation surfaces like `archive/session-notes/README.md`

Rationale:
This resolves the main public-facing divergence without destroying provenance.

### Phase 6 — publish/reconcile state layers
Actions:
1. clean working tree into intentional staged changes
2. separate commits by purpose:
   - root/repro restoration
   - docs reorganization
   - output curation
   - archival demotion
3. push only after T is explicit enough that G no longer silently misrepresents project posture
4. update public README/docs to explain archive posture and model-validity boundaries clearly

Rationale:
The governance debt is not just local mess; it is silent divergence between public and local project identity.

## Explicit move list by class

### Keep at root
- `README.md`
- `ARCHITECTURE.md`
- `MODEL-VALIDITY.md`
- `LICENSE` (new)
- `.gitignore` (restore)
- `pyproject.toml` (restore)
- `requirements.txt` (restore)
- optionally `requirements-dev.txt`

### Move to `docs/`
- `CANONICAL_ARTIFACTS.md`
- `CLAIM_STATUS_MATRIX.md`
- `RESEARCH_ASSUMPTION_REGISTER.md` if canonical
- `GR_QM_TESTABILITY_BLUEPRINT.md`
- `GR_QM_TOY_MODEL_SPEC.md`
- `GR_QM_NUMERICS_PROTOCOL.md`
- `GR_QM_REPLICATION_REPORT_V1.md` if current
- `WDW_INTEGRATION_PROTOCOL.md` if current
- `AUDIT-NOTES.md` after reconciliation

### Move to `archive/`
- `GR_QM_ACTION_PLAN.md`
- `GR_QM_CYCLE3_CLOSE_NOTE.md`
- `GR_QM_CYCLE3_PLAN.md`
- `GR_QM_CYCLE_JOURNAL.md`
- `GR_QM_EDGE305_ACCEPTANCE_CRITERIA_PREREGISTER.md`
- `GR_QM_EXECUTION_LOG_8H.md`
- `GR_QM_MONTHLY_GATE_REPORT_01.md`
- `GR_QM_MONTHLY_GATE_REPORT_01_DRAFT.md`
- `Q1_Q2_GATE_UPDATE.md`
- promotion ledgers
- most archive/session note families
- most notebook-era output bundles if kept in-repo at all

### Leave only in cold archive M unless specifically needed
- PDF/reference corpus
- unrelated course/library materials
- exploratory scratch files
- redundant notebook/output clutter with no current claim role

## Recommended immediate next actions
1. Record explicit decisions for the four Phase 0 gates.
2. Build the exact target root/docs manifest.
3. Compare shoulder-causality bundles for redundancy/supersession.
4. Restore minimal reproducibility files into the working tree.
5. Begin docs relocation before any broad deletion/push.

## Success condition
Reconciliation is complete when:
- G no longer presents the old provenance-heavy root as the public identity
- L is no longer an over-trimmed dirty working tree
- T is explicit, reproducible, and understandable to outsiders
- M has a named role rather than acting as an accidental shadow archive
