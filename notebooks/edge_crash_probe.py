from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

omega_m = 0.3075
alpha_qg = 7e-7
correction_power = 5

y0 = [0.1, 1.5]
t_span = (0.0, 3.0)

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
        "t": t,
        "a": a,
        "v": v,
        "classical": classical,
        "correction": correction,
        "corr_over_classical": ratio,
    })
    return [v, classical + correction]

sol = None
err = None
try:
    sol = solve_ivp(
        rhs,
        t_span=t_span,
        y0=y0,
        method="RK45",
        rtol=1e-3,
        atol=1e-5,
        max_step=1e-3,
        dense_output=False,
    )
except Exception as e:
    err = str(e)

out = {
    "success": None if sol is None else bool(sol.success),
    "message": None if sol is None else sol.message,
    "nfev": None if sol is None else int(sol.nfev),
    "njev": None if sol is None else int(getattr(sol, "njev", 0) or 0),
    "t_end": None if sol is None else float(sol.t[-1]),
    "a_end": None if sol is None else float(sol.y[0, -1]),
    "v_end": None if sol is None else float(sol.y[1, -1]),
    "exception": err,
    "last20": log[-20:],
    "max_corr_over_classical": float(max((x["corr_over_classical"] for x in log if np.isfinite(x["corr_over_classical"])), default=float("nan"))),
    "min_a_seen": float(min((x["a"] for x in log), default=float("nan"))),
}

out_path = Path(__file__).resolve().parents[0] / "outputs" / "edge_crash_probe_omega0.3075_alpha7e-7.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps({"out_path": str(out_path), **{k: out[k] for k in ["success","message","t_end","a_end","v_end","exception","max_corr_over_classical","min_a_seen"]}}, indent=2))
