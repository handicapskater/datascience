# Research evolution: longitudinal foundation to integrated evidence

The original **HandicapSkater-Public.ipynb established the longitudinal
WHOOP/Strava analysis and the original research hypotheses**. It was not merely
an early machine-learning demonstration. Its activity history, physiological
comparisons, distance/route context, and engineering workflow supplied the
research foundation that informed the legal notebooks and subsequent targeted
measurement. Correcting an analysis does not erase that contribution or discard
the underlying observations.

This companion documents the scientific progression outside the preserved legal
tree. It is a methods/history crosswalk, not a replacement exhibit, a new
analysis, or an assertion that later findings were available at filing.

## 1. The progression, with overlapping stages

| Stage | Scientific contribution | Relationship to the next stage |
| --- | --- | --- |
| Longitudinal foundation: original Public | Assemble repeated WHOOP activity/physiology and Strava activity/distance/route context; formulate walking-versus-skating hypotheses; explore distributions and predictive models | Establish the questions and observational context that motivated more specific comparisons |
| Documented evidence integration: legal notebooks | Organize WHOOP physiological context, Strava functional distance, and targeted Kubios/Polar H10 comparisons; preserve evidence manifests, cohort rules and exhibit reconciliation | Make source roles and the evidence snapshot reviewable; preserve what that version actually contains |
| Refined longitudinal-plus-episodic analysis: governed platform | Retain the long history while linking eligible targeted recordings to context; separate recovery from session HRV; use defined movement metrics and paired-date comparisons | Test narrower questions with explicit eligibility, units, uncertainty, counter-results and provenance |
| Current public companions | Explain the full research lineage and present selected governed aggregates | Make the reasoning inspectable without distributing private session or legal records |

These are stages of development, not mutually exclusive data periods. The legal
notebook already contained a **Kubios RRI/HRV+ and accelerometer** section when
introduced into the inspected repository history. Episodic measurement did not
begin only after the legal work. The later platform develops that integration
further; it does not replace the longitudinal foundation with Polar H10.

## 2. Repository evidence for this account

The following locators are source-code history, not dates of data collection,
preregistration, clinical validation, or proof of when an idea was first formed.
They allow a maintainer with the existing checkout to inspect the account
without including historical outputs or private records in this document.

| Repository version inspected | Source locator | What it documents |
| --- | --- | --- |
| `6342ccc` (authored 2025-06-02) | Original Public, “Hypotheses” and “Data Engineering - Data Pipeline” (zero-based cells 3 and 4) | Earliest retained Public version inspected: explicit H₀/H₁, WHOOP merging/feature engineering, recurring activity updates and Strava mapping/distance context |
| `bb2306d` (authored 2026-06-04) | Filed-notebook introduction; sections 4, 5, 6 and 8 | WHOOP physiology, Strava functional distance, Kubios RRI/HRV+/ACC, and reconciliation against the exhibit's own values already coexist |
| `84f5f7d` (authored 2026-06-10), plus preserved working source | Living research notebook, “Source Roles,” “Duplicate Handling,” and “Court-Safe Findings” | Longitudinal chronology plus targeted sensor evidence; duplicate retention; Kubios attachment requires time-alignment review |
| `c687577` (authored 2026-06-15) and local role documentation | Notebook-role separation | Filed reproduction and living research are separate from the original public analysis |
| Current pinned public bundle, data through 2026-09-03 | `data/public/skating_evidence.v1.json` and its SHA-256 sidecar | Selected current findings with source identities and endpoint-specific denominators; no historical exhibit recalculation |

The user's account identifies the foundational design relationship; the source
history corroborates the earlier hypotheses and the later source-role
structure. **This is hypothesis/design lineage, not a verified row-for-row data
derivation between notebook versions.** Such a derivation would require the
existing governed source IDs, hashes, mapping versions and event links. This
documentation does not infer missing links from similar labels or dates.

## 3. Original hypotheses and their scientific refinement

The earliest inspected Public version explicitly stated:

> **Null Hypothesis (H₀):** There is no significant difference in HRV or HR zone distribution between walking and skating activities.

> **Alternative Hypothesis (H₁):** Skating yields significantly different cardiovascular metrics (e.g., lower HR Zone 4/5 percentages, higher HRV), due to less pain-induced stress.

These quotations record the **original hypothesis wording**, not a current
finding or a preregistration claim. The original variables also included heart
rate parameters, duration, and distance for walking and skating. Thus the
research question already connected physiology to functional output; the later
mechanical work is a refinement of that question, not its origin.

For current inference, separate the distributional/paired contrast from its
proposed explanation. A statistical null concerns a specified parameter or
distribution, not whether a p-value will cross a threshold. The proposed
pain-related mechanism requires evidence beyond an activity label or HR/HRV
difference. WHOOP recovery HRV is overnight context; it cannot establish a
within-session HRV effect. The original directional HRV expectation can be
supported, qualified, contradicted or unresolved at the appropriate scope.
Higher walking RMS/jerk does not itself confirm that HRV hypothesis.

The present public excerpt contains longitudinal functional-distance summaries
and paired distance/mechanics, not a WHOOP physiological-effect table or an
episodic HRV contrast. The source-role crosswalk below describes the research
continuity; it does not assert an unreported physiological result. Extending
the public presentation to those longitudinal physiology questions requires
a reviewed, source-linked aggregate projection, not renewed distribution of
the original private records or reuse of a defective historical test.

### Hypothesis-to-evidence crosswalk

| Foundational question | How the legal design organizes it | Current scientific development | What is not implied |
| --- | --- | --- | --- |
| Does walking impose a different physiological burden relative to recorded activity? | WHOOP physiological-context section alongside Strava distance; targeted Kubios physiology treated separately | Activity-level WHOOP and overnight readiness remain longitudinal context; eligible Polar/Kubios session HR/RMSSD address episodic physiology | HR or HRV alone identifies pain, or one source's HRV can fill the other's missing values |
| Does skating enable sustained useful mobility? | Strava functional-distance/route section and long-history context | Longitudinal FNS/SNS evidence plus a distinct paired Walking→PT distance comparison | A protocol distance is maximum capacity, or long-history and paired subsets share the same denominator |
| Can movement measurements make the burden question more specific? | Kubios accelerometer comparator section with orientation/proxy caveats | Defined vertical dynamic RMS, magnitude jerk, shock-spike rates, retrospective tails/event density and paired-date checks | A body-worn accelerometer directly measures internal joint force, or every impact definition must agree |
| How can the evidence be reviewed and reproduced? | Source manifests, cohort rules, duplicate accounting and exhibit-value reconciliation | Governed event/source linkage, versioned metrics, explicit missingness, pinned aggregates and audit boundaries | Similar summaries prove row-level identity or later analyses retroactively validate every filed number |

## 4. What improves with episodic measurement

“Better metrics” here means **more specific, source-appropriate and auditable
measurements for a defined question**, not that a newer device automatically
produces clinical proof.

- **Temporal specificity:** an eligible targeted RRI/HRV recording describes
  that episode, while WHOOP recovery describes an overnight period and Strava
  describes an activity. Link them as distinct roles when provenance supports
  the relationship; do not flatten them into one interchangeable HRV column.
- **Mechanical specificity:** RMS, jerk and explicitly defined event/tail
  measures describe different aspects of recorded motion. Preserve sampling,
  filtering, orientation, units, windows and threshold definitions. A legacy
  ACC summary must not be compared numerically with a current g-valued metric
  without verifying those definitions and conversions.
- **Comparison specificity:** the frozen exhibit's combined Mall/PT controlled
  skating group is not the current separate Mall and PT stage comparison.
  Preserve the earlier group and explain the newer design rather than silently
  relabeling the historical values.
- **Uncertainty and quality:** report eligible dates, effects and intervals,
  missingness, fixed-order/duration limitations and sensitivity results. More
  samples within an episode do not create more participants.
- **Convergent evidence:** longitudinal function and targeted physiology/
  mechanics can support a coherent within-person account. Shared recordings
  and overlapping dates are not independent replication. The opposite
  MAD-impact direction and qualified shock-rate results remain informative.

Polar's [official H10 documentation](https://github.com/polarofficial/polar-ble-sdk/blob/master/documentation/products/PolarH10.md)
describes the device's available recording capabilities. It does not establish
which streams were actually collected in a historical session; the source
artifacts and processing provenance establish that. Literature on
[pain-related autonomic responses](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2016.00109/full)
motivates the physiology question but does not make those responses a specific
pain detector. See the corrected bibliography in
[Public](../HandicapSkater-Public.ipynb#references) for the wider context.

## 5. Back the preserved record with science without rewriting it

The scientific support is an **external, versioned explanatory companion**:
identify the earlier question and source-role design, then distinguish what
current evidence corroborates, qualifies, contradicts or leaves unmeasured.
The current [computational evidence](https://handicapskater.com/data/public/evidence-observatory/v1/computational-evidence.json)
and [biomechanics evidence](https://handicapskater.com/data/public/evidence-observatory/v1/biomechanics-evidence.json)
are current result authorities, not substitutes for the exhibit's frozen input
corpus, eligible cohorts, processing rules or cut-off.

| Companion task | Preservation rule |
| --- | --- |
| Explain why the legal notebook used WHOOP, Strava and targeted Kubios sections | Cite the preserved section and distinguish design continuity from numerical replication |
| Relate an earlier claim to a later finding | Name the source version, cohort, metric definition, observation period, denominator and relevant qualification for each |
| Correct a historical interpretation or method | Record the correction outside the filed artifact; preserve both the historical statement and the scope of the correction |
| Investigate an exact historical numerical claim | Require a separately scoped, read-only source/definition reconciliation; no claim-by-claim revalidation is completed by this narrative |
| Explain FSI/CSS evolution | Preserve each historical/current formula identity, component scope and observed/default coverage; do not backfill new scores into the exhibit |

No file under `legal/`, expected hash, filed output or legal reproduction command
is changed or executed by this work. The separate local preservation check
detects changes relative to the pre-edit inventory; it does not resolve the
pre-existing raw-notebook-lock and output-copy discrepancies. No prospective
holdout is inspected. No new session data, raw signals, legal excerpts with
personal findings, routes or private identifiers are included in the public
aggregate input.

## 6. Cohesive reading order and next work

1. **Public:** the original longitudinal motivation and hypotheses, full
   technical portfolio, development history and current evidence-backed
   conclusions.
2. **Scientific:** the source/time-scale and hypothesis-to-metric distinctions,
   current inference units, counter-results and publication provenance.
3. **Preserved legal notebooks:** the historical source-role and exhibit/research
   structures, consulted through their existing access and integrity boundary;
   this companion is not a replacement filing.
4. **FSI/CSS integration:** follow the
   [component/coverage plan](fsi_css_notebook_integration.md), using existing
   governed adapters and keeping longitudinal function distinct from episodic
   synthesis. Any future platform/Observatory consumer change requires its
   normal parity and compatibility gates.

The next scientific support step, if separately undertaken, is a claim-level
crosswalk using preserved source identities—not a legal notebook rerun. For
each selected claim, record whether the current evidence is corroborating,
qualifying, contradictory or insufficient, and whether observations overlap.
Publication remains limited to reviewed aggregates. The Evidence Observatory,
canonical FSI/CSS formulas and existing legal locks remain unchanged.
