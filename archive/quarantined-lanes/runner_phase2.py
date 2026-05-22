"""
QUARANTINED LANE: Bohmian phase-2 envelope comparison runner.

This file was moved out of the live canonical execution surface during the
2026-05-21 prune/coherence pass because it imports `grqm.core`, which is not
present in the reduced public repository.

Why quarantined instead of silently patched:
- the reduced GRQM public repo no longer claims the older full toy-model /
  multi-runner execution surface as live
- reconstructing `grqm.core` or adding compatibility shims would risk restoring
  older architecture implicitly rather than by explicit design decision

Restoration path:
- recover or deliberately recreate `grqm.core` from archival sources if this
  lane is intentionally reactivated
- then move this file back under `src/grqm/bohmian_probe/` with tests and docs
  updated accordingly
"""

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
    raise RuntimeError("runner_phase2.py is quarantined. Restore grqm.core intentionally before reactivating this lane.")


def main():
    raise RuntimeError("runner_phase2.py is quarantined. Restore grqm.core intentionally before reactivating this lane.")


if __name__ == "__main__":
    main()
