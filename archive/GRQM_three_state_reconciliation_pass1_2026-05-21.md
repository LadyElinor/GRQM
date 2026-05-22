# GRQM Three-State Reconciliation — Pass 1 (2026-05-21)

## States
- **L** = local `C:\Users\arren\.openclaw\workspace\repos\GRQM` working tree
- **G** = public `origin/main`
- **M** = `C:\Users\arren\Molt\workspace\Physics`
- **T** = target canonical state to be defined explicitly

## Why this pass exists
The project is no longer a simple keep/restore/archive problem. It is a reconciliation problem across three existing states with a fourth target state still undecided.

This pass stays at the **directory / file-class level** to answer the architectural question before file-level gravity takes over.

## Mechanical findings
- Local branch is **3 commits ahead, 0 behind** `origin/main`.
- Current local working tree is also dirty relative to `origin/main`.
- `git diff --stat origin/main` reports **292 changed paths** and **340660 deletions**, dominated by removed notebooks/output/archive material.
- Top diff concentration by top-level class:
  - `notebooks`: 203
  - `archive`: 40
  - `src`: 8
  - `tests`: 4
  - `docs`: 4
  - `scripts`: 3
  - many single root governance files

## State snapshots at top level

### L (local trimmed working tree)
- dirs: `.git`, `.pytest_cache`, `archive`, `notebooks`, `outputs`, `src`, `tests`
- root files: `README.md`, `ARCHITECTURE.md`, `MODEL-VALIDITY.md`, `AUDIT-NOTES.md`
- visible posture: sparse, trimmed, maintainer-facing

### G (`origin/main` public state)
Top-level tracked items include:
- root governance docs (`CANONICAL_ARTIFACTS.md`, `CLAIM_STATUS_MATRIX.md`, `RESEARCH_ASSUMPTION_REGISTER.md`, `WDW_INTEGRATION_PROTOCOL.md`, many `GR_QM_*` notes)
- `.github`, `.gitignore`
- `archive`, `docs`, `notebooks`, `scripts`, `src`, `tests`
- packaging/runtime files: `pyproject.toml`, `requirements*.txt`
- root markdown count: **23**
- visible posture: provenance-heavy, governance-heavy, cluttered for outsiders

### M (`Molt\workspace\Physics` richer workspace)
- contains `archive`, `docs`, `notebooks`, `outputs`, `scripts`, `src`, `tests`, `.github`
- also contains a very large background corpus of PDFs/reference texts and additional directories like `ComputationalPhysics`
- includes many root governance docs also seen in G
- visible posture: rich local research workspace / corpus, not a clean public repo shape

## Pass 1 reconciliation matrix

| Class | L | G | M | Pass 1 reading | Provisional T recommendation |
|---|---|---|---|---|---|
| Root public orientation docs | yes, but trimmed to 4 docs | yes, but mixed into 23+ root md files | yes, mixed into broader workspace clutter | L is closer to a sane public surface than G or M | Keep a small curated root surface in T |
| Root governance / cycle docs | mostly absent from root | heavily present | heavily present | G and M preserve provenance, but root placement creates public clutter | Move most out of root in T, likely archive/docs |
| `README.md` | yes, rewritten | yes, older and broken quickstart | yes | L is the active rewrite; G is stale public orientation | Keep rewritten README in T, verify commands |
| `LICENSE` | missing | missing | missing | absence is consistent across all states | Add in T |
| `.github` / CI | absent in working tree | present | present | likely removed locally during reduction, not yet reconciled | Reassess for T; probably restore minimal CI if repo remains public |
| Packaging/runtime files (`pyproject.toml`, `requirements*`) | absent in working tree root | present | present | local reduction currently weakens reproducibility surface | Restore minimal reproducibility packaging in T unless repo becomes purely archival |
| `src/` | present, narrowed | present, broader older code lanes | present | code is canonical repo content in all meaningful states | Keep in T |
| `tests/` | present, narrowed | present, broader older tests | present | tests belong in T, but target breadth depends on scientific identity | Keep in T with identity-aligned scope |
| `scripts/` | absent in L root | present in G and M | present | likely useful but not root-critical | Keep selectively in T or fold into documented run paths |
| `docs/` | absent as live directory class in L | present | present | L reduction over-trimmed discoverability if no replacement docs dir exists | Restore a small curated docs layer in T |
| `archive/` | present | present | present | all states agree provenance exists; dispute is scope and visibility | Keep archive in T, but clearly secondary |
| `archive/session-notes/2026-03` and similar dated notes | present subset | present richer set | present richer set | provenance-bearing but not orientation-first | Archive in T, not root |
| `notebooks/` | present but apparently reduced/dirty relative to G | present and very large | present and very large | major reduction zone; likely largest governance-debt area | Keep only canonical/needed notebooks in T, archive or exclude the rest |
| `outputs/` | present with newer bohmian/shoulder bundles | not top-level tracked in same visible way from earlier summary, but many output artifacts exist in repo history/diff | present richly | output selection is identity-defining, not just clutter | Keep only canonical evidence bundles in T |
| Background PDF/reference corpus | no | no | yes, heavily | M contains deep archive/reference material not suited to public repo | Keep out of T; preserve M separately as cold archive or local corpus |
| Extra local workspace dirs (e.g. `ComputationalPhysics`) | no | no | yes | beyond GRQM public repo scope | Exclude from T |

## Architectural reading from Pass 1
The strongest current reading is:
- **T should not look like G.** G is too provenance-heavy and root-cluttered for a clear public-facing canonical state.
- **T should also not simply equal current L.** L appears over-trimmed and currently drops useful reproducibility/discoverability surfaces like packaging files, possible CI, and a docs layer.
- Therefore **T is probably a hybrid**:
  - small curated public root, closer to L
  - explicit docs/archive organization for provenance, rather than G-style root sprawl
  - restored minimal reproducibility/runtime surfaces from G/M
  - selective canonical outputs and notebooks only

## Governance-debt interpretation
The biggest silent divergence is not just a few root files.
It is that a large local reduction has been performed privately across notebooks, archive notes, outputs, packaging surfaces, and governance docs while the public repo still presents an older richer shape.

That divergence is governance debt and should be resolved explicitly, not by drift.

## `Molt\workspace\Physics` role options
Pass 1 suggests three viable roles for M:
1. **Cold archive of record** for full provenance and reference corpus
2. temporary staging workspace to be retired after reconciliation
3. canonical internal research workspace from which public GRQM is derived

Current evidence makes **(1) cold archive of record** the most honest provisional reading.

## Open decisions to resolve before Pass 2
1. What is the canonical scientific identity of GRQM post-reduction?
2. Is T a public research sandbox with receipts, or a full provenance repository?
3. Should packaging/runtime reproducibility surfaces be restored fully or minimally?
4. Which notebook/output families are canonical evidence versus historical residue?
5. Is `Molt\workspace\Physics` explicitly designated as cold archive of record?

## Recommended next move
Do Pass 2 only for the highest-signal classes first:
- root governance docs
- packaging/runtime files
- `docs/`
- `scripts/`
- notebook/output families by bundle, not by individual file initially
