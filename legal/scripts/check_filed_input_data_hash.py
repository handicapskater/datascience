from __future__ import annotations

import hashlib
from pathlib import Path


DATA_DIR = Path("legal/cases/25-7526/data")
DATA_FILE = DATA_DIR / "2026-06-03_fsicss_legal_corpus_categorized.jsonl"
SHA256SUMS = DATA_DIR / "SHA256SUMS.txt"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expected_hash() -> str:
    for line in SHA256SUMS.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[1] == DATA_FILE.name:
            return parts[0]
    raise FileNotFoundError(f"No SHA-256 entry for {DATA_FILE.name} in {SHA256SUMS}")


def main() -> int:
    expected = expected_hash()
    actual = sha256_file(DATA_FILE)
    if actual != expected:
        print(
            "Filed Exhibit A input data hash mismatch. "
            f"Expected {expected} for {DATA_FILE}, got {actual}. "
            "Do not use this file for court reproduction until the data snapshot is restored or the record is intentionally corrected."
        )
        return 1

    print(f"OK: filed Exhibit A input data hash matches {actual}")
    print(f"data_file={DATA_FILE}")
    print(f"sha256sums={SHA256SUMS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
