from __future__ import annotations

import numpy as np

from grqm.bohmian_probe.guidance import BohmianParams, classical_accel, guidance_rhs, guarded_quantum_accel, integrate_fixed


def test_guidance_rhs_returns_finite_state_derivative_above_floor():
    p = BohmianParams(epsilon_q=0.25, quantum_model="gaussian")
    y = np.array([0.2, 0.01, 1.5, 0.0], dtype=float)

    rhs = guidance_rhs(0.0, y, p)

    assert rhs.shape == (4,)
    assert np.all(np.isfinite(rhs))
    assert rhs[0] == y[2]
    assert rhs[1] == y[3]


def test_guidance_rhs_freezes_below_floor():
    p = BohmianParams(a_floor=1e-6)
    y = np.array([1e-7, 0.0, 1.0, 1.0], dtype=float)

    rhs = guidance_rhs(0.0, y, p)

    assert np.array_equal(rhs, np.zeros(4, dtype=float))


def test_guarded_quantum_accel_respects_configured_bound():
    p = BohmianParams(epsilon_q=1.0, quantum_model="gaussian", max_quantum_accel_ratio=0.1)
    a = 0.15
    phi = 0.02

    q = guarded_quantum_accel(a, phi, p)
    c = classical_accel(a, phi, p)
    bound = p.max_quantum_accel_ratio * (abs(c) + 1e-12)

    assert np.isfinite(q)
    assert abs(q) <= bound + 1e-12


def test_integrate_fixed_returns_finite_trajectory_for_smoke_case():
    p = BohmianParams(epsilon_q=0.25, quantum_model="plateau")
    y0 = np.array([0.1, 0.01, 1.5, 0.0], dtype=float)

    t, y = integrate_fixed(0.0, 0.2, 0.01, y0, p, method="rk4")

    assert t.ndim == 1
    assert y.ndim == 2
    assert y.shape == (len(t), 4)
    assert np.all(np.isfinite(y))
    assert np.all(y[:, 0] >= p.a_floor)
