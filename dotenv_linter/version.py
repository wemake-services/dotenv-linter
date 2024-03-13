from importlib import metadata as importlib_metadata

#: Package name:
pkg_name = 'dotenv-linter'

#: We store the version number inside the `pyproject.toml`:
pkg_version = importlib_metadata.version(pkg_name)
