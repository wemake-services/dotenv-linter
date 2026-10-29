from importlib import metadata
from pathlib import Path

pkg_name = str(Path(__file__).parent.name)
"""Package name."""

pkg_version = metadata.version(pkg_name)
"""We store the version number inside the `pyproject.toml`."""
