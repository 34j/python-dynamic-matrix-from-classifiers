# Python dynamic matrix from classifiers

A composite GitHub Action that extracts version-specific Python classifiers from
`pyproject.toml` and returns them as a JSON array for a dynamic GitHub Actions
matrix.

## Usage

Generate the matrix in a separate job, then use its output in a dependent job.
A matrix cannot be created by a step in the job that consumes it.

```yaml
jobs:
  python-matrix:
    runs-on: ubuntu-latest
    outputs:
      versions: ${{ steps.versions.outputs.versions }}
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.11"
      - id: versions
        uses: 34j/python-dynamic-matrix-from-classifiers@v1.0.0

  test:
    needs: python-matrix
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ${{ fromJSON(needs.python-matrix.outputs.versions) }}
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: ${{ matrix.python-version }}
      - run: python -m unittest
```

## Inputs

| Name | Description | Required | Default |
| --- | --- | --- | --- |
| `pyproject-path` | Path to the `pyproject.toml` file to inspect. | No | `pyproject.toml` |

## Outputs

| Name | Description |
| --- | --- |
| `versions` | A JSON array of Python versions. |

Only classifiers in this exact form are included:

```toml
"Programming Language :: Python :: 3.12"
```

Generic classifiers, such as `Programming Language :: Python :: 3 :: Only`,
and implementation classifiers are ignored. Duplicate version classifiers are
removed while preserving their first-declared order.

The action requires Python 3.11 or later because it uses the standard-library
`tomllib` parser.

## Releases

Releases are created from Conventional Commit messages with semantic-release.
The first Marketplace publication must be completed through the GitHub
Marketplace publishing flow for a GitHub Release.
