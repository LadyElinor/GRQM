"""
BoO branch starter (conservative scaffold).

Purpose:
- Reuse existing toy-model integrator to create a first Born-Oppenheimer-style
  slow/fast diagnostic table on the core corridor.
- No gate policy changes, no claim-state changes.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import csv
import numpy as np

from grqm_proxy_toymodel_v1 import IC, Params, RunConfig, integrate, l2_rel_err


def moving_average(x: np.ndarray, win: int = 21) -> np.ndarray:
    win = max(3, int(win) | 1)  # odd, >=3
    pad = win // 2
    xpad = np.pad(x, (pad, pad), mode="edge")
    kernel = np.ones(win, dtype=float) / float(win)
    return np.convolve(xpad, kernel, mode="valid")


def boo_diagnostics(a_baseline: np.ndarray, a_corrected: np.ndarray) -> tuple[float, float]:
    delta = a_corrected - a_baseline
    slow = moving_average(delta, win=21)
    fast = delta - slow
    slow_l2 = l2_rel_err(slow, a_baseline)
    fast_rms = float(np.sqrt(np.mean(fast ** 2)))
    return float(slow_l2), fast_rms


def run() -> Path:
    omega_list = [0.285, 0.290, 0.295, 0.300]
    alpha_list = [3e-7, 5e-7, 7e-7, 1e-6, 1.3e-6]

    ic = IC()
    dt = 1.0e-3

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(__file__).resolve().parent / "outputs" / f"grqm_boo_branch_starter_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / "boo_branch_summary.csv"

    rows = []
    for om in omega_list:
        for aq in alpha_list:
            p = Params(omega_m=om, omega_l=1.0 - om, alpha_qg=aq)
            _, a_b, _ = integrate(ic, p, RunConfig(dt=dt, method="rk4", corrected=False))
            _, a_c, _ = integrate(ic, p, RunConfig(dt=dt, method="rk4", corrected=True))

            q1_proxy_l2 = l2_rel_err(a_c - a_b, a_b)
            boo_slow_l2, boo_fast_rms = boo_diagnostics(a_b, a_c)

            rows.append(
                {
                    "omega_m": om,
                    "alpha_qg": aq,
                    "q1_proxy_l2": q1_proxy_l2,
                    "boo_slow_l2": boo_slow_l2,
                    "boo_fast_rms": boo_fast_rms,
                    "fast_to_slow_ratio": boo_fast_rms / (abs(boo_slow_l2) + 1e-15),
                }
            )

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"[boo-branch] wrote {out_csv}")
    return out_dir


if __name__ == "__main__":
    run()
