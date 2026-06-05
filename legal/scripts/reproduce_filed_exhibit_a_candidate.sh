#!/usr/bin/env bash
set -euo pipefail

NOTEBOOK="legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb"
FILED_PDF="legal/cases/25-7526/filed/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf"
OUT_DIR="legal/cases/25-7526/reproduced_candidate"
OUT_NAME="Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf"
CANDIDATE_PDF="${OUT_DIR}/${OUT_NAME}"

mkdir -p "${OUT_DIR}"

echo "Generating candidate Exhibit A PDF from notebook..."
echo "Notebook: ${NOTEBOOK}"
echo "Candidate output: ${CANDIDATE_PDF}"

jupyter nbconvert \
  --to pdf "${NOTEBOOK}" \
  --TemplateExporter.exclude_input=True \
  --output "${OUT_NAME}" \
  --output-dir "${OUT_DIR}"

if command -v shasum >/dev/null 2>&1; then
  FILED_HASH="$(shasum -a 256 "${FILED_PDF}" | awk '{print $1}')"
  CANDIDATE_HASH="$(shasum -a 256 "${CANDIDATE_PDF}" | awk '{print $1}')"
elif command -v sha256sum >/dev/null 2>&1; then
  FILED_HASH="$(sha256sum "${FILED_PDF}" | awk '{print $1}')"
  CANDIDATE_HASH="$(sha256sum "${CANDIDATE_PDF}" | awk '{print $1}')"
else
  echo "WARNING: no SHA-256 command found; skipping hash comparison"
  exit 0
fi

printf "%s  %s\n" "${CANDIDATE_HASH}" "${CANDIDATE_PDF}" > "${CANDIDATE_PDF}.sha256"

if [ "${FILED_HASH}" = "${CANDIDATE_HASH}" ]; then
  echo "OK: reproduced candidate matches filed PDF hash."
else
  echo "WARNING: reproduced candidate does not match filed PDF byte-for-byte. This can happen because PDF generation embeds timestamps or environment-specific metadata. Compare extracted text/page count/figures before treating it as a failure of substance."
  echo "filed_sha256=${FILED_HASH}"
  echo "candidate_sha256=${CANDIDATE_HASH}"
fi
