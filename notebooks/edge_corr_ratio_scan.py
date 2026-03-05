from __future__ import annotations

import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

alpha_qg = 7e-7
correction_power = 5

def run_case(omega_m: float):
    log = []

    def terms(a: float):
        classical = -(omega_m) / (2.0 * a * a) + (1.0 - omega_m) * a
        correction = alpha_qg / (a**correction_power)
        return classical, correction

    def rhs(t, y):
        a, v = float(y[0]), float(y[1])
        if a <= 0:
            classical, correction = float('nan'), float('nan')
            ratio = float('inf')
            log.append({"t": t, "a": a, "v": v, "classical": classical, "correction": correction, "corr_over_classical": ratio})
            return [0.0, 0.0]
        classical, correction = terms(a)
        ratio = abs(correction / (classical + 1e-30))
        log.append({
            "t": float(t),
            "a": float(a),
            "v": float(v),
            "classical": float(classical),
            "correction": float(correction),
            "corr_over_classical": float(ratio),
        })
        return [v, classical + correction]

    sol = solve_ivp(
        rhs,
        t_span=(0.0, 3.0),
        y0=[0.1, 1.5],
        method="RK45",
        rtol=1e-3,
        atol=1e-5,
        max_step=1e-3,
        dense_output=False,
    )

    finite = [x for x in log if np.isfinite(x["corr_over_classical"]) ]
    peak = max(finite, key=lambda x: x["corr_over_classical"]) if finite else None
    return {
        "omega_m": omega_m,
        "alpha_qg": alpha_qg,
        "success": bool(sol.success),
        "message": sol.message,
        "t_end": float(sol.t[-1]),
        "a_end": float(sol.y[0, -1]),
        "min_a_seen": float(min((x["a"] for x in log), default=float('nan'))),
        "max_corr_over_classical": float(peak["corr_over_classical"]) if peak else float('nan'),
        "peak_entry": peak,
    }

if __name__ == "__main__":
    out = [run_case(0.3075), run_case(0.295)]
    out_path = Path(__file__).resolve().parents[0] / "outputs" / "edge_corr_ratio_scan.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps({"out_path": str(out_path), "results": out}, indent=2))
