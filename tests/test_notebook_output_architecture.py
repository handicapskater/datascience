from __future__ import annotations

import ast
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
FILED_NOTEBOOK = REPO_ROOT / "legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb"
RESEARCH_NOTEBOOK = REPO_ROOT / "legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb"
DEFAULT_NOTEBOOKS = (FILED_NOTEBOOK, RESEARCH_NOTEBOOK)


def selected_notebooks() -> tuple[Path, ...]:
    notebook_args = [arg for arg in sys.argv[1:] if arg.endswith(".ipynb")]
    paths = tuple(Path(arg).resolve() for arg in notebook_args)
    if paths:
        sys.argv[1:] = [arg for arg in sys.argv[1:] if not arg.endswith(".ipynb")]
        return paths
    return DEFAULT_NOTEBOOKS


NOTEBOOKS = selected_notebooks()


def load_notebook(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def joined_sources(notebook: dict, cell_type: str | None = None) -> str:
    sources = []
    for cell in notebook["cells"]:
        if cell_type is None or cell["cell_type"] == cell_type:
            sources.append("".join(cell.get("source", [])))
    return "\n".join(sources)


class NotebookOutputArchitectureTest(unittest.TestCase):
    def test_notebook_files_exist(self) -> None:
        for path in NOTEBOOKS:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_code_cells_parse_and_research_outputs_are_stripped(self) -> None:
        for path in NOTEBOOKS:
            notebook = load_notebook(path)
            for index, cell in enumerate(notebook["cells"]):
                if cell["cell_type"] != "code":
                    continue
                with self.subTest(path=path.name, cell=index):
                    ast.parse("".join(cell.get("source", [])))
                    if path == FILED_NOTEBOOK:
                        continue
                    self.assertEqual(cell.get("outputs", []), [])
                    self.assertIsNone(cell.get("execution_count"))

    def test_filed_notebook_uses_filed_run_and_guardrail(self) -> None:
        if FILED_NOTEBOOK not in NOTEBOOKS:
            self.skipTest("filed notebook not selected")
        source = joined_sources(load_notebook(FILED_NOTEBOOK))
        markdown = joined_sources(load_notebook(FILED_NOTEBOOK), "markdown")
        self.assertIn("Filed Exhibit A Reproducibility Notebook", markdown)
        self.assertIn("legal/cases/25-7526/filed/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf", markdown)
        self.assertIn("court, defendants, and technical reviewers", markdown)
        self.assertIn("def find_repo_root() -> Path:", source)
        self.assertIn("COLAB_REPO_ROOT", source)
        self.assertIn("def is_repo_root(path: Path) -> bool:", source)
        self.assertIn("from legal.src.evidence_config import EvidenceConfig", source)
        self.assertIn("from legal.src.evidence_paths import FILED_RECORD_RUN_ID", source)
        self.assertIn('mode="FILED_RECORD"', source)
        self.assertIn("prepare_output_dir(config.output_dir", source)
        self.assertLess(source.index("def find_repo_root() -> Path:"), source.index("from legal.src.evidence_config import EvidenceConfig"))
        self.assertNotIn('OUTPUT_DIR = CASE_ROOT / "outputs" / EXHIBIT_ID', source)

    def test_research_notebook_uses_research_run(self) -> None:
        if RESEARCH_NOTEBOOK not in NOTEBOOKS:
            self.skipTest("research notebook not selected")
        source = joined_sources(load_notebook(RESEARCH_NOTEBOOK))
        markdown = joined_sources(load_notebook(RESEARCH_NOTEBOOK), "markdown")
        self.assertIn("Living Wearable Research Notebook", markdown)
        self.assertIn("WEARABLE_RESEARCH_RUN_ID", source)
        self.assertIn('mode="RESEARCH"', source)
        self.assertIn("allow_overwrite=True", source)
        self.assertIn("prepare_output_dir(config.output_dir", source)
        self.assertIn("wearable_research_current", markdown)
        self.assertNotIn('OUTPUT_DIR = CASE_ROOT / "outputs" / EXHIBIT_ID', source)
        self.assertNotIn("outputs/exhibit_a", source)

    def test_shared_output_constants_are_current(self) -> None:
        from legal.src.evidence_paths import FILED_RECORD_RUN_ID, WEARABLE_RESEARCH_RUN_ID

        self.assertEqual(FILED_RECORD_RUN_ID, "exhibit_a_filed_2026-06-04")
        self.assertEqual(WEARABLE_RESEARCH_RUN_ID, "wearable_research_current")

    def test_gitignore_keeps_notebooks_and_ignores_research_outputs(self) -> None:
        gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertNotIn("*.ipynb", gitignore)
        self.assertIn("legal/cases/*/outputs/**", gitignore)
        self.assertNotIn("exhibit_a_filed_2026-06-03", gitignore)
        self.assertIn("!legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/README.md", gitignore)
        self.assertIn(
            "!legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/NonTraditional_notebook.sha256",
            gitignore,
        )
        self.assertIn(
            "!legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/manifest/evidence_manifest_sha256.json",
            gitignore,
        )
        gitattributes = (REPO_ROOT / ".gitattributes").read_text(encoding="utf-8")
        self.assertIn(
            "legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb -filter",
            gitattributes,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
