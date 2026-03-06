from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str, rel_path: str):
    path = ROOT / rel_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_symbolic_ratio_receipt_function_smoke():
    mod = _load_module("wdw_symbolic_receipt", "notebooks/wdw_symbolic_correction_ratio_receipt.py")
    p = mod.Params(omega_m=0.3, omega_l=0.7, alpha_qg=1e-7)
    row = mod.correction_to_classical_ratio(a=1e-2, p=p, correction_power=5)

    assert set(row.keys()) == {"classical", "correction", "ratio_signed", "ratio_abs"}
    assert row["ratio_abs"] >= 0.0


def test_core_edge_summarize_case_smoke():
    mod = _load_module("wdw_core_edge_diag", "notebooks/wdw_core_edge_diagnostic_pack.py")
    row = mod.summarize_case(omega_m=0.300, omega_label="core_0p300", correction_power=5)

    required = {
        "omega_label",
        "omega_m",
        "delta_proxy_l2",
        "traj_ratio_abs_max",
        "path_nonnegative",
    }
    assert required.issubset(set(row.keys()))
    assert row["delta_proxy_l2"] > 0.0
    assert row["traj_ratio_abs_max"] >= row["traj_ratio_abs_min"]


def test_dual_receipt_acceptance_logic_smoke(tmp_path: Path):
    mod = _load_module("cgrqm002_dual_audit", "notebooks/cgrqm002_dual_receipt_audit.py")

    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True)
    (run_dir / "summary.json").write_text(
        json.dumps(
            {
                "n_points": 9,
                "all_points_pass": True,
                "global_max_q2_D_p95": 0.1,
                "global_max_q2_D_p99": 0.2,
                "global_max_rk_family_abs_spread_p95": 1e-10,
                "global_max_replication_rel_diff": 1e-9,
            }
        ),
        encoding="utf-8",
    )

    metrics = mod.load_metrics(run_dir)
    assert mod.acceptance_pass(metrics) is True
