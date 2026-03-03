from __future__ import annotations

from pathlib import Path
from datetime import datetime
import csv
import math
import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, RunConfig, integrate, l2_rel_err
from boo_branch_starter import boo_diagnostics


def rankdata(x):
    x = np.asarray(x, dtype=float)
    order = np.argsort(x)
    ranks = np.empty(len(x), dtype=float)
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and x[order[j + 1]] == x[order[i]]:
            j += 1
        r = 0.5 * (i + j) + 1.0
        ranks[order[i : j + 1]] = r
        i = j + 1
    return ranks


def spearman(x, y):
    rx = rankdata(x)
    ry = rankdata(y)
    cx = rx - rx.mean()
    cy = ry - ry.mean()
    den = float(np.sqrt(np.sum(cx * cx) * np.sum(cy * cy)))
    if den == 0.0:
        return float("nan")
    return float(np.sum(cx * cy) / den)


def eval_point(om, aq, dt):
    ic = IC()
    p = Params(omega_m=om, omega_l=1.0 - om, alpha_qg=aq)
    _, a_b, _ = integrate(ic, p, RunConfig(dt=dt, method="rk4", corrected=False))
    _, a_c, _ = integrate(ic, p, RunConfig(dt=dt, method="rk4", corrected=True))
    q1 = l2_rel_err(a_c - a_b, a_b)
    slow, fast = boo_diagnostics(a_b, a_c)
    return q1, slow, fast, fast / (abs(slow) + 1e-15)


def main():
    base = Path(__file__).resolve().parent / "outputs"
    runs = sorted(base.glob("grqm_boo_branch_starter_*"))
    if not runs:
        raise SystemExit("No boo_branch_starter outputs found")
    run_dir = runs[-1]

    summary_csv = run_dir / "boo_branch_summary.csv"
    rows = []
    with summary_csv.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({k: float(v) for k, v in r.items()})

    q1 = np.array([r["q1_proxy_l2"] for r in rows])
    slow = np.array([r["boo_slow_l2"] for r in rows])
    fast = np.array([r["boo_fast_rms"] for r in rows])

    rho = spearman(q1, slow)

    # deterministic reproducibility check over full corridor by exact re-eval
    max_abs_delta = 0.0
    max_rel_delta = 0.0
    for r in rows:
        q1_2, slow_2, fast_2, ratio_2 = eval_point(r["omega_m"], r["alpha_qg"], 1.0e-3)
        for key, v2 in [
            ("q1_proxy_l2", q1_2),
            ("boo_slow_l2", slow_2),
            ("boo_fast_rms", fast_2),
            ("fast_to_slow_ratio", ratio_2),
        ]:
            v1 = r[key]
            da = abs(v2 - v1)
            dr = da / (abs(v1) + 1e-15)
            if da > max_abs_delta:
                max_abs_delta = da
            if dr > max_rel_delta:
                max_rel_delta = dr

    # sensitivity spot-check
    subset = [
        (0.285, 3e-7),
        (0.295, 7e-7),
        (0.300, 1.3e-6),
    ]
    dts = [9e-4, 1.0e-3, 1.1e-3]

    sens_rows = []
    for om, aq in subset:
        ref = None
        for dt in dts:
            q1v, sv, fv, rv = eval_point(om, aq, dt)
            if math.isclose(dt, 1.0e-3):
                ref = (q1v, sv, fv, rv)
            sens_rows.append(
                {
                    "omega_m": om,
                    "alpha_qg": aq,
                    "dt": dt,
                    "q1_proxy_l2": q1v,
                    "boo_slow_l2": sv,
                    "boo_fast_rms": fv,
                    "fast_to_slow_ratio": rv,
                }
            )
        # add relative deltas vs dt=1e-3
        for r in sens_rows:
            if r["omega_m"] == om and r["alpha_qg"] == aq:
                r["rel_delta_q1_vs_dt1e-3"] = abs(r["q1_proxy_l2"] - ref[0]) / (abs(ref[0]) + 1e-15)
                r["rel_delta_boo_slow_vs_dt1e-3"] = abs(r["boo_slow_l2"] - ref[1]) / (abs(ref[1]) + 1e-15)
                r["rel_delta_boo_fast_vs_dt1e-3"] = abs(r["boo_fast_rms"] - ref[2]) / (abs(ref[2]) + 1e-15)

    sens_csv = run_dir / "boo_sensitivity_spotcheck.csv"
    with sens_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(sens_rows[0].keys()))
        writer.writeheader()
        writer.writerows(sens_rows)

    max_rel_q1 = max(r["rel_delta_q1_vs_dt1e-3"] for r in sens_rows)
    max_rel_slow = max(r["rel_delta_boo_slow_vs_dt1e-3"] for r in sens_rows)
    max_rel_fast = max(r["rel_delta_boo_fast_vs_dt1e-3"] for r in sens_rows)

    metrics = {
        "run_dir": str(run_dir),
        "timestamp_eval": datetime.now().isoformat(),
        "n_core_points": len(rows),
        "spearman_q1_vs_boo_slow": rho,
        "deterministic_max_abs_delta": max_abs_delta,
        "deterministic_max_rel_delta": max_rel_delta,
        "signal_retention_q1_min": float(q1.min()),
        "signal_retention_q1_max": float(q1.max()),
        "signal_retention_q1_span_ratio": float(q1.max() / (q1.min() + 1e-15)),
        "signal_retention_boo_slow_min": float(slow.min()),
        "signal_retention_boo_slow_max": float(slow.max()),
        "signal_retention_boo_slow_span_ratio": float(slow.max() / (slow.min() + 1e-15)),
        "sensitivity_max_rel_delta_q1": max_rel_q1,
        "sensitivity_max_rel_delta_boo_slow": max_rel_slow,
        "sensitivity_max_rel_delta_boo_fast": max_rel_fast,
        "criteria": {
            "table_complete_20": len(rows) == 20,
            "deterministic_reproducible": max_abs_delta < 1e-14,
            "spearman_ge_0p95": bool(rho >= 0.95),
            "spearman_lt_0p8_failure": bool(rho < 0.8),
        },
    }

    import json
    with (run_dir / "boo_eval_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
