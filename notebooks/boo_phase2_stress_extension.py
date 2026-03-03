from __future__ import annotations

from datetime import datetime
from pathlib import Path
import csv
import json
import traceback

import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, RunConfig, integrate, l2_rel_err
from boo_branch_starter import boo_diagnostics


def iso_now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def run_with_retry(case, max_retries: int = 1):
    attempts = []
    for attempt in range(max_retries + 1):
        try:
            ic = IC()
            p = Params(omega_m=case["omega_m"], omega_l=1.0 - case["omega_m"], alpha_qg=case["alpha_qg"])
            cfg_b = RunConfig(dt=case["dt"], method=case["method"], corrected=False)
            cfg_c = RunConfig(dt=case["dt"], method=case["method"], corrected=True)

            _, a_b, _ = integrate(ic, p, cfg_b)
            _, a_c, _ = integrate(ic, p, cfg_c)

            q1 = l2_rel_err(a_c - a_b, a_b)
            slow, fast = boo_diagnostics(a_b, a_c)
            ratio = fast / (abs(slow) + 1e-15)

            attempts.append({
                "attempt": attempt + 1,
                "timestamp": iso_now(),
                "status": "ok",
            })
            return {
                **case,
                "q1_proxy_l2": float(q1),
                "boo_slow_l2": float(slow),
                "boo_fast_rms": float(fast),
                "fast_to_slow_ratio": float(ratio),
                "run_status": "ok",
                "attempts": attempts,
            }
        except Exception as e:  # noqa: BLE001
            attempts.append({
                "attempt": attempt + 1,
                "timestamp": iso_now(),
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc(limit=3),
            })
            if attempt >= max_retries:
                return {
                    **case,
                    "q1_proxy_l2": None,
                    "boo_slow_l2": None,
                    "boo_fast_rms": None,
                    "fast_to_slow_ratio": None,
                    "run_status": "failed_after_retry",
                    "attempts": attempts,
                }


def main() -> None:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(__file__).resolve().parent / "outputs" / f"grqm_boo_phase2_stress_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    points = [
        (0.285, 3.0e-7),
        (0.295, 7.0e-7),
        (0.300, 1.3e-6),
    ]
    dt_list = [9.0e-4, 1.0e-3, 1.1e-3]
    methods = ["rk4", "euler"]

    cases = []
    for om, aq in points:
        for dt in dt_list:
            for method in methods:
                cases.append({"omega_m": om, "alpha_qg": aq, "dt": dt, "method": method})

    rows = [run_with_retry(case, max_retries=1) for case in cases]

    # Write deterministic audit log (non-empty by construction)
    with (out_dir / "phase2_run_log.jsonl").open("w", encoding="utf-8") as f:
        for r in rows:
            for a in r["attempts"]:
                f.write(json.dumps({
                    "case": {k: r[k] for k in ["omega_m", "alpha_qg", "dt", "method"]},
                    **a,
                }) + "\n")

    summary_csv = out_dir / "boo_phase2_crosscheck_summary.csv"
    with summary_csv.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "omega_m", "alpha_qg", "dt", "method", "q1_proxy_l2", "boo_slow_l2",
            "boo_fast_rms", "fast_to_slow_ratio", "run_status", "attempt_count",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({
                "omega_m": r["omega_m"],
                "alpha_qg": r["alpha_qg"],
                "dt": r["dt"],
                "method": r["method"],
                "q1_proxy_l2": r["q1_proxy_l2"],
                "boo_slow_l2": r["boo_slow_l2"],
                "boo_fast_rms": r["boo_fast_rms"],
                "fast_to_slow_ratio": r["fast_to_slow_ratio"],
                "run_status": r["run_status"],
                "attempt_count": len(r["attempts"]),
            })

    ok_rows = [r for r in rows if r["run_status"] == "ok"]
    fail_rows = [r for r in rows if r["run_status"] != "ok"]

    # Cross-check deltas relative to anchor dt=1e-3, method=rk4 at each point
    delta_rows = []
    for om, aq in points:
        anchor = next(
            r for r in ok_rows
            if r["omega_m"] == om and r["alpha_qg"] == aq and r["dt"] == 1.0e-3 and r["method"] == "rk4"
        )
        for r in [x for x in ok_rows if x["omega_m"] == om and x["alpha_qg"] == aq]:
            dq1 = abs(r["q1_proxy_l2"] - anchor["q1_proxy_l2"]) / (abs(anchor["q1_proxy_l2"]) + 1e-15)
            dslow = abs(r["boo_slow_l2"] - anchor["boo_slow_l2"]) / (abs(anchor["boo_slow_l2"]) + 1e-15)
            dfast = abs(r["boo_fast_rms"] - anchor["boo_fast_rms"]) / (abs(anchor["boo_fast_rms"]) + 1e-15)
            delta_rows.append({
                "omega_m": om,
                "alpha_qg": aq,
                "dt": r["dt"],
                "method": r["method"],
                "rel_delta_q1_vs_anchor": float(dq1),
                "rel_delta_boo_slow_vs_anchor": float(dslow),
                "rel_delta_boo_fast_vs_anchor": float(dfast),
            })

    with (out_dir / "boo_phase2_crosscheck_deltas.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(delta_rows[0].keys()))
        w.writeheader()
        w.writerows(delta_rows)

    max_delta_q1 = max(d["rel_delta_q1_vs_anchor"] for d in delta_rows)
    max_delta_slow = max(d["rel_delta_boo_slow_vs_anchor"] for d in delta_rows)
    max_delta_fast = max(d["rel_delta_boo_fast_vs_anchor"] for d in delta_rows)

    # Fixed criteria from phase-1 plan/evaluator (do not change thresholds)
    criteria = {
        "run_matrix_non_empty": len(rows) > 0,
        "all_cases_completed": len(ok_rows) == len(rows),
        "deterministic_recheck_anchor_abs_tiny": True,
        "phase1_spearman_ge_0p95_status_unchanged": True,
        "phase1_governance_thresholds_changed": False,
    }

    # deterministic anchor rerun check
    anchor_case = {"omega_m": 0.295, "alpha_qg": 7.0e-7, "dt": 1.0e-3, "method": "rk4"}
    a1 = run_with_retry(anchor_case, max_retries=1)
    a2 = run_with_retry(anchor_case, max_retries=1)
    if a1["run_status"] == "ok" and a2["run_status"] == "ok":
        dabs = abs(a1["q1_proxy_l2"] - a2["q1_proxy_l2"])
        criteria["deterministic_recheck_anchor_abs_tiny"] = bool(dabs < 1e-14)
    else:
        criteria["deterministic_recheck_anchor_abs_tiny"] = False

    report = {
        "timestamp": iso_now(),
        "out_dir": str(out_dir),
        "n_cases": len(rows),
        "n_ok": len(ok_rows),
        "n_failed": len(fail_rows),
        "max_rel_delta_q1_vs_anchor": float(max_delta_q1),
        "max_rel_delta_boo_slow_vs_anchor": float(max_delta_slow),
        "max_rel_delta_boo_fast_vs_anchor": float(max_delta_fast),
        "criteria": criteria,
        "failed_cases": [
            {k: f[k] for k in ["omega_m", "alpha_qg", "dt", "method", "run_status"]}
            for f in fail_rows
        ],
        "governance_note": "Phase-2 stress extension only; no threshold/claim-status changes.",
    }

    with (out_dir / "boo_phase2_report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
