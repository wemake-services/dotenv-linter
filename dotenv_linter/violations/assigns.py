# -*- coding: utf-8 -*-

"""
Rules that define how assigns should be made.

.. currentmodule:: dotenv_linter.violations.assigns

.. autoclass:: SpacedAssignViolation

"""

from typing_extensions import final

from dotenv_linter.violations.base import BaseFSTViolation


@final
class SpacedAssignViolation(BaseFSTViolation):
    """
    Restricts to write ``=`` signs with extra spaces.

    Reasoning:
        Valid ``shell`` syntax requires to write assigns without any spaces.

    Solution:
        Remove any spaces between the ``=`` char.

    Example::

        # Correct:
        KEY=1
        OTHER=

        # Wrong:
        KEY = 1
        OTHER =

    .. versionadded:: 0.1.0

    """

    code = 200
    error_template = 'Found spaced assign'
