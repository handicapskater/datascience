"""Read-only comparison against a private pre-edit legal tree hash inventory."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def check(baseline: Path) -> tuple[int, int, int]:
    # Missing baselines fail; this verifier never initializes or updates a lock.
    expected = json.loads(baseline.read_text(encoding="utf-8"))
    actual = {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((ROOT / "legal").rglob("*")) if path.is_file()
    }
    changed = sum(actual.get(path) != digest for path, digest in expected.items())
    added = len(set(actual) - set(expected))
    return len(expected), changed, added


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=ROOT / ".notebook_backups/2026-09-10/legal_baseline_sha256.json")
    args = parser.parse_args()
    count, changed, added = check(args.baseline)
    print(f"Legal preservation: {count} baseline files, {changed} changed/missing, {added} added")
    raise SystemExit(1 if changed or added else 0)


if __name__ == "__main__":
    main()
