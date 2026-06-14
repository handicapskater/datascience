# FSI/CSS Mobility Burden Analysis for Case 25-7526

## Executive summary

This report extends the existing Exhibit A / Appendix A evidence layer with Fractal Stability Index (FSI) and Comparable Similarity Score (CSS) metrics. FSI summarizes source linked accelerometer burden features into a reproducible instability/burden score. CSS summarizes how far a comparison context is from the lower burden reference context after feature normalization.

FSI and CSS do not diagnose pain and do not independently prove pain, disability, or legal entitlement. They provide objective, reproducible, source linked burden and similarity measurements that corroborate the broader medical, biomechanical, agency, DMV, transportation, video, declaration, WHOOP, Strava, and Kubios record.

The current Kubios/Polar H10 samples are small and should be treated as presumptive and directional while additional data is gathered. The present results reproduce the filed Exhibit A ratios and trend toward a conclusive burden pattern if future samples continue to align with these measurements.

## Data sources

| source | path | sha256 |
| --- | --- | --- |
| case_corpus | legal/cases/25-7526/data/2026-06-03_fsicss_legal_corpus_categorized.jsonl | f31810dadd85e57a8ae5199af504d6f0708349f05bc651ae66a8d05079d917db |
| walking_summary | legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/kubios_walk_vs_mall_pt_summary.csv | 13d41f275c79c0d0d78d6b791b59468c3b87e11993e253e75443cc4f4cd973b9 |
| walking_ratios | legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/walking_vs_mall_pt_ratios.csv | 6c31621a0faa71113624aa5219660c2ae68a530f2045cfd6c27546a901c00e77 |
| vehicle_summary | legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/kubios_paratransit_vehicle_summary.csv | f245ea5c309570a6a7827f1172bc391fe84e32284840c84bc7cfd8fd9905d448 |
| vehicle_ratios | legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/paratransit_vehicle_ratios.csv | 132d163b3250565ea5933b707bbb35173b81dae83d7fa7b096193bf32eedb593 |
| whoop_summary | legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/whoop_hr_summary.csv | 08e05c9dcf51c03d3414bee0556c0adb228ea191e1c99fcd28b9d7de3e741ffe |
| strava_summary | legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/strava_functional_distance_summary.csv | 0142738c2f00679ec0d1964c110cf821b150ee034257ed81cce81766fa63429b |
| reconciliation | legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/tables/exhibit_value_reconciliation.csv | 13adfdbe4c84105d5ece5a23e664b2dfeda2e20c7b27249174f06335db13492f |

## Reproducibility

Run from the repository root:

```bash
python3 scripts/analyze_fsi_css_25_7526.py --case-dir legal/cases/25-7526 --pretty
```

The script first validates the filed Exhibit A ratios within rounding tolerance. If a filed ratio does not reproduce, it stops rather than silently changing cohort labels.

## Definitions

**FSI (Fractal Stability Index).** Higher FSI burden means less stable or more mechanically burdensome movement/ride. This case specific FSI uses normalized accelerometer derived features. For walking versus Mall/PT controlled skating, the lower burden reference is Mall/PT controlled skating and the features are `vertical_mean`, `vertical_rms`, `movement_std`, and `peaks_per_min`. For ParaTransit vehicle comparison, the lower burden reference is sedan and the features are `vertical_mean`, `vertical_rms`, `movement_std`, `peaks_per_min`, `peak_abs`, and `peak_to_peak`. FSI is the mean of feature ratios to the reference.

**CSS (Context Similarity Score).** CSS compares normalized feature vectors to the lower burden reference. A CSS closer to 1.0 means more similar to the lower burden reference; a larger distance means a greater difference from that reference. CSS is reported as `1 / (1 + Euclidean distance from reference)`.

These definitions are reproducible summary metrics for the filed tables. They are proxy metrics, not exact anatomical force measurements.

## Comparator 1: Walking vs Mall/PT controlled skating

### Raw feature means

| group | records | vertical_mean | vertical_rms | movement_std | peaks_per_min | peak_to_peak |
| --- | --- | --- | --- | --- | --- | --- |
| Walking | 3 | 99.86 | 131.77 | 127.07 | 29.06 | 1153.0 |
| Mall/PT controlled skating | 11 | 65.51 | 87.7 | 83.67 | 27.76 | 1463.36 |

### Feature ratios

| metric | walking | Mall/PT controlled skating | walking_to_mall_pt_ratio |
| --- | --- | --- | --- |
| vertical_mean | 99.86 | 65.51 | 1.5243 |
| vertical_rms | 131.77 | 87.7 | 1.5025 |
| movement_std | 127.07 | 83.67 | 1.5187 |
| peaks_per_min | 29.06 | 27.76 | 1.0468 |

### FSI and CSS scores

| group | reference | records | FSI | FSI ratio | benefit | CSS similarity | CSS distance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Walking | Mall/PT controlled skating | 3 | 1.3981 | 1.3981 |  | 0.5281 | 0.8937 |
| Mall/PT controlled skating | Mall/PT controlled skating | 11 | 1.0 | 1.0 | 0.2847 | 1.0 | 0.0 |

Walking produced greater vertical and instability burden despite far shorter exposure, while controlled skating supported substantially greater functional mobility. The primary basic mobility comparator remains walking versus Mall/PT controlled skating; FNS/SNS endurance skating is not used as the primary basic walking comparator here.

## Comparator 2: ParaTransit bus/cutaway and van vs sedan

### Raw feature means

| group | records | vertical_mean | vertical_rms | movement_std | peaks_per_min | peak_abs | peak_to_peak |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ParaTransit bus/cutaway | 3 | 114.56 | 178.67 | 121.86 | 31.57 | 2717.68 | 4750.0 |
| ParaTransit van | 2 | 115.7 | 181.08 | 96.65 | 25.63 | 2813.89 | 5022.5 |
| ParaTransit sedan | 3 | 74.77 | 119.48 | 65.29 | 21.54 | 1954.9 | 2883.0 |

### Vehicle ratios

| vehicle | metric | vehicle_value | sedan_value | ratio_vs_sedan |
| --- | --- | --- | --- | --- |
| ParaTransit bus/cutaway | vertical_mean | 114.56 | 74.77 | 1.53 |
| ParaTransit bus/cutaway | vertical_rms | 178.67 | 119.48 | 1.5 |
| ParaTransit bus/cutaway | movement_std | 121.86 | 65.29 | 1.87 |
| ParaTransit bus/cutaway | peaks_per_min | 31.57 | 21.54 | 1.47 |
| ParaTransit bus/cutaway | peak_abs | 2717.68 | 1954.9 | 1.39 |
| ParaTransit bus/cutaway | peak_to_peak | 4750.0 | 2883.0 | 1.65 |
| ParaTransit van | vertical_mean | 115.7 | 74.77 | 1.55 |
| ParaTransit van | vertical_rms | 181.08 | 119.48 | 1.52 |
| ParaTransit van | movement_std | 96.65 | 65.29 | 1.48 |
| ParaTransit van | peaks_per_min | 25.63 | 21.54 | 1.19 |
| ParaTransit van | peak_abs | 2813.89 | 1954.9 | 1.44 |
| ParaTransit van | peak_to_peak | 5022.5 | 2883.0 | 1.74 |

### FSI and CSS scores

| group | reference | records | FSI | FSI ratio | sedan benefit | CSS similarity | CSS distance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ParaTransit bus/cutaway | ParaTransit sedan | 3 | 1.5662 | 1.5662 |  | 0.4102 | 1.438 |
| ParaTransit van | ParaTransit sedan | 2 | 1.4858 | 1.4858 |  | 0.4434 | 1.2554 |
| ParaTransit sedan | ParaTransit sedan | 3 | 1.0 | 1.0 | vs_bus=0.3615; vs_van=0.327 | 1.0 | 0.0 |

Bus/cutaway and van rides should be evaluated as passive mechanical stressors, not ordinary seated travel, because the same pipeline shows higher movement burden than sedan. WHOOP ParaTransit records remain useful general physiological context, but the vehicle type comparison here relies primarily on Kubios/Polar H10 accelerometer and RRI context supported by video/declaration evidence.

## Accommodation relevance

- Controlled skating FSI burden was 1.00 against a walking FSI burden of 1.40, an estimated controlled skating burden reduction of 28.5% relative to walking.
- Sedan FSI burden was 1.00 by definition against bus/cutaway FSI burden of 1.57, an estimated sedan burden reduction of 36.2% relative to bus/cutaway.
- Sedan FSI burden was 1.00 by definition against van FSI burden of 1.49, an estimated sedan burden reduction of 32.7% relative to van.

FSI/CSS help quantify accommodation relevance by translating the filed accelerometer comparisons into repeatable burden and similarity estimates. They support individualized accommodation review by showing that the lower burden mobility and transportation contexts are measurable, source linked, and reproducible.

## Limitations

- Kubios/Polar H10 sample sizes are small and should be treated as presumptive while additional data is gathered.
- Accelerometer derived features are proxy metrics, not exact anatomical force measurements.
- This report is not a medical diagnosis.
- FSI, CSS, WHOOP, Strava, Kubios, and wearable data do not independently prove pain.
- The results should be read with medical history, biomechanics evidence, agency records, DMV records, videos, declaration testimony, WHOOP context, Strava route/distance context, and Kubios/Polar H10 evidence.
- Strava is strongest for functional route/distance evidence and is not used as the primary bus/van/sedan comparator.

## Court safe language

FSI and CSS provide reproducible, source linked metrics for comparing mechanical burden across specific mobility and transportation contexts. In this record, walking shows higher vertical and instability burden than Mall/PT controlled skating, while controlled skating is associated with substantially greater functional route capacity. These metrics corroborate the broader record; they do not diagnose pain or independently prove pain.

For ParaTransit, Kubios/Polar H10 accelerometer features show higher passive movement burden in bus/cutaway and van contexts than in sedan context. That comparison supports individualized accommodation review because vehicle type can materially affect mechanical exposure even while the person is seated.

The FSI/CSS analysis should be presented as objective burden quantification that complements the medical, biomechanical, agency, DMV, transportation, video, declaration, WHOOP, Strava, and Kubios record. It supports accommodation relevance and burden reduction analysis without claiming that any single metric proves pain or guarantees a legal outcome.
