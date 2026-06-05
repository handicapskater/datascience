from pathlib import Path


FILED_RECORD_RUN_ID = "exhibit_a_filed_2026-06-03"
WEARABLE_RESEARCH_RUN_ID = "wearable_research_current"
SCOTUS_CANDIDATE_RUN_ID = "scotus_record_candidate"


def prepare_output_dir(output_dir: Path, allow_overwrite: bool = False) -> Path:
    output_dir = Path(output_dir)
    if output_dir.exists() and any(output_dir.iterdir()) and not allow_overwrite:
        raise RuntimeError(
            f"Refusing to overwrite existing filed/stable output directory: {output_dir}. "
            "Use a new run_id or set allow_overwrite=True only for research runs."
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def ensure_standard_dirs(config) -> None:
    config.output_dir.mkdir(parents=True, exist_ok=True)
    config.manifest_dir.mkdir(parents=True, exist_ok=True)
    config.tables_dir.mkdir(parents=True, exist_ok=True)
    config.charts_dir.mkdir(parents=True, exist_ok=True)
