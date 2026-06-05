from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceConfig:
    case_id: str
    run_id: str
    mode: str
    corpus_filename: str | None = None
    allow_overwrite: bool = False
    repo_root: Path | None = None

    @property
    def case_root(self) -> Path:
        root = self.repo_root or Path.cwd()
        return root / "legal" / "cases" / self.case_id

    @property
    def data_dir(self) -> Path:
        return self.case_root / "data"

    @property
    def output_dir(self) -> Path:
        return self.case_root / "outputs" / self.run_id

    @property
    def manifest_dir(self) -> Path:
        return self.output_dir / "manifest"

    @property
    def tables_dir(self) -> Path:
        return self.output_dir / "tables"

    @property
    def charts_dir(self) -> Path:
        return self.output_dir / "charts"
