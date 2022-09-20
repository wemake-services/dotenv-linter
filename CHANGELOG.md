# Version history

We follow Semantic Versions.


## Version 0.4.0

### Features

- `python3.6` support is dropped
- `pkg_resources` is removed, now `importlib_metadata` is used


## Version 0.3.0

### Features

- Now using `attrs` instead of `dataclasses`
- `python3.9` and `python3.10` support
- Updates `click` version

### Misc

- Updates `wemake-python-styleguide` to `0.16`
- Updates `typing_extensions` package


## Version 0.2.0

### Features

- Adds `python3.8` support
- Adds black-list of variable names

### Misc

- Updates `wemake-python-styleguide` to `0.14`
- Updates `poetry` to `1.0`
- Updates `reviewdog` to `v0.11.0`
- Moves from Travis to GitHub actions
- Adds support for [pre-commit](https://github.com/pre-commit/pre-commit)


## Version 0.1.5

### Misc

- Adds docker support
- Adds Github Action support
- Updates `wemake-python-styleguide` to `0.13`
- Documentation updates


## Version 0.1.4

### Misc

- Now allows to work with `click<7`, it resolves compatibility with other tools
- Updates `wemake-python-styleguide` to `0.7`


## Version 0.1.3

### Bugfixes

- Fixes issue with duplicate values across different files


## Version 0.1.2

### Bugfixes

- Fixes issue with empty comments

### Misc

- `wemake-python-styleguide` upgrade


## Version 0.1.1

### Bugfixes

- Fixes how homepage in defined in `pyproject.toml`

### Misc

- Improves docs: adds examples and usage section to the `README.md`
- Changes state: from Alpha to Beta


## Version 0.1.0

- Initial release
