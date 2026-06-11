# Datascience Evidence Alignment Audit

Audit branch: `audit/pr21-datascience-evidence-alignment`

Audit date: 2026-06-06

## Current Repo State

The datascience repo is the reproducible evidence layer for HandicapSkater wearable, biomechanical, and ParaTransit evidence. Current `main` includes PR-20 through PR-13, including the evidence/citation index, clean Colab reproducibility work, filed Exhibit A verification, filed/research output separation, and case 25-7526 Exhibit A setup.

The repo now distinguishes four categories:

| Category | Primary paths | Status |
| --- | --- | --- |
| Filed court artifact | `legal/cases/25-7526/filed/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf` | Locked by SHA-256 and verified by `make verify-filed-exhibit-a` |
| Filed reproducibility notebook | `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb` | Frozen notebook; protected by `NonTraditional_notebook.sha256` and `make check-filed-notebook-lock` |
| Ongoing research notebook | `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb` | Living research notebook; output run id is `wearable_research_current` |
| Raw/intermediate/generated artifacts | `legal/cases/25-7526/data/`, `legal/cases/25-7526/outputs/`, `legal/cases/25-7526/reproduced_candidate/` | Input corpus is hash-locked; generated outputs are separated from filed artifacts |

## Evidence Inventory

Primary evidence files:

- `legal/cases/25-7526/data/2026-06-03_fsicss_legal_corpus_categorized.jsonl`
- `legal/cases/25-7526/data/SHA256SUMS.txt`
- `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/manifest/evidence_manifest_sha256.csv`
- `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/manifest/evidence_manifest_sha256.json`
- `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/`
- `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/charts/`
- `legal/docs/evidence_index.md`
- `legal/docs/legal_language_snippets.md`

Primary comparators:

- Walking vs Mall/PT controlled skating
- ParaTransit bus/cutaway and van vs sedan
- WHOOP physiological context
- Strava functional distance context
- Kubios RRI/accelerometer movement-burden context

## HR/HRV Inventory

Filed HR/HRV table:

`legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/whoop_hr_summary.csv`

Current filed summary values sampled during audit:

| Category | Records | Mean average HR | Highest max HR | Mean HRV | Mean strain |
| --- | ---: | ---: | ---: | ---: | ---: |
| walking | 33 | 123.39 | 195.00 | 38.47 | 9.75 |
| skates | 596 | 112.97 | 197.00 | 36.05 | 12.61 |
| paratransit_surrogate | 112 | 88.38 | 171.00 | 35.33 | 3.76 |

Interpretation rule:

WHOOP HR/HRV supports longitudinal physiological context and within-person pattern analysis. It does not diagnose pain, does not prove pain by itself, and is not used as the precise bus/van/sedan mechanical comparator.

## Exhibit A Reproducibility Status

Filed Exhibit A is represented by:

- Court-filed PDF: `legal/cases/25-7526/filed/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf`
- Filed output copy: `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf`
- Frozen source notebook: `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb`
- Candidate reproduction path: `legal/cases/25-7526/reproduced_candidate/`

Current instructions are clear:

- `make verify-filed-exhibit-a` verifies the canonical filed PDF hash, 15-page count, and page-1 title text.
- `make check-filed-artifact-locks` verifies the filed input corpus hash, frozen notebook lock, and legal import smoke test.
- `make reproduce-filed-exhibit-a-candidate` generates a candidate without overwriting the filed PDF.
- `make compare-filed-exhibit-a` compares a candidate to the filed PDF.

No notebooks were regenerated during this audit.

## Citation/Index Status

Traceability is documented in:

- `legal/docs/evidence_index.md`
- `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/manifest/evidence_manifest_sha256.csv`
- `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/manifest/evidence_manifest_sha256.json`

The evidence index maps:

- Filed Exhibit A notebook and PDF
- Living research notebook
- Input corpus and expected SHA-256
- Filed WHOOP, Kubios, ParaTransit, category-count, reconciliation, and validation-warning tables
- Legal language snippets and limitation language

## Court-Safe Claim Language

Audit changes softened legacy exploratory notebook language from proof-oriented claims to court-safe phrasing. Preferred terms now used include:

- supports
- corroborates
- within-person pattern
- consistent with functional burden
- accommodation relevance
- not medical diagnosis
- not proof of pain alone

Examples of softened claims:

| Risky framing | Court-safe framing |
| --- | --- |
| HR/HRV proves pain | HR/HRV supports physiological context and within-person burden analysis |
| clinically validated proof | useful autonomic context metric |
| definitive discrimination proof | evidence that corroborates a longer record |
| guaranteed legal conclusion | accommodation relevance |
| skating is medically necessary by itself | skating appears accommodation-relevant in this record |

The filed and living legal notebooks already contain strong limitations language, including that wearable outputs are corroborative and not a standalone diagnosis, clinical pain score, or exact force-plate measurement.

## Platform Story

WHOOP and Strava are appropriate in this repo as source-specific evidence contexts:

- WHOOP: longitudinal HR, HRV, recovery, and strain context.
- Strava: functional distance and route context.
- Kubios/Polar H10: RRI/HRV and accelerometer movement-burden context.

Google is appropriate only as a reproducibility/runtime context for Colab instructions. No Google, Fitbit, Apple Health, or generalized health-platform story should be used as a legal conclusion unless the sourced record supports that specific platform claim.

## Gaps/TODOs

- The top-level `README.md` still mixes modern filed Exhibit A verification guidance with older generic Jupyter setup notes. A later docs cleanup should split legal reproducibility instructions from general environment setup.
- `legal/README.md` is empty. A later pass should either add a short legal evidence architecture overview or remove the empty file if it is intentionally unused.
- Legacy exploratory notebooks still contain old stored outputs and historical analysis cells. This audit softened source text but did not clear or recompute outputs.
- The requested broad `find . -maxdepth 4` command surfaces local environment and IDE files such as `.venv`, `.idea`, and support libraries. The audit itself used tracked files for evidence-layer conclusions.
- The filed-output `legal_language_snippets.md` under `legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/` is an ignored generated artifact. The tracked drafting copy is `legal/docs/legal_language_snippets.md`.

## Recommended Merge/Readiness Status

Recommended status: ready to merge after validation passes.

Reasoning:

- Filed evidence was not deleted.
- Frozen filed notebook was not edited.
- Court-filed artifacts were not regenerated.
- Existing hash and smoke checks pass.
- Evidence/index traceability exists and points to concrete paths.
- Legacy overclaiming in exploratory notebook source text was reduced.

Manual review should focus on whether to further clean or archive legacy top-level notebooks, not on filed Exhibit A integrity.
