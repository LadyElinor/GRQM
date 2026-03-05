from __future__ import annotations

import csv
import json
import math
import traceback
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


@dataclass(frozen=True)
class Case:
    omega_m: float
    alpha_qg: float


def classical_term(a: float, omega_m: float) -> float:
    return -(omega_m) / (2.0 * a * a) + (1.0 - omega_m) * a


def correction_term(a: float, alpha_qg: float, variant: str, a_cut: float = 0.02, k: int = 6) -> float:
    if variant == "baseline_n5":
        return alpha_qg / (a**5)
    if variant == "higher_order_n6":
        return alpha_qg / (a**6)
    if variant == "softcap_denom":
        return alpha_qg / (a**5 + a_cut**5)
    if variant == "tanh_gate":
        return (alpha_qg / (a**5)) * math.tanh((a / a_cut) ** k)
    raise ValueError(f"Unknown variant: {variant}")


def run_case(case: Case, variant: str, method: str = "Radau", max_step: float = 1e-3):
    ratio_log = []

    def rhs(t, y):
        a, v = float(y[0]), float(y[1])
        if a <= 0:
            ratio_log.append({"t": float(t), "a": float(a), "ratio": float("inf")})
            return [0.0, 0.0]

        cls = classical_term(a, case.omega_m)
        corr = correction_term(a, case.alpha_qg, variant)
        ratio = abs(corr / (cls + 1e-30))
        ratio_log.append({"t": float(t), "a": float(a), "ratio": float(ratio)})
        return [v, cls + corr]

    try:
        sol = solve_ivp(
            rhs,
            t_span=(0.0, 3.0),
            y0=[0.1, 1.5],
            method=method,
            rtol=1e-9,
            atol=1e-11,
            max_step=max_step,
            dense_output=False,
        )

        finite = [r for r in ratio_log if np.isfinite(r["ratio"])]
        peak = max(finite, key=lambda r: r["ratio"]) if finite else None

        return {
            "omega_m": case.omega_m,
            "alpha_qg": case.alpha_qg,
            "variant": variant,
            "solver": method,
            "solver_success": bool(sol.success),
            "solver_message": str(sol.message),
            "solver_outcome": "success" if bool(sol.success) else "failed",
            "t_end": float(sol.t[-1]) if len(sol.t) > 0 else float("nan"),
            "a_end": float(sol.y[0, -1]) if sol.y.size else float("nan"),
            "min_a": float(min((x["a"] for x in ratio_log), default=float("nan"))),
            "max_ratio": float(peak["ratio"]) if peak else float("nan"),
            "peak_t": float(peak["t"]) if peak else float("nan"),
        }
    except Exception as e:
        tb = traceback.format_exc()
        return {
            "omega_m": case.omega_m,
            "alpha_qg": case.alpha_qg,
            "variant": variant,
            "solver": method,
            "solver_success": False,
            "solver_message": f"EXCEPTION: {e}",
            "solver_outcome": "exception",
            "t_end": float("nan"),
            "a_end": float("nan"),
            "min_a": float("nan"),
            "max_ratio": float("nan"),
            "peak_t": float("nan"),
            "traceback": tb,
        }


def main():
    root = Path(__file__).resolve().parents[1]
    out_dir = root / "notebooks" / "outputs" / f"grqm_edge_nonlinear_extension_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=True)

    omega_vals = [0.305, 0.3075, 0.310]
    alpha_vals = [3e-7, 7e-7, 1e-6, 1.3e-6]
    variants = ["baseline_n5", "higher_order_n6", "softcap_denom", "tanh_gate"]

    rows = []
    for om in omega_vals:
        for aq in alpha_vals:
            case = Case(omega_m=om, alpha_qg=aq)
            for variant in variants:
                rows.append(run_case(case, variant=variant, method="Radau", max_step=1e-3))

    fields = [
        "omega_m",
        "alpha_qg",
        "variant",
        "solver",
        "solver_outcome",
        "solver_success",
        "solver_message",
        "min_a",
        "max_ratio",
        "peak_t",
        "t_end",
        "a_end",
    ]

    with (out_dir / "edge_nonlinear_extension_sweep.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})

    # requested concise output keys
    concise = [
        {
            "omega_m": r["omega_m"],
            "alpha_qg": r["alpha_qg"],
            "variant": r["variant"],
            "min_a": r["min_a"],
            "max_ratio": r["max_ratio"],
            "peak_t": r["peak_t"],
            "solver_outcome": r["solver_outcome"],
        }
        for r in rows
    ]
    (out_dir / "edge_nonlinear_extension_table.json").write_text(json.dumps(concise, indent=2), encoding="utf-8")

    # aggregate by variant
    agg = {}
    for variant in variants:
        rr = [r for r in rows if r["variant"] == variant]
        success = [r for r in rr if r["solver_success"]]
        agg[variant] = {
            "n": len(rr),
            "success_rate": float(len(success) / len(rr)) if rr else float("nan"),
            "max_ratio_worst": float(max((r["max_ratio"] for r in success), default=float("nan"))),
            "min_a_worst": float(min((r["min_a"] for r in success), default=float("nan"))),
        }

    # prereg checks
    checks = {}
    for variant in variants:
        v = agg[variant]
        checks[variant] = {
            "A_ratio_control_pass": bool(v["max_ratio_worst"] <= 0.10) if np.isfinite(v["max_ratio_worst"]) else False,
            "B_min_a_guard_pass": bool(v["min_a_worst"] >= 0.02) if np.isfinite(v["min_a_worst"]) else False,
            "C_solver_robustness_pass": bool(abs(v["success_rate"] - 1.0) < 1e-12),
        }
        checks[variant]["all_pass"] = (
            checks[variant]["A_ratio_control_pass"]
            and checks[variant]["B_min_a_guard_pass"]
            and checks[variant]["C_solver_robustness_pass"]
        )

    summary = {"aggregate": agg, "acceptance_checks": checks, "out_dir": str(out_dir)}
    (out_dir / "edge_nonlinear_extension_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # traceback capture file if any failures
    failures = [r for r in rows if (not r.get("solver_success", False)) or ("traceback" in r)]
    if failures:
        lines = []
        for f in failures:
            lines.append(f"CASE omega_m={f['omega_m']} alpha_qg={f['alpha_qg']} variant={f['variant']}")
            lines.append(f"outcome={f.get('solver_outcome')} message={f.get('solver_message')}")
            if "traceback" in f:
                lines.append("TRACEBACK:")
                lines.append(f["traceback"])
            lines.append("-")
        (out_dir / "edge_nonlinear_extension_failures.log").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
