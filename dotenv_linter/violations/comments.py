# -*- coding: utf-8 -*-

"""
Rules that define how comments should be written.

.. currentmodule:: dotenv_linter.violations.comments

.. autoclass:: SpacedCommentViolation

"""

from typing_extensions import final

from dotenv_linter.violations.base import BaseFSTViolation


@final
class SpacedCommentViolation(BaseFSTViolation):
    """
    Restricts to write comment with leading or trailing spaces.

    Reasoning:
        These spaces are meaningless and will be removed.
        So, why would you want to have them?

    Solution:
        Remove leading or trailing spaces from the comment body.

    .. versionadded:: 0.1.0

    """

    code = 400
    error_template = 'Found spaced comment: {0}'
