from __future__ import annotations

import hashlib
import re
from difflib import unified_diff
from pathlib import Path


FILED_PDF = Path("legal/cases/25-7526/filed/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf")
CANDIDATE_PDF = Path("legal/cases/25-7526/reproduced_candidate/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf")
EXPECTED_PAGE_COUNT = 15


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_pdf_reader(path: Path):
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError as exc:
            raise SystemExit("Missing PDF reader dependency. Install with: pip install pypdf") from exc
    return PdfReader(str(path))


def extracted_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")
    reader = load_pdf_reader(path)
    page_count = len(reader.pages)
    if page_count != EXPECTED_PAGE_COUNT:
        raise RuntimeError(f"{path} page count mismatch: expected {EXPECTED_PAGE_COUNT}, got {page_count}")
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def normalize_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main() -> int:
    try:
        filed_hash = sha256_file(FILED_PDF)
        candidate_hash = sha256_file(CANDIDATE_PDF)

        if filed_hash == candidate_hash:
            print(f"OK: exact byte match. sha256={filed_hash}")
            return 0

        filed_text = normalize_text(extracted_text(FILED_PDF))
        candidate_text = normalize_text(extracted_text(CANDIDATE_PDF))

        if filed_text == candidate_text:
            print("OK: text-equivalent but byte-different PDF.")
            print(f"filed_sha256={filed_hash}")
            print(f"candidate_sha256={candidate_hash}")
            return 0

        filed_words = filed_text.split()
        candidate_words = candidate_text.split()
        diff = unified_diff(
            filed_words[:400],
            candidate_words[:400],
            fromfile=str(FILED_PDF),
            tofile=str(CANDIDATE_PDF),
            lineterm="",
        )
        print("ERROR: filed and candidate PDF text differ. First differing section:")
        print("\n".join(list(diff)[:80]))
        print(f"filed_sha256={filed_hash}")
        print(f"candidate_sha256={candidate_hash}")
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
