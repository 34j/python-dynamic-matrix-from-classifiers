import tempfile
import unittest
from pathlib import Path

from extract import extract_versions


class ExtractVersionsTests(unittest.TestCase):
    def test_extracts_versioned_python_classifiers_in_order(self) -> None:
        pyproject = self.write_pyproject(
            '''
[project]
classifiers = [
  "Programming Language :: Python :: 3 :: Only",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: Implementation :: CPython",
  "Programming Language :: Python :: 3.12",
  "Programming Language :: Python :: 3.10",
]
'''
        )

        self.assertEqual(extract_versions(pyproject), ["3.10", "3.12"])

    def test_rejects_missing_versioned_python_classifiers(self) -> None:
        pyproject = self.write_pyproject(
            '''
[project]
classifiers = ["Programming Language :: Python :: 3 :: Only"]
'''
        )

        with self.assertRaisesRegex(ValueError, "No versioned Python classifiers"):
            extract_versions(pyproject)

    def test_rejects_non_list_classifiers(self) -> None:
        pyproject = self.write_pyproject(
            '''
[project]
classifiers = "Programming Language :: Python :: 3.12"
'''
        )

        with self.assertRaisesRegex(ValueError, "array of strings"):
            extract_versions(pyproject)

    def write_pyproject(self, content: str) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        path = Path(temporary_directory.name) / "pyproject.toml"
        path.write_text(content, encoding="utf-8")
        return path


if __name__ == "__main__":
    unittest.main()
