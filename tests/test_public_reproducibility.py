from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from scripts.public_notebook_bootstrap import (
    RESOURCE_SHA256, _fetch, ensure_resources, ensure_runtime_dependencies,
    locate_repository_root, prepare_environment,
)
from scripts.public_notebook_evidence import (
    BUNDLE, EXPECTED_BUNDLE_SHA256, load_bundle, plot_paired_effects,
    validate_bundle, validation_report,
)

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "54d6072f35050f1ca32fa9ee4210463b0ee0eb70"


class EvidenceValidationTests(unittest.TestCase):
    def test_reviewed_bundle_and_report(self):
        bundle = load_bundle()
        result = validate_bundle(bundle)
        self.assertEqual(len(bundle["core_findings"]), 6)
        self.assertEqual({row["independent_N"] for row in bundle["core_findings"]}, {44})
        self.assertEqual(len(result["passed"]), 6)
        self.assertIn("Not independently verifiable here", validation_report(bundle))
        self.assertEqual(hashlib.sha256(BUNDLE.read_bytes()).hexdigest(), EXPECTED_BUNDLE_SHA256)

    def test_schema_unit_denominator_direction_and_interval_fail_closed(self):
        changes = (
            (lambda b: b.pop("sources"), "required fields"),
            (lambda b: b["core_findings"][0].update(effect="median paired Δ -1.8644 g"), "unit changed"),
            (lambda b: b["core_findings"][0].update(independent_N=44.0), "denominator"),
            (lambda b: b["core_findings"][0].update(CI="[-1.0, -2.0]"), "bounds"),
            (lambda b: b["core_findings"][0].update(direction_consistency="110%"), "consistency"),
            (lambda b: b["sources"]["core"].update(sha256="0"*64), "source identity"),
            (lambda b: b["mechanics"]["vertical_rms"].update(unit="N"), "unit or denominator"),
            (lambda b: b["longitudinal"].update(activity_N=599), "denominators"),
            (lambda b: b["tails"]["metrics"]["p90_g"].update(walking_minus_mall=float("nan")), "nonfinite"),
        )
        for change, message in changes:
            with self.subTest(message=message):
                bundle = copy.deepcopy(load_bundle())
                change(bundle)
                with self.assertRaisesRegex(ValueError, message):
                    validate_bundle(bundle)

    def test_changed_lock_and_data_fail_integrity(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "bundle.json"
            lock = Path(directory) / "bundle.sha256"
            target.write_bytes(BUNDLE.read_bytes())
            lock.write_text("0"*64)
            with self.assertRaisesRegex(ValueError, "lock differs"):
                load_bundle(target, lock)
            lock.write_text(EXPECTED_BUNDLE_SHA256)
            target.write_bytes(BUNDLE.read_bytes() + b" ")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                load_bundle(target, lock)

    def test_forest_plot_renders_without_recomputing_values(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        bundle = load_bundle()
        before = copy.deepcopy(bundle)
        fig = plot_paired_effects(bundle)
        self.assertEqual(len(fig.axes), 4)
        self.assertEqual([axis.get_xlabel() for axis in fig.axes], [
            "Published median paired change (mi)", "Published median paired change (g)",
            "Published median paired change (g/s)", "Published median paired change (/min)",
        ])
        output = io.BytesIO()
        fig.savefig(output, format="png", dpi=110)
        self.assertGreater(len(output.getvalue()), 20_000)
        self.assertEqual(bundle, before)
        plt.close(fig)

    def test_missing_optional_ci_is_labelled_and_nonfinite_rejected(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        bundle = copy.deepcopy(load_bundle())
        bundle["core_findings"][0]["CI"] = None
        fig = plot_paired_effects(bundle)
        self.assertTrue(any("CI unavailable" in text.get_text() for text in fig.axes[0].texts))
        plt.close(fig)
        bundle["core_findings"][0]["effect"] = "median paired Δ nan mi"
        with self.assertRaisesRegex(ValueError, "Malformed"):
            plot_paired_effects(bundle)


class BootstrapTests(unittest.TestCase):
    def test_local_discovery_and_repeatable_initialization(self):
        self.assertEqual(locate_repository_root(ROOT / "data/public"), ROOT)
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(FileNotFoundError, "repository checkout"):
                locate_repository_root(Path(directory))
        with patch("scripts.public_notebook_bootstrap.ensure_runtime_dependencies", return_value=False):
            self.assertEqual(prepare_environment(ROOT, COMMIT, colab=False), ROOT)
            self.assertEqual(prepare_environment(ROOT, COMMIT, colab=False), ROOT)

    def test_allowlisted_colab_download_is_pinned_and_idempotent(self):
        relative = "data/public/skating_evidence.v1.json"
        payload = (ROOT / relative).read_bytes()
        response = io.BytesIO(payload)
        opener = Mock(return_value=response)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / relative
            _fetch(relative, COMMIT, target, opener=opener)
            self.assertEqual(target.read_bytes(), payload)
            self.assertIn(COMMIT, opener.call_args.args[0])
            opener.reset_mock(side_effect=True)
            _fetch(relative, COMMIT, target, opener=opener)
            opener.assert_not_called()
            with self.assertRaisesRegex(ValueError, "outside the public allowlist"):
                _fetch("legal/private.json", COMMIT, target, opener=opener)

    def test_all_declared_resources_have_matching_local_hashes(self):
        ensure_resources(ROOT, COMMIT, download=False)
        for relative, digest in RESOURCE_SHA256.items():
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), digest)

    def test_full_colab_resource_fetch_uses_only_allowlist(self):
        calls = []
        def opener(url, timeout):
            relative = url.split(COMMIT + "/", 1)[1]
            calls.append(relative)
            return io.BytesIO((ROOT / relative).read_bytes())
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            ensure_resources(target, COMMIT, download=True, opener=opener)
            ensure_resources(target, COMMIT, download=True, opener=opener)
            self.assertEqual(set(calls), set(RESOURCE_SHA256))
            self.assertEqual(len(calls), len(RESOURCE_SHA256))
            with patch("scripts.public_notebook_bootstrap.ensure_runtime_dependencies", return_value=False):
                self.assertEqual(prepare_environment(target, COMMIT, colab=False), target.resolve())

    def test_dependency_install_only_when_needed(self):
        requirement = ROOT / "requirements-public-runtime.txt"
        installer = Mock()
        with patch("scripts.public_notebook_bootstrap.importlib.metadata.version", return_value="3.10.2"):
            self.assertFalse(ensure_runtime_dependencies(requirement, installer=installer))
        installer.assert_not_called()
        from importlib.metadata import PackageNotFoundError
        with patch("scripts.public_notebook_bootstrap.importlib.metadata.version", side_effect=PackageNotFoundError):
            self.assertTrue(ensure_runtime_dependencies(requirement, installer=installer))
        self.assertEqual(installer.call_count, 1)


class NotebookExecutionTests(unittest.TestCase):
    def test_bootstrap_cell_pins_the_reviewed_module(self):
        notebook = json.loads((ROOT / "HandicapSkater-Public.ipynb").read_text())
        source = "".join(next(cell["source"] for cell in notebook["cells"] if cell["cell_type"] == "code"))
        from scripts import public_notebook_bootstrap as bootstrap
        self.assertIn(hashlib.sha256(Path(bootstrap.__file__).read_bytes()).hexdigest(), source)
        self.assertIn("d54b38a61cdd3135e51afd57a7b2c5cfd16d79dc", source)
        self.assertIn("import google.colab", source)

    def test_first_cell_fetches_pinned_bootstrap_in_simulated_colab(self):
        notebook = json.loads((ROOT / "HandicapSkater-Public.ipynb").read_text())
        source = "".join(next(cell["source"] for cell in notebook["cells"] if cell["cell_type"] == "code"))
        bootstrap_bytes = (ROOT / "scripts/public_notebook_bootstrap.py").read_bytes()
        urls = []
        def opener(url, timeout):
            urls.append(url)
            return io.BytesIO(bootstrap_bytes)
        google = types.ModuleType("google")
        google.__path__ = []
        colab = types.ModuleType("google.colab")
        previous_cwd, previous_path = Path.cwd(), sys.path[:]
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                with patch.dict(sys.modules, {"google": google, "google.colab": colab}):
                    with patch("urllib.request.urlopen", side_effect=opener):
                        with patch("scripts.public_notebook_bootstrap.prepare_environment", return_value=ROOT):
                            scope = {}
                            exec(source, scope)
                            self.assertTrue(scope["in_colab"])
                            self.assertEqual(scope["bundle"]["schema_version"], "notebook_public_evidence.v1")
                self.assertEqual(len(urls), 1)
                self.assertIn(scope["PINNED_COMMIT"], urls[0])
                self.assertEqual((Path(directory) / "handicapskater_public/scripts/public_notebook_bootstrap.py").read_bytes(), bootstrap_bytes)
            finally:
                os.chdir(previous_cwd)
                sys.path[:] = previous_path

    def test_complete_notebook_runs_from_clean_public_checkout(self):
        import nbformat
        from nbclient import NotebookClient
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            for relative in ("HandicapSkater-Public.ipynb", "scripts/public_notebook_bootstrap.py",
                             *RESOURCE_SHA256):
                destination = target / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, destination)
            notebook = nbformat.read(target / "HandicapSkater-Public.ipynb", as_version=4)
            executed = NotebookClient(notebook, timeout=120, kernel_name="python3",
                                      resources={"metadata": {"path": str(target)}}).execute()
            code = [cell for cell in executed.cells if cell.cell_type == "code"]
            self.assertEqual(len(code), 5)
            self.assertFalse(any(output.output_type == "error" for cell in code for output in cell.outputs))
            rendered = [output for cell in code for output in cell.outputs
                        if output.output_type in ("display_data", "execute_result")]
            markdown = "\n".join(str(output.data.get("text/markdown", "")) for output in rendered)
            self.assertIn("Public evidence validation", markdown)
            self.assertIn("Mall→Walking", markdown)
            self.assertGreaterEqual(sum("image/png" in output.data for output in rendered), 2)


if __name__ == "__main__":
    unittest.main()
