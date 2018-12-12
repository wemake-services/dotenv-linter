# -*- coding: utf-8 -*-

"""
Different error that might happen during file parsing phase.

.. currentmodule:: dotenv_linter.violations.parsing

.. autoclass:: ParsingViolation

"""

from typing_extensions import final

from dotenv_linter.violations.base import BaseFileViolation


@final
class ParsingViolation(BaseFileViolation):
    """
    Indicates that given file can not be correctly parsed.

    This may include:
    1. Incorrect OS behavior
    2. Incorrect syntax inside this file
    3. Errors in our grammar definition
    4. Our internal errors

    .. versionadded:: 0.1.0

    """

    code = 1
    error_template = 'Unable to correctly parse dotenv file'
