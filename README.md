# Python dynamic matrix from classifiers

- Extracts classifiers `Programming Language :: Python :: 3.yy` from
`pyproject.toml`.
- Returns them as a JSON array.
- Then `matrix` for Python versions may be dynamically generated.

## Usage

Matrix must be generated in a separate job.

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
          python-version: '>=3.11'
          check-latest: true 
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
