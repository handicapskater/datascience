from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


FILED_PDF = Path("legal/cases/25-7526/filed/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf")
HASH_FILE = FILED_PDF.with_suffix(FILED_PDF.suffix + ".sha256")
EXPECTED_PAGE_COUNT = 15
KNOWN_BAD_OUTLINE_HASH = "a954682b2153575ba56920174e7b86c6b87e4f767db0c0090418bb8550723168"
REQUIRED_PAGE_1_TEXT = (
    "EXHIBIT A",
    "Wearable and Biomechanical Evidence",
    "Walking vs. Mall/PT Skating and ParaTransit Bus/Van vs. Sedan",
)


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


def read_expected_hash() -> str:
    if not HASH_FILE.exists():
        raise FileNotFoundError(
            f"Missing filed PDF hash file: {HASH_FILE}. "
            "Initialize it only after verifying the filed artifact, with: "
            "python legal/scripts/verify_filed_exhibit_a.py --update"
        )
    return HASH_FILE.read_text(encoding="utf-8").split()[0]


def write_expected_hash(digest: str) -> None:
    HASH_FILE.write_text(f"{digest}  {FILED_PDF}\n", encoding="utf-8")


def verify_pdf_structure(path: Path) -> None:
    reader = load_pdf_reader(path)
    page_count = len(reader.pages)
    if page_count != EXPECTED_PAGE_COUNT:
        raise RuntimeError(
            f"Filed Exhibit A page count mismatch: expected {EXPECTED_PAGE_COUNT}, got {page_count}. "
            "Never accept a short generated notebook-outline PDF as the filed exhibit."
        )

    page_1_text = reader.pages[0].extract_text() or ""
    missing = [text for text in REQUIRED_PAGE_1_TEXT if text not in page_1_text]
    if missing:
        raise RuntimeError(f"Filed Exhibit A page 1 is missing required text: {missing}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Write/update the expected hash from the current filed PDF.")
    args = parser.parse_args()

    if not FILED_PDF.exists():
        raise FileNotFoundError(f"Filed Exhibit A PDF not found: {FILED_PDF}")

    digest = sha256_file(FILED_PDF)
    if digest == KNOWN_BAD_OUTLINE_HASH:
        raise RuntimeError(
            "Filed Exhibit A PDF matches the known bad 2-page generated outline hash. "
            "Restore the court-filed 15-page PDF before continuing."
        )

    verify_pdf_structure(FILED_PDF)

    if args.update:
        write_expected_hash(digest)
        print(f"Updated filed Exhibit A PDF hash: {HASH_FILE}")
        print(f"sha256={digest}")
        return 0

    expected = read_expected_hash()
    if digest != expected:
        raise RuntimeError(f"Filed Exhibit A PDF hash mismatch. Expected {expected}, got {digest}.")

    print(f"OK: filed Exhibit A PDF hash matches {digest}")
    print(f"OK: filed Exhibit A page count is {EXPECTED_PAGE_COUNT}")
    print("OK: filed Exhibit A page 1 contains required title text")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
