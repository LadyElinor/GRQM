from __future__ import annotations

"""Toy Bohmian minisuperspace guidance dynamics.

This lane is intentionally a bounded exploratory proxy, not a full Wheeler-DeWitt,
LQC, or validated GR cosmology implementation.

Key audit notes:
- `a_floor` is a numerical domain guard enforcing `a > 0`.
- `max_quantum_accel_ratio` clips the quantum correction relative to the
  classical acceleration, which improves containment but can mask physically
  informative boundary/failure behavior if not reported.
- The scalar-sector dynamics are local and proxy-like; interpretation should
  stay inside that stated regime.
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BohmianParams:
    omega_m: float = 0.3
    omega_l: float = 0.7
    epsilon_q: float = 0.0
    m_phi: float = 1.0
    hbar: float = 1.0
    a_floor: float = 1e-6
    quantum_model: str = "gaussian"
    q_shape: float = 1.0
    q_scale: float = 1.0
    max_quantum_accel_ratio: float = 0.85
    max_abs_state: float = 1e6


def classical_accel(a: float, phi: float, p: BohmianParams) -> float:
    vphi = p.omega_l + 0.5 * p.m_phi * p.m_phi * phi * phi
    return -(p.omega_m) / (2.0 * a * a) + vphi * a


def _gaussian_q(aa: float, phi: float, p: BohmianParams) -> float:
    return -0.5 * p.hbar * p.hbar * np.exp(-((aa - 1.0) ** 2 + (p.q_shape * phi) ** 2))


def _plateau_q(aa: float, phi: float, p: BohmianParams) -> float:
    # Smoother, longer-tail profile for sensitivity checks.
    denom = 1.0 + (aa - 1.0) ** 2 + (p.q_shape * phi) ** 2
    return -0.5 * p.hbar * p.hbar / denom


def _unified_dmde_proxy_q(aa: float, phi: float, p: BohmianParams) -> float:
    """
    Closest traceable approximation to an exact unified DM/DE Bohmian potential in
    this reduced toy lane. We blend short-range (Gaussian) and long-tail (plateau)
    structure with FRW-density weighting from (omega_m, omega_l).
    """
    w_m = max(float(p.omega_m), 0.0)
    w_l = max(float(p.omega_l), 0.0)
    denom = w_m + w_l + 1e-15
    mix = float(np.clip(w_m / denom, 0.0, 1.0))
    return mix * _gaussian_q(aa, phi, p) + (1.0 - mix) * _plateau_q(aa, phi, p)


def quantum_potential(a: float, phi: float, p: BohmianParams) -> float:
    aa = max(float(a), p.a_floor)
    if p.quantum_model == "off" or p.epsilon_q == 0.0:
        return 0.0
    if p.quantum_model == "gaussian":
        q0 = _gaussian_q(aa, float(phi), p)
    elif p.quantum_model == "plateau":
        q0 = _plateau_q(aa, float(phi), p)
    elif p.quantum_model in {"unified_dmde", "unified_dmde_proxy"}:
        q0 = _unified_dmde_proxy_q(aa, float(phi), p)
    else:
        raise ValueError(f"Unknown quantum_model: {p.quantum_model}")
    return float(p.epsilon_q * p.q_scale * q0 / (aa * aa))


def guarded_quantum_accel(a: float, phi: float, p: BohmianParams) -> float:
    """Return a bounded quantum acceleration proxy.

    The bound is a governance/audit guard, not a derivation from first principles.
    Any result that depends materially on this clipping should be reported as
    guard-sensitive rather than treated as direct physical evidence.
    """
    q_raw = quantum_potential(a, phi, p)
    if p.max_quantum_accel_ratio <= 0.0:
        return 0.0
    c = classical_accel(a, phi, p)
    q_bound = p.max_quantum_accel_ratio * (abs(c) + 1e-12)
    return float(np.clip(q_raw, -q_bound, q_bound))


def guidance_rhs(_t: float, y: np.ndarray, p: BohmianParams) -> np.ndarray:
    a, phi, va, vphi = [float(v) for v in y]
    if a <= p.a_floor:
        return np.array([0.0, 0.0, 0.0, 0.0], dtype=float)

    a_dot = va
    phi_dot = vphi
    a_ddot = classical_accel(a, phi, p) + guarded_quantum_accel(a, phi, p)
    phi_ddot = -p.m_phi * p.m_phi * phi - 3.0 * (va / max(a, p.a_floor)) * vphi
    return np.array([a_dot, phi_dot, a_ddot, phi_ddot], dtype=float)


def integrate_fixed(t0: float, t1: float, dt: float, y0: np.ndarray, p: BohmianParams, method: str = "rk4"):
    n = int(round((t1 - t0) / dt))
    t = np.linspace(t0, t1, n + 1)
    y = np.zeros((n + 1, 4), dtype=float)
    y[0] = y0

    for i in range(n):
        if y[i, 0] <= p.a_floor:
            y[i + 1 :] = y[i]
            break
        if not np.all(np.isfinite(y[i])) or float(np.max(np.abs(y[i]))) > p.max_abs_state:
            y[i + 1 :] = y[i]
            break

        if method == "euler":
            y_next = y[i] + dt * guidance_rhs(t[i], y[i], p)
        elif method == "heun":
            k1 = guidance_rhs(t[i], y[i], p)
            k2 = guidance_rhs(t[i] + dt, y[i] + dt * k1, p)
            y_next = y[i] + 0.5 * dt * (k1 + k2)
        elif method == "rk4":
            k1 = guidance_rhs(t[i], y[i], p)
            k2 = guidance_rhs(t[i] + 0.5 * dt, y[i] + 0.5 * dt * k1, p)
            k3 = guidance_rhs(t[i] + 0.5 * dt, y[i] + 0.5 * dt * k2, p)
            k4 = guidance_rhs(t[i] + dt, y[i] + dt * k3, p)
            y_next = y[i] + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        else:
            raise ValueError(f"Unknown method: {method}")

        if not np.all(np.isfinite(y_next)):
            y[i + 1 :] = y[i]
            break

        # Reflective floor guard keeps the integrator in-domain numerically.
        # This is operationally useful, but future analyses should disclose when
        # boundary-touching trajectories are being regularized rather than allowed
        # to fail transparently.
        if y_next[0] <= p.a_floor:
            y_next = y_next.copy()
            y_next[0] = p.a_floor
            y_next[2] = abs(y_next[2]) * 0.25

        y[i + 1] = y_next

    return t, y
