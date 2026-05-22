# GRQM Three-State Reconciliation — Pass 2A Root / Repro Surfaces (2026-05-21)

## Scope
This pass reconciles the highest-signal public-shape artifacts first:
- root orientation docs
- root governance docs
- packaging/runtime reproducibility files
- CI / `.github`
- `docs/` and `scripts/` as supporting surface classes

States:
- **L** = local `repos/GRQM` working tree
- **G** = public `origin/main`
- **M** = `Molt\workspace\Physics`
- **T** = proposed target canonical placement

## Root / reproducibility decision table

| Artifact / class | L | G | M | Pass 2 reading | Proposed T |
|---|---|---|---|---|---|
| `README.md` | present, rewritten | present, older | present | L version is the active correction and should replace G public orientation | **Keep at root** |
| `ARCHITECTURE.md` | present | absent at root | absent at root | local-only public architecture layer; useful and probably worth publishing once stabilized | **Keep at root** |
| `MODEL-VALIDITY.md` | present | absent at root | absent at root | valuable boundary-setting surface; aligns with honest public posture | **Keep at root** |
| `AUDIT-NOTES.md` | present | absent at root | absent at root | live governance artifact, useful during reconciliation but probably not permanent root furniture | **Move to `docs/` or `archive/governance/` in T after reconciliation** |
| `LICENSE` | absent | absent | absent | universal gap across all states | **Add at root** |
| `CANONICAL_ARTIFACTS.md` | absent | present | present | important public orientation/control surface if repo remains receipts-bearing | **Restore, but likely in `docs/` with root link unless very compact** |
| `CLAIM_STATUS_MATRIX.md` | absent | present | present | high-value scientific/governance status artifact, but root placement may be too heavy | **Restore in `docs/` or root only if kept concise** |
| `RESEARCH_ASSUMPTION_REGISTER.md` | absent | present | present | strong epistemic artifact, but likely too internal/dense for root | **Restore in `docs/` or archive depending on target identity** |
| `WDW_INTEGRATION_PROTOCOL.md` | absent | present | present | depends heavily on whether WDW framing remains canonical identity | **Restore to `docs/` if scientifically current; otherwise archive** |
| `GR_QM_ACTION_PLAN.md` | absent | present | present | planning artifact, historically useful but not canonical public root material | **Archive, not root** |
| `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.csv` | modified/unsettled | present | present | provenance artifact; machine-readable but not root-facing | **Archive/governance, not root** |
| `GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.md` | modified/unsettled | present | present | provenance artifact; not root-facing | **Archive/governance, not root** |
| `GR_QM_CWDW001_FALSIFICATION_PROTOCOL.md` | absent | present | present | could matter scientifically, but should live in docs/archive not root | **Docs or archive** |
| `GR_QM_CYCLE3_CLOSE_NOTE.md` | absent | present | present | dated cycle note | **Archive** |
| `GR_QM_CYCLE3_PLAN.md` | absent | present | present | dated planning note | **Archive** |
| `GR_QM_CYCLE_JOURNAL.md` | absent | present | present | long historical journal, not public root | **Archive** |
| `GR_QM_EDGE305_ACCEPTANCE_CRITERIA_PREREGISTER.md` | absent | present | present | provenance-bearing preregister, not root | **Archive** |
| `GR_QM_EXECUTION_LOG_8H.md` | absent | present | present | execution log, not root | **Archive** |
| `GR_QM_MONTHLY_GATE_REPORT_01*.md` | absent | present | present | dated governance report, not root | **Archive** |
| `GR_QM_NULL_TEST_LOG.md` | absent | present | present | technical provenance artifact | **Docs or archive** |
| `GR_QM_NUMERICS_PROTOCOL.md` | absent | present | present | protocol may still matter, but not as root clutter | **Docs** |
| `GR_QM_QUESTIONS_Q1.md` | absent | present | present | exploratory question file | **Archive** |
| `GR_QM_REPLICATION_REPORT_V1.md` | absent | present | present | potentially important, but better in docs/archive | **Docs if still current, else archive** |
| `GR_QM_TESTABILITY_BLUEPRINT.md` | absent | present | present | strong public-scientific surface, but likely docs not root | **Docs** |
| `GR_QM_TOY_MODEL_SPEC.md` | absent | present | present | important if toy-model framing remains canonical | **Docs** |
| `GR_QM_UNCERTAINTY_BUDGET_V1.md` | absent | present | present | governance/scientific rigor artifact | **Docs or archive** |
| `Q1_Q2_GATE_UPDATE.md` | absent | present | present | dated update note | **Archive** |
| `.github/workflows/ci.yml` | absent | present | present | current L reduction dropped CI entirely; public repo probably should retain a minimal CI path | **Restore minimal CI in T** |
| `.gitignore` | absent | present | present | basic repo hygiene surface removed locally | **Restore at root** |
| `pyproject.toml` | absent | present | present | key reproducibility surface | **Restore at root** |
| `requirements.txt` | absent | present | present | key reproducibility surface | **Restore at root** |
| `requirements-dev.txt` | absent | present | present | useful if tests/CI remain | **Restore at root or simplify** |
| `requirements-lock.txt` | absent | present | present | evaluate whether it is still maintained; if not, omit rather than cargo-cult | **Restore only if curated** |
| `docs/` class | absent as active L layer | present | present | T likely needs a small curated docs layer to carry non-root scientific/governance context | **Restore curated `docs/`** |
| `scripts/` class | absent in L | present | present | T should probably retain only canonical runnable helpers | **Restore selectively** |

## Strongest Pass 2A calls

### Root in T should likely contain only a compact set
Probable root set:
- `README.md`
- `LICENSE`
- `ARCHITECTURE.md`
- `MODEL-VALIDITY.md`
- `.gitignore`
- `pyproject.toml`
- `requirements.txt` (and maybe dev requirements)
- `src/`
- `tests/`
- curated `docs/`
- `archive/`
- possibly `scripts/`

### Root items from G that should probably **not** return to root
Most `GR_QM_*` dated notes, ledgers, gate reports, action plans, and journals.

### Root items from G that probably **should** survive somewhere in T
- `CANONICAL_ARTIFACTS.md`
- `CLAIM_STATUS_MATRIX.md`
- `RESEARCH_ASSUMPTION_REGISTER.md`
- `GR_QM_TESTABILITY_BLUEPRINT.md`
- `GR_QM_TOY_MODEL_SPEC.md`
- maybe `WDW_INTEGRATION_PROTOCOL.md`, depending on identity decision

These look more like `docs/` residents than root residents.

## Main unresolved identity-sensitive items
1. Is `CLAIM_STATUS_MATRIX.md` public-facing and current enough to restore prominently?
2. Does WDW remain part of canonical scientific identity, or is it historical framing?
3. Is the toy-model / testability framing central enough to elevate into curated docs?
4. Which reproducibility files are still maintained versus stale cargo carried from G/M?

## Recommended next move
Proceed to Pass 2B by grouping:
- notebook families
- output bundles
- archive note families

Do that by family/bundle, not by individual file.
