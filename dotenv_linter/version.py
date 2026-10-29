from importlib import metadata
from pathlib import Path

pkg_name = str(Path(__file__).parent.name)
"""Package name."""

try:
    pkg_version = metadata.version(pkg_name)
except metadata.PackageNotFoundError:  # pragma: no cover
    # Package is not installed as a distribution
    pkg_version = ''
"""We store the version number inside the `pyproject.toml`."""
