# -*- coding: utf-8 -*-

from typing_extensions import final


class BaseViolation(object):
    """Base class for all violations."""

    def as_line(self, filename: str) -> str:
        """Coverts violation to a single line information."""
