import os
from importlib import metadata as importlib_metadata

#: Package name:
pkg_name = os.path.basename(os.path.dirname(__file__))

#: We store the version number inside the `pyproject.toml`:
pkg_version = importlib_metadata.version(pkg_name)
