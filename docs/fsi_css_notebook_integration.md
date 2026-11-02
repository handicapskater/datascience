# FSI/CSS usability without changing the Observatory

This is a consumer design and a small input-readiness demonstration. The
notebooks consume existing publication artifacts. No platform source, formula,
registry entity, API, warehouse, deployment, or production UI is changed.

The [research evolution companion](research_evolution.md) places synthesis in
the original WHOOP/Strava hypothesis lineage and subsequent targeted
Kubios/Polar integration. Longitudinal context remains part of the scientific
account; it must not be used to manufacture missing episodic inputs. Historical
FSI/CSS-style fields in a legal snapshot are not automatically equivalent to
today's canonical formula identities. Verify that relationship before comparing
values, and never backfill current scores into a preserved exhibit.

## Findings first, synthesis second

The strongest accommodation-relevant pattern is repeated functional loss in
walking, greater distance in PT skating, and greater walking vertical RMS/jerk
than Mall skating. A synthesis should keep those dimensions visible, with a
link from each value to its source. A single scalar must not replace them.

The authority remains the platform's `EVIDENCE_AUTHORITY_CONTRACT.md`, frozen
implementations, and REG-06 synthesis/provenance records. FSI is Fractal
Stability Index. CSS is Cohort Similarity Score.

| Public finding / input | Frozen Tensor v0.3 relationship | Consumer treatment |
| --- | --- | --- |
| Vertical dynamic RMS | Existing session input, mapped to `vertical_rms` | Verify unit/conversion, scope and observed coverage |
| MAD-based impact rate | Existing input `impact_rate_per_min` | Preserve exact threshold definition, including contrary result |
| Shock-spike rate | Different threshold definition | Companion finding; never silently substitute for impact rate |
| Session mean HR and RMSSD | Existing physiology inputs | Require episodic scope; exclude overnight WHOOP HRV substitution |
| Session duration | Existing input; canonical seconds require platform conversion to minutes | Preserve exposure separately from function |
| Jerk and P90/P95/P99/P99.9 tails | No direct substitution in the frozen five-input session envelope | Display as companion mechanical findings |
| Recorded functional distance | Strong direct functional evidence; not interchangeable with the Tensor's functional-output axis | Keep observed distance separate from cohort-derived defaults |
| FNS/SNS longitudinal distance | Different grain/context | Do not manufacture an episodic FSI from an aggregate median |

Tensor has additional axes and can fall back to cohort-specific defaults.
The bounded source audit below traces the current input adapter. Before
presenting stronger score comparisons, review its normalization scale and
default-axis sensitivity against the frozen formula's intended calibration.
Public aggregate medians cannot replace session inputs.

Distinguish observed inputs, formula-derived axes, and assumed/default axes.
A cohort-dependent score contrast partly driven by those defaults cannot be
used as independent confirmation of the cohort difference. Likewise, a score
derived from RMS cannot independently validate the same RMS finding.

## Preserve each identity

| Identity | Formula version | What it can do |
| --- | --- | --- |
| `fsi_raw_signal` | `fsi_raw_signal_c_k_f.v1` | Summarize eligible original signal structure with C/K/F/V lineage |
| `fsi_tensor_v0_3` | `fsi_tensor_v0_3_msk_autonomic_gated_burden` | Summarize eligible session inputs and named axes under the frozen formula |
| `css_raw_pairwise` | `css_raw_pairwise.v1` | Compare governed representations; disclose any FSI-only fallback |
| `css_cohort_review` | `css_cohort_review_robust_distance.v1` | Describe typicality relative to a specified cohort/reference |
| `css_same_day_triplet` | `css_same_day_triplet.v1` | Represent stage similarity in the governed same-day comparison |

Legacy cohort-relative burden ratios are not official FSI. Pairwise CSS,
same-day CSS, and descriptive return-toward-Mall direction are different
contracts. Reciprocal cohort summaries need not share identical row counts;
pair counts must not be described as independent sample sizes. Higher
similarity does not imply a preferred mobility aid or less pain.

The current publication includes session-level FSI graph points and repeated
protocol records. They are deliberately not copied into this minimal excerpt.
The excerpt therefore reports no numeric FSI/CSS score and no session coverage
percentage. REG-06 eligibility flags alone cannot fill that gap.

## Safe adoption sequence

1. Use these notebooks as the external consumer prototype. They read pinned,
   local aggregate artifacts and can validate against an existing publication
   snapshot; no live Observatory dependency is introduced.
2. Extend the source audit below to persisted FSI/CSS outputs using governed read-only
   adapters. Verify formula/code hash, unit conversion, session identity,
   cohort provenance, component coverage, default/fallback use and validation.
   Keep expected and available inputs separate; missing is not zero.
3. Define a platform-owned aggregate score/component projection with explicit
   sample grain and privacy review. Reuse existing registry synthesis IDs and
   provenance routes. Make no numerical claims from unsupported projections.
4. If a UI addition is warranted, add component and coverage disclosure through
   existing Observatory adapters behind a default-off feature flag. Preserve
   feature-off response shape, graph/resource IDs, scientific values, and
   existing navigation. Compare against the existing runtime fixtures and
   required focused adapter/UI tests before a deployment decision.
5. Retain the prior artifact/flag state for rollback. Promote only after
   read-only parity and local visual review. No deployment is part of this
   notebook update.

The notebook helper `scripts/synthesis_readiness.py` demonstrates missing,
nonfinite, unit/scope and impact-definition checks using synthetic tests. It
does not resolve sessions, calculate a score, approve eligibility, or replace
the platform validator. It returns no score even when all example inputs are
present.

## Bounded source audit completed

This read-only inspection followed `scientific_persistence.py` into `fsi.py`,
`fsi_tensor_v0_3.py`, `similarity.py`, and `same_day_css_triplets.py`. It did not
open DuckDB, recompute a session or inspect prospective outcomes.

1. **Tensor input mapping is explicit.** `_formula_record` passes canonical
   `vertical_dynamic_g_rms` directly as `vertical_rms`, and converts full-recording
   duration seconds to minutes. The scalar adapter passes that record to frozen
   Tensor v0.3. The fallback mechanical axis divides vertical RMS by `300.0`;
   no g-to-milli-g conversion occurs at this adapter boundary. That combination
   warrants a calibration/scale review before attributing substantial influence
   to measured RMS. It is not authorization to change the frozen denominator.
2. **Several axes are default-derived in this path.** `_source_values` marks
   load-path, passive exposure, control loss, functional-output burden and
   complexity source axes unavailable. Component persistence records whether
   frozen defaults were used. A display should expose those component records,
   not equate a scalar confidence/coverage label with fully observed axes.
3. **Persisted raw-pairwise CSS uses the FSI-only fallback.** `_pairwise_css_rows`
   passes only `{"FSI": score}` for each session and records
   `feature_matrix_supplied=false`. In `compute_css`, all three similarity
   terms then equal `1 - clip(abs(FSI_A - FSI_B), 0, 1)`. Under the default
   weights, the published scalar is that same quantity. It supplies no
   independent confirmation of the input Tensor contrast.
4. **Existing same-day CSS already uses measured domains.** Its feature list
   includes session HR/RMSSD/SDNN, vertical/horizontal RMS, their ratio,
   vertical/magnitude jerk, shock-spike rate, cumulative dynamic shock, movement
   fraction and duration. It records shared metrics and uses within-triplet
   normalized vector distance. Observed distance and tail percentiles are not
   in that list. Show its feature contributions alongside functional distance;
   do not relabel it as the raw-pairwise scalar or a burden direction.

Practical choice: use existing same-day CSS for a stage-profile comparison,
while keeping functional distance and signed mechanical differences visible.
Use Tensor as a qualified descriptive synthesis with default/coverage disclosure.
Complete the calibration and persisted-lineage review before proposing any new
FSI weighting, expanded CSS domain vector or production UI change.

## Future metrics and experiments

Jerk, tail/event morphology, observed function and domain-level CSS could
improve interpretability. They should first remain visible as separate
measurements. CSS-X01's Function/Mechanics/Physiology/Exposure/Control domain
representation is promising experimental work, not canonical CSS. FSI-X01 is
unexecuted with low information value. BCT is design-only; PVC-01 remains
waiting for new post-lock data. No prospective outcome is needed for this
presentation update.

Adding metrics to a formula requires explicit approval of a new version and
an evaluation protocol. That protocol should test incremental information on
independent dates with transparent baselines and measured-input/default-axis
sensitivity, without using the score's own inputs as independent validation.
