from __future__ import annotations

import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

def max_ratio_case(omega_m: float, alpha_qg: float):
    log = []

    def rhs(t, y):
        a, v = float(y[0]), float(y[1])
        if a <= 0:
            return [0.0, 0.0]
        classical = -(omega_m) / (2.0 * a * a) + (1.0 - omega_m) * a
        correction = alpha_qg / (a**5)
        ratio = abs(correction / (classical + 1e-30))
        log.append({"t": t, "a": a, "ratio": ratio, "classical": classical, "correction": correction})
        return [v, classical + correction]

    sol = solve_ivp(rhs, (0.0, 3.0), [0.1, 1.5], method="RK45", rtol=1e-3, atol=1e-5, max_step=1e-3)
    peak = max(log, key=lambda r: r["ratio"]) if log else None
    return {
        "omega_m": omega_m,
        "alpha_qg": alpha_qg,
        "success": bool(sol.success),
        "max_corr_over_classical": float(peak["ratio"]) if peak else float("nan"),
        "peak_t": float(peak["t"]) if peak else float("nan"),
        "peak_a": float(peak["a"]) if peak else float("nan"),
        "min_a": float(min((r["a"] for r in log), default=float("nan"))),
    }

if __name__ == "__main__":
    test_cases = [
        (0.28, 7e-7),
        (0.29, 7e-7),
        (0.295, 7e-7),
        (0.300, 7e-7),
        (0.28, 1e-6),
        (0.300, 1e-6),
    ]
    rows = [max_ratio_case(om, aq) for om, aq in test_cases]
    out = Path(__file__).resolve().parents[0] / "outputs" / "corridor_corr_ratio_sweep.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(json.dumps(rows, indent=2))
