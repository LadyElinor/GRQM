from __future__ import annotations

from pathlib import Path

from grqm.core import run_cycle


def _run(tmp_path: Path):
    out = tmp_path / "run"
    return run_cycle(out)


def test_refinement_residuals_pass_threshold(tmp_path: Path):
    r = _run(tmp_path)
    assert r["q1"]["baseline_refinement_error"] < 5e-3
    assert r["q1"]["corrected_refinement_error"] < 5e-3


def test_proxy_signal_persists(tmp_path: Path):
    r = _run(tmp_path)
    assert r["q1"]["delta_proxy_l2"] > 1e-4


def test_deterministic_repeatability(tmp_path: Path):
    r1 = _run(tmp_path / "a")
    r2 = _run(tmp_path / "b")
    assert r1["q1"]["delta_proxy_l2"] == r2["q1"]["delta_proxy_l2"]
    assert r1["q2"]["D_star"] == r2["q2"]["D_star"]
