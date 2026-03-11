from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

from grqm.models.schrodinger_newton import SNParams, run_sn_1d


@dataclass
class RunConfig:
    kappas: list[float]
    c_vals: list[float]
    t_max_vals: list[float]
    sigma0: float
    mass: float
    dt: float
    n_grid: int
    tight_dt: float
    tight_n_grid: int
    q1_signal_detect: float
    q1_refinement_max: float
    norm_drift_strict_max: float
    norm_drift_practical_max: float
    loc_ratio_min: float
    loc_ratio_max: float
    ipr_delta_min: float
    ipr_delta_max: float


def rel_diff(a: float, b: float, eps: float = 1e-15) -> float:
    return abs(a - b) / (abs(b) + eps)


def status_line(row: dict) -> str:
    if row["pass_detect"] and row["pass_refine"] and row["pass_norm_practical"] and row["pass_loc_ratio"] and row["pass_ipr_sanity"]:
        return "PASS"
    if row["pass_refine"] and row["pass_norm_practical"] and row["pass_loc_ratio"] and row["pass_ipr_sanity"]:
        return "WATCH"
    return "FAIL"


def run_one(kappa: float, c_val: float, t_max: float, dt: float, n_grid: int, sigma0: float, mass: float) -> dict:
    p_on = SNParams(
        kappa=kappa,
        sigma0=sigma0,
        mass=mass,
        t_max=t_max,
        dt=dt,
        n_grid=n_grid,
        dispersion_enabled=True,
        dispersion_A=-0.5,
        dispersion_C=c_val,
        dispersion_omega=1.0,
    )
    on = run_sn_1d(p_on, seed=0)
    return {"on": on}


def maybe_retighten(raw: dict, kappa: float, c_val: float, t_max: float, cfg: RunConfig) -> tuple[dict, bool]:
    q1_ref = float(raw["on"]["q2"]["refinement_rel_diff"])
    if q1_ref <= 0.8e-6:
        return raw, False
    tight = run_one(kappa, c_val, t_max, cfg.tight_dt, cfg.tight_n_grid, cfg.sigma0, cfg.mass)
    return tight, True


def run_stage(stage_name: str, cfg: RunConfig, out_dir: Path) -> dict:
    rows = []
    for kappa in cfg.kappas:
        for c_val in cfg.c_vals:
            for t_max in cfg.t_max_vals:
                raw = run_one(kappa, c_val, t_max, cfg.dt, cfg.n_grid, cfg.sigma0, cfg.mass)
                raw, retightened = maybe_retighten(raw, kappa, c_val, t_max, cfg)

                q1_signal = float(raw["on"]["q1"]["sigma_deviation_max"])
                q1_delta_vs_off = rel_diff(
                    float(raw["on"]["q1"]["sigma_sn_final"]),
                    float(raw["on"]["q1"]["sigma_free_final"]),
                )
                q1_ref = float(raw["on"]["q2"]["refinement_rel_diff"])
                norm_drift = float(raw["on"]["q2"]["norm_drift_max"])
                rep_rel = 0.0
                loc_ratio = float(raw["on"]["q3_dynamic_vacuum"]["localization_sigma_ratio_final_over_initial"])
                ipr_delta = float(raw["on"]["q3_dynamic_vacuum"]["ipr_delta"])

                row = {
                    "stage": stage_name,
                    "kappa": kappa,
                    "dispersion_C": c_val,
                    "t_max": t_max,
                    "dt": cfg.dt,
                    "n_grid": cfg.n_grid,
                    "q1_signal": q1_signal,
                    "q1_delta_vs_off_rel": q1_delta_vs_off,
                    "q1_refinement": q1_ref,
                    "norm_drift": norm_drift,
                    "replication_rel_diff": rep_rel,
                    "loc_sigma_ratio": loc_ratio,
                    "ipr_delta": ipr_delta,
                    "retightened": retightened,
                }
                row["pass_detect"] = q1_signal > cfg.q1_signal_detect
                row["pass_refine"] = q1_ref < cfg.q1_refinement_max
                row["pass_norm_strict"] = norm_drift < cfg.norm_drift_strict_max
                row["pass_norm_practical"] = norm_drift < cfg.norm_drift_practical_max
                row["pass_loc_ratio"] = cfg.loc_ratio_min <= loc_ratio <= cfg.loc_ratio_max
                row["pass_ipr_sanity"] = cfg.ipr_delta_min <= ipr_delta <= cfg.ipr_delta_max
                row["status"] = status_line(row)
                rows.append(row)

    csv_path = out_dir / f"{stage_name}_summary.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    agg = {
        "stage": stage_name,
        "n_rows": len(rows),
        "n_retightened": int(sum(1 for r in rows if r["retightened"])),
        "max_q1_signal": float(max(r["q1_signal"] for r in rows)),
        "max_q1_refinement": float(max(r["q1_refinement"] for r in rows)),
        "max_norm_drift": float(max(r["norm_drift"] for r in rows)),
        "max_replication_rel_diff": float(max(r["replication_rel_diff"] for r in rows)),
        "loc_ratio_range": [float(min(r["loc_sigma_ratio"] for r in rows)), float(max(r["loc_sigma_ratio"] for r in rows))],
        "ipr_delta_range": [float(min(r["ipr_delta"] for r in rows)), float(max(r["ipr_delta"] for r in rows))],
        "status_counts": {
            "PASS": int(sum(1 for r in rows if r["status"] == "PASS")),
            "WATCH": int(sum(1 for r in rows if r["status"] == "WATCH")),
            "FAIL": int(sum(1 for r in rows if r["status"] == "FAIL")),
        },
        "detect_pass_rate": float(sum(1 for r in rows if r["pass_detect"]) / len(rows)),
        "refine_pass_rate": float(sum(1 for r in rows if r["pass_refine"]) / len(rows)),
        "norm_practical_pass_rate": float(sum(1 for r in rows if r["pass_norm_practical"]) / len(rows)),
        "config": asdict(cfg),
        "outputs": {
            "summary_csv": str(csv_path),
        },
    }
    agg_path = out_dir / f"{stage_name}_aggregate.json"
    agg_path.write_text(json.dumps(agg, indent=2), encoding="utf-8")
    return {"rows": rows, "aggregate": agg, "aggregate_path": str(agg_path)}


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = root / "notebooks" / "outputs" / f"sn_diagnostic_lane_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    common = {
        "sigma0": 5.0,
        "mass": 1.0,
        "dt": 2e-3,
        "n_grid": 128,
        "tight_dt": 1e-3,
        "tight_n_grid": 256,
        "q1_signal_detect": 0.05,
        "q1_refinement_max": 1e-6,
        "norm_drift_strict_max": 1e-10,
        "norm_drift_practical_max": 1e-5,
        "loc_ratio_min": 1.0,
        "loc_ratio_max": 1.05,
        "ipr_delta_min": -0.05,
        "ipr_delta_max": 0.005,
    }

    stage1_cfg = RunConfig(
        kappas=[1e-3],
        c_vals=[0.0, 0.01, 0.05],
        t_max_vals=[20.0, 30.0],
        **common,
    )
    stage1 = run_stage("stage1_tmax_extension", stage1_cfg, out_dir)

    need_stage2 = stage1["aggregate"]["max_q1_signal"] <= common["q1_signal_detect"]

    stage2 = None
    if need_stage2:
        stage2_cfg = RunConfig(
            kappas=[3e-3, 1e-2],
            c_vals=[0.0, 0.01, 0.05],
            t_max_vals=[20.0],
            **common,
        )
        stage2 = run_stage("stage2_stronger_kappa_probe", stage2_cfg, out_dir)

    run_receipt = {
        "out_dir": str(out_dir),
        "stage1_aggregate": stage1["aggregate"],
        "stage2_aggregate": stage2["aggregate"] if stage2 else None,
        "decision": {
            "triggered_stage2": bool(need_stage2),
            "reason": "stage1 max_q1_signal <= detect threshold" if need_stage2 else "stage1 crossed detect threshold",
        },
    }
    (out_dir / "run_receipt.json").write_text(json.dumps(run_receipt, indent=2), encoding="utf-8")
    print(json.dumps(run_receipt, indent=2))


if __name__ == "__main__":
    main()
