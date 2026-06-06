# Filed Exhibit A Artifact

Canonical filed PDF:

Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf

This is the court-filed Exhibit A artifact. Do not overwrite it with generated notebook output.

The request text referenced `Exhibit_A_Wearable_Biomechancial_ParaTransit.pdf`, but this repository currently contains the filed PDF with the corrected `Biomechanical` spelling above. Preserve the filed filename that exists in this directory unless the court-filed artifact is intentionally replaced.

Verification:

    make verify-filed-exhibit-a

Verifies that the canonical filed PDF exists, matches its recorded SHA-256, has 15 pages, and has the expected Exhibit A title text on page 1.

Update hash only after intentionally replacing the filed artifact:

    make update-filed-exhibit-a-hash

Writes `Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf.sha256` from the current canonical filed PDF. Do not use this unless the filed artifact is intentionally replaced.

Generate a candidate from the notebook without overwriting the filed PDF:

    make reproduce-filed-exhibit-a-candidate

Writes a generated candidate PDF under `legal/cases/25-7526/reproduced_candidate/` and compares its byte hash to the canonical filed PDF.

Compare candidate to filed PDF:

    make compare-filed-exhibit-a

Requires both PDFs to exist and have 15 pages. It reports exact byte match, text-equivalent but byte-different, or a clear failure.

Notebook integrity:

    make hash-nontraditional-notebook
    make update-nontraditional-notebook-hash

The notebook hash is a normalized integrity hash, not necessarily a byte-for-byte ipynb hash, because Jupyter notebooks can change execution counts, metadata, and outputs.

Additional court-safety checks:

    make check-filed-input-data-hash
    make check-filed-notebook-lock
    make check-filed-artifact-locks

`make check-filed-input-data-hash` verifies the dated JSONL input corpus against `legal/cases/25-7526/data/SHA256SUMS.txt`.

`make check-filed-notebook-lock` verifies the legacy raw notebook lock under `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/`.

`make check-filed-artifact-locks` runs the input data hash check, legacy notebook lock check, and `legal.src` import smoke test.

Local reproduction note:

The canonical legal safety check is the filed PDF hash. A generated candidate PDF may differ from the filed artifact because notebook output state, PDF layout, fonts, LaTeX, timestamps, and local rendering dependencies can change PDF bytes or pagination. Do not replace the canonical filed PDF with a generated candidate unless the court-filed artifact is intentionally updated.
