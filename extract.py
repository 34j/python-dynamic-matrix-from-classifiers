from __future__ import annotations

import json
import re
import sys
import tomllib
import warnings
from pathlib import Path

CLASSIFIER_PATTERN = re.compile(r"Programming Language :: Python :: (\d+\.\d+)")
OS_CLASSIFIERS = {
    "Operating System :: Microsoft :: Windows": "windows-latest",
    "Operating System :: MacOS": "macos-latest",
    "Operating System :: POSIX :: Linux": "ubuntu-latest",
}
ALL_OSES = list(OS_CLASSIFIERS.values())


def load_classifiers(pyproject_path: Path) -> list[str]:
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

    return classifiers


def extract_versions(pyproject_path: Path) -> list[str]:
    versions = [
        match.group(1)
        for classifier in load_classifiers(pyproject_path)
        if (match := CLASSIFIER_PATTERN.fullmatch(classifier))
    ]
    versions = list(dict.fromkeys(versions))

    if not versions:
        raise ValueError("No versioned Python classifiers were found")

    return versions


def extract_oses(pyproject_path: Path) -> list[str]:
    classifiers = load_classifiers(pyproject_path)
    oses = [OS_CLASSIFIERS[classifier] for classifier in classifiers if classifier in OS_CLASSIFIERS]

    if oses:
        return list(dict.fromkeys(oses))
    if "Operating System :: OS Independent" not in classifiers:
        warnings.warn(
            "No supported operating system classifiers were found; assuming OS Independent",
            stacklevel=2,
        )
    return ALL_OSES.copy()


def main() -> int:
    if sys.version_info < (3, 11):
        print("Python 3.11 or later is required to parse pyproject.toml", file=sys.stderr)
        return 1

    if len(sys.argv) != 2:
        print("Usage: extract.py PYPROJECT_PATH", file=sys.stderr)
        return 1

    try:
        path = Path(sys.argv[1])
        versions = extract_versions(path)
        oses = extract_oses(path)
    except (OSError, tomllib.TOMLDecodeError, ValueError) as error:
        print(f"Unable to extract Python versions: {error}", file=sys.stderr)
        return 1

    print(f"versions={json.dumps(versions, separators=(',', ':'))}")
    print(f"oses={json.dumps(oses, separators=(',', ':'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
