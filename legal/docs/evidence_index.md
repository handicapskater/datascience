# Evidence Index and Citation Map

This index maps the filed Exhibit A record, the living research notebook, the verified input corpus, generated filed tables, limitations, and reusable legal-language snippets. It is documentation only. Do not regenerate notebooks or overwrite filed artifacts when updating this index.

## Canonical Claim IDs

These IDs align the legal evidence index with the public website, LinkedIn
copy, and FSICSS platform source map.

| Claim ID | Legal-evidence role |
| --- | --- |
| `HS-CLAIM-001` | Skating as documented functional mobility support in this within-person record. |
| `HS-CLAIM-002` | Walking burden can be disproportionate to distance and should be reviewed with physiological and biomechanical context. |
| `HS-CLAIM-003` | ParaTransit bus/cutaway and van records can show passive mechanical burden compared with sedan-like transport. |
| `HS-CLAIM-004` | WHOOP, Strava, Kubios/H10, legal records, and generated reports have distinct evidence roles and corroborate the broader record. |
| `HS-CLAIM-005` | FSI/CSS/RAG platform outputs are reviewer-safe decision-support artifacts, not diagnoses or legal determinations. |
| `HS-CLAIM-006` | Public website, standards site, notebooks, and platform outputs have distinct repo and data-boundary responsibilities. |

## Public/Private Boundary

- This index may list paths, hashes, notebooks, generated tables, legal-language
  snippets, and reproducibility commands.
- Do not add raw private WHOOP, Strava, Kubios/H10, medical, identity, or
  unredacted legal records to this index.
- Filed artifacts are locked evidence. Use candidate outputs for future
  regeneration and compare them to the filed record instead of overwriting it.
- Public website and LinkedIn copy should cite this index only through
  court-safe language: corroborates, supports, consistent with, within-person
  pattern, source-linked record, and reviewable evidence.

## Court-Filed Artifact Lock

Filed/court artifacts are locked and should be treated as read-only unless an intentional filed-record correction is being made:

| Item | Path | Lock/check |
| --- | --- | --- |
| Court-filed Exhibit A PDF | `legal/cases/25-7526/filed/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf` | `legal/cases/25-7526/filed/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf.sha256`; `make verify-filed-exhibit-a` |
| Filed Exhibit A output PDF | `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf` | `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf.sha256` |
| Frozen filed source notebook | `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb` | `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/NonTraditional_notebook.sha256`; `make check-filed-notebook-lock` |
| Normalized frozen-notebook hash | `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb.normalized.sha256` | `make hash-nontraditional-notebook` |
| Filed input corpus | `legal/cases/25-7526/data/2026-06-03_fsicss_legal_corpus_categorized.jsonl` | `legal/cases/25-7526/data/SHA256SUMS.txt`; `make check-filed-input-data-hash` |
| Filed manifest | `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/manifest/evidence_manifest_sha256.csv` and `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/manifest/evidence_manifest_sha256.json` | expected corpus SHA-256 `f31810dadd85e57a8ae5199af504d6f0708349f05bc651ae66a8d05079d917db` |

The living research notebook is separate:

`legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb`

Use the living notebook for continuing wearable biomechanics, ParaTransit burden, and legal-record development. Do not use the frozen filed notebook for ongoing research.

## Filed Table Paths

The filed Exhibit A tables are generated outputs under:

`legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/`

Key filed table paths:

| Evidence topic | Filed table path | Notebook source reference |
| --- | --- | --- |
| WHOOP HR/HRV context | `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/whoop_hr_summary.csv` | `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1355`, `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1488` |
| Kubios walking vs Mall/PT skating summary | `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/kubios_walk_vs_mall_pt_summary.csv` | `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1992`, `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:1203` |
| Kubios walking vs Mall/PT ratios | `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/walking_vs_mall_pt_ratios.csv` | `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:2007`, `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:1215` |
| ParaTransit bus/van/sedan summary | `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/kubios_paratransit_vehicle_summary.csv` | `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:2286`, `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:1247` |
| ParaTransit bus/van/sedan ratios | `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/paratransit_vehicle_ratios.csv` | `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:2301`, `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:1262` |
| Category counts | `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/category_counts.csv` | `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:931`, `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:693` |
| Cohort counts | `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/cohort_counts.csv` | `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1335`, `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:938` |
| Reconciliation | `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/exhibit_value_reconciliation.csv` | `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:2475`, `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:2938` |
| Limitations and validation caveats | `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/validation_warnings.csv` | `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1078`, `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1101` |
| Filed legal language snippets | `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/legal_language_snippets.md` | `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:2974`, `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:3041` |
| Tracked reusable snippets copy | `legal/docs/legal_language_snippets.md` | Documentation copy for drafting; not a filed artifact |

Note: the filed tables and filed `legal_language_snippets.md` currently exist under the filed output directory but are ignored generated outputs. This index records their paths without adding, regenerating, or modifying them.

## Evidence Citation Map

### WHOOP HR/HRV

- Input corpus source path: `legal/cases/25-7526/data/2026-06-03_fsicss_legal_corpus_categorized.jsonl`
- Claim IDs: `HS-CLAIM-004`
- Filed table: `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/whoop_hr_summary.csv`
- Notebook logic: `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1355`, `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1488`
- Living research source: `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:1006`, `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:1049`

### Kubios Walking vs Mall/PT Skating

- Input corpus source path: `legal/cases/25-7526/data/2026-06-03_fsicss_legal_corpus_categorized.jsonl`
- Claim IDs: `HS-CLAIM-001`, `HS-CLAIM-002`, `HS-CLAIM-004`
- Filed summary table: `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/kubios_walk_vs_mall_pt_summary.csv`
- Filed ratio table: `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/walking_vs_mall_pt_ratios.csv`
- Notebook logic: `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1227`, `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1240`, `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1992`
- Living research source: `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:1180`, `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:1215`

### ParaTransit Bus/Van/Sedan

- Input corpus source path: `legal/cases/25-7526/data/2026-06-03_fsicss_legal_corpus_categorized.jsonl`
- Claim IDs: `HS-CLAIM-003`, `HS-CLAIM-004`
- Filed summary table: `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/kubios_paratransit_vehicle_summary.csv`
- Filed ratio table: `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/paratransit_vehicle_ratios.csv`
- Notebook logic: `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1284`, `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1293`, `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1302`, `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:2283`
- Living research source: `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:887`, `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:896`, `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:905`, `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:1244`

### Category Counts

- Filed table: `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/category_counts.csv`
- Filed notebook logic: `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:931`
- Living research source: `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:693`

### Reconciliation

- Filed reconciliation table: `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/exhibit_value_reconciliation.csv`
- Filed notebook logic: `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:2475`, `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:2938`
- Living research source: `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:1439`, `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:1510`

### Limitations

- Filed validation table: `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/validation_warnings.csv`
- Filed legal snippets: `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/legal_language_snippets.md`
- Tracked reusable snippets: `legal/docs/legal_language_snippets.md`
- Filed notebook limitations/caveats: `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:1078`, `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:2976`, `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb:3041`
- Living research limitations/caveats: `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:1273`, `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:1296`, `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb:1651`

## Existing Verification Commands

Run from repository root:

```sh
make check-filed-artifact-locks
make verify-filed-exhibit-a
python tests/test_notebook_output_architecture.py
```

These checks verify filed input hash integrity, frozen notebook lock integrity, legal import resolution, filed PDF hash/page/title integrity, and notebook output architecture without regenerating the notebooks.
