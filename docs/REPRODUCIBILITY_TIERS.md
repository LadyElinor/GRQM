# Reproducibility Dependency Tiers

This project uses two dependency tiers to keep governance reruns stable while allowing research iteration.

## Tier 1 — Strict governed reruns (canonical)
Use when generating or re-validating governance-facing/canonical artifacts.

- Install from lockfile: `requirements-lock.txt`
- Expected path: `./requirements-lock.txt` (repo root)
- Output targets: canonical artifacts listed in `CANONICAL_ARTIFACTS.md`

Recommended install:
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-lock.txt
python -m pip install -e .
pytest
```

## Tier 2 — Research / exploratory environment
Use for notebooks, exploratory diagnostics, and non-canonical experiments.

- Baseline: `pyproject.toml` + `requirements.txt` + `requirements-dev.txt`
- Optional extras (e.g., pandas/jupyter/matplotlib) may be installed ad hoc.
- Research outputs remain archival unless explicitly promoted.

## Policy boundary
- Do **not** use Tier-2-only packages to regenerate canonical receipts unless they are added to the strict lockfile.
- If a research dependency becomes required for governed workflows, promote it by updating `requirements-lock.txt` in a dedicated change.
