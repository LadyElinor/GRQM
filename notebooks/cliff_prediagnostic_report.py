from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean


def read_rows(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def f(x: str) -> float:
    return float(x)


def main():
    root = Path(__file__).resolve().parents[1]
    dense = root / "notebooks" / "outputs" / "grqm_cycle2_dense_followup_20260301_215901" / "envelope_summary.csv"
    edge = root / "notebooks" / "outputs" / "grqm_edge305_microbatch_dop853_20260302_174237" / "edge305_microbatch_summary.csv"

    dense_rows = read_rows(dense)
    edge_rows = read_rows(edge)

    core = [r for r in dense_rows if f(r["omega_m"]) <= 0.300 + 1e-12]
    edge305 = [r for r in dense_rows if abs(f(r["omega_m"]) - 0.305) < 1e-12]

    out = {
        "core_n": len(core),
        "edge305_n": len(edge305),
        "core_pass_all_rate": mean(1.0 if r["pass_all_envelope"].lower() == "true" else 0.0 for r in core),
        "edge305_pass_all_rate": mean(1.0 if r["pass_all_envelope"].lower() == "true" else 0.0 for r in edge305),
        "core_q1_refine_max": max(f(r["q1_refinement_max_obs"]) for r in core),
        "edge305_q1_refine_min": min(f(r["q1_refinement_max_obs"]) for r in edge305),
        "edge305_q1_refine_max": max(f(r["q1_refinement_max_obs"]) for r in edge305),
        "core_q2_p95_max": max(f(r["q2_D_p95"]) for r in core),
        "edge305_q2_p95_min": min(f(r["q2_D_p95"]) for r in edge305),
        "edge305_q2_p95_max": max(f(r["q2_D_p95"]) for r in edge305),
        "core_method_disagreement_mean": mean(f(r["q2_method_disagreement_rel_diff"]) for r in core),
        "edge305_method_disagreement_mean": mean(f(r["q2_method_disagreement_rel_diff"]) for r in edge305),
        "edge305_spike_detected_rate": mean(1.0 if r["q2_spike_detected"].lower() == "true" else 0.0 for r in edge305),
        "edge305_microbatch_q2_p95_max": max(f(r["q2_D_p95"]) for r in edge_rows),
        "edge305_microbatch_q2_p99_max": max(f(r["q2_D_p99"]) for r in edge_rows),
    }

    out_dir = root / "notebooks" / "outputs" / "grqm_cliff_prediagnostic_20260303"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "cliff_prediagnostic_metrics.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    md = [
        "# GR_QM Cliff Pre-Diagnostic (2026-03-03)",
        "",
        "## Data sources",
        "- grqm_cycle2_dense_followup_20260301_215901/envelope_summary.csv",
        "- grqm_edge305_microbatch_dop853_20260302_174237/edge305_microbatch_summary.csv",
        "",
        "## Snapshot",
        f"- core pass-all rate (Ω_m<=0.300): {out['core_pass_all_rate']:.3f}",
        f"- edge305 pass-all rate (dense follow-up): {out['edge305_pass_all_rate']:.3f}",
        f"- core q1_refine max: {out['core_q1_refine_max']:.6g}",
        f"- edge305 q1_refine range: {out['edge305_q1_refine_min']:.6g} .. {out['edge305_q1_refine_max']:.6g}",
        f"- core q2_p95 max: {out['core_q2_p95_max']:.6g}",
        f"- edge305 q2_p95 range (dense): {out['edge305_q2_p95_min']:.6g} .. {out['edge305_q2_p95_max']:.6g}",
        f"- edge305 spike_detected rate (dense): {out['edge305_spike_detected_rate']:.3f}",
        f"- method disagreement mean core vs edge305: {out['core_method_disagreement_mean']:.6f} vs {out['edge305_method_disagreement_mean']:.6f}",
        f"- edge305 microbatch DOP853 q2_p95/q2_p99 max: {out['edge305_microbatch_q2_p95_max']:.6g} / {out['edge305_microbatch_q2_p99_max']:.6g}",
        "",
        "## Conservative read",
        "- Existing evidence suggests the cliff manifestation is highly path/method sensitive.",
        "- Dense follow-up at edge shows severe fragility signatures; DOP853-focused microbatch at edge remains stable.",
        "- This supports keeping edge lane blocked and treating mechanism explanation as mandatory before any expansion.",
    ]
    (out_dir / "cliff_prediagnostic_note.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps({"out_dir": str(out_dir), "metrics": out}, indent=2))


if __name__ == "__main__":
    main()
