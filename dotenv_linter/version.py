import sys

# Note that we use ``sys.version_info`` directly,
# because that's how ``mypy`` knows about what we are doing.
if sys.version_info >= (3, 8):  # pragma: no cover
    from importlib import metadata as importlib_metadata  # noqa: WPS433
else:  # pragma: no cover
    import importlib_metadata  # noqa: WPS440, WPS433


def _get_version(distribution_name: str) -> str:  # pragma: no cover
    """Fetches distribution version."""
    return importlib_metadata.version(distribution_name)  # type: ignore


pkg_name = 'dotenv-linter'

#: We store the version number inside the `pyproject.toml`:
pkg_version = _get_version(pkg_name)
