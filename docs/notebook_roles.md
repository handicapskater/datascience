# Notebook Roles and Boundaries

This repository has three notebook roles. They should not be treated as interchangeable.

## 1. Frozen filed Exhibit A notebook

Path:

`legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb`

Role:

- Reproduce the filed Exhibit A record for case `25-7526`.
- Preserve the court-filed evidence logic and locked output paths.
- Support verification of the filed PDF, input corpus hash, and frozen notebook hash.

Primary verification commands:

```sh
make check-filed-artifact-locks
make verify-filed-exhibit-a
make compare-filed-exhibit-a
```

Use this notebook only for filed-record reproduction or intentional filed-record correction. Do not use it for living research edits.

## 2. Living wearable research notebook

Path:

`legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb`

Role:

- Maintain the reproducible case-study record for wearable-health analytics, mobility accommodation intelligence, and source-linked evidence organization.
- Generate living research outputs under non-filed output locations, including notebook summary reports, manifests, cohort tables, and figures.
- Explain ongoing research caveats without implying mutation of filed court artifacts.

This notebook may consume integrated evidence and produce platform-facing research outputs, but it does not update the filed Exhibit A PDF or the frozen Exhibit A notebook lock.

## 3. Legacy/supporting public notebook

Path:

`HandicapSkater-Public.ipynb`

Role:

- Preserve earlier public/scientific exploration and supporting narrative context.
- Provide historical analysis context that predates the filed legal evidence architecture.
- Serve as a legacy supporting notebook, not the canonical legal reproduction path.

Do not cite this notebook as the filed Exhibit A reproduction source. For filed legal verification, use the frozen Exhibit A notebook and `make` commands above.
