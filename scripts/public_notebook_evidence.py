"""Read and display a pinned aggregate publication excerpt; never run science."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "data/public/skating_evidence.v1.json"
LOCK = ROOT / "data/public/skating_evidence.v1.sha256"
EXPECTED_BUNDLE_SHA256 = "123f9ca90c10a39350f2c39b370b7ec8c10708a836688bbadd3b97185e0ccf30"
EXPECTED_SOURCE_SHA256 = {
    "biomechanics": "72fb09078c2878a284a898797c2e0e6b8c98abe5da7c4352d72d6f53179ee7b9",
    "core": "817264738ad583db5b0c33fa579d1280cedf78d1ad09fdf5b55e3ebf5c929859",
}
EXPECTED_CORE = {
    "triplet_distance_miles_Mall_to_Walk": ("Mall→Walking", "distance_miles", -1.8644, "mi", (-1.8808, -1.8465)),
    "triplet_distance_miles_Walk_to_PT": ("Walking→PT", "distance_miles", 1.6683, "mi", (1.6529, 1.6852)),
    "triplet_vertical_dynamic_g_rms_Mall_to_Walk": ("Mall→Walking", "vertical_dynamic_g_rms", 0.0849, "g", (0.0827, 0.0861)),
    "triplet_jerk_rms_g_per_s_Mall_to_Walk": ("Mall→Walking", "jerk_rms_g_per_s", 0.6370, "g/s", (0.6180, 0.6610)),
    "triplet_shock_spike_rate_per_min_Mall_to_Walk": ("Mall→Walking", "shock_spike_rate_per_min", 3.0019, "/min", (2.1829, 4.3558)),
    "triplet_shock_spike_rate_per_min_Walk_to_PT": ("Walking→PT", "shock_spike_rate_per_min", -1.7744, "/min", (-2.0759, -1.0971)),
}
EXPECTED_TOP_LEVEL = {
    "schema_version", "snapshot_date", "data_through_date", "scope", "sources",
    "core_findings", "mechanics", "pt_distance", "longitudinal", "pareto",
    "fixed_reference_event_density", "tails", "shock_taxonomy", "boundaries",
    "scientific_recomputation", "boundary_notes",
}
EFFECT_RE = re.compile(r"^median paired Δ ([+-]?\d+(?:\.\d+)?) (mi|g|g/s|/min)$")
CI_RE = re.compile(r"^\[([+-]?\d+(?:\.\d+)?), ([+-]?\d+(?:\.\d+)?)\]$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
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
    if expected != EXPECTED_BUNDLE_SHA256:
        raise ValueError("Public aggregate lock differs from the reviewed release")
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError("Public aggregate hash mismatch; obtain the matching reviewed bundle.")
    bundle = read_json(path)
    validate_bundle(bundle)
    return bundle


def _finite_number(value, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label}: expected a finite number")
    return float(value)


def _reject_nonfinite(value, label: str = "bundle") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_nonfinite(item, f"{label}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_nonfinite(item, f"{label}[{index}]")
    elif isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{label}: nonfinite numerical value")


def _positive_count(value, label: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{label}: expected a positive integer")


def _interval(value, label: str) -> tuple[float, float]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f"{label}: expected two confidence bounds")
    low, high = (_finite_number(v, label) for v in value)
    if low >= high:
        raise ValueError(f"{label}: confidence bounds are not ordered")
    return low, high


def paired_effect(row: dict) -> tuple[float, str, tuple[float, float] | None]:
    """Parse a published paired effect; optional CI is for plotting only."""
    effect = EFFECT_RE.fullmatch(row.get("effect", ""))
    if effect is None:
        raise ValueError("Malformed published paired effect or unit")
    value, unit = float(effect.group(1)), effect.group(2)
    _finite_number(value, "paired effect")
    ci = row.get("CI")
    if ci is None:
        return value, unit, None
    match = CI_RE.fullmatch(ci) if isinstance(ci, str) else None
    if match is None:
        raise ValueError("Malformed published confidence interval")
    bounds = _interval((float(match.group(1)), float(match.group(2))), "published CI")
    if not bounds[0] <= value <= bounds[1]:
        raise ValueError("Paired effect lies outside published CI")
    return value, unit, bounds


def validate_bundle(bundle: dict) -> dict:
    """Validate the fixed public projection; no source-level inference occurs."""
    if not isinstance(bundle, dict) or set(bundle) != EXPECTED_TOP_LEVEL:
        raise ValueError("Public aggregate required fields differ from schema")
    _reject_nonfinite(bundle)
    if bundle["schema_version"] != "notebook_public_evidence.v1":
        raise ValueError("Unsupported public bundle version")
    if bundle["scientific_recomputation"] is not False:
        raise ValueError("Scientific recomputation flag changed")
    if not isinstance(bundle["scope"], str) or "N-of-1" not in bundle["scope"]:
        raise ValueError("N-of-1 scope is missing")
    for key in ("mechanics", "pt_distance", "longitudinal", "pareto",
                "fixed_reference_event_density", "tails", "shock_taxonomy", "boundaries"):
        if not isinstance(bundle[key], dict):
            raise ValueError(f"{key}: expected an aggregate object")
    if set(bundle["mechanics"]) != {"vertical_rms", "magnitude_jerk"}:
        raise ValueError("Missing mechanical endpoint")
    if not isinstance(bundle["pareto"].get("core"), dict) or not isinstance(bundle["pareto"].get("with_shock"), dict):
        raise ValueError("Missing Pareto denominators")
    if set(bundle["tails"].get("metrics", {})) != {"p90_g", "p95_g", "p99_g", "p99_9_g"}:
        raise ValueError("Missing tail endpoints")
    from datetime import date
    try:
        snapshot = date.fromisoformat(bundle["snapshot_date"])
        coverage = date.fromisoformat(bundle["data_through_date"])
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid public coverage dates") from exc
    if coverage > snapshot:
        raise ValueError("Coverage date follows snapshot date")
    if not isinstance(bundle["sources"], dict) or set(bundle["sources"]) != set(EXPECTED_SOURCE_SHA256):
        raise ValueError("Missing source provenance")
    for name, expected_sha in EXPECTED_SOURCE_SHA256.items():
        source = bundle["sources"][name]
        if not isinstance(source, dict) or set(source) != {"url", "sha256", "content_hash", "resource_version"}:
            raise ValueError(f"{name}: invalid source reference")
        if source["sha256"] != expected_sha or not isinstance(source["content_hash"], str) or not SHA_RE.fullmatch(source["content_hash"]):
            raise ValueError(f"{name}: source identity changed")
        if source["url"] != f"https://handicapskater.com/data/public/evidence-observatory/v1/{'biomechanics' if name == 'biomechanics' else 'computational'}-evidence.json":
            raise ValueError(f"{name}: unapproved source URL")
        if source["resource_version"] != "fsi_publication_resource.v1":
            raise ValueError(f"{name}: resource version changed")
    rows = bundle["core_findings"]
    if not isinstance(rows, list) or len(rows) != len(CORE_IDS):
        raise ValueError("Missing primary endpoint rows")
    if tuple(row.get("evidence_id") for row in rows if isinstance(row, dict)) != CORE_IDS:
        raise ValueError("Unexpected primary endpoint identifiers")
    for row in rows:
        eid = row["evidence_id"]
        if set(row) != set(CORE_FIELDS):
            raise ValueError(f"{eid}: required fields differ")
        comparison, metric, expected_value, expected_unit, expected_ci = EXPECTED_CORE[eid]
        value, unit, ci = paired_effect(row)
        if (row["comparison"], row["metric"], value, unit, ci) != (comparison, metric, expected_value, expected_unit, expected_ci):
            raise ValueError(f"{eid}: published endpoint value or unit changed")
        if type(row["independent_N"]) is not int or row["independent_N"] != 44:
            raise ValueError(f"{eid}: paired-date denominator changed")
        consistency = row["direction_consistency"]
        if not isinstance(consistency, str) or not consistency.endswith("%"):
            raise ValueError(f"{eid}: invalid direction consistency")
        rate = _finite_number(float(consistency[:-1]), f"{eid} consistency")
        if not 0 <= rate <= 100:
            raise ValueError(f"{eid}: invalid direction consistency")
        if row["grain"] != "whole reviewed triplet" or row["source_authority"] != "CORE_TRIPLET_EVIDENCE.json":
            raise ValueError(f"{eid}: provenance or inference grain changed")
        for key in ("classification", "p_value", "p_value_type", "plain_language_finding"):
            if not isinstance(row[key], str) or not row[key]:
                raise ValueError(f"{eid}: missing {key}")
    for name, unit in (("vertical_rms", "g"), ("magnitude_jerk", "g/s")):
        row = bundle["mechanics"].get(name)
        if not isinstance(row, dict) or row.get("unit") != unit or type(row.get("N")) is not int or row.get("N") != 44 or type(row.get("direction_count")) is not int or row.get("direction_count") != 44:
            raise ValueError(f"{name}: unit or denominator changed")
        for key in ("mall_median", "walking_median", "walking_minus_mall"):
            _finite_number(row.get(key), f"{name}.{key}")
        low, high = _interval(row.get("bootstrap_95CI"), f"{name} CI")
        if not low <= row["walking_minus_mall"] <= high:
            raise ValueError(f"{name}: paired effect outside CI")
    pt = bundle["pt_distance"]
    if any(type(pt.get(key)) is not int for key in ("eligible_N", "right_higher_count", "left_higher_count", "tie_count")) or pt.get("eligible_N") != 44 or pt.get("right_higher_count") != 44 or pt.get("left_higher_count") != 0 or pt.get("tie_count") != 0:
        raise ValueError("PT distance denominator or direction changed")
    for key in ("left_median", "right_median", "median_paired_difference_right_minus_left"):
        _finite_number(pt.get(key), f"pt_distance.{key}")
    low, high = _interval(pt.get("bootstrap_95CI"), "PT distance CI")
    if not low <= pt["median_paired_difference_right_minus_left"] <= high:
        raise ValueError("PT paired distance outside CI")
    for key, value in (("longitudinal.activity_N", bundle["longitudinal"].get("activity_N")),
                       ("longitudinal.date_N", bundle["longitudinal"].get("date_N")),
                       ("pareto.core.N", bundle["pareto"]["core"].get("N")),
                       ("pareto.with_shock.N", bundle["pareto"]["with_shock"].get("N")),
                       ("fixed_reference_event_density.N", bundle["fixed_reference_event_density"].get("N")),
                       ("tails.N", bundle["tails"].get("N"))):
        _positive_count(value, key)
    if (bundle["longitudinal"]["activity_N"], bundle["longitudinal"]["date_N"],
        bundle["pareto"]["core"]["N"], bundle["pareto"]["with_shock"]["N"],
        bundle["fixed_reference_event_density"]["N"], bundle["tails"]["N"]) != (598, 589, 43, 43, 25, 25):
        raise ValueError("Supporting endpoint denominators changed")
    if not isinstance(bundle["boundaries"], dict) or any(value is not False for value in bundle["boundaries"].values()):
        raise ValueError("Measurement boundary flags changed")
    if bundle["shock_taxonomy"].get("adaptive_mad_counter_result_preserved") is not True:
        raise ValueError("Contrary MAD impact result omitted")
    if not isinstance(bundle["boundary_notes"], list) or not all(isinstance(note, str) for note in bundle["boundary_notes"]):
        raise ValueError("Boundary notes missing")
    density = bundle["fixed_reference_event_density"]
    if density.get("unit") != "events/min" or density.get("direction_count") != 25:
        raise ValueError("Fixed-reference event-density unit or direction changed")
    low, high = _interval(density.get("bootstrap_95CI"), "fixed-reference event-density CI")
    if not low <= density.get("walking_minus_mall", float("nan")) <= high:
        raise ValueError("Fixed-reference event-density effect outside CI")
    if bundle["tails"].get("direction_count") != 25:
        raise ValueError("Tail direction denominator changed")
    for name, row in bundle["tails"].get("metrics", {}).items():
        if row.get("unit") != "g" or row.get("N") != 25 or row.get("direction_count") != 25:
            raise ValueError(f"{name}: tail unit or denominator changed")
        _finite_number(row.get("walking_minus_mall"), f"{name}.walking_minus_mall")
    return {
        "passed": [
            "Pinned file SHA-256 and schema", "Required fields and finite paired effects",
            "Six source-identified primary endpoints", "Units, directions, CIs and 44 paired-date denominators",
            "Supporting endpoint denominators", "Source identities and interpretation boundaries",
        ],
        "not_independently_verified": [
            "Underlying date/session records and bootstrap draws are not in this public bundle",
            "Current mutable publication parity requires the matching historical source snapshot",
        ],
    }


def validation_report(bundle: dict) -> str:
    report = validate_bundle(bundle)
    lines = ["### Public evidence validation", "", "| Check | Result |", "| --- | --- |"]
    lines.extend(f"| {item} | PASS |" for item in report["passed"])
    lines.extend(f"| {item} | Not independently verifiable here |" for item in report["not_independently_verified"])
    return "\n".join(lines)


def plot_paired_effects(bundle: dict):
    """Four aligned unit-specific panels of the six published paired effects."""
    import matplotlib.pyplot as plt

    groups = [
        ("mi", "Recorded distance", [0, 1]),
        ("g", "Vertical acceleration RMS", [2]),
        ("g/s", "Magnitude jerk RMS", [3]),
        ("/min", "Shock-spike rate", [4, 5]),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), layout="constrained")
    rows = bundle["core_findings"]
    for ax, (unit, title, indices) in zip(axes.flat, groups):
        labels = []
        for position, index in enumerate(indices):
            row = rows[index]
            value, actual_unit, ci = paired_effect(row)
            if actual_unit != unit:
                raise ValueError(f"{row['evidence_id']}: wrong plot unit")
            label = f"{row['comparison']}  (N={row['independent_N']})"
            labels.append(label)
            color = "#145f69" if value > 0 else "#a54d2f"
            if ci is None:
                ax.plot(value, position, "o", color=color, markersize=7)
                ax.text(value, position + 0.16, "CI unavailable", fontsize=8, color=color)
            else:
                ax.errorbar(value, position, xerr=[[value-ci[0]], [ci[1]-value]],
                            fmt="o", capsize=4, color=color, markersize=7)
        ax.axvline(0, color="#5e6469", linewidth=1, linestyle="--")
        ax.set_yticks(range(len(labels)), labels)
        ax.invert_yaxis()
        ax.set_ylim(len(labels)-0.35, -0.6)
        ax.set_xlabel(f"Published median paired change ({unit})")
        ax.set_title(title, fontsize=11)
        ax.grid(axis="x", alpha=0.2)
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Within-date paired effects and published 95% intervals", fontsize=15)
    return fig


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
