# GRQM Keep / Restore / Archive Matrix — First Pass (2026-05-21)

## Purpose
First-pass matrix to resolve the post-reduction identity of GRQM using three buckets:
- **Public-facing**: belongs in the repo’s visible canonical surface
- **Archived in repo**: provenance preserved in-repo but not in the main navigation surface
- **Out of repo / local-only**: useful local working material that need not ship in the canonical repo

This pass is evidence-grounded but provisional.

## High-level observations
- `repos/GRQM` root is currently sparse and maintainer-facing, not root-cluttered.
- `Molt\workspace\Physics` remains the richer reference workspace.
- The live repo working tree is dirty, so this matrix should be treated as a decision aid before cleanup/publish work.

## First-pass bucket proposals

### Public-facing (keep or restore into canonical repo surface)
Core navigation / trust surfaces:
- `README.md`
- `LICENSE` (**missing, should be added**)
- `ARCHITECTURE.md`
- `MODEL-VALIDITY.md`
- `AUDIT-NOTES.md`
- `CLAIM_STATUS_MATRIX.md` (**restore or recreate; present in richer tree, absent in live repo root**)
- `CANONICAL_ARTIFACTS.md` (**restore or recreate; present in richer tree, absent in live repo root**)
- `RESEARCH_ASSUMPTION_REGISTER.md` (if the governance/epistemic layer remains part of the canonical identity)
- `WDW_INTEGRATION_PROTOCOL.md` (if FRW/WDW-lane interpretation remains canonical rather than purely archival)
- `docs/ORIENTATION.md` (**missing, recommended if repo is meant for outside readers**)

Core executable / scientific surfaces:
- `src/grqm/`
- `tests/`
- `pyproject.toml`
- `requirements*.txt`

Selective output bundles worth public retention if they define the current scientific claim:
- `outputs/bohmian_adaptation_20260319_191614/`
- `outputs/shoulder_causality_20260323T215813Z/`
- `outputs/shoulder_causality_20260323T222400Z/`

### Archived in repo
Historical governance/provenance surfaces that matter but should not dominate navigation:
- `archive/session-notes/2026-03/` (39 notes currently visible in live repo archive)
- dated `GR_QM_*` cycle notes and closure notes
- preregisters, snapshots, and monthly gate reports
- older notebooks/output runs that are provenance-bearing but not canonical public entrypoints
- `docs/METHODS_NOTE_DRAFT_2026-03-23.md`
- `docs/METHODS_NOTE_ONEPAGER_2026-03-23.md`
- `docs/PROXY_RATIONALE.md`
- `docs/REPRODUCIBILITY_TIERS.md`
- `docs/CURRENT_TRUTH_2026-03.md`
- `docs/C-WDW-001_CORRECTION_DERIVATION.md`

### Out of repo / local-only candidates
These should be scrutinized for exclusion from the canonical public repo unless explicitly required:
- broad background PDF library in `Molt\workspace\Physics`
- unrelated course/reference material
- exploratory scratch notes like `critique.txt`, `roadmap.txt`, `SWhite.txt`, temporary scripts
- heavyweight local corpus directories unrelated to GRQM’s direct public evidence surface
- any notebook or output that is purely intermediate and not part of the final provenance story

## Immediate unresolved decisions
1. Is `RESEARCH_ASSUMPTION_REGISTER.md` canonical public governance, or archive-only?
2. Is `WDW_INTEGRATION_PROTOCOL.md` part of the active scientific identity, or should it move to archive?
3. Should `docs/` be restored as a public-facing directory, or should the trimmed repo stay almost root-only?
4. Which outputs are canonical evidence bundles vs excess historical residue?

## Recommended next move
Resolve the **canonical scientific identity of GRQM post-reduction** first, then turn this first-pass matrix into a file-by-file action list.
