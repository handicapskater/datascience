from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.public_notebook_evidence import BUNDLE, LOCK, core_table, load_bundle, plot_aggregates
from scripts.synthesis_readiness import TENSOR_INPUTS, tensor_input_readiness
from scripts import check_legal_preservation


class PublicBundleTests(unittest.TestCase):
    def public_markdown(self):
        notebook = json.loads((ROOT / "HandicapSkater-Public.ipynb").read_text())
        return "\n".join("".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "markdown")

    def test_public_portfolio_sections_and_citation_navigation_are_preserved(self):
        markdown = self.public_markdown()
        anchors = re.findall(r'<a id="([^"]+)"></a>', markdown)
        required = {
            "intro", "policy", "hypotheses", "data", "desc-stats", "inf-stats",
            "hrv-analysis", "pred-ml", "model-evaluation", "explainability",
            "synthesis", "reproducibility", "conclusion", "references",
            "research-lineage",
        }
        self.assertTrue(required <= set(anchors))
        self.assertEqual(len(anchors), len(set(anchors)))
        links = set(re.findall(r'\]\(#([^)]+)\)', markdown))
        self.assertTrue(required <= links)
        self.assertTrue(links <= set(anchors))
        for title in ("Data Engineering", "Descriptive Statistics", "Inferential Statistics", "Deep Learning", "Model Evaluation", "XGBoost and SHAP", "Conclusions"):
            self.assertIn(title, markdown)
        conclusions = markdown.split('<a id="conclusion"></a>', 1)[1].split('<a id="references"></a>', 1)[0]
        self.assertIn("](#ref-", conclusions)
        self.assertIn("computational-evidence.json", conclusions)

    def test_public_method_templates_are_syntactically_valid_and_nonexecuting(self):
        import ast

        markdown = self.public_markdown()
        templates = re.findall(r'```python\n(.*?)```', markdown, re.DOTALL)
        self.assertEqual(len(templates), 2)
        for template in templates:
            ast.parse(template)
        self.assertIn("non-executing", markdown)
        self.assertIn("Current model results: not reported", markdown)

    def test_public_model_plan_blocks_historical_leakage(self):
        markdown = self.public_markdown()
        model_section = markdown.split('### 8.3 Why the historical performance', 1)[1].split('<a id="model-evaluation"></a>', 1)[0]
        template = re.findall(r'```python\n(.*?)```', model_section, re.DOTALL)[0]
        self.assertIn("SMOTE-generated rows", model_section)
        self.assertIn("`Manual Labor` row to `Walking`", model_section)
        self.assertIn("XGBoost row split", model_section)
        self.assertIn("future observations", model_section)
        self.assertIn("dates < validation_start", template)
        self.assertIn("dates >= test_start", template)
        self.assertIn("SimpleImputer(strategy='median')", template)
        self.assertLess(template.index("train = np.flatnonzero"), template.index("preprocess.fit_transform(X[train])"))
        self.assertNotIn("fit_transform(X[test])", template)
        self.assertNotIn("fit_resample", template)

    def test_public_notebook_relative_resources_exist(self):
        from urllib.parse import unquote, urlsplit

        for target in re.findall(r'\]\(([^)]+)\)', self.public_markdown()):
            parsed = urlsplit(target)
            if parsed.scheme or not parsed.path:
                continue
            relative = Path(unquote(parsed.path))
            self.assertFalse(relative.is_absolute())
            self.assertTrue((ROOT / relative).is_file(), target)

    def test_foundational_hypotheses_and_research_bridge_are_preserved(self):
        markdown = self.public_markdown()
        self.assertIn("Null Hypothesis (H₀)", markdown)
        self.assertIn("Alternative Hypothesis (H₁)", markdown)
        self.assertIn("WHOOP/Strava foundation and original hypotheses", markdown)
        bridge = (ROOT / "docs/research_evolution.md").read_text()
        for locator in ("6342ccc", "bb2306d", "84f5f7d"):
            self.assertIn(locator, bridge)
        for role in ("WHOOP physiological context", "Strava functional distance", "Kubios/Polar H10"):
            self.assertIn(role, bridge)
        self.assertIn("not a verified row-for-row data", bridge)
        for name in ("Public", "Scientific", "ScientificSuccinct"):
            data = json.loads((ROOT / f"HandicapSkater-{name}.ipynb").read_text())
            narrative = "\n".join("".join(c["source"]) for c in data["cells"] if c["cell_type"] == "markdown")
            self.assertIn("](docs/research_evolution.md)", narrative)

    def test_research_bridge_local_links_and_disclosure_boundary(self):
        from urllib.parse import unquote, urlsplit

        path = ROOT / "docs/research_evolution.md"
        markdown = path.read_text()
        for forbidden in ("/Users/", "data/raw/", "strava_activity:", "kubios-", "patient_id"):
            self.assertNotIn(forbidden, markdown)
        for target in re.findall(r'\]\(([^)]+)\)', markdown):
            parsed = urlsplit(target)
            if parsed.scheme or not parsed.path:
                continue
            relative = Path(unquote(parsed.path))
            self.assertFalse(relative.is_absolute())
            self.assertTrue((path.parent / relative).is_file(), target)

    def test_static_notebook_tables_match_pinned_results(self):
        expected = core_table(load_bundle())
        for name in ("Public", "Scientific", "ScientificSuccinct"):
            data = json.loads((ROOT / f"HandicapSkater-{name}.ipynb").read_text())
            markdown = "\n".join("".join(c["source"]) for c in data["cells"] if c["cell_type"] == "markdown")
            self.assertIn(expected, markdown)

    def test_tampered_measurement_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "bundle.json"
            data = json.loads(BUNDLE.read_text())
            data["mechanics"]["vertical_rms"]["walking_median"] = 999
            target.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                load_bundle(target, LOCK)

    def test_excerpt_contains_no_session_or_raw_records(self):
        data = load_bundle()
        allowed = {
            "schema_version", "snapshot_date", "data_through_date", "scope", "sources",
            "core_findings", "mechanics", "pt_distance", "longitudinal", "pareto",
            "fixed_reference_event_density", "tails", "shock_taxonomy", "boundaries",
            "scientific_recomputation", "boundary_notes",
        }
        self.assertEqual(set(data), allowed)
        forbidden = {"session_id", "source_record_id", "date_local", "timestamps", "samples", "coordinates", "latitude", "longitude", "raw_data", "embedding", "patient_id"}

        def inspect(value):
            if isinstance(value, dict):
                self.assertFalse(set(value) & forbidden)
                for child in value.values():
                    inspect(child)
            elif isinstance(value, list):
                for child in value:
                    inspect(child)
            elif isinstance(value, str):
                self.assertNotIn("/Users/", value)
                self.assertNotIn("data/raw/", value)
                self.assertNotIn("strava_activity:", value)

        inspect(data)
        self.assertLess(BUNDLE.stat().st_size, 20000)

    def test_notebooks_are_valid_and_do_not_access_legal_or_live_services(self):
        import ast
        import nbformat

        for name in ("Public", "Scientific", "ScientificSuccinct"):
            path = ROOT / f"HandicapSkater-{name}.ipynb"
            notebook = nbformat.read(path, as_version=4)
            nbformat.validate(notebook)
            for cell in notebook.cells:
                if cell.cell_type == "code":
                    ast.parse(cell.source)
                    self.assertEqual(cell.outputs, [])
                    self.assertIsNone(cell.execution_count)
                    for forbidden in ("legal/", "wget", "requests.", "duckdb", "fit_resample", "model.fit"):
                        self.assertNotIn(forbidden, cell.source)

    def test_render_preserves_stored_medians_and_separate_units(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        # Explicitly synthetic presentation fixture: no real inference.
        fixture = {
            "mechanics": {
                "vertical_rms": {"mall_median": 1, "walking_median": 3, "unit": "g", "N": 4},
                "magnitude_jerk": {"mall_median": 2, "walking_median": 5, "unit": "g/s", "N": 6},
            },
            "pt_distance": {"left_median": 0.1, "right_median": 2, "eligible_N": 7},
        }
        before = copy.deepcopy(fixture)
        figure = plot_aggregates(fixture)
        self.assertEqual([p.get_height() for p in figure.axes[0].patches], [1, 3])
        self.assertEqual([p.get_height() for p in figure.axes[2].patches], [0.1, 2])
        self.assertIn("g/s", figure.axes[1].get_ylabel())
        self.assertEqual(before, fixture)
        plt.close(figure)


class LegalPreservationTests(unittest.TestCase):
    def test_missing_baseline_never_initializes_a_lock(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.json"
            with self.assertRaises(FileNotFoundError):
                check_legal_preservation.check(missing)
            self.assertFalse(missing.exists())

    def test_changed_added_and_missing_files_are_detected_without_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "legal").mkdir()
            artifact = root / "legal/artifact.txt"
            artifact.write_text("original")
            digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
            baseline = root / "baseline.json"
            baseline.write_text(json.dumps({"legal/artifact.txt": digest, "legal/missing.txt": digest}))
            artifact.write_text("changed")
            (root / "legal/added.txt").write_text("added")
            with patch.object(check_legal_preservation, "ROOT", root):
                self.assertEqual(check_legal_preservation.check(baseline), (2, 2, 1))
            self.assertEqual(artifact.read_text(), "changed")
            self.assertEqual(json.loads(baseline.read_text())["legal/artifact.txt"], digest)


class SynthesisReadinessTests(unittest.TestCase):
    def fixture(self):
        values = {name: {"value": 1.0, "unit": unit, "scope": scope} for name, (unit, scope) in TENSOR_INPUTS.items()}
        values["impact_rate_per_min"]["definition"] = "MAD_BASED_IMPACT_RATE"
        return values

    def test_overnight_hrv_cannot_satisfy_session_input(self):
        values = self.fixture()
        values["rmssd_ms"]["scope"] = "overnight_recovery_not_session_hrv"
        result = tensor_input_readiness(values)
        self.assertTrue(any("scope mismatch" in s for s in result["issues"]))

    def test_shock_count_is_not_mad_impact_count(self):
        values = self.fixture()
        values["impact_rate_per_min"]["definition"] = "MEAN_SD_SHOCK_SPIKE_RATE"
        self.assertTrue(tensor_input_readiness(values)["issues"])

    def test_zero_is_present_and_missing_stays_missing(self):
        values = self.fixture()
        values["impact_rate_per_min"]["value"] = 0.0
        self.assertEqual(tensor_input_readiness(values)["issues"], [])
        values["impact_rate_per_min"]["value"] = None
        self.assertTrue(tensor_input_readiness(values)["issues"])

    def test_nonfinite_and_boolean_are_not_measurements(self):
        for invalid in (float("nan"), float("inf"), True):
            values = self.fixture()
            values["mean_hr_bpm"]["value"] = invalid
            self.assertTrue(tensor_input_readiness(values)["issues"])

    def test_complete_inputs_never_calculate_or_authorize_score(self):
        result = tensor_input_readiness(self.fixture())
        self.assertIn("REQUIRES_PLATFORM_LINEAGE_REVIEW", result["status"])
        self.assertIsNone(result["score"])
        self.assertFalse(result["score_computed"])


if __name__ == "__main__":
    unittest.main()
