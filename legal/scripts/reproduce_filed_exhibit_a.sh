#!/usr/bin/env bash
set -euo pipefail

NOTEBOOK="legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb"
OUT_DIR="legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04"
OUT_NAME="Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf"

mkdir -p "${OUT_DIR}"

echo "Reproducing filed Exhibit A from frozen notebook..."
echo "Notebook: ${NOTEBOOK}"
echo "Output dir: ${OUT_DIR}"

jupyter nbconvert \
  --to pdf "${NOTEBOOK}" \
  --TemplateExporter.exclude_input=True \
  --output "${OUT_NAME}" \
  --output-dir "${OUT_DIR}"

echo "Wrote ${OUT_DIR}/${OUT_NAME}"

if command -v shasum >/dev/null 2>&1; then
  shasum -a 256 "${OUT_DIR}/${OUT_NAME}" > "${OUT_DIR}/${OUT_NAME}.sha256"
  echo "Wrote ${OUT_DIR}/${OUT_NAME}.sha256"
elif command -v sha256sum >/dev/null 2>&1; then
  sha256sum "${OUT_DIR}/${OUT_NAME}" > "${OUT_DIR}/${OUT_NAME}.sha256"
  echo "Wrote ${OUT_DIR}/${OUT_NAME}.sha256"
else
  echo "WARNING: no SHA-256 command found; skipping checksum"
fi
