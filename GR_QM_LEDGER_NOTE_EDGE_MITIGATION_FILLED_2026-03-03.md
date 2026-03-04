# Ledger Note — Edge Mitigation Review (Filled)

Cycle ID: `edge-mitigation-micro-20260303`

## Scope
- Envelope tested: `Ω_m in [0.305, 0.31]` (edge lane)
- α corridor: `{3e-7, 5e-7, 7e-7, 1e-6, 1.3e-6}`
- Methods: DOP853 (ref), LSODA, Radau
- Artifact: `notebooks/outputs/grqm_edge_mitigation_micro_20260303_213950/edge_mitigation_micro_summary.csv`

## Results snapshot
- q2_D_p95 max (global): `5.118016110916557e-08`
- q2_D_p99 max (global): `6.730758567163875e-08`
- By method (max q2_D_p95 / q2_D_p99):
  - DOP853: `5.272054681704219e-09 / 6.94278662338732e-09`
  - LSODA: `5.118016110916557e-08 / 6.730758567163875e-08`
  - Radau: `1.848005082294435e-11 / 2.8614867420007073e-11`
- q1_refine max: **not measured in this micro-package**
- q1_assumption_sensitivity_hardened max: **not measured in this micro-package**
- true replication rel diff max: **not measured in this micro-package**

## Gate disposition
- G-ROBUST-Q2: **PASS** (far below prereg targets: p95<0.01, p99<0.05)
- G-REFINE: **PENDING** (requires companion q1/refinement run)
- G-ROBUST-Q1: **PENDING** (requires companion hardening run)
- G-REPLICATION: **PENDING** (not included in this script)
- G-ENVELOPE (edge lane): **BLOCKED (unchanged)**

## Decision
- [x] Keep edge BLOCKED
- [ ] Allow exploratory edge inclusion (non-promoting)
- [ ] Escalate to governance review for policy change

## Notes
- Strong evidence of numerical-path dominance for Q2-style edge divergence under stiff-capable integrators.
- No claim-status mutation executed; this is partial mitigation evidence only.
- Next required step: companion run adding q1_refine + hardening + replication checks under same edge scope.
