"""Read and display a pinned aggregate publication excerpt; never run science."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "data/public/skating_evidence.v1.json"
LOCK = ROOT / "data/public/skating_evidence.v1.sha256"
CORE_FIELDS = (
    "CI", "classification", "comparison", "direction_consistency", "effect",
    "evidence_id", "grain", "independent_N", "metric", "p_value", "p_value_type",
    "plain_language_finding", "source_authority",
)
CORE_IDS = (
    "triplet_distance_miles_Mall_to_Walk", "triplet_distance_miles_Walk_to_PT",
    "triplet_vertical_dynamic_g_rms_Mall_to_Walk",
    "triplet_jerk_rms_g_per_s_Mall_to_Walk",
    "triplet_shock_spike_rate_per_min_Mall_to_Walk",
    "triplet_shock_spike_rate_per_min_Walk_to_PT",
)


def reject_constant(value: str):
    raise ValueError(f"Nonfinite JSON constant: {value}")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_constant)


def load_bundle(path: Path = BUNDLE, lock: Path = LOCK) -> dict:
    expected = lock.read_text(encoding="utf-8").split()[0]
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError("Public aggregate hash mismatch; obtain the matching reviewed bundle.")
    bundle = read_json(path)
    if bundle["schema_version"] != "notebook_public_evidence.v1":
        raise ValueError("Unsupported public bundle version")
    if bundle["scientific_recomputation"] is not False:
        raise ValueError("This consumer may not compute scientific results")
    if any(bundle["boundaries"].values()):
        raise ValueError("Measurement boundaries changed; review a new release")
    if tuple(r["evidence_id"] for r in bundle["core_findings"]) != CORE_IDS:
        raise ValueError("Unexpected evidence selection")
    for row in bundle["core_findings"]:
        if set(row) != set(CORE_FIELDS) or row["independent_N"] <= 0:
            raise ValueError("Invalid aggregate finding")
    return bundle


def _source(path: Path, value: dict) -> dict:
    return {
        "url": "https://handicapskater.com/data/public/evidence-observatory/v1/" + path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "content_hash": value["content_hash"],
        "resource_version": value["resource_version"],
    }


def check_source_parity(bundle: dict, source_root: Path) -> None:
    """Compare only approved aggregate fields; never inspect telemetry or a DB."""
    bp = source_root / "biomechanics-evidence.json"
    cp = source_root / "computational-evidence.json"
    biomech, core = read_json(bp), read_json(cp)
    if bundle["sources"] != {"biomechanics": _source(bp, biomech), "core": _source(cp, core)}:
        raise ValueError("Source release/hash drift; do not silently refresh")
    if bundle["data_through_date"] != biomech["data_through_date"]:
        raise ValueError("Coverage date drift")
    # Select by evidence ID, not incidental row order. Only six aggregates leave
    # the published source; all other nested experiment/session data is ignored.
    payload = core["approved_values"]["bands"][2]["offline_rl_lab"]["core_confirmatory_evidence"]
    by_id = {r["evidence_id"]: r for r in payload["rows"]}
    expected = [{k: by_id[eid][k] for k in CORE_FIELDS} for eid in CORE_IDS]
    if bundle["core_findings"] != expected:
        raise ValueError("Core result parity failure")
    approved = biomech["approved_values"]
    ib = approved["ib01"]
    projections = {
        "mechanics": {k: ib[k] for k in ("vertical_rms", "magnitude_jerk")},
        "pt_distance": ib["pt"]["distance"], "longitudinal": ib["longitudinal"],
        "pareto": ib["pareto"], "fixed_reference_event_density": ib["fixed_reference_event_density"],
        "tails": ib["tails"], "shock_taxonomy": ib["shock_taxonomy"],
        "boundaries": approved["measurement_boundaries"],
    }
    for key, expected_value in projections.items():
        if bundle[key] != expected_value:
            raise ValueError(f"Aggregate parity failure: {key}")


def core_table(bundle: dict) -> str:
    lines = [
        "| Comparison / measure | Published paired change | Published 95% CI | Dates | Direction consistency |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for row in bundle["core_findings"]:
        lines.append(f"| {row['comparison']} / {row['metric']} | {row['effect']} | {row['CI']} | {row['independent_N']} | {row['direction_consistency']} |")
    return "\n".join(lines)


def plot_aggregates(bundle: dict):
    """Plot stored group medians, without inference or reconstructed observations."""
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(12, 4.8), layout="constrained")
    specs = []
    for key, title in (("vertical_rms", "Vertical acceleration"), ("magnitude_jerk", "Rate of acceleration change")):
        row = bundle["mechanics"][key]
        specs.append((title, ["Mall skating", "Walking"], [row["mall_median"], row["walking_median"]], row["unit"], row["N"]))
    row = bundle["pt_distance"]
    specs.append(("Functional distance after walking", ["Walking", "PT skating"], [row["left_median"], row["right_median"]], "miles", row["eligible_N"]))
    for ax, (title, labels, values, unit, count) in zip(axes, specs):
        bars = ax.bar(labels, values, color=["#146b68" if "skating" in label else "#a9512f" for label in labels], width=0.58)
        ax.bar_label(bars, labels=[f"{value:.3f}" for value in values], padding=5)
        ax.set_ylim(0, max(values) * 1.25)
        ax.set_title(title, fontsize=11, pad=15)
        ax.set_ylabel(f"Published group median ({unit})")
        ax.spines[["top", "right"]].set_visible(False)
        ax.text(0.5, -0.20, f"{count} eligible paired dates", transform=ax.transAxes, ha="center", fontsize=10)
    fig.suptitle("More mobility with skating; lower Mall mechanical intensity", fontsize=15)
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, help="Optional local published bundle directory for read-only parity")
    parser.add_argument("--render", action="store_true", help="Render three aggregate panels locally; no scientific computation")
    args = parser.parse_args()
    bundle = load_bundle()
    if args.source_root:
        check_source_parity(bundle, args.source_root)
    if args.render:
        target = ROOT / "data/public/figures"
        target.mkdir(parents=True, exist_ok=True)
        fig = plot_aggregates(bundle)
        fig.savefig(target / "skating_evidence.png", dpi=160)
        import matplotlib.pyplot as plt
        plt.close(fig)
    print("PASS: pinned public aggregate bundle" + (" and source parity" if args.source_root else ""))


if __name__ == "__main__":
    main()
