from __future__ import annotations

import traceback
import numpy as np
from scipy.integrate import solve_ivp

omega_m = 0.3075
alpha_qg = 7e-7

def rhs(_t, y, omega_m: float, alpha_qg: float, corrected: bool, correction_power: int = 5):
    a, v = y
    if a <= 0:
        return [0.0, 0.0]
    base = -(omega_m) / (2.0 * a * a) + (1.0 - omega_m) * a
    corr = alpha_qg / (a**correction_power) if corrected else 0.0
    return [v, base + corr]

calls = []

def integrate(omega_m, alpha_qg, use_approx, method='Radau', t_span=None, rtol=1e-11, atol=1e-13, a0=1.0, v0=0.0):
    if t_span is None:
        t_span = (0.0, 3.0)
    if method not in ['Radau', 'LSODA']:
        method = 'Radau'

    stiffness_factor = 1 + 10 * (omega_m - 0.30)
    max_step = 1e-4 / stiffness_factor
    first_step = 1e-6 / stiffness_factor
    event_floor = 1e-7

    def event_stop(t, y):
        return y[0] - event_floor
    event_stop.terminal = True
    event_stop.direction = -1

    def scaled_rhs(t, y):
        dy = rhs(t, y, omega_m, alpha_qg, use_approx)
        scale = 1.0 / (1.0 + 1e-3 * np.linalg.norm(y)**2)
        a, v = float(y[0]), float(y[1])
        classical = -(omega_m) / (2.0 * a * a) + (1.0 - omega_m) * a if a > 0 else float('nan')
        corr = alpha_qg / (a**5) if (a > 0 and use_approx) else 0.0
        calls.append({
            't': float(t), 'a': a, 'v': v,
            'classical': float(classical), 'correction': float(corr),
            'corr_ratio': float(abs(corr) / (abs(classical) + 1e-30)) if a > 0 else float('inf')
        })
        return np.asarray(dy) * scale

    sol = solve_ivp(
        fun=scaled_rhs,
        t_span=t_span,
        y0=[a0, v0],
        method=method,
        rtol=rtol,
        atol=atol,
        max_step=max_step,
        first_step=first_step,
        events=event_stop,
        dense_output=False,
    )
    return sol

if __name__ == '__main__':
    try:
        sol = integrate(omega_m, alpha_qg, True, method='Radau', t_span=(0.0, 3.0), rtol=1e-10, atol=1e-12, a0=0.1, v0=1.5)
        print('success:', sol.success)
        print('message:', sol.message)
        print('t_end:', sol.t[-1])
        print('a_end:', sol.y[0, -1])
    except Exception:
        traceback.print_exc()
    finally:
        print('last_calls:')
        for row in calls[-20:]:
            print(row)
