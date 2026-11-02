# Notebook Roles and Boundaries

This repository separates current public companions, living private research,
and frozen legal reproduction. They should not be treated as interchangeable.

## Current public companions (September 2026)

- `HandicapSkater-Public.ipynb`: systematic technical portfolio, governed
  aggregate mobility evidence, and referenced conclusions, retaining its role
  as the original longitudinal WHOOP/Strava and hypothesis foundation.
  Historical modeling designs remain visible without republishing unvalidated
  performance.
- `HandicapSkater-Scientific.ipynb`: research lineage, hypothesis-to-metric
  crosswalk, source/time-scale distinctions, methods and synthesis readiness.
- `HandicapSkater-ScientificSuccinct.ipynb`: compact reviewer summary.

See `public_notebooks.md` for setup, source/hash verification and the local
historical backups. These notebooks are not legal reproduction sources.
The external [research evolution companion](research_evolution.md) explains how
the original questions informed the legal source-role design and how targeted
Polar/Kubios evidence was integrated and refined. It does not backdate later
findings into the filed record or claim row-level equivalence across versions.

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

## 3. Foundational longitudinal public analysis

Path:

`HandicapSkater-Public.ipynb`

Role:

- The original Public notebook established the longitudinal WHOOP/Strava
  analysis and explicit hypotheses that informed the legal notebook design.
  The source history and pre-update bytes remain in Git and ignored backups.
- The current root Public notebook restores the systematic overview and
  technical narrative alongside governed aggregate evidence. Its model
  templates are non-executing and its bibliography records corrections and
  unresolved sources. Corrections attach to specific methods and claims; they
  do not discard the foundational observations or rewrite the legal notebooks.
  Historical hypothesis authority is distinct from current numerical-result
  authority and from the frozen exhibit's own source and value locks.

Do not cite this notebook as the filed Exhibit A reproduction source. For filed legal verification, use the frozen Exhibit A notebook and `make` commands above.
