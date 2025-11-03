from __future__ import annotations

import pathlib
import tempfile
import unittest

from assistant_clone.validation import iter_python_files, validate_files


class ValidationTests(unittest.TestCase):
    def test_iter_python_files_finds_sources(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[1]
        files = list(iter_python_files(root))
        self.assertTrue(any(path.name == "config.py" for path in files))

    def test_validate_files_reports_syntax_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad_file = pathlib.Path(tmp) / "bad.py"
            bad_file.write_text("def broken(:\n", encoding="utf-8")
            errors = validate_files([bad_file])
        self.assertTrue(errors)
        self.assertIn("bad.py", errors[0])


if __name__ == "__main__":
    unittest.main()
