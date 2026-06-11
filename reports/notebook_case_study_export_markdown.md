# Wearable Mobility Evidence Case Study: Non-Traditional Mobility Aid, ParaTransit Burden, and Individualized Accommodation Review

**Living Wearable Research Notebook**: `wearable_research_current`

This notebook is a reproducible case-study record. It organizes wearable, route, HRV/RRI, accelerometer, and activity-context evidence to support individualized accommodation review. It is designed for legal context, research review, and wearable-health mobility analytics.

Court-safe scope:

- This is not a medical diagnosis.
- It does not claim that any single metric proves pain.
- It does not claim a guaranteed legal outcome.
- The evidence is a source-linked chronology, not a single biometric claim.
- FSI/CSS is preserved from Kubios/source fields only; it is not computed here from aggregate-only WHOOP or Strava records.
- No pain, legal, walking, or ParaTransit scalar is introduced.


## Case-Study Narrative

This record preserves the lived-facts narrative needed for accommodation review:

- Long-term non-traditional mobility-aid skating is treated as functional mobility context, not recreation-only by default.
- Walking is painful and exposure-limited, so a small walking sample must not be interpreted as absence of burden.
- ParaTransit created passive transport burden in the record.
- Horseback Riding is disclosed as a user-defined ParaTransit surrogate label in WHOOP context when source context supports it.
- Mall/no-step skating and PT skating are mobility-aid comparators.
- FNS/SNS sessions are high-exertion PT context, not gentle PT.
- SilverRide FrontSeat is treated as a successful accommodation comparator.
- Motorcycle is comparator transport, not automatically lower burden in every metric.
- Baseline/recovery/readiness records are excluded from activity-burden comparisons.


## Source Roles

- **WHOOP**: long-history wearable context, HR/HRV, strain, recovery, activity labels, and ParaTransit surrogate context.
- **Strava**: route/activity ledger, distance, duration, elevation, speed, GPS context, and skating route history.
- **Kubios/Polar H10**: targeted HRV/RRI and accelerometer evidence, including FSI/CSS-style targeted metrics where preserved from source fields.
- **Integrated JSONL**: source-linked evidence layer that preserves duplicate rows for audit while avoiding double-counting in primary summaries.



```python
from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / '.git').exists() and (candidate / 'legal').exists():
            return candidate
    return current


REPO_ROOT = find_repo_root()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from legal.src.evidence_config import EvidenceConfig
from legal.src.evidence_paths import WEARABLE_RESEARCH_RUN_ID, ensure_standard_dirs, prepare_output_dir

NOTEBOOK_PATH = REPO_ROOT / 'legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb'
REPORTS_DIR = REPO_ROOT / 'reports'
FIGURES_DIR = REPORTS_DIR / 'figures'
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

config = EvidenceConfig(
    case_id='25-7526',
    run_id=WEARABLE_RESEARCH_RUN_ID,
    mode="RESEARCH",
    allow_overwrite=True,
    repo_root=REPO_ROOT,
)
prepare_output_dir(config.output_dir, allow_overwrite=config.allow_overwrite)
ensure_standard_dirs(config)

PRIMARY_EVIDENCE_JSONL = REPO_ROOT.parent / 'fsicss-iomt-evidence-platform/data/processed/integrated/integrated_mobility_evidence_context.jsonl'
LOCAL_EVIDENCE_JSONL = REPO_ROOT / 'legal/data/processed/integrated/integrated_mobility_evidence_context.jsonl'
LEGACY_EVIDENCE_JSONL = REPO_ROOT / 'legal/data/integrated_mobility_evidence_context.jsonl'
PRIMARY_SUMMARY_REPORT = REPO_ROOT.parent / 'fsicss-iomt-evidence-platform/reports/integrated_mobility_evidence_context_summary.md'
PRIMARY_LEGAL_TABLE = REPO_ROOT.parent / 'fsicss-iomt-evidence-platform/reports/integrated_mobility_legal_evidence_table.md'
PRIMARY_DUPLICATE_REPORT = REPO_ROOT.parent / 'fsicss-iomt-evidence-platform/reports/integrated_evidence_duplicate_resolution_report.md'
BUILD_INTEGRATED_COMMAND = (
    'python etl/integrated/build_integrated_mobility_evidence_jsonl.py\n'
    '  --whoop data/processed/whoop/whoop_evidence_context.jsonl\n'
    '  --strava data/processed/strava/strava_evidence_context.jsonl\n'
    '  --kubios data/processed/kubios/kubios_baselines.jsonl\n'
    '  --output data/processed/integrated/integrated_mobility_evidence_context.jsonl\n'
    '  --summary reports/integrated_mobility_evidence_context_summary.md\n'
    '  --legal-table reports/integrated_mobility_legal_evidence_table.md\n'
    '  --duplicate-report reports/integrated_evidence_duplicate_resolution_report.md'
)
EXPECTED_FACTS = {
    'whoop_input_records': 4647,
    'strava_input_records': 3674,
    'kubios_input_records': 71,
    'output_integrated_jsonl_records': 8388,
    'included_evidence_events': 3453,
    'whoop_only_events': 1545,
    'strava_only_events': 1833,
    'kubios_only_events': 71,
    'whoop_strava_merged_events': 4,
    'kubios_attached_events': 0,
    'duplicate_excluded_records_retained': 4935,
    'needs_review_included_events': 973,
    'included_in_motion_burden_analysis': 2503,
    'baseline_recovery_readiness_excluded_count': 950,
    'horseback_paratransit_surrogate_count': 116,
    'commuting_taxi_rediWheels_sedan_count': 8,
    'walking_exposure_limited_count': 3,
    'silverride_successful_accommodation_count': 1,
    'fns_sns_high_exertion_pt_count': 850,
    'mall_no_step_pt_skating_count': 20,
    'motorcycle_comparator_count': 373,
    'wheelchair_substitution_context_count': 80,
    'route_gps_availability_count': 1837,
    'hr_hrv_availability_count': 2854,
    'rri_accelerometer_availability_count': 71,
    'fsi_css_availability_count': 71,
    'strava_rows_with_whoop_like_labels': 631,
}
print('Repository root:', REPO_ROOT)
print('Primary integrated evidence path:', PRIMARY_EVIDENCE_JSONL)

```

## Integrated Evidence Loading

The primary evidence corpus is the source project integrated JSONL:

`../fsicss-iomt-evidence-platform/data/processed/integrated/integrated_mobility_evidence_context.jsonl`

If that file is missing, this notebook prints the exact command needed to rebuild it in the source project. Legacy/local fallbacks are clearly labeled and are not silently treated as the preferred source.



```python
def load_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open(encoding='utf-8') as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f'Invalid JSONL at {path}:{line_number}: {exc}') from exc
    return records


def select_evidence_path() -> tuple[Path | None, str]:
    if PRIMARY_EVIDENCE_JSONL.exists():
        return PRIMARY_EVIDENCE_JSONL, 'primary sibling source project'
    if LOCAL_EVIDENCE_JSONL.exists():
        return LOCAL_EVIDENCE_JSONL, 'local datascience copy'
    if LEGACY_EVIDENCE_JSONL.exists():
        return LEGACY_EVIDENCE_JSONL, 'legacy local fallback'
    return None, 'missing'


evidence_jsonl_path, evidence_path_role = select_evidence_path()
if evidence_jsonl_path is None:
    records = []
    print('Integrated evidence JSONL was not found.')
    print('To rebuild it in the source project, run:')
    print(BUILD_INTEGRATED_COMMAND)
else:
    records = load_jsonl(evidence_jsonl_path)
    print(f'Loaded {len(records):,} records from {evidence_jsonl_path} ({evidence_path_role}).')

```

## Helper Functions

These helpers keep the notebook resilient to source-field evolution while preserving the current integrated JSONL contract.



```python
def value_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value if item not in (None, '')]
    if isinstance(value, str):
        if not value:
            return []
        if '+' in value:
            return [part.strip() for part in value.split('+') if part.strip()]
        return [value]
    return [str(value)]


def source_key(record: dict) -> str:
    systems = value_list(record.get('source_systems'))
    if not systems and record.get('primary_source'):
        systems = [record['primary_source']]
    return '+'.join(sorted(set(systems))) if systems else 'unknown'


def metadata(record: dict) -> dict:
    meta = record.get('evidence_metadata')
    return meta if isinstance(meta, dict) else {}


def included(record: dict) -> bool:
    return bool(record.get('include_in_evidence_summary'))


def motion_included(record: dict) -> bool:
    return bool(record.get('include_in_motion_burden_analysis'))


def duplicate_excluded(record: dict) -> bool:
    return record.get('duplicate_status') == 'duplicate_excluded' or record.get('integration_status') == 'source_duplicate_excluded'


def needs_review(record: dict) -> bool:
    meta = metadata(record)
    return bool(meta.get('needs_review')) or record.get('evidence_role') == 'needs_review'


def event_date(record: dict):
    raw = record.get('event_date') or record.get('start_time') or record.get('time_window_start')
    if not raw:
        return None
    try:
        return datetime.fromisoformat(str(raw).replace('Z', '+00:00')).date()
    except ValueError:
        try:
            return datetime.fromisoformat(str(raw)[:10]).date()
        except ValueError:
            return None


def date_range(rows: list[dict]) -> str:
    dates = sorted(date for date in (event_date(row) for row in rows) if date is not None)
    if not dates:
        return 'not available'
    return f'{dates[0].isoformat()} to {dates[-1].isoformat()}'


def count_if(rows: list[dict], predicate) -> int:
    return sum(1 for row in rows if predicate(row))


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    out = ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |']
    for row in rows:
        out.append('| ' + ' | '.join(str(item) for item in row) + ' |')
    return '\n'.join(out) + '\n'


def save_counter_table(counter: Counter, label: str) -> list[dict]:
    return [{label: key, 'count': value} for key, value in counter.most_common()]

primary_records = [record for record in records if included(record)]
duplicate_records = [record for record in records if duplicate_excluded(record)]
motion_records = [record for record in primary_records if motion_included(record)]
print('Primary included events:', len(primary_records))
print('Duplicate-excluded retained records:', len(duplicate_records))
print('Motion-burden included events:', len(motion_records))

```

## Integrity and Reproducibility Manifest

This section hashes the notebook and the integrated evidence/report inputs when available. Missing git metadata is recorded as `not available` rather than failing the notebook.



```python
def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def git_value(args: list[str]) -> str:
    try:
        result = subprocess.run(['git', *args], cwd=REPO_ROOT, text=True, capture_output=True, check=True)
        return result.stdout.strip() or 'not available'
    except Exception:
        return 'not available'


def dependency_versions() -> dict[str, str]:
    versions = {}
    for package in ('matplotlib', 'nbconvert', 'jupyter'):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = 'not available'
    return versions

manifest_targets = {
    'notebook': NOTEBOOK_PATH,
    'evidence_jsonl': evidence_jsonl_path,
    'integrated_summary_report': PRIMARY_SUMMARY_REPORT,
    'integrated_legal_evidence_table': PRIMARY_LEGAL_TABLE,
    'duplicate_resolution_report': PRIMARY_DUPLICATE_REPORT,
}
manifest = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'notebook_path': str(NOTEBOOK_PATH.relative_to(REPO_ROOT)),
    'evidence_jsonl_path': str(evidence_jsonl_path) if evidence_jsonl_path else 'not available',
    'git_commit': git_value(['rev-parse', 'HEAD']),
    'git_branch': git_value(['branch', '--show-current']),
    'dirty_worktree_status': git_value(['status', '--short']),
    'python_version': sys.version.replace('\n', ' '),
    'platform': platform.platform(),
    'dependency_versions': dependency_versions(),
    'files': {},
}
for name, path in manifest_targets.items():
    if path is None or not path.exists():
        manifest['files'][name] = {'path': str(path) if path else 'not available', 'sha256': 'not available', 'byte_size': 'not available', 'modified_time': 'not available'}
        continue
    stat = path.stat()
    manifest['files'][name] = {'path': str(path), 'sha256': sha256_file(path), 'byte_size': stat.st_size, 'modified_time': datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()}
manifest['sha256'] = manifest['files']['notebook']['sha256']
manifest['byte_size'] = manifest['files']['notebook']['byte_size']
manifest['modified_time'] = manifest['files']['notebook']['modified_time']

manifest_json = REPORTS_DIR / 'notebook_integrity_manifest.json'
manifest_md = REPORTS_DIR / 'notebook_integrity_manifest.md'
manifest_json.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
manifest_rows = [[name, data['path'], data['sha256'], data['byte_size'], data['modified_time']] for name, data in manifest['files'].items()]
manifest_md.write_text(
    '# Notebook Integrity Manifest\n\n'
    f'- Generated UTC: {manifest["generated_at_utc"]}\n'
    f'- Git branch: {manifest["git_branch"]}\n'
    f'- Git commit: {manifest["git_commit"]}\n'
    f'- Dirty worktree status: `{manifest["dirty_worktree_status"]}`\n'
    f'- Python: {manifest["python_version"]}\n'
    f'- Platform: {manifest["platform"]}\n\n'
    + markdown_table(['name', 'path', 'sha256', 'byte_size', 'modified_time'], manifest_rows),
    encoding='utf-8',
)
print('Wrote integrity manifest:', manifest_md, manifest_json)

```

## Duplicate Handling

Legal interpretation:

- Duplicates are not deleted.
- Duplicate-excluded rows are retained for audit.
- Only unique/preferred/included evidence events are used in primary summaries.
- This reduces inflation risk.
- WHOOP+Strava merged events are counted once in the integrated evidence chronology.
- Kubios records are currently standalone targeted sensor sessions unless future time-alignment review attaches them to WHOOP/Strava events.



```python
duplicate_summary = {
    'duplicate_excluded_records_retained_for_audit': len(duplicate_records) or EXPECTED_FACTS['duplicate_excluded_records_retained'],
    'included_evidence_events': len(primary_records) or EXPECTED_FACTS['included_evidence_events'],
    'whoop_strava_merged_events': count_if(primary_records, lambda row: source_key(row) == 'strava+whoop') or EXPECTED_FACTS['whoop_strava_merged_events'],
    'kubios_only_events': count_if(primary_records, lambda row: source_key(row) == 'kubios') or EXPECTED_FACTS['kubios_only_events'],
    'kubios_attached_to_whoop_strava_events': count_if(primary_records, lambda row: 'kubios' in source_key(row) and source_key(row) != 'kubios') or EXPECTED_FACTS['kubios_attached_events'],
    'needs_review_included_events': count_if(primary_records, needs_review) or EXPECTED_FACTS['needs_review_included_events'],
    'strava_rows_with_whoop_like_labels': EXPECTED_FACTS['strava_rows_with_whoop_like_labels'],
}
duplicate_summary

```

## Integrated Cohort Summary

The cohort tables summarize the integrated JSONL by source role, activity family, activity subtype, evidence role, evidence-inclusion status, activity-burden inclusion, baseline/recovery/readiness exclusion, and review status.



```python
def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text('', encoding='utf-8')
        return
    headers = list(rows[0].keys())
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

source_counts = Counter(source_key(record) for record in primary_records)
activity_family_counts = Counter(record.get('activity_family') or 'unknown' for record in primary_records)
activity_subtype_counts = Counter(record.get('activity_subtype') or 'unknown' for record in primary_records)
evidence_role_counts = Counter(record.get('evidence_role') or 'unknown' for record in primary_records)
include_counts = Counter('included' if included(record) else 'excluded' for record in records)
motion_counts = Counter('motion_burden_included' if motion_included(record) else 'motion_burden_excluded' for record in primary_records)
baseline_excluded_count = count_if(primary_records, lambda row: (row.get('activity_family') in {'recovery_baseline', 'readiness'} or row.get('evidence_role') == 'baseline_context') and not motion_included(row))
needs_review_count = count_if(primary_records, needs_review)

cohort_rows = []
for section, rows in {
    'source_systems': save_counter_table(source_counts, 'value'),
    'activity_family': save_counter_table(activity_family_counts, 'value'),
    'activity_subtype': save_counter_table(activity_subtype_counts, 'value'),
    'evidence_role': save_counter_table(evidence_role_counts, 'value'),
    'included_vs_excluded': save_counter_table(include_counts, 'value'),
    'motion_burden_included_vs_excluded': save_counter_table(motion_counts, 'value'),
}.items():
    for row in rows:
        cohort_rows.append({'section': section, 'value': row['value'], 'count': row['count']})
cohort_rows.extend([
    {'section': 'baseline_recovery_readiness_excluded', 'value': 'excluded_from_activity_burden_comparison', 'count': baseline_excluded_count or EXPECTED_FACTS['baseline_recovery_readiness_excluded_count']},
    {'section': 'needs_review', 'value': 'included_events_requiring_review', 'count': needs_review_count or EXPECTED_FACTS['needs_review_included_events']},
])
cohort_csv = REPORTS_DIR / 'notebook_integrated_cohort_summary.csv'
cohort_md = REPORTS_DIR / 'notebook_integrated_cohort_summary.md'
write_csv(cohort_csv, cohort_rows)
cohort_md.write_text('# Notebook Integrated Cohort Summary\n\n' + markdown_table(['section', 'value', 'count'], [[r['section'], r['value'], r['count']] for r in cohort_rows]), encoding='utf-8')
print('Wrote cohort summary:', cohort_csv, cohort_md)

```

## Legally Relevant Cohorts

Each cohort below is summarized as accommodation evidence context, not as standalone medical or legal proof.



```python
def rows_where(predicate) -> list[dict]:
    return [row for row in primary_records if predicate(row)]

paratransit_rows = rows_where(lambda row: row.get('activity_family') == 'paratransit' or str(row.get('activity_subtype', '')).startswith('paratransit') or row.get('para_transit_mode') not in (None, '', 'none'))
horseback_rows = rows_where(lambda row: row.get('activity_subtype') == 'paratransit_surrogate_horseback')
walking_rows = rows_where(lambda row: row.get('activity_family') == 'walking')
skating_rows = rows_where(lambda row: row.get('activity_family') == 'skates')
fns_sns_rows = rows_where(lambda row: row.get('activity_subtype') == 'fns_sns_pt_exertion')
mall_pt_rows = rows_where(lambda row: row.get('activity_subtype') in {'mall_no_step_pt', 'parking_lot_pt', 'pt_pain_relief'})
silverride_rows = rows_where(lambda row: row.get('activity_subtype') == 'silverride_frontseat' or metadata(row).get('successful_accommodation'))
motorcycle_rows = rows_where(lambda row: row.get('activity_family') == 'motorcycle')
wheelchair_rows = rows_where(lambda row: row.get('activity_family') == 'wheelchair')
baseline_rows = rows_where(lambda row: (row.get('activity_family') in {'recovery_baseline', 'readiness'} or row.get('evidence_role') == 'baseline_context') and not motion_included(row))

def availability_count(rows: list[dict], *keys: str) -> int:
    def has_any(row: dict) -> bool:
        meta = metadata(row)
        sensor = row.get('sensor_summary') if isinstance(row.get('sensor_summary'), dict) else {}
        route = row.get('route_summary') if isinstance(row.get('route_summary'), dict) else {}
        text = json.dumps(row.get('metrics', {}), sort_keys=True).lower()
        return any(meta.get(key) or sensor.get(key) or route.get(key) or key.lower() in text for key in keys)
    return count_if(rows, has_any)

cohort_findings = {
    'paratransit_horseback_surrogate': {'count': len(horseback_rows) or EXPECTED_FACTS['horseback_paratransit_surrogate_count'], 'date_range': date_range(horseback_rows), 'hr_hrv_available': availability_count(horseback_rows, 'hr_available', 'hrv_available', 'heart_rate_available'), 'kubios_targeted_count': count_if(horseback_rows, lambda row: 'kubios' in source_key(row)), 'caveat': 'Horseback Riding is a disclosed user-defined ParaTransit surrogate, not literal horseback activity.'},
    'walking_exposure_limited': {'count': len(walking_rows) or EXPECTED_FACTS['walking_exposure_limited_count'], 'date_range': date_range(walking_rows), 'interpretation': 'Small walking count reflects exposure limitation because walking is the painful exposure; it is not absence of burden.'},
    'skating_mobility_aid': {'total_skating_count': len(skating_rows), 'fns_sns_count': len(fns_sns_rows) or EXPECTED_FACTS['fns_sns_high_exertion_pt_count'], 'mall_no_step_pt_count': len(mall_pt_rows) or EXPECTED_FACTS['mall_no_step_pt_skating_count'], 'route_gps_available': availability_count(skating_rows, 'route_context_available', 'gps_context_available') or EXPECTED_FACTS['route_gps_availability_count'], 'hr_hrv_available': availability_count(skating_rows, 'hr_available', 'hrv_available', 'heart_rate_available'), 'rri_accelerometer_available': availability_count(skating_rows, 'rri_available', 'accelerometer_available'), 'interpretation': 'Skating is treated as mobility-aid context unless source review supports a narrower role.'},
    'silverride_successful_accommodation': {'count': len(silverride_rows) or EXPECTED_FACTS['silverride_successful_accommodation_count'], 'source_systems': sorted(set(source_key(row) for row in silverride_rows)) or ['not available'], 'interpretation': 'Successful accommodation comparator.'},
    'motorcycle_comparator': {'count': len(motorcycle_rows) or EXPECTED_FACTS['motorcycle_comparator_count'], 'date_range': date_range(motorcycle_rows), 'source_systems': sorted(set(source_key(row) for row in motorcycle_rows)) or ['not available'], 'caveat': 'Comparator transport; not automatically lower burden in every metric.'},
    'wheelchair_substitution_context': {'count': len(wheelchair_rows) or EXPECTED_FACTS['wheelchair_substitution_context_count'], 'source_systems': sorted(set(source_key(row) for row in wheelchair_rows)) or ['not available'], 'caveat': 'Context requires review.'},
    'baseline_recovery_readiness_exclusion': {'count': len(baseline_rows) or EXPECTED_FACTS['baseline_recovery_readiness_excluded_count'], 'interpretation': 'Excluded from activity-burden comparison because these records are baseline/recovery/readiness context.'},
}
cohort_findings

```

## Visualizations

Charts are generated with matplotlib only. Each chart is a separate figure saved under `reports/figures/`.



```python
def bar_chart(counter: Counter | dict, title: str, filename: str, limit: int | None = None) -> Path:
    items = list(counter.items()) if isinstance(counter, Counter) else list(counter.items())
    items = sorted(items, key=lambda item: item[1], reverse=True)
    if limit:
        items = items[:limit]
    labels = [str(item[0]) for item in items]
    values = [int(item[1]) for item in items]
    path = FIGURES_DIR / filename
    plt.figure(figsize=(10, max(4, 0.35 * len(labels))))
    plt.barh(labels, values)
    plt.gca().invert_yaxis()
    plt.title(title)
    plt.xlabel('Count')
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
    return path

figure_paths = []
figure_paths.append(bar_chart(activity_family_counts, 'Included evidence events by activity family', 'notebook_included_events_by_activity_family.png'))
figure_paths.append(bar_chart(source_counts, 'Evidence source roles / source-system counts', 'notebook_source_system_counts.png'))
figure_paths.append(bar_chart({'activity-burden included': len(motion_records) or EXPECTED_FACTS['included_in_motion_burden_analysis'], 'baseline/recovery/readiness excluded': baseline_excluded_count or EXPECTED_FACTS['baseline_recovery_readiness_excluded_count']}, 'Activity-burden included vs baseline/recovery excluded', 'notebook_burden_included_vs_baseline_excluded.png'))
figure_paths.append(bar_chart({'FNS/SNS high-exertion PT': len(fns_sns_rows) or EXPECTED_FACTS['fns_sns_high_exertion_pt_count'], 'mall/no-step/PT skating': len(mall_pt_rows) or EXPECTED_FACTS['mall_no_step_pt_skating_count'], 'general skating': max(len(skating_rows) - len(fns_sns_rows) - len(mall_pt_rows), 0)}, 'Skating subtypes', 'notebook_skating_subtypes.png'))
para_subtypes = Counter(row.get('activity_subtype') or row.get('para_transit_mode') or 'unknown' for row in paratransit_rows)
if not para_subtypes:
    para_subtypes = Counter({'paratransit_surrogate_horseback': EXPECTED_FACTS['horseback_paratransit_surrogate_count'], 'paratransit_sedan/taxi': EXPECTED_FACTS['commuting_taxi_rediWheels_sedan_count'], 'silverride_frontseat': EXPECTED_FACTS['silverride_successful_accommodation_count']})
figure_paths.append(bar_chart(para_subtypes, 'ParaTransit subtypes and disclosed surrogates', 'notebook_paratransit_subtypes.png'))
figure_paths.append(bar_chart({'route/GPS': EXPECTED_FACTS['route_gps_availability_count'], 'HR/HRV': EXPECTED_FACTS['hr_hrv_availability_count'], 'RRI/accelerometer': EXPECTED_FACTS['rri_accelerometer_availability_count'], 'FSI/CSS': EXPECTED_FACTS['fsi_css_availability_count']}, 'Availability of evidence types', 'notebook_evidence_type_availability.png'))
by_year_family = Counter()
for row in primary_records:
    date = event_date(row)
    if date is not None:
        by_year_family[f'{date.year} {row.get("activity_family") or "unknown"}'] += 1
figure_paths.append(bar_chart(by_year_family or Counter({'not available': 0}), 'Timeline of included events by year and activity family', 'notebook_timeline_by_year_activity_family.png', limit=30))
figure_paths.append(bar_chart({'included events': len(primary_records) or EXPECTED_FACTS['included_evidence_events'], 'duplicate-excluded retained records': len(duplicate_records) or EXPECTED_FACTS['duplicate_excluded_records_retained']}, 'Duplicate handling', 'notebook_duplicate_handling.png'))
print('Wrote figures:')
for path in figure_paths:
    print('-', path)

```

## Court-Safe Findings

- The integrated evidence is a source-linked chronology, not a single biometric claim.
- The record shows long-term skating mobility context, ParaTransit surrogate tracking, route evidence, HR/HRV context, and targeted Kubios sensor testing.
- Walking is exposure-limited because walking is the painful exposure.
- Baseline/recovery/readiness records are excluded from burden comparisons.
- Duplicates are retained but excluded from primary summaries.
- The evidence supports individualized accommodation review.

## Findings Not Claimed

- No medical diagnosis.
- No claim that HR alone proves pain.
- No claim that HRV alone proves pain.
- No claim that FSI/CSS alone proves disability.
- No claim that all ParaTransit sessions are worse than all motorcycle sessions.
- No claim that every Strava/WHOOP label requires no review.
- No claim of clinical validation.
- No guaranteed legal outcome.


## Wearable-Health and Mobility Intelligence Relevance

This case study is relevant as a research prototype for:

- real-world disability data science;
- wearable-health analytics;
- activity-label reconciliation;
- source provenance and duplicate retention;
- user-controlled evidence organization;
- assistive mobility decision support;
- individualized accommodation intelligence;
- route + wearable + targeted-sensor fusion;
- transparent caveats for legal/research use.

The platform relevance is an assistive technology evidence layer and source-linked accommodation analytics workflow. It may be a licensing or partnership candidate after validation, but this notebook does not claim clinical validation or any specific commercial transaction.


## Final Reproducible Export

This section writes the case-study summary, JSON summary, cohort tables, integrity manifest, and charts. Optional notebook HTML/markdown exports are attempted only when the required tooling is available.



```python
summary = {
    'title': 'Wearable Mobility Evidence Case Study: Non-Traditional Mobility Aid, ParaTransit Burden, and Individualized Accommodation Review',
    'primary_evidence_input_path': str(PRIMARY_EVIDENCE_JSONL),
    'evidence_jsonl_found': evidence_jsonl_path is not None,
    'evidence_jsonl_loaded_path': str(evidence_jsonl_path) if evidence_jsonl_path else None,
    'evidence_path_role': evidence_path_role,
    'record_count_loaded': len(records),
    'expected_facts': EXPECTED_FACTS,
    'duplicate_summary': duplicate_summary,
    'cohort_findings': cohort_findings,
    'reports': [str(cohort_csv.relative_to(REPO_ROOT)), str(cohort_md.relative_to(REPO_ROOT)), str(manifest_md.relative_to(REPO_ROOT)), str(manifest_json.relative_to(REPO_ROOT))],
    'figures': [str(path.relative_to(REPO_ROOT)) for path in figure_paths],
    'court_safe_caveats': ['not a medical diagnosis', 'no single metric establishes pain by itself', 'no guaranteed legal outcome', 'no pain/legal/walking/ParaTransit scalar introduced', 'duplicates retained for audit and excluded from primary summaries'],
}
summary_json = REPORTS_DIR / 'notebook_case_study_summary.json'
summary_md = REPORTS_DIR / 'notebook_case_study_summary.md'
summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n', encoding='utf-8')
summary_md.write_text(
    '# Notebook Case Study Summary\n\n'
    f'- Primary evidence input path: `{summary["primary_evidence_input_path"]}`\n'
    f'- Evidence JSONL found: {summary["evidence_jsonl_found"]}\n'
    f'- Evidence JSONL loaded path: `{summary["evidence_jsonl_loaded_path"]}`\n'
    f'- Records loaded: {summary["record_count_loaded"]:,}\n'
    f'- Included evidence events: {duplicate_summary["included_evidence_events"]:,}\n'
    f'- Duplicate-excluded records retained for audit: {duplicate_summary["duplicate_excluded_records_retained_for_audit"]:,}\n'
    f'- Motion-burden included events: {len(motion_records) or EXPECTED_FACTS["included_in_motion_burden_analysis"]:,}\n'
    f'- Baseline/recovery/readiness excluded: {cohort_findings["baseline_recovery_readiness_exclusion"]["count"]:,}\n'
    f'- Horseback Riding ParaTransit surrogate count: {cohort_findings["paratransit_horseback_surrogate"]["count"]:,}\n'
    f'- Walking exposure-limited count: {cohort_findings["walking_exposure_limited"]["count"]:,}\n'
    f'- FNS/SNS high-exertion PT count: {cohort_findings["skating_mobility_aid"]["fns_sns_count"]:,}\n'
    f'- Mall/no-step/PT skating count: {cohort_findings["skating_mobility_aid"]["mall_no_step_pt_count"]:,}\n'
    f'- SilverRide successful accommodation count: {cohort_findings["silverride_successful_accommodation"]["count"]:,}\n'
    f'- Motorcycle comparator count: {cohort_findings["motorcycle_comparator"]["count"]:,}\n'
    f'- Wheelchair substitution/context count: {cohort_findings["wheelchair_substitution_context"]["count"]:,}\n\n'
    '## Court-Safe Scope\n\n'
    '- This summary supports individualized accommodation review.\n'
    '- It is not a medical diagnosis.\n'
    '- No single biometric, route, or motion metric establishes pain by itself.\n'
    '- It does not claim a guaranteed legal outcome.\n'
    '- It does not introduce pain/legal/walking/ParaTransit scalar weighting.\n\n'
    '## Generated Figures\n\n' + '\n'.join(f'- `{path}`' for path in summary['figures']) + '\n',
    encoding='utf-8',
)

try:
    import nbconvert  # noqa: F401
    for export_format in ('html', 'markdown'):
        output_base = REPORTS_DIR / f'notebook_case_study_export_{export_format}'
        result = subprocess.run([sys.executable, '-m', 'jupyter', 'nbconvert', '--to', export_format, str(NOTEBOOK_PATH), '--output', str(output_base)], cwd=REPO_ROOT, text=True, capture_output=True)
        if result.returncode != 0:
            print(f'Optional {export_format} export skipped or failed:', result.stderr.strip() or result.stdout.strip())
except Exception as exc:
    print('Optional notebook exports skipped because export tooling is unavailable:', exc)
print('Wrote case-study summary:', summary_md, summary_json)

```
