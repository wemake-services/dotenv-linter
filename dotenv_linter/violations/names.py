# -*- coding: utf-8 -*-

"""
Rules that define how names should be defined.

.. currentmodule:: dotenv_linter.violations.names

.. autoclass:: SpacedNameViolation
.. autoclass:: IncorrectNameViolation
.. autoclass:: DuplicateNameViolation
.. autoclass:: RawNameViolation

"""

from typing_extensions import final

from dotenv_linter.violations.base import BaseFSTViolation


@final
class SpacedNameViolation(BaseFSTViolation):
    """
    Restricts to use duplicate names variables.

    Reasoning:
        This spaces will be removed by the parsing mechanism, but they
        might cause some confusion to users.

    Solution:
        Remove leading spaces.

    Example::

        # Correct:
        SOME_KEY=1

        # Wrong:
            SOME_KEY=1

    .. versionadded:: 0.1.0

    """

    code = 100
    error_template = 'Found leading spaces: {0}'


@final
class IncorrectNameViolation(BaseFSTViolation):
    """
    Restricts to use restricted symbols to define names.

    Reasoning:
        By convention we can only use letters, numbers, and underscores to
        define dotenv variables.
        Moreover, variables can not start with numbers.

    Solution:
        Refactor your file to contain only allowed characters.

    Example::

        # Correct:
        SOME_KEY=1

        # Wrong:
        SOME-KEY=1

    .. versionadded:: 0.1.0

    """

    code = 101
    error_template = 'Found incorrect name: {0}'


@final
class DuplicateNameViolation(BaseFSTViolation):
    """
    Restricts to use duplicate names variables.

    Reasoning:
        There is no need to crate duplicate variables inside your
        dotenv file. Since it will be implicitly overridden by the parsing
        mechanism.

    Solution:
        Remove one of the duplicate variables.

    Example::

        # Correct:
        SOME_KEY=1
        OTHER_KEY=2

        # Wrong:
        SOME_KEY=1
        SOME_KEY=2

    .. versionadded:: 0.1.0

    """

    code = 102
    error_template = 'Found duplicate name: {0}'


@final
class RawNameViolation(BaseFSTViolation):
    """
    Restricts to use raw names without equal sign or value.

    Reasoning:
        It does not make any sense to just state some names.
        It might also break some ``.env`` parsers.

    Solution:
        Append equal sign to it.
        So, this would became a declaration of an empty variable.
        You can also add a value if it makes sense.

    Example::

        # Correct:
        KEY=1
        OTHER=

        # Wrong:
        KEY

    .. versionadded:: 0.1.0

    """

    code = 103
    error_template = 'Found raw name without assign: {0}'
