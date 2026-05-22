from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np

from grqm.core import IC, Params, RunConfig, accel, integrate

from .guidance import BohmianParams, classical_accel, guarded_quantum_accel, integrate_fixed


@dataclass(frozen=True)
class Phase2Config:
    omega_grid: tuple[float, ...] = tuple(np.round(np.arange(0.295, 0.315 + 1e-12, 0.0025), 4))
    amplitude_grid: tuple[float, ...] = tuple(np.geomspace(3e-7, 2e-6, 12))
    q_models: tuple[str, ...] = ("off", "gaussian", "plateau", "unified_dmde_proxy")
    t0: float = 0.0
    t1: float = 2.0
    dt_main: float = 5e-4
    dt_ref: float = 2.5e-4
    dt_stress: float = 1e-3
    a_floor: float = 1e-6
    max_abs_state: float = 1e6
    refinement_gate: float = 1e-6
    correction_ratio_gate: float = 1.0
    null_gate: float = 1e-8


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def l2_rel(x: np.ndarray, y: np.ndarray, eps: float = 1e-15) -> float:
    return float(np.sqrt(np.mean((x - y) ** 2)) / (np.sqrt(np.mean(y**2)) + eps))


def _interp_to_ref(t_ref: np.ndarray, t: np.ndarray, x: np.ndarray) -> np.ndarray:
    return np.interp(t_ref, t, x)


def _turning_metrics(a: np.ndarray, v: np.ndarray) -> tuple[int, bool]:
    v_prev = v[:-1]
    v_next = v[1:]
    idx = np.where((v_prev > 0.0) & (v_next <= 0.0) | (v_prev < 0.0) & (v_next >= 0.0))[0]
    n_turn = int(idx.size)
    if n_turn == 0:
        return 0, False
    scale = float(np.median(np.abs(a)) + 1e-12)
    blowup = False
    for i in idx:
        lo = max(0, i - 3)
        hi = min(len(a), i + 4)
        if not np.all(np.isfinite(a[lo:hi])) or float(np.max(np.abs(a[lo:hi]))) > 10.0 * scale:
            blowup = True
            break
    return n_turn, blowup


def _integrate_alpha(omega_m: float, alpha_qg: float, dt: float, method: str, cfg: Phase2Config):
    p = Params(omega_m=omega_m, omega_l=0.7, alpha_qg=alpha_qg)
    ic = IC(t0=cfg.t0, t1=cfg.t1, a0=0.1, v0=1.5)

    if method in {"euler", "rk4"}:
        t, a, v = integrate(ic, p, RunConfig(dt=dt, method=method, corrected=True, correction_power=5))
    elif method == "heun":
        n = int(round((cfg.t1 - cfg.t0) / dt))
        t = np.linspace(cfg.t0, cfg.t1, n + 1)
        y = np.zeros((n + 1, 2), dtype=float)
        y[0] = np.array([ic.a0, ic.v0], dtype=float)
        for i in range(n):
            if y[i, 0] <= cfg.a_floor or not np.all(np.isfinite(y[i])):
                y[i + 1 :] = y[i]
                break
            a0, v0 = y[i]
            k1 = np.array([v0, accel(float(a0), p, corrected=True, correction_power=5)], dtype=float)
            yp = y[i] + dt * k1
            k2 = np.array([yp[1], accel(float(max(yp[0], cfg.a_floor)), p, corrected=True, correction_power=5)], dtype=float)
            y[i + 1] = y[i] + 0.5 * dt * (k1 + k2)
        a = y[:, 0]
        v = y[:, 1]
    else:
        raise ValueError(f"Unknown alpha lane method: {method}")

    classical = -(omega_m) / (2.0 * np.maximum(a, cfg.a_floor) ** 2) + 0.7 * a
    corr = alpha_qg / (np.maximum(a, cfg.a_floor) ** 5)
    ratio = np.abs(corr) / (np.abs(classical) + 1e-15)
    max_ratio = float(np.max(ratio))

    finite = bool(np.all(np.isfinite(a)) and np.all(np.isfinite(v)))
    stable = bool(finite and float(np.max(np.abs(a))) < cfg.max_abs_state)
    n_turn, blowup = _turning_metrics(a, v)

    return {
        "t": t,
        "a": a,
        "v": v,
        "stable": stable and (not blowup),
        "blowup_near_turning": bool(blowup),
        "turning_points": n_turn,
        "max_corr_ratio": max_ratio,
        "final_a": float(a[-1]),
    }


def _integrate_q(omega_m: float, epsilon_q: float, model: str, dt: float, method: str, cfg: Phase2Config):
    p = BohmianParams(
        omega_m=omega_m,
        omega_l=0.7,
        epsilon_q=epsilon_q,
        quantum_model=model,
        a_floor=cfg.a_floor,
        max_abs_state=cfg.max_abs_state,
    )
    y0 = np.array([0.1, 0.01, 1.5, 0.0], dtype=float)
    t, y = integrate_fixed(cfg.t0, cfg.t1, dt, y0, p, method=method)
    a = y[:, 0]
    phi = y[:, 1]
    va = y[:, 2]

    classical = np.array([classical_accel(ai, phii, p) for ai, phii in zip(a, phi)], dtype=float)
    corr = np.array([guarded_quantum_accel(ai, phii, p) for ai, phii in zip(a, phi)], dtype=float)
    ratio = np.abs(corr) / (np.abs(classical) + 1e-15)

    finite = bool(np.all(np.isfinite(y)))
    stable = bool(finite and float(np.max(np.abs(y))) < cfg.max_abs_state)
    n_turn, blowup = _turning_metrics(a, va)

    return {
        "t": t,
        "a": a,
        "va": va,
        "stable": stable and (not blowup),
        "blowup_near_turning": bool(blowup),
        "turning_points": n_turn,
        "max_corr_ratio": float(np.max(ratio)),
        "final_a": float(a[-1]),
    }


def _cfg_to_dict(cfg: Phase2Config) -> dict:
    return {
        "omega_grid": [float(x) for x in cfg.omega_grid],
        "amplitude_grid": [float(x) for x in cfg.amplitude_grid],
        "q_models": list(cfg.q_models),
        "t0": float(cfg.t0),
        "t1": float(cfg.t1),
        "dt_main": float(cfg.dt_main),
        "dt_ref": float(cfg.dt_ref),
        "dt_stress": float(cfg.dt_stress),
        "a_floor": float(cfg.a_floor),
        "max_abs_state": float(cfg.max_abs_state),
        "refinement_gate": float(cfg.refinement_gate),
        "correction_ratio_gate": float(cfg.correction_ratio_gate),
        "null_gate": float(cfg.null_gate),
    }


def run_phase2(out_dir: Path, cfg: Phase2Config | None = None) -> dict:
    cfg = cfg or Phase2Config()
    out_dir.mkdir(parents=True, exist_ok=True)

    boundary_rows: list[dict] = []
    stress_rows: list[dict] = []
    null_rows: list[dict] = []
    variant_rows: list[dict] = []

    widths_alpha: dict[float, list[float]] = {om: [] for om in cfg.omega_grid}
    widths_q_gauss: dict[float, list[float]] = {om: [] for om in cfg.omega_grid}

    max_refinement = 0.0
    max_corr_ratio = 0.0
    unstable = 0
    total = 0

    pivot_amp = float(np.geomspace(cfg.amplitude_grid[0], cfg.amplitude_grid[-1], 3)[1])

    for om in cfg.omega_grid:
        # Null checks: off/zero-amplitude equivalence
        q_off = _integrate_q(om, 0.0, "off", cfg.dt_main, "rk4", cfg)
        for model in cfg.q_models:
            q_zero = _integrate_q(om, 0.0, model, cfg.dt_main, "rk4", cfg)
            null_l2 = l2_rel(q_zero["a"], q_off["a"])
            null_rows.append(
                {
                    "omega_m": om,
                    "lane": "bohmian_q",
                    "null_type": f"{model}_at_zero_amplitude_vs_off",
                    "l2": null_l2,
                    "threshold": cfg.null_gate,
                    "passes": bool(null_l2 <= cfg.null_gate),
                }
            )

        alpha_zero = _integrate_alpha(om, 0.0, cfg.dt_main, "rk4", cfg)
        alpha_null_l2 = l2_rel(alpha_zero["a"], q_off["a"])
        null_rows.append(
            {
                "omega_m": om,
                "lane": "cross_lane",
                "null_type": "alpha_zero_vs_q_off",
                "l2": alpha_null_l2,
                "threshold": cfg.null_gate,
                "passes": bool(alpha_null_l2 <= cfg.null_gate),
            }
        )

        # Solver stress invariance at pivot amplitude
        for lane, model in (("alpha_qg", "n/a"), ("bohmian_q", "gaussian"), ("bohmian_q", "plateau"), ("bohmian_q", "unified_dmde_proxy")):
            ref = (
                _integrate_alpha(om, pivot_amp, cfg.dt_ref, "rk4", cfg)
                if lane == "alpha_qg"
                else _integrate_q(om, pivot_amp, model, cfg.dt_ref, "rk4", cfg)
            )
            methods = ("euler", "heun", "rk4")
            for method in methods:
                run = (
                    _integrate_alpha(om, pivot_amp, cfg.dt_stress, method, cfg)
                    if lane == "alpha_qg"
                    else _integrate_q(om, pivot_amp, model, cfg.dt_stress, method, cfg)
                )
                a_on_ref = _interp_to_ref(ref["t"], run["t"], run["a"])
                stress_rows.append(
                    {
                        "omega_m": om,
                        "lane": lane,
                        "quantum_model": model,
                        "amplitude": pivot_amp,
                        "method": method,
                        "l2_vs_rk4_ref": l2_rel(a_on_ref, ref["a"]),
                        "stable": run["stable"],
                        "blowup_near_turning": run["blowup_near_turning"],
                    }
                )

        for amp in cfg.amplitude_grid:
            # alpha_qg lane
            alpha_main = _integrate_alpha(om, float(amp), cfg.dt_main, "rk4", cfg)
            alpha_ref = _integrate_alpha(om, float(amp), cfg.dt_ref, "rk4", cfg)
            a_main_on_ref = _interp_to_ref(alpha_ref["t"], alpha_main["t"], alpha_main["a"])
            ref_l2 = l2_rel(a_main_on_ref, alpha_ref["a"])

            max_refinement = max(max_refinement, ref_l2)
            max_corr_ratio = max(max_corr_ratio, alpha_main["max_corr_ratio"])
            total += 1
            if (not alpha_main["stable"]) or ref_l2 > cfg.refinement_gate or alpha_main["max_corr_ratio"] > cfg.correction_ratio_gate:
                unstable += 1

            widths_alpha[om].append(alpha_main["final_a"])
            boundary_rows.append(
                {
                    "omega_m": om,
                    "lane": "alpha_qg",
                    "quantum_model": "n/a",
                    "amplitude": float(amp),
                    "stable": alpha_main["stable"],
                    "refinement_l2": ref_l2,
                    "max_correction_ratio": alpha_main["max_corr_ratio"],
                    "turning_points": alpha_main["turning_points"],
                    "blowup_near_turning": alpha_main["blowup_near_turning"],
                    "final_a": alpha_main["final_a"],
                    "passes_refinement_gate": bool(ref_l2 <= cfg.refinement_gate),
                    "passes_ratio_gate": bool(alpha_main["max_corr_ratio"] <= cfg.correction_ratio_gate),
                }
            )

            # Bohmian-Q lane variants
            for model in cfg.q_models:
                q_main = _integrate_q(om, float(amp), model, cfg.dt_main, "rk4", cfg)
                q_ref = _integrate_q(om, float(amp), model, cfg.dt_ref, "rk4", cfg)
                q_on_ref = _interp_to_ref(q_ref["t"], q_main["t"], q_main["a"])
                q_ref_l2 = l2_rel(q_on_ref, q_ref["a"])

                max_refinement = max(max_refinement, q_ref_l2)
                max_corr_ratio = max(max_corr_ratio, q_main["max_corr_ratio"])
                total += 1
                if (not q_main["stable"]) or q_ref_l2 > cfg.refinement_gate or q_main["max_corr_ratio"] > cfg.correction_ratio_gate:
                    unstable += 1

                if model == "gaussian":
                    widths_q_gauss[om].append(q_main["final_a"])

                boundary_rows.append(
                    {
                        "omega_m": om,
                        "lane": "bohmian_q",
                        "quantum_model": model,
                        "amplitude": float(amp),
                        "stable": q_main["stable"],
                        "refinement_l2": q_ref_l2,
                        "max_correction_ratio": q_main["max_corr_ratio"],
                        "turning_points": q_main["turning_points"],
                        "blowup_near_turning": q_main["blowup_near_turning"],
                        "final_a": q_main["final_a"],
                        "passes_refinement_gate": bool(q_ref_l2 <= cfg.refinement_gate),
                        "passes_ratio_gate": bool(q_main["max_corr_ratio"] <= cfg.correction_ratio_gate),
                    }
                )

        # Variant sensitivity at pivot amplitude
        alpha_n5 = _integrate_alpha(om, pivot_amp, cfg.dt_main, "rk4", cfg)
        p_n4 = Params(omega_m=om, omega_l=0.7, alpha_qg=pivot_amp)
        ic = IC(t0=cfg.t0, t1=cfg.t1, a0=0.1, v0=1.5)
        t_n4, a_n4, _ = integrate(ic, p_n4, RunConfig(dt=cfg.dt_main, method="rk4", corrected=True, correction_power=4))
        variant_rows.append(
            {
                "omega_m": om,
                "lane": "alpha_qg",
                "variant": "correction_power_4_vs_5",
                "amplitude": pivot_amp,
                "l2": l2_rel(a_n4, alpha_n5["a"]),
            }
        )
        q_gauss = _integrate_q(om, pivot_amp, "gaussian", cfg.dt_main, "rk4", cfg)
        for model in ("plateau", "unified_dmde_proxy"):
            q_alt = _integrate_q(om, pivot_amp, model, cfg.dt_main, "rk4", cfg)
            variant_rows.append(
                {
                    "omega_m": om,
                    "lane": "bohmian_q",
                    "variant": f"{model}_vs_gaussian",
                    "amplitude": pivot_amp,
                    "l2": l2_rel(q_alt["a"], q_gauss["a"]),
                }
            )

    # Envelope widths (final_a spread across amplitudes)
    width_alpha = {str(k): float(np.max(v) - np.min(v)) for k, v in widths_alpha.items()}
    width_q = {str(k): float(np.max(v) - np.min(v)) for k, v in widths_q_gauss.items()}
    rel_width = {
        k: float(width_q[k] / (width_alpha[k] + 1e-15)) for k in width_alpha.keys()
    }

    max_null_l2 = max(float(r["l2"]) for r in null_rows)
    max_stress_l2 = max(float(r["l2_vs_rk4_ref"]) for r in stress_rows)
    unstable_rate = float(unstable / total) if total else 1.0

    refinement_gate_pass = bool(max_refinement <= cfg.refinement_gate)
    ratio_gate_pass = bool(max_corr_ratio <= cfg.correction_ratio_gate)
    null_gate_pass = bool(max_null_l2 <= cfg.null_gate)
    stability_gate_pass = bool(unstable_rate == 0.0)

    rec = "PASS_FOUNDATION" if all((refinement_gate_pass, ratio_gate_pass, null_gate_pass, stability_gate_pass)) else "HOLD_FOUNDATION"
    rationale = (
        "All extended numerical gates pass on the configured envelope-comparison grid."
        if rec == "PASS_FOUNDATION"
        else "At least one extended gate failed; retain HOLD pending tighter numerics or narrower operating region."
    )

    write_csv(out_dir / "01_boundary_map_comparison.csv", boundary_rows)
    write_csv(out_dir / "02_solver_stress.csv", stress_rows)
    write_csv(out_dir / "03_null_checks.csv", null_rows)
    write_csv(out_dir / "04_variant_sensitivity.csv", variant_rows)

    summary = {
        "timestamp": datetime.now().isoformat(),
        "config": _cfg_to_dict(cfg),
        "metrics": {
            "max_refinement_l2": max_refinement,
            "max_correction_ratio": max_corr_ratio,
            "max_null_l2": max_null_l2,
            "max_solver_stress_l2": max_stress_l2,
            "unstable_rate": unstable_rate,
            "total_cases": total,
            "failed_cases": unstable,
            "envelope_width_final_a": {
                "alpha_qg": width_alpha,
                "bohmian_q_gaussian": width_q,
                "relative_q_over_alpha": rel_width,
            },
        },
        "notes": {
            "q_model_unified_mode": "unified_dmde_proxy",
            "q_model_caveat": "No exact unified DM/DE potential is currently available in this lane; using weighted gaussian+plateau proxy.",
            "claim_scope": "Internal numerical/governance diagnostics only. No observational-fit claim.",
        },
    }
    decision = {
        "recommendation": rec,
        "rationale": rationale,
        "gates": {
            "refinement_error_le_1e-6": refinement_gate_pass,
            "correction_ratio_le_1": ratio_gate_pass,
            "null_checks": null_gate_pass,
            "stability_and_blowup": stability_gate_pass,
            "max_refinement_l2": max_refinement,
            "max_correction_ratio": max_corr_ratio,
            "max_null_l2": max_null_l2,
            "unstable_rate": unstable_rate,
        },
        "caveats": [
            "unified_dmde_proxy is a traceable approximation, not an exact symbolic unified potential.",
            "Results are deterministic minisuperspace diagnostics and should not be over-interpreted as empirical evidence.",
            "Solver-stress table is a numerical robustness probe, not a proof of uniqueness.",
        ],
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out_dir / "decision.json").write_text(json.dumps(decision, indent=2), encoding="utf-8")

    md = [
        "# Phase-2 Bohmian Envelope Comparison (alpha_qg vs Bohmian-Q)",
        "",
        f"- Recommendation: **{rec}**",
        f"- Rationale: {rationale}",
        "",
        "## Extended Gates",
        f"- Max refinement L2 (target <= {cfg.refinement_gate:.1e}): {max_refinement:.3e}",
        f"- Max |correction|/|classical| (target <= {cfg.correction_ratio_gate:.1f}): {max_corr_ratio:.3e}",
        f"- Max null-check L2 (target <= {cfg.null_gate:.1e}): {max_null_l2:.3e}",
        f"- Unstable/blowup rate (target 0): {unstable_rate:.3f}",
        "",
        "## Envelope Width (final_a spread across amplitude grid)",
    ]
    for om in cfg.omega_grid:
        key = str(om)
        md.append(
            f"- omega_m={om:.4f}: alpha={width_alpha[key]:.3e}, Q(gaussian)={width_q[key]:.3e}, rel(Q/alpha)={rel_width[key]:.3e}"
        )
    md += [
        "",
        "## Caveats",
        "- 'unified_dmde_proxy' is used because an exact unified symbolic lane is not yet available.",
        "- Numerical diagnostics are governance-facing quality checks, not observational confirmation.",
    ]
    (out_dir / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    return {"summary": summary, "decision": decision, "out_dir": str(out_dir)}


def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path("outputs") / f"bohmian_envelope_comparison_{ts}"
    result = run_phase2(out)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
