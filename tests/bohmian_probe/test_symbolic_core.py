from __future__ import annotations

import sympy as sp

from grqm.bohmian_probe.symbolic_core import (
    build_minisuperspace_hamiltonian,
    build_operator_set,
    build_symbols,
    scalar_potential,
    symbolic_receipt,
)


def test_scalar_potential_matches_declared_local_form():
    s = build_symbols()
    V = scalar_potential(s.phi, s.omega_l, s.m_phi)

    expected = s.omega_l + sp.Rational(1, 2) * s.m_phi**2 * s.phi**2
    assert sp.simplify(V - expected) == 0


def test_hamiltonian_and_operator_set_are_constructible():
    s = build_symbols()
    psi = sp.exp(-(s.a - 1) ** 2 - s.phi**2)

    H = build_minisuperspace_hamiltonian(s)
    ops = build_operator_set(psi, s)

    assert H.is_finite is not False
    assert ops.kinetic_a is not None
    assert ops.kinetic_phi is not None
    assert ops.potential is not None
    assert ops.wdw_total is not None


def test_symbolic_receipt_smoke_flags_stay_true():
    receipt = symbolic_receipt()

    assert receipt.model_label == "bohmian_minisuperspace_phase1_adaptation"
    assert receipt.branch_choice == "principal_arg"
    assert receipt.hamiltonian_finite_on_nominal_point is True
    assert receipt.decomposition_reconstruction_ok is True
    assert receipt.wdw_residual_nominal_finite is True
    assert len(receipt.assumptions) >= 4
