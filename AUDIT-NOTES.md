# GRQM Live-State Audit Note (2026-05-21)

## Scope
This note records the observed live state of `C:\Users\arren\.openclaw\workspace\repos\GRQM` relative to the richer reference tree in `C:\Users\arren\Molt\workspace\Physics` and the local corpus at `C:\Users\arren\.openclaw\workspace\Physics`.

## Observed repo state
- The live GRQM repo root is currently sparse and maintainer-facing, containing only:
  - `README.md`
  - `ARCHITECTURE.md`
  - `MODEL-VALIDITY.md`
  - `AUDIT-NOTES.md`
  - plus `archive/`, `notebooks/`, `outputs/`, `src/`, and `tests/`
- This means the earlier concern about root markdown clutter is **not true for the current GRQM repo checkout**.
- The repo does **not** currently contain a `LICENSE` file.
- The repo does **not** currently contain `CLAIM_STATUS_MATRIX.md` or `CANONICAL_ARTIFACTS.md`.
- The repo does contain `archive/session-notes/2026-03/`, so the archive pattern is present in the live tree.

## README / orientation findings
- The current `README.md` is a compact maintainer-facing orientation surface.
- It does **not** contain the previously cited broken quickstart line `cd Physics`.
- It does describe the repo as exploratory and receipts-first, which is directionally good.
- However, it still lacks:
  - a license pointer
  - an outsider-facing orientation layer
  - canonical artifact / claim-matrix links at root

## Code / tests footprint
- `src/grqm/` is present with three visible active lanes:
  - `bohmian_probe/`
  - `models/`
  - `solvers/`
- `tests/` is present and not empty.
- Visible checked-in tests now include at least:
  - `tests/bohmian_probe/test_guidance_sanity.py`
  - `tests/bohmian_probe/test_schrodinger_newton_smoke.py`
  - `tests/bohmian_probe/test_symbolic_core.py`
- This means the stronger earlier concern that tests were absent is also **no longer true in full**. The better statement is: test coverage may still be narrow, but visible tests do exist.

## Critical integrity finding
- The live repo is in a **heavily modified working-tree state**.
- `git status --short` shows a large deletion set against tracked files from an older/richer project shape, plus a smaller untracked rewritten surface.
- After fetching, the checked-out branch itself is **3 commits ahead of `origin/main` and 0 behind**. So the branch history is not the same thing as the current dirty working tree.
- This distinction matters:
  - `origin/main` is the public GitHub-facing state
  - local `HEAD` is a newer committed state
  - the current working tree is an additional unresolved reduction/rewrite layer on top of that
- In practice, this means the current repo is not a clean settled snapshot of a mature GRQM state. It is a transitional rewrite/reduction of a richer earlier workspace.
- The richer reference tree under `C:\Users\arren\Molt\workspace\Physics` still contains many files absent from the live repo, including:
  - `CLAIM_STATUS_MATRIX.md`
  - `CANONICAL_ARTIFACTS.md`
  - `RESEARCH_ASSUMPTION_REGISTER.md`
  - `WDW_INTEGRATION_PROTOCOL.md`
  - many `GR_QM_*` governance artifacts
  - `docs/`
  - `scripts/`
  - broader notebooks/output history

## Interpretation
The immediate issue is **not** root clutter in the current GRQM checkout.
The immediate issue is that GRQM appears to be a reduced live repo sitting on top of a much richer predecessor/reference workspace, with a large unresolved diff.

Also important: public GitHub state, local committed state, and current working-tree state are three different layers right now. That is itself a governance-relevant fact and should be resolved explicitly.

That changes the recommended next move:
1. establish whether the reduced GRQM repo is the intended new canonical public shape
2. decide which artifacts from the richer Physics tree must be restored, migrated, or intentionally left archived
3. only then draft the outsider roadmap and orientation surfaces for the final intended shape

## Recommended next actions
1. Resolve repo intent first:
   - Is `repos/GRQM` meant to be the new canonical trimmed public repo?
   - Or is it an incomplete reduction pass that still needs restoration from `Molt\workspace\Physics`?
   - Open identity question to register explicitly: **What is the canonical scientific identity of GRQM post-reduction?**
   - Separate tracked decision: **What is `Molt\workspace\Physics` for going forward?**
     - cold archive of record
     - temporary staging workspace pending reconciliation
     - canonical internal research workspace from which public GRQM is derived
2. If canonical trimmed repo:
   - add `LICENSE`
   - restore or recreate `CLAIM_STATUS_MATRIX.md` / `CANONICAL_ARTIFACTS.md` equivalents if still important
   - add `docs/ORIENTATION.md`
3. If incomplete reduction:
   - diff against `Molt\workspace\Physics`
   - decide a keep/archive/restore list before messaging the repo publicly
