from importlib import metadata
from pathlib import Path

#: Package name:
pkg_name = str(Path(__file__).parent.name)

#: We store the version number inside the `pyproject.toml`:
try:
    pkg_version = metadata.version(pkg_name)
except metadata.PackageNotFoundError:
    # This mainly happens in RTD env, where we set the metadata
    # from `pyproject.toml` file:
    pkg_version = ''
