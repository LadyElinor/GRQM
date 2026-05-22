from __future__ import annotations

import numpy as np

from grqm.models import SNParams, run_sn_1d
from grqm.solvers import poisson_solve_periodic_1d, split_step_sn_1d


def test_poisson_solve_periodic_1d_returns_zero_mean_field_for_constant_density():
    rho = np.ones(32, dtype=float)
    phi = poisson_solve_periodic_1d(rho, dx=0.5, kappa=0.02)

    assert phi.shape == rho.shape
    assert np.all(np.isfinite(phi))
    assert abs(float(np.mean(phi))) <= 1e-10


def test_split_step_sn_1d_smoke_shapes_and_finiteness():
    x = np.linspace(-5.0, 5.0, 64)
    psi0 = np.exp(-(x**2)).astype(complex)
    psi0 = psi0 / np.sqrt(np.trapezoid(np.abs(psi0) ** 2, x))

    psi_hist, phi_hist = split_step_sn_1d(
        psi0=psi0,
        dt=1e-3,
        n_steps=8,
        x=x,
        mass=1.0,
        hbar=1.0,
        kappa=0.02,
    )

    assert psi_hist.shape == (9, x.size)
    assert phi_hist.shape == (9, x.size)
    assert np.all(np.isfinite(psi_hist))
    assert np.all(np.isfinite(phi_hist))


def test_run_sn_1d_returns_expected_receipt_structure():
    params = SNParams(n_grid=64, x_max=8.0, t_max=0.02, dt=1e-3, kappa=0.01)
    result = run_sn_1d(params, seed=0)

    assert result["metadata"]["model"] == "schrodinger-newton-1d-toy"
    assert result["grid"]["n_grid"] == 64
    assert len(result["series"]["t"]) == result["grid"]["n_steps"] + 1
    assert len(result["series"]["sigma_sn"]) == len(result["series"]["t"])
    assert np.isfinite(result["q1"]["sigma_deviation_max"])
    assert np.isfinite(result["q2"]["refinement_rel_diff"])
    assert np.isfinite(result["q2"]["norm_drift_max"])
