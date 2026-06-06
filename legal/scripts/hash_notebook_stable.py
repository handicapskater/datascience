from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


NOTEBOOK = Path("legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb")
HASH_FILE = NOTEBOOK.with_suffix(NOTEBOOK.suffix + ".normalized.sha256")
VOLATILE_METADATA_KEYS = {
    "execution",
    "ExecuteTime",
    "collapsed",
    "scrolled",
    "trusted",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_metadata(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: normalize_metadata(item)
            for key, item in sorted(value.items())
            if key not in VOLATILE_METADATA_KEYS
        }
    if isinstance(value, list):
        return [normalize_metadata(item) for item in value]
    return value


def normalized_notebook() -> dict[str, Any]:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    notebook["metadata"] = normalize_metadata(notebook.get("metadata", {}))

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []
        cell["metadata"] = normalize_metadata(cell.get("metadata", {}))

    return notebook


def normalized_digest() -> str:
    payload = json.dumps(normalized_notebook(), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def raw_digest() -> str:
    return sha256_bytes(NOTEBOOK.read_bytes())


def read_expected_hash() -> str:
    if not HASH_FILE.exists():
        raise FileNotFoundError(
            f"Missing normalized notebook hash file: {HASH_FILE}. "
            "Initialize it intentionally with: python legal/scripts/hash_notebook_stable.py --update"
        )
    return HASH_FILE.read_text(encoding="utf-8").split()[0]


def write_expected_hash(digest: str) -> None:
    HASH_FILE.write_text(f"{digest}  {NOTEBOOK}  normalized-no-outputs-no-execution-counts\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Write/update the normalized notebook integrity hash.")
    args = parser.parse_args()

    digest = normalized_digest()
    raw = raw_digest()

    if args.update:
        write_expected_hash(digest)
        print(f"Updated normalized notebook hash: {HASH_FILE}")
        print(f"normalized_sha256={digest}")
        print(f"raw_file_sha256={raw}")
        return 0

    expected = read_expected_hash()
    if digest != expected:
        raise RuntimeError(f"Normalized notebook hash mismatch. Expected {expected}, got {digest}. raw_file_sha256={raw}")

    print(f"OK: normalized notebook hash matches {digest}")
    print(f"raw_file_sha256={raw}")
    print("NOTE: normalized hash ignores execution counts, outputs, and selected volatile metadata.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
