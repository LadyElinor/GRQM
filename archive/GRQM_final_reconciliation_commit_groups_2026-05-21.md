# GRQM Final Reconciliation Pass — Commit Groupings (2026-05-21)

## Purpose
Convert the current transitional working tree into explicit, intentional commit groupings.

This is a packaging artifact, not a push action. It defines how the current reconciled GRQM state should be staged and explained.

## Current interpretation
The live working tree still appears extremely noisy in `git status`, but most of that noise comes from comparing:
- an older richer tracked public shape in `origin/main`
against
- a newer reduced local canonical shape built around root docs, curated docs, minimal reproducibility surfaces, code/tests, and a narrow outputs layer.

The meaningful new canonical surface is now compact enough to package deliberately.

## Proposed commit groupings

### Commit 1 — root/repro/license stabilization
**Intent:** establish a valid public root and reproducibility surface.

#### Include
- `README.md`
- `ARCHITECTURE.md`
- `MODEL-VALIDITY.md`
- `.gitignore`
- `pyproject.toml`
- `requirements.txt`
- `requirements-dev.txt`
- `LICENSE`

#### Commit message shape
`stabilize root surface, packaging, and license`

#### Notes
- This commit establishes the new public repo posture.
- It intentionally does **not** restore old root sprawl.

---

### Commit 2 — curated docs layer
**Intent:** move scientific/governance orientation out of root and into a curated docs surface.

#### Include
- `docs/CANONICAL_ARTIFACTS.md`
- `docs/CLAIM_STATUS_MATRIX.md`
- `docs/GR_QM_TESTABILITY_BLUEPRINT.md`
- `docs/GR_QM_TOY_MODEL_SPEC.md`
- `docs/GR_QM_NUMERICS_PROTOCOL.md`

#### Possibly include later, not required for this commit
- `docs/PROXY_RATIONALE.md`
- `docs/REPRODUCIBILITY_TIERS.md`
- `docs/WDW_INTEGRATION_PROTOCOL.md` (historical context only if wanted)
- future relocation target for `AUDIT-NOTES.md`

#### Commit message shape
`restore curated docs layer for canonical scientific surfaces`

#### Notes
- This commit makes the repo legible without restoring old root clutter.
- It reflects the chosen toy-probe identity rather than the older provenance-heavy repo shape.

---

### Commit 3 — scripts and CI minimal surface
**Intent:** restore the smallest runnable helper/CI layer that still fits the current repo identity.

#### Include
- `scripts/run_toy_model.py`
- `scripts/run_schrodinger_newton.py`
- `.github/workflows/ci.yml`

#### Explicitly exclude
- `scripts/regenerate_golden_run.py`
- `scripts/run_shoulder_causality_packet.py`

#### Commit message shape
`restore minimal scripts and CI for active code surface`

#### Notes
- Excluded scripts point back toward the older notebook-era or workflow-heavy repo shape and are not required for the current canonical surface.

---

### Commit 4 — output posture and reconciliation governance notes
**Intent:** encode the selected canonical-vs-archival output posture and preserve the reconciliation audit trail.

#### Include
- `outputs/shoulder_causality_20260323T222400Z/`
- `outputs/shoulder_causality_20260323T215813Z/` (if retained in-repo as predecessor/archive provenance)
- `docs/CANONICAL_ARTIFACTS.md` (if final edits land after commit 2, otherwise leave in commit 2)
- reconciliation artifacts under `archive/`:
  - `GRQM_keep_restore_archive_matrix_first_pass_2026-05-21.md`
  - `GRQM_three_state_reconciliation_pass1_2026-05-21.md`
  - `GRQM_three_state_reconciliation_pass2_root_and_repro_2026-05-21.md`
  - `GRQM_three_state_reconciliation_pass2B_bundles_2026-05-21.md`
  - `GRQM_reconciliation_action_plan_2026-05-21.md`
  - `GRQM_phase0_decisions_2026-05-21.md`
  - `GRQM_target_manifest_and_gap_list_2026-05-21.md`
  - this file

#### Conditional include
- `outputs/bohmian_adaptation_20260319_191614/` only if actually recovered into the live tree

#### Commit message shape
`document canonical output posture and preserve reconciliation audit trail`

#### Notes
- If you want to keep the public repo cleaner, the reconciliation audit notes could also be squashed into one summarized archive note instead of shipping every intermediate analysis artifact.
- But as governance receipts, their presence in `archive/` is defensible.

---

## What should NOT be restored or staged as part of the canonical reconciliation

### Do not restore to root
- `CANONICAL_ARTIFACTS.md` (root old location)
- `CLAIM_STATUS_MATRIX.md` (root old location)
- `GR_QM_*` dated action plans, gate reports, cycle notes, journals
- `RESEARCH_ASSUMPTION_REGISTER.md` unless you later explicitly decide it belongs in curated docs
- `WDW_INTEGRATION_PROTOCOL.md` unless added as historical docs context

### Do not restore wholesale
- notebook-era exploratory scripts/notebooks
- historical `notebooks/outputs/grqm_*` bundle sprawl
- broad WDW/LQC exploratory lane artifacts as canonical public surface
- PDF/reference corpus from M

## Recommended staging order
1. stage Commit 1 files
2. stage Commit 2 files
3. stage Commit 3 files
4. stage Commit 4 files
5. only after those are secured, review whether any additional archive-demotion deletes should be committed in a later cleanup commit

## Suggested follow-on cleanup commit (optional)
After the four main commits, a fifth cleanup commit could:
- relocate `AUDIT-NOTES.md` out of root
- add optional historical docs (`PROXY_RATIONALE.md`, `REPRODUCIBILITY_TIERS.md`)
- add `WDW_INTEGRATION_PROTOCOL.md` only as historical context if desired
- explicitly prune any remaining accidental files from the new canonical surface

## Ready-to-stage file groups (concise)

### Group 1
`README.md`, `ARCHITECTURE.md`, `MODEL-VALIDITY.md`, `.gitignore`, `pyproject.toml`, `requirements.txt`, `requirements-dev.txt`, `LICENSE`

### Group 2
`docs/CANONICAL_ARTIFACTS.md`, `docs/CLAIM_STATUS_MATRIX.md`, `docs/GR_QM_TESTABILITY_BLUEPRINT.md`, `docs/GR_QM_TOY_MODEL_SPEC.md`, `docs/GR_QM_NUMERICS_PROTOCOL.md`

### Group 3
`scripts/run_toy_model.py`, `scripts/run_schrodinger_newton.py`, `.github/workflows/ci.yml`

### Group 4
`outputs/shoulder_causality_20260323T222400Z/`, `outputs/shoulder_causality_20260323T215813Z/` (if retained), selected `archive/GRQM_*2026-05-21.md` reconciliation artifacts

## Final note
The repo is now at the point where the main remaining work is **staging discipline and commit hygiene**, not architectural uncertainty.
