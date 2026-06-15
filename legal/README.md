# Legal Evidence Layer

This directory contains the court-safe evidence layer for case `25-7526`.

## Filed Exhibit A path

Frozen notebook:

`legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb`

Canonical filed PDF:

`legal/cases/25-7526/filed/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf`

Primary verification commands from the repository root:

```sh
make check-filed-artifact-locks
make verify-filed-exhibit-a
make compare-filed-exhibit-a
```

Do not use the frozen filed notebook for ongoing research edits.

## Living research path

Living wearable notebook:

`legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb`

This notebook is for ongoing wearable-health analytics, mobility accommodation intelligence, integrated evidence review, and source-linked research outputs. It may generate living reports, tables, manifests, and figures, but it does not mutate the filed Exhibit A notebook, filed PDF, or filed hash locks.

## Legacy/supporting public notebook

Legacy public notebook:

`HandicapSkater-Public.ipynb`

This is retained for historical public/scientific context and supporting analysis. It is not the filed legal reproduction notebook.

See `docs/notebook_roles.md` and `legal/notebooks/README.md` for the concise notebook-role landing pages.
