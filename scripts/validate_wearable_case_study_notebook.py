from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NOTEBOOK = REPO_ROOT / "legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb"


def resolve_notebook(argument: str | None) -> Path:
    if argument is None:
        return DEFAULT_NOTEBOOK
    path = Path(argument)
    candidates = [
        path,
        REPO_ROOT / path,
        REPO_ROOT / "legal/notebooks" / path,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[-1]


def load_source(path: Path) -> str:
    with path.open(encoding="utf-8") as handle:
        notebook = json.load(handle)
    return "\n".join("".join(cell.get("source", [])) for cell in notebook.get("cells", []))


def source_lines(source: str) -> list[str]:
    return [line.strip() for line in source.splitlines() if line.strip()]


def contains_required(source: str, needle: str) -> bool:
    return needle in source


def unsafe_diagnosis_line(line: str) -> bool:
    lowered = line.lower()
    if "diagnosis" not in lowered and "diagnose" not in lowered:
        return False
    allowed_markers = (
        "not a medical diagnosis",
        "not medical diagnosis",
        "no medical diagnosis",
        "not a diagnosis",
        "does not diagnose",
    )
    return not any(marker in lowered for marker in allowed_markers)


def unsafe_proves_pain_line(line: str) -> bool:
    lowered = line.lower()
    phrase = "proves pain"
    if phrase not in lowered:
        return False
    allowed_markers = (
        "does not claim",
        "no claim",
        "not claim",
        "not claimed",
    )
    return not any(marker in lowered for marker in allowed_markers)


def unsafe_guaranteed_legal_line(line: str) -> bool:
    lowered = line.lower()
    phrase = "guaranteed legal"
    if phrase not in lowered:
        return False
    allowed_markers = (
        "does not claim",
        "no guaranteed",
        "not guaranteed",
        "not claim",
    )
    return not any(marker in lowered for marker in allowed_markers)


def find_unsafe_lines(source: str) -> list[str]:
    direct_company_patterns = (r"\b" + "G" + r"oogle\b", r"\b" + "Fit" + r"bit\b")
    unsafe_patterns = (
        r"\bclinically validated\b",
        r"\bwill acquire\b",
        r"\bwill buy\b",
    )
    findings: list[str] = []
    for line in source_lines(source):
        if unsafe_diagnosis_line(line) or unsafe_proves_pain_line(line) or unsafe_guaranteed_legal_line(line):
            findings.append(line)
            continue
        for pattern in (*direct_company_patterns, *unsafe_patterns):
            if re.search(pattern, line, flags=re.IGNORECASE):
                findings.append(line)
                break
    return findings


def validate(path: Path) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"Notebook not found: {path}"]

    source = load_source(path)
    required_sections = (
        "Wearable Mobility Evidence Case Study",
        "Source Roles",
        "Integrity and Reproducibility Manifest",
        "Duplicate Handling",
        "Integrated Cohort Summary",
        "Legally Relevant Cohorts",
        "Court-Safe Findings",
        "Findings Not Claimed",
        "Wearable-Health and Mobility Intelligence Relevance",
        "Final Reproducible Export",
    )
    for section in required_sections:
        if not contains_required(source, section):
            failures.append(f"Missing required section: {section}")

    required_terms = (
        "../fsicss-iomt-evidence-platform/data/processed/integrated/integrated_mobility_evidence_context.jsonl",
        "notebook_integrity_manifest.md",
        "notebook_integrity_manifest.json",
        "notebook_case_study_summary.md",
        "notebook_integrated_cohort_summary.csv",
        "reports/figures",
    )
    for term in required_terms:
        if not contains_required(source, term):
            failures.append(f"Missing required notebook reference: {term}")

    unsafe_lines = find_unsafe_lines(source)
    if unsafe_lines:
        failures.append("Unsafe wording found:\n" + "\n".join(f"- {line}" for line in unsafe_lines))

    return failures


def main() -> int:
    path = resolve_notebook(sys.argv[1] if len(sys.argv) > 1 else None)
    failures = validate(path)
    if failures:
        print("Notebook validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Notebook validation passed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
