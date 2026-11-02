"""Explain measured input readiness without calculating or modifying FSI/CSS."""
from __future__ import annotations

import math


TENSOR_FORMULA = "fsi_tensor_v0_3_msk_autonomic_gated_burden"
TENSOR_INPUTS = {
    "vertical_dynamic_g_rms": ("g", "episodic_sensor"),
    "impact_rate_per_min": ("count/min", "episodic_sensor"),
    "mean_hr_bpm": ("bpm", "episodic_sensor"),
    "rmssd_ms": ("ms", "episodic_sensor"),
    "duration_seconds": ("s", "episodic_sensor"),
}


def tensor_input_readiness(metrics: dict) -> dict:
    """A stricter consumer preflight, not formula eligibility or a score.

    Values here must describe a single compatible session. Overnight RMSSD and
    other shock definitions cannot satisfy the session input contract. Actual
    Tensor input conversion, cohort defaults, axes, and fallbacks remain owned
    by the platform and must be exposed before consuming a persisted score.
    """
    issues = []
    for name, (unit, scope) in TENSOR_INPUTS.items():
        record = metrics.get(name)
        if record is None:
            issues.append(f"{name}: unavailable")
            continue
        value = record.get("value")
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            issues.append(f"{name}: unavailable or nonfinite")
        if record.get("unit") != unit or record.get("scope") != scope:
            issues.append(f"{name}: unit/scope mismatch")
        if name == "impact_rate_per_min" and record.get("definition") != "MAD_BASED_IMPACT_RATE":
            issues.append(f"{name}: MAD-based definition required")
    return {
        "formula_version": TENSOR_FORMULA,
        "status": "INPUTS_PRESENT_REQUIRES_PLATFORM_LINEAGE_REVIEW" if not issues else "INPUTS_INCOMPLETE_OR_INCOMPATIBLE",
        "issues": issues,
        "score": None,
        "score_computed": False,
        "requires": ["same_session_identity", "platform_unit_conversion", "cohort_provenance", "axes_and_fallback_disclosure", "persisted_output_hash", "validation_status"],
    }
