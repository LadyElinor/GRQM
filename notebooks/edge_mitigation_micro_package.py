from __future__ import annotations

"""
Edge mitigation micro-package (pre-registered scaffold).

Scope (diagnostic-only):
- Ω_m in [0.305, 0.31] representative points
- α_qg log-spaced subset
- solver family: DOP853 primary, LSODA/Radau cross-check
- no governance or claim-state mutation in this script
"""

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


@dataclass
class IC:
    t0: float = 0.0
    t1: float = 3.0
    a0: float = 0.1
    v0: float = 1.5


@dataclass
class Params:
    omega_m: float
    omega_l: float
    alpha_qg: float


def rhs(_t, y, p: Params, correction_power: int = 5):
    a, v = y
    if a <= 0:
        return [0.0, 0.0]
    base = -(p.omega_m) / (2.0 * a * a) + p.omega_l * a
    corr = p.alpha_qg / (a**correction_power)
    return [v, base + corr]


def integrate_adaptive(ic: IC, p: Params, method: str, t_eval: np.ndarray, rtol: float, atol: float):
    sol = solve_ivp(
        fun=lambda t, y: rhs(t, y, p),
        t_span=(ic.t0, ic.t1),
        y0=np.array([ic.a0, ic.v0], dtype=float),
        t_eval=t_eval,
        method=method,
        rtol=rtol,
        atol=atol,
    )
    if not sol.success:
        raise RuntimeError(f"{method} failed: {sol.message}")
    return sol.y[0]


def metrics_vs_ref(a_cmp: np.ndarray, a_ref: np.ndarray):
    d = np.abs(a_cmp - a_ref)
    return {
        "q2_D_star": float(np.mean(d)),
        "q2_D_p95": float(np.quantile(d, 0.95)),
        "q2_D_p99": float(np.quantile(d, 0.99)),
        "q2_D_max": float(np.max(d)),
    }


def main():
    root = Path(__file__).resolve().parents[1]
    out_dir = root / "notebooks" / "outputs" / f"grqm_edge_mitigation_micro_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=True)

    ic = IC()
    omega_vals = [0.305, 0.3075, 0.31]
    alpha_vals = [3e-7, 5e-7, 7e-7, 1e-6, 1.3e-6]
    t_eval = np.linspace(ic.t0, ic.t1, int(round((ic.t1 - ic.t0) / 1e-3)) + 1)

    # Predeclared policy
    ref_method = "DOP853"
    ref_rtol, ref_atol = 1e-12, 1e-14
    compare = [
        ("DOP853", 1e-10, 1e-12),
        ("LSODA", 1e-10, 1e-12),
        ("Radau", 1e-10, 1e-12),
    ]

    rows = []
    for om in omega_vals:
        for aq in alpha_vals:
            p = Params(omega_m=om, omega_l=1.0 - om, alpha_qg=aq)
            a_ref = integrate_adaptive(ic, p, ref_method, t_eval, ref_rtol, ref_atol)
            for method, rtol, atol in compare:
                a_cmp = integrate_adaptive(ic, p, method, t_eval, rtol, atol)
                m = metrics_vs_ref(a_cmp, a_ref)
                rows.append({
                    "omega_m": om,
                    "alpha_qg": aq,
                    "method": method,
                    "rtol": rtol,
                    "atol": atol,
                    **m,
                })

    with (out_dir / "edge_mitigation_micro_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    policy = {
        "pass_targets": {
            "q2_D_p95_max": 0.01,
            "q2_D_p99_max": 0.05,
            "q1_refine_max": 1e-6,
            "q1_assumption_sensitivity_hardened_max": 0.18,
        },
        "note": "This script computes q2-style method diagnostics only; q1/hardening checks require dedicated companion run.",
    }
    (out_dir / "edge_mitigation_policy.json").write_text(json.dumps(policy, indent=2), encoding="utf-8")

    print(json.dumps({"out_dir": str(out_dir), "n_rows": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
