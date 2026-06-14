from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CASE_ID = "25-7526"
SNAPSHOT_DATE = "2026-06-03"
FILED_RUN = "exhibit_a_filed_2026-06-04"

WALKING_FEATURES = ("vertical_mean", "vertical_rms", "movement_std", "peaks_per_min")
VEHICLE_FEATURES = (
    "vertical_mean",
    "vertical_rms",
    "movement_std",
    "peaks_per_min",
    "peak_abs",
    "peak_to_peak",
)

EXPECTED_WALKING_RATIOS = {
    "vertical_mean": 1.52,
    "vertical_rms": 1.50,
    "movement_std": 1.52,
}
EXPECTED_BUS_RATIOS = {
    "vertical_mean": 1.53,
    "vertical_rms": 1.50,
    "movement_std": 1.87,
    "peaks_per_min": 1.47,
    "peak_abs": 1.39,
    "peak_to_peak": 1.65,
}
EXPECTED_VAN_RATIOS = {
    "vertical_mean": 1.55,
    "vertical_rms": 1.52,
    "movement_std": 1.48,
    "peaks_per_min": 1.19,
    "peak_abs": 1.44,
    "peak_to_peak": 1.74,
}


@dataclass(frozen=True)
class ScoreResult:
    group: str
    reference_group: str
    records: int
    fsi_burden_score: float
    fsi_ratio_vs_reference: float
    benefit_vs_comparator: float | None
    css_similarity_to_reference: float
    css_distance_from_reference: float
    features_used: tuple[str, ...]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = fieldnames or list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def as_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    if value == "":
        raise ValueError(f"Missing numeric field {key!r} in row {row}")
    return float(value)


def row_by(rows: Iterable[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    raise KeyError(f"Could not find row where {key}={value!r}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ratio(numerator: float, denominator: float) -> float:
    if denominator == 0:
        raise ZeroDivisionError("Cannot divide by zero-valued reference metric")
    return numerator / denominator


def rounded(value: float) -> float:
    return round(value, 4)


def assert_close(label: str, current: float, expected: float, tolerance: float = 0.02) -> None:
    if abs(current - expected) > tolerance:
        raise RuntimeError(
            f"Exhibit A ratio mismatch for {label}: current={current:.4f}, "
            f"expected about {expected:.4f}, tolerance={tolerance:.4f}"
        )


def validate_filed_ratios(walking_ratios: list[dict[str, str]], vehicle_ratios: list[dict[str, str]]) -> None:
    walking_by_metric = {row["metric"]: float(row["walking_to_mall_pt_ratio"]) for row in walking_ratios}
    for metric, expected in EXPECTED_WALKING_RATIOS.items():
        assert_close(f"walking/Mall-PT {metric}", walking_by_metric[metric], expected)

    vehicle_by_pair = {
        (row["vehicle"], row["metric"]): float(row["ratio_vs_sedan"]) for row in vehicle_ratios
    }
    for metric, expected in EXPECTED_BUS_RATIOS.items():
        assert_close(f"bus/sedan {metric}", vehicle_by_pair[("ParaTransit bus/cutaway", metric)], expected)
    for metric, expected in EXPECTED_VAN_RATIOS.items():
        assert_close(f"van/sedan {metric}", vehicle_by_pair[("ParaTransit van", metric)], expected)


def feature_means(row: dict[str, str], features: tuple[str, ...]) -> dict[str, float]:
    return {feature: as_float(row, feature) for feature in features}


def normalized_vector(row: dict[str, str], reference: dict[str, str], features: tuple[str, ...]) -> list[float]:
    return [ratio(as_float(row, feature), as_float(reference, feature)) for feature in features]


def fsi_from_vector(vector: list[float]) -> float:
    return sum(vector) / len(vector)


def euclidean_distance_from_reference(vector: list[float]) -> float:
    return math.sqrt(sum((value - 1.0) ** 2 for value in vector))


def css_similarity_from_distance(distance: float) -> float:
    return 1.0 / (1.0 + distance)


def score_group(
    group: str,
    row: dict[str, str],
    reference_group: str,
    reference: dict[str, str],
    features: tuple[str, ...],
    comparator_fsi: float | None = None,
) -> ScoreResult:
    vector = normalized_vector(row, reference, features)
    fsi = fsi_from_vector(vector)
    distance = euclidean_distance_from_reference(vector)
    benefit = None
    if comparator_fsi and comparator_fsi > 0:
        benefit = 1.0 - (fsi / comparator_fsi)
    return ScoreResult(
        group=group,
        reference_group=reference_group,
        records=int(float(row.get("records", 0))),
        fsi_burden_score=fsi,
        fsi_ratio_vs_reference=fsi,
        benefit_vs_comparator=benefit,
        css_similarity_to_reference=css_similarity_from_distance(distance),
        css_distance_from_reference=distance,
        features_used=features,
    )


def score_to_row(score: ScoreResult) -> dict[str, object]:
    return {
        "group": score.group,
        "reference_group": score.reference_group,
        "records": score.records,
        "fsi_burden_score": rounded(score.fsi_burden_score),
        "fsi_ratio_vs_reference": rounded(score.fsi_ratio_vs_reference),
        "benefit_vs_comparator": "" if score.benefit_vs_comparator is None else rounded(score.benefit_vs_comparator),
        "css_similarity_to_reference": rounded(score.css_similarity_to_reference),
        "css_distance_from_reference": rounded(score.css_distance_from_reference),
        "features_used": ";".join(score.features_used),
    }


def ratio_rows(
    rows: list[dict[str, str]],
    numerator_group: str,
    denominator_group: str,
    features: tuple[str, ...],
) -> list[dict[str, object]]:
    numerator = row_by(rows, "analysis_group", numerator_group)
    denominator = row_by(rows, "analysis_group", denominator_group)
    return [
        {
            "metric": feature,
            "numerator_group": numerator_group,
            "numerator_value": rounded(as_float(numerator, feature)),
            "denominator_group": denominator_group,
            "denominator_value": rounded(as_float(denominator, feature)),
            "ratio": rounded(ratio(as_float(numerator, feature), as_float(denominator, feature))),
        }
        for feature in features
    ]


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines) + "\n"


def build_report(
    case_dir: Path,
    source_paths: dict[str, Path],
    hashes: dict[str, str],
    walking_raw: list[dict[str, str]],
    walking_ratios: list[dict[str, object]],
    walking_scores: list[dict[str, object]],
    vehicle_raw: list[dict[str, str]],
    vehicle_ratios: list[dict[str, object]],
    vehicle_scores: list[dict[str, object]],
    summary: dict[str, object],
) -> str:
    data_rows = [[name, str(path), hashes[name]] for name, path in source_paths.items()]
    walking_raw_rows = [
        [row["analysis_group"], row["records"], row["vertical_mean"], row["vertical_rms"], row["movement_std"], row["peaks_per_min"], row["peak_to_peak"]]
        for row in walking_raw
    ]
    vehicle_raw_rows = [
        [row["analysis_group"], row["records"], row["vertical_mean"], row["vertical_rms"], row["movement_std"], row["peaks_per_min"], row["peak_abs"], row["peak_to_peak"]]
        for row in vehicle_raw
    ]
    walking_ratio_rows = [
        [row["metric"], row["numerator_value"], row["denominator_value"], row["ratio"]]
        for row in walking_ratios
    ]
    vehicle_ratio_rows = [
        [row["vehicle"], row["metric"], row["vehicle_value"], row["sedan_value"], row["ratio_vs_sedan"]]
        for row in vehicle_ratios
    ]
    walking_score_rows = [
        [row["group"], row["reference_group"], row["records"], row["fsi_burden_score"], row["fsi_ratio_vs_reference"], row["benefit_vs_comparator"], row["css_similarity_to_reference"], row["css_distance_from_reference"]]
        for row in walking_scores
    ]
    vehicle_score_rows = [
        [row["group"], row["reference_group"], row["records"], row["fsi_burden_score"], row["fsi_ratio_vs_reference"], row["benefit_vs_comparator"], row["css_similarity_to_reference"], row["css_distance_from_reference"]]
        for row in vehicle_scores
    ]

    return (
        f"# FSI/CSS Mobility Burden Analysis for Case {CASE_ID}\n\n"
        "## Executive summary\n\n"
        "This report extends the existing Exhibit A / Appendix A evidence layer with Functional Stability Index "
        "(FSI) and Context Similarity Score (CSS) metrics. FSI summarizes source-linked accelerometer burden "
        "features into a reproducible instability/burden score. CSS summarizes how far a comparison context is "
        "from the lower-burden reference context after feature normalization.\n\n"
        "FSI and CSS do not diagnose pain and do not independently prove pain, disability, or legal entitlement. "
        "They provide objective, reproducible, source-linked burden and similarity measurements that corroborate "
        "the broader medical, biomechanical, agency, DMV, transportation, video, declaration, WHOOP, Strava, and "
        "Kubios record.\n\n"
        "The current Kubios/Polar H10 samples are small and should be treated as presumptive and directional while "
        "additional data is gathered. The present results reproduce the filed Exhibit A ratios and trend toward "
        "a conclusive burden pattern if future samples continue to align with these measurements.\n\n"
        "## Data sources\n\n"
        + markdown_table(["source", "path", "sha256"], data_rows)
        + "\n## Reproducibility\n\n"
        "Run from the repository root:\n\n"
        "```bash\n"
        f"python3 scripts/analyze_fsi_css_25_7526.py --case-dir {case_dir} --pretty\n"
        "```\n\n"
        "The script first validates the filed Exhibit A ratios within rounding tolerance. If a filed ratio does not "
        "reproduce, it stops rather than silently changing cohort labels.\n\n"
        "## Definitions\n\n"
        "**FSI (Functional Stability Index).** Higher FSI burden means less stable or more mechanically burdensome "
        "movement/ride. This case-specific FSI uses normalized accelerometer-derived features. For walking versus "
        "Mall/PT controlled skating, the lower-burden reference is Mall/PT controlled skating and the features are "
        "`vertical_mean`, `vertical_rms`, `movement_std`, and `peaks_per_min`. For ParaTransit vehicle comparison, "
        "the lower-burden reference is sedan and the features are `vertical_mean`, `vertical_rms`, `movement_std`, "
        "`peaks_per_min`, `peak_abs`, and `peak_to_peak`. FSI is the mean of feature ratios to the reference.\n\n"
        "**CSS (Context Similarity Score).** CSS compares normalized feature vectors to the lower-burden reference. "
        "A CSS closer to 1.0 means more similar to the lower-burden reference; a larger distance means a greater "
        "difference from that reference. CSS is reported as `1 / (1 + Euclidean distance from reference)`.\n\n"
        "These definitions are reproducible summary metrics for the filed tables. They are proxy metrics, not exact "
        "anatomical force measurements.\n\n"
        "## Comparator 1: Walking vs Mall/PT controlled skating\n\n"
        "### Raw feature means\n\n"
        + markdown_table(["group", "records", "vertical_mean", "vertical_rms", "movement_std", "peaks_per_min", "peak_to_peak"], walking_raw_rows)
        + "\n### Feature ratios\n\n"
        + markdown_table(["metric", "walking", "Mall/PT controlled skating", "walking_to_mall_pt_ratio"], walking_ratio_rows)
        + "\n### FSI and CSS scores\n\n"
        + markdown_table(["group", "reference", "records", "FSI", "FSI ratio", "benefit", "CSS similarity", "CSS distance"], walking_score_rows)
        + "\nWalking produced greater vertical and instability burden despite far shorter exposure, while controlled "
        "skating supported substantially greater functional mobility. The primary basic-mobility comparator remains "
        "walking versus Mall/PT controlled skating; FNS/SNS endurance skating is not used as the primary basic "
        "walking comparator here.\n\n"
        "## Comparator 2: ParaTransit bus/cutaway and van vs sedan\n\n"
        "### Raw feature means\n\n"
        + markdown_table(["group", "records", "vertical_mean", "vertical_rms", "movement_std", "peaks_per_min", "peak_abs", "peak_to_peak"], vehicle_raw_rows)
        + "\n### Vehicle ratios\n\n"
        + markdown_table(["vehicle", "metric", "vehicle_value", "sedan_value", "ratio_vs_sedan"], vehicle_ratio_rows)
        + "\n### FSI and CSS scores\n\n"
        + markdown_table(["group", "reference", "records", "FSI", "FSI ratio", "sedan benefit", "CSS similarity", "CSS distance"], vehicle_score_rows)
        + "\nBus/cutaway and van rides should be evaluated as passive mechanical stressors, not ordinary seated travel, "
        "because the same pipeline shows higher movement burden than sedan. WHOOP ParaTransit records remain useful "
        "general physiological context, but the vehicle-type comparison here relies primarily on Kubios/Polar H10 "
        "accelerometer and RRI context supported by video/declaration evidence.\n\n"
        "## Accommodation relevance\n\n"
        f"- Controlled skating FSI burden was {summary['walking']['mall_pt_fsi']:.2f} against a walking FSI burden "
        f"of {summary['walking']['walking_fsi']:.2f}, an estimated controlled-skating burden reduction of "
        f"{summary['walking']['skating_benefit_percent']:.1f}% relative to walking.\n"
        f"- Sedan FSI burden was 1.00 by definition against bus/cutaway FSI burden of "
        f"{summary['vehicle']['bus_fsi']:.2f}, an estimated sedan burden reduction of "
        f"{summary['vehicle']['sedan_benefit_vs_bus_percent']:.1f}% relative to bus/cutaway.\n"
        f"- Sedan FSI burden was 1.00 by definition against van FSI burden of {summary['vehicle']['van_fsi']:.2f}, "
        f"an estimated sedan burden reduction of {summary['vehicle']['sedan_benefit_vs_van_percent']:.1f}% "
        "relative to van.\n\n"
        "FSI/CSS help quantify accommodation relevance by translating the filed accelerometer comparisons into "
        "repeatable burden and similarity estimates. They support individualized accommodation review by showing "
        "that the lower-burden mobility and transportation contexts are measurable, source-linked, and reproducible.\n\n"
        "## Limitations\n\n"
        "- Kubios/Polar H10 sample sizes are small and should be treated as presumptive while additional data is gathered.\n"
        "- Accelerometer-derived features are proxy metrics, not exact anatomical force measurements.\n"
        "- This report is not a medical diagnosis.\n"
        "- FSI, CSS, WHOOP, Strava, Kubios, and wearable data do not independently prove pain.\n"
        "- The results should be read with medical history, biomechanics evidence, agency records, DMV records, videos, "
        "declaration testimony, WHOOP context, Strava route/distance context, and Kubios/Polar H10 evidence.\n"
        "- Strava is strongest for functional route/distance evidence and is not used as the primary bus/van/sedan comparator.\n\n"
        "## Court-safe language\n\n"
        "FSI and CSS provide reproducible, source-linked metrics for comparing mechanical burden across specific "
        "mobility and transportation contexts. In this record, walking shows higher vertical and instability burden "
        "than Mall/PT controlled skating, while controlled skating is associated with substantially greater functional "
        "route capacity. These metrics corroborate the broader record; they do not diagnose pain or independently "
        "prove pain.\n\n"
        "For ParaTransit, Kubios/Polar H10 accelerometer features show higher passive movement burden in bus/cutaway "
        "and van contexts than in sedan context. That comparison supports individualized accommodation review because "
        "vehicle type can materially affect mechanical exposure even while the person is seated.\n\n"
        "The FSI/CSS analysis should be presented as objective burden quantification that complements the medical, "
        "biomechanical, agency, DMV, transportation, video, declaration, WHOOP, Strava, and Kubios record. It supports "
        "accommodation relevance and burden reduction analysis without claiming that any single metric proves pain or "
        "guarantees a legal outcome.\n"
    )


def analyze(case_dir: Path, pretty: bool = False) -> dict[str, object]:
    filed_tables = case_dir / "outputs" / FILED_RUN / "tables"
    if not filed_tables.exists():
        filed_tables = case_dir / "outputs" / "exhibit_a" / "tables"

    source_paths = {
        "case_corpus": case_dir / "data" / f"{SNAPSHOT_DATE}_fsicss_legal_corpus_categorized.jsonl",
        "walking_summary": filed_tables / "kubios_walk_vs_mall_pt_summary.csv",
        "walking_ratios": filed_tables / "walking_vs_mall_pt_ratios.csv",
        "vehicle_summary": filed_tables / "kubios_paratransit_vehicle_summary.csv",
        "vehicle_ratios": filed_tables / "paratransit_vehicle_ratios.csv",
        "whoop_summary": filed_tables / "whoop_hr_summary.csv",
        "strava_summary": filed_tables / "strava_functional_distance_summary.csv",
        "reconciliation": filed_tables / "exhibit_value_reconciliation.csv",
    }
    missing = [str(path) for path in source_paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required source files:\n" + "\n".join(missing))

    walking_summary = read_csv(source_paths["walking_summary"])
    walking_ratio_table = read_csv(source_paths["walking_ratios"])
    vehicle_summary = read_csv(source_paths["vehicle_summary"])
    vehicle_ratio_table = read_csv(source_paths["vehicle_ratios"])
    validate_filed_ratios(walking_ratio_table, vehicle_ratio_table)

    walking = row_by(walking_summary, "analysis_group", "Walking")
    mall_pt = row_by(walking_summary, "analysis_group", "Mall/PT controlled skating")
    sedan = row_by(vehicle_summary, "analysis_group", "ParaTransit sedan")
    bus = row_by(vehicle_summary, "analysis_group", "ParaTransit bus/cutaway")
    van = row_by(vehicle_summary, "analysis_group", "ParaTransit van")

    walking_score = score_group("Walking", walking, "Mall/PT controlled skating", mall_pt, WALKING_FEATURES)
    mall_score = score_group("Mall/PT controlled skating", mall_pt, "Mall/PT controlled skating", mall_pt, WALKING_FEATURES)
    skating_benefit = 1.0 - (mall_score.fsi_burden_score / walking_score.fsi_burden_score)

    sedan_score = score_group("ParaTransit sedan", sedan, "ParaTransit sedan", sedan, VEHICLE_FEATURES)
    bus_score = score_group("ParaTransit bus/cutaway", bus, "ParaTransit sedan", sedan, VEHICLE_FEATURES)
    van_score = score_group("ParaTransit van", van, "ParaTransit sedan", sedan, VEHICLE_FEATURES)
    sedan_benefit_vs_bus = 1.0 - (sedan_score.fsi_burden_score / bus_score.fsi_burden_score)
    sedan_benefit_vs_van = 1.0 - (sedan_score.fsi_burden_score / van_score.fsi_burden_score)

    walking_score_rows = [score_to_row(walking_score), score_to_row(mall_score)]
    walking_score_rows[1]["benefit_vs_comparator"] = rounded(skating_benefit)
    vehicle_scores = [score_to_row(bus_score), score_to_row(van_score), score_to_row(sedan_score)]
    vehicle_scores[2]["benefit_vs_comparator"] = (
        f"vs_bus={rounded(sedan_benefit_vs_bus)}; vs_van={rounded(sedan_benefit_vs_van)}"
    )

    walking_ratios = ratio_rows(walking_summary, "Walking", "Mall/PT controlled skating", WALKING_FEATURES)
    vehicle_ratio_rows = [
        {
            "vehicle": row["vehicle"],
            "metric": row["metric"],
            "vehicle_value": row["vehicle_value"],
            "sedan_value": row["sedan_value"],
            "ratio_vs_sedan": row["ratio_vs_sedan"],
        }
        for row in vehicle_ratio_table
        if row["metric"] in VEHICLE_FEATURES
    ]

    output_dir = case_dir / "outputs"
    report_dir = case_dir / "reports"
    walking_csv = output_dir / "fsi_css_walking_vs_mall_pt_skating.csv"
    vehicle_csv = output_dir / "fsi_css_paratransit_vehicle_comparison.csv"
    summary_json = output_dir / "fsi_css_accommodation_summary.json"
    report_path = report_dir / "fsi_css_mobility_burden_analysis.md"

    write_csv(walking_csv, walking_score_rows)
    write_csv(vehicle_csv, vehicle_scores)

    summary = {
        "case_id": CASE_ID,
        "snapshot_date": SNAPSHOT_DATE,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_files": {name: str(path) for name, path in source_paths.items()},
        "source_sha256": {name: sha256_file(path) for name, path in source_paths.items()},
        "walking": {
            "walking_fsi": walking_score.fsi_burden_score,
            "mall_pt_fsi": 1.0,
            "fsi_ratio_walking_vs_mall_pt": walking_score.fsi_burden_score,
            "skating_benefit_vs_walking": skating_benefit,
            "skating_benefit_percent": skating_benefit * 100,
            "css_similarity_walking_to_mall_pt": walking_score.css_similarity_to_reference,
            "css_distance_walking_to_mall_pt": walking_score.css_distance_from_reference,
            "features_used": WALKING_FEATURES,
        },
        "vehicle": {
            "bus_fsi": bus_score.fsi_burden_score,
            "van_fsi": van_score.fsi_burden_score,
            "sedan_fsi": 1.0,
            "sedan_benefit_vs_bus": sedan_benefit_vs_bus,
            "sedan_benefit_vs_van": sedan_benefit_vs_van,
            "sedan_benefit_vs_bus_percent": sedan_benefit_vs_bus * 100,
            "sedan_benefit_vs_van_percent": sedan_benefit_vs_van * 100,
            "css_similarity_bus_to_sedan": bus_score.css_similarity_to_reference,
            "css_similarity_van_to_sedan": van_score.css_similarity_to_reference,
            "css_distance_bus_to_sedan": bus_score.css_distance_from_reference,
            "css_distance_van_to_sedan": van_score.css_distance_from_reference,
            "features_used": VEHICLE_FEATURES,
        },
        "outputs": {
            "walking_csv": str(walking_csv),
            "vehicle_csv": str(vehicle_csv),
            "summary_json": str(summary_json),
            "report": str(report_path),
        },
    }
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report_dir.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        build_report(
            case_dir=case_dir,
            source_paths=source_paths,
            hashes=summary["source_sha256"],
            walking_raw=walking_summary,
            walking_ratios=walking_ratios,
            walking_scores=walking_score_rows,
            vehicle_raw=vehicle_summary,
            vehicle_ratios=vehicle_ratio_rows,
            vehicle_scores=vehicle_scores,
            summary=summary,
        ),
        encoding="utf-8",
    )

    if pretty:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"Wrote {report_path}")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute FSI/CSS mobility burden comparisons for case 25-7526.")
    parser.add_argument("--case-dir", type=Path, default=Path("legal/cases/25-7526"))
    parser.add_argument("--pretty", action="store_true", help="Print JSON summary after writing outputs.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    analyze(args.case_dir, pretty=args.pretty)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
