# Public notebook guide

The three root notebooks now present a small governed aggregate excerpt:

- `HandicapSkater-Public.ipynb`: restored technical portfolio and systematic
  overview spanning problem formulation, Data Engineering, Descriptive and
  Inferential Statistics, Deep Learning, Model Evaluation, XGBoost/SHAP,
  FSI/CSS, evidence-backed conclusions, and a corrected bibliography; retains
  the functional mobility argument, aggregate results and chart.
- `HandicapSkater-Scientific.ipynb`: hypothesis-to-metric continuity, methods,
  inference grain, source/time-scale roles, effect/interval provenance and
  FSI/CSS input readiness.
- `HandicapSkater-ScientificSuccinct.ipynb`: compact reviewer summary.

They are readable as static notebooks and run from a local repository checkout.
The public figure contains six group medians across three panels; it is not a
reconstruction of session records. The JSON excerpt is less than 20 KB and
contains no session rows, activity identifiers, raw telemetry or routes.

Public distinguishes current governed findings, historical modeling work, and
corrected designs awaiting execution. Its dense-network architecture and
grouped split-before-scaling examples are non-executing Markdown templates;
they do not add training dependencies or imply replacement model performance.
The reference audit preserves the original bibliography's provenance, corrects
misattributed authors/years, and marks unresolved entries and the historical
Rogers quotation as unverified rather than reusing them as evidence. The
conclusions cite both current result authorities and relevant literature.

All three notebooks link the [research evolution companion](research_evolution.md).
It preserves the original WHOOP/Strava hypotheses and longitudinal foundation,
maps them to the legal notebook's source-role sections, and explains the
refinement of combined longitudinal-plus-episodic evidence. Polar/Kubios
comparisons were already part of the legal notebook design; the later work
deepens their integration rather than replacing the long-history record.
This external scientific context does not revise a filed artifact, declare
record-level equivalence, or retrospectively validate every historical claim.

## Local setup and checks

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-public.txt
make public-notebook-check PYTHON=.venv/bin/python
```

Installing `nbstripout` repairs the missing dependency in this checkout's
existing Git filter. Creating a fresh checkout does not require a Git filter
to read the notebooks. Do not apply stripping or trust/execute commands to the
frozen legal notebook.

The notebooks find the repository from the working directory; launch Jupyter
from this checkout. A standalone copied notebook needs the `scripts/` and
`data/public/` companion files. No credential, live service or download is
required to inspect the pinned results.

Read-only parity against the matching local publication snapshot:

```sh
.venv/bin/python scripts/public_notebook_evidence.py --source-root \
  ../biomechanics/data/public/evidence-observatory/v1
```

A changed upstream hash intentionally fails this check. Update the excerpt,
source identities and lock only as a reviewed new release; never silently
refresh from a mutable URL. Bootstrap intervals, effects and denominators are
copied from existing authorities, not recomputed.

Render the aggregate chart on the operator's M1 Max:

```sh
make public-notebook-figures PYTHON=.venv/bin/python
```

The public JSON carries source byte hashes and semantic content hashes. Core
effects/intervals retain Core authority; IB-01 method-check summaries retain
their separate scope. Source reuse is not independent replication.

## Historical and legal preservation

Before replacement, all three root notebooks were copied byte-for-byte to the
ignored local `.notebook_backups/2026-09-10/` directory. Existing Git history is
also retained. Do not commit that private backup directory. The old untracked
Public PDF and modified manual-labor CSV were left untouched and are not
current outputs of these notebooks.

All files beneath `legal/`, including both notebooks, scripts, PDFs, input
corpus and hash locks, were preserved. A private pre-edit hash inventory is
stored with the local backups. Verify preservation locally with:

```sh
.venv/bin/python scripts/check_legal_preservation.py
```

This checks preservation, not correctness of the pre-existing evidence locks.
The known raw-notebook mismatch, invalid two-page output copy and 12-page
candidate remain recorded in the workspace audit. The original expected
hashes were not changed. The stronger instruction to leave legal files intact
defers the earlier plan's legal-script hardening and living-legal-notebook edits.

Only the new excerpt and notebook outputs were reviewed for limited disclosure.
Historical `data/`, `html/`, `reports/`, legal files and prior Git history have
not been certified public-safe by this update. Keep any repository-wide privacy
or history remediation a separate, explicitly scoped task.

No platform, website, registry, or Observatory source was changed. See
`fsi_css_notebook_integration.md` for the proposed next integration steps.
