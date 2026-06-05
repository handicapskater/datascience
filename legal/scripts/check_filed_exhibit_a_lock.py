from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


NOTEBOOK = Path("legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb")
LOCK_FILE = Path("legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/NonTraditional_notebook.sha256")
LOCK_ERROR = (
    "Frozen filed Exhibit A notebook has changed. Do not modify this notebook unless making an intentional "
    "filed-record correction. For research changes, use "
    "Wearable_Biomechanical_ParaTransit_Reproducible.ipynb. To intentionally update the lock, run: "
    "python legal/scripts/check_filed_exhibit_a_lock.py --update"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_lock(digest: str) -> None:
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOCK_FILE.write_text(f"{digest}  {NOTEBOOK}\n", encoding="utf-8")


def read_lock() -> str:
    return LOCK_FILE.read_text(encoding="utf-8").split()[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    digest = sha256_file(NOTEBOOK)
    if args.update or not LOCK_FILE.exists():
        write_lock(digest)
        print(f"Updated filed Exhibit A notebook lock: {LOCK_FILE}")
        return 0

    if read_lock() == digest:
        print(f"OK: filed Exhibit A notebook lock matches {digest}")
        return 0

    print(LOCK_ERROR)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
