from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from legal.src.evidence_config import EvidenceConfig
from legal.src.evidence_paths import FILED_RECORD_RUN_ID, prepare_output_dir, ensure_standard_dirs

config = EvidenceConfig(
    case_id="25-7526",
    run_id=FILED_RECORD_RUN_ID,
    mode="FILED_RECORD",
    allow_overwrite=False,
    repo_root=repo_root,
)

print("OK: legal.src imports work")
print(f"repo_root={repo_root}")
print(f"output_dir={config.output_dir}")
