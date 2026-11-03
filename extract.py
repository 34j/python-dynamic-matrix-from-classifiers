from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

CLASSIFIER_PATTERN = re.compile(r"Programming Language :: Python :: (\d+\.\d+)")


def extract_versions(pyproject_path: Path) -> list[str]:
    with pyproject_path.open("rb") as file:
        pyproject = tomllib.load(file)

    project = pyproject.get("project")
    if not isinstance(project, dict):
        raise ValueError("pyproject.toml must define a [project] table")

    classifiers = project.get("classifiers", [])
    if not isinstance(classifiers, list) or not all(
        isinstance(classifier, str) for classifier in classifiers
    ):
        raise ValueError("project.classifiers must be an array of strings")

    versions = [
        match.group(1)
        for classifier in classifiers
        if (match := CLASSIFIER_PATTERN.fullmatch(classifier))
    ]
    versions = list(dict.fromkeys(versions))

    if not versions:
        raise ValueError("No versioned Python classifiers were found")

    return versions


def main() -> int:
    if sys.version_info < (3, 11):
        print("Python 3.11 or later is required to parse pyproject.toml", file=sys.stderr)
        return 1

    if len(sys.argv) != 2:
        print("Usage: extract.py PYPROJECT_PATH", file=sys.stderr)
        return 1

    try:
        versions = extract_versions(Path(sys.argv[1]))
    except (OSError, tomllib.TOMLDecodeError, ValueError) as error:
        print(f"Unable to extract Python versions: {error}", file=sys.stderr)
        return 1

    print(f"versions={json.dumps(versions, separators=(',', ':'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
