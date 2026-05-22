# GRQM Phase 0 Decisions (2026-05-21)

## Purpose
Record the four explicit decision gates required before reconciliation cleanup.

These are evidence-grounded provisional decisions derived from the current live repo state, public `origin/main`, the richer `Molt\workspace\Physics` workspace, and the surviving output bundles.

## 1. Canonical identity of GRQM
**Decision:** GRQM should be treated canonically as a **receipts-first exploratory toy-probe research sandbox**, not as a full provenance monorepo and not as a validated GR/QM theory implementation.

### Why
- `README.md` describes GRQM as a receipts-first exploratory workspace centered on toy Bohmian minisuperspace and 1D Schrödinger-Newton lanes.
- `ARCHITECTURE.md` frames the repo as a "receipts-bearing probe bench rather than a unified theory engine."
- `MODEL-VALIDITY.md` explicitly says the repo should not be described as a solved GR/QM theory project.
- The local reduction pattern strongly favors a smaller public root, selected evidence bundles, and supporting code/docs over full notebook-era provenance sprawl.

### Practical implication for T
T should be:
- code-first
- docs-supported
- evidence-bundle-based
- archive-backed

It should **not** attempt to expose the entire historical research workspace as its public identity.

## 2. Role of `Molt\workspace\Physics`
**Decision:** `Molt\workspace\Physics` should be treated as the **cold archive of record** for the richer predecessor workspace and reference corpus.

### Why
- M contains the broader provenance layer, older governance surfaces, notebook history, scripts, docs, and large reference-PDF corpus.
- M is not shaped like a clean public repo and contains substantial material clearly outside the canonical public GRQM surface.
- Current L and proposed T make more sense as a reduced canonical repo derived from a richer predecessor/archive layer than as the full internal scientific workspace itself.

### Practical implication for T
- T does not need to preserve all of M in-repo.
- M should be retained deliberately as a cold archive rather than left as an accidental shadow workspace.

## 3. Whether WDW/LQC remain canonical
**Decision:** WDW and LQC should be treated as **non-canonical historical / exploratory lanes** unless future work explicitly reactivates them.

### Why
- `MODEL-VALIDITY.md` explicitly states the Bohmian minisuperspace lane is **not** interpretable as a full Wheeler-DeWitt solver or a validated LQC model.
- Current L has already removed the visible WDW/LQC notebook-era surfaces from the live canonical shape.
- Pass 2 bundle classification shows WDW/LQC artifacts living mainly in older G/M exploratory families rather than in the newer canonical-looking live outputs.
- The current center of gravity is Bohmian minisuperspace proxy work plus the Schrödinger-Newton toy lane, with boundary-heavy validity language.

### Practical implication for T
- `WDW_INTEGRATION_PROTOCOL.md` should move to docs only if retained as historical context, otherwise archive.
- WDW/LQC notebook and output families should remain archived, not canonical.

## 4. Shoulder-causality bundle decision
**Decision:** The two shoulder-causality bundles should **not** both be treated as independent canonical artifacts. The later bundle appears to be a near-duplicate rerun / superseding pass.

### Evidence
- Live root `outputs/` currently contains:
  - `shoulder_causality_20260323T215813Z`
  - `shoulder_causality_20260323T222400Z`
- A direct directory diff showed only a tiny change:
  - one-file difference in `phase2_raw/summary.json`
- `phase2_raw/summary.md` in both bundles is textually identical at the current read surface.
- `decision.json` in both bundles is textually identical:
  - recommendation = `HOLD_FOUNDATION`
  - same failed gates
  - same caveats

### Provisional call
- Treat `shoulder_causality_20260323T222400Z` as the likely **superseding rerun**.
- Keep `shoulder_causality_20260323T215813Z` only if retaining immediate rerun provenance is useful; otherwise archive it as predecessor evidence rather than elevate both equally.

### Practical implication for T
Canonical output set should likely be:
- `outputs/bohmian_adaptation_20260319_191614/` if recovered/confirmed in live target tree
- `outputs/shoulder_causality_20260323T222400Z/`
- optionally archive `outputs/shoulder_causality_20260323T215813Z/` as the earlier rerun

## Summary posture
The four decisions together imply:
- **GRQM canonical identity:** exploratory toy-probe sandbox with receipts
- **M role:** cold archive of record
- **WDW/LQC:** historical exploratory lanes, not canonical public center
- **Shoulder bundles:** treat later rerun as canonical, earlier as archival provenance unless needed

## Consequence for cleanup
Cleanup should now proceed under a coherent target:
- restore minimal reproducibility surfaces
- build curated `docs/`
- keep a narrow canonical `outputs/` set
- archive historical governance and exploratory notebook layers
- avoid re-expanding root or restoring older public sprawl from G
