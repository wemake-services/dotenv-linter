# -*- coding: utf-8 -*-

from dotenv_linter.violations.base import BaseFSTViolation


class RawNameViolation(BaseFSTViolation):
    """
    Restricts to use raw names withour equal sign or value.

    Example::

        # Correct:
        KEY=1

        # Wrong:
        KEY

    """

    code = 100
    error_template = 'Found raw name without assign'
