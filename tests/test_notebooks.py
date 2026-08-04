"""Structural checks for the repository's Jupyter notebooks."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class NotebookTests(unittest.TestCase):
    def test_notebook_json_and_python_syntax(self) -> None:
        notebooks = sorted(ROOT.rglob("*.ipynb"))
        self.assertTrue(notebooks)
        for path in notebooks:
            notebook = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(notebook.get("nbformat"), 4, path)
            for index, cell in enumerate(notebook.get("cells", [])):
                if cell.get("cell_type") == "code":
                    ast.parse("".join(cell.get("source", [])), filename=f"{path}:cell-{index}")

    def test_no_stored_errors_or_large_outputs(self) -> None:
        for path in ROOT.rglob("*.ipynb"):
            notebook = json.loads(path.read_text(encoding="utf-8"))
            for cell in notebook.get("cells", []):
                outputs = cell.get("outputs", [])
                self.assertFalse(
                    any(output.get("output_type") == "error" for output in outputs),
                    f"Stored error in {path}",
                )
                self.assertLess(
                    len(json.dumps(outputs)),
                    100_000,
                    f"Oversized stored output in {path}",
                )


if __name__ == "__main__":
    unittest.main()
