import os
from importlib import metadata

#: Package name:
pkg_name = os.path.basename(os.path.dirname(__file__))

#: We store the version number inside the `pyproject.toml`:
try:
    pkg_version = metadata.version(pkg_name)
except metadata.PackageNotFoundError:
    # This mainly happens in RTD env, where we set the metadata
    # from `pyproject.toml` file:
    pkg_version = ''
