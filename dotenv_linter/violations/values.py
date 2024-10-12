"""
Rules about writing correct dotenv values.

By convention we do not print values to the output.
Since they might contain private values.

.. currentmodule:: dotenv_linter.violations.values

.. autoclass:: SpacedValueViolation
.. autoclass:: QuotedValueViolation
.. autoclass:: InvalidEOLViolation

"""

from typing_extensions import final

from dotenv_linter.violations.base import BaseFSTViolation


@final
class SpacedValueViolation(BaseFSTViolation):
    """
    Restricts to write values with trailing spaces.

    Reasoning:
        These spaces are not guaranteed to be preserved.
        So, it is better not to rely on them.

    Solution:
        Remove trailing spaces from the value.

    .. versionadded:: 0.1.0

    """

    code = 300
    error_template = 'Found spaced value'


@final
class QuotedValueViolation(BaseFSTViolation):
    """
    Restricts to quoted values.

    Reasoning:
        Dotenv parser usually strips quotes away, so it is hard to say
        whether these quotes will stay on a final value, or not.

    Solution:
        Remove any quotes from the value.

    Example::

        # Correct:
        KEY=1

        # Wrong:
        KEY="1"

    .. versionadded:: 0.1.0

    """

    code = 301
    error_template = 'Found quoted value'


@final
class InvalidEOLViolation(BaseFSTViolation):
    r"""
    Restricts to use `\r\n` (CRLF) end-of-line.

    Reasoning:
        Mixing different end-of-line chars can lead to different
        hard-to-debug problems.

    Solution:
        Use `\n` (LF) end-of-line.
        Another option is to add line `text eol=lf` to `.gitattributes`.

    .. versionadded:: 0.6.0

    """

    code = 302
    error_template = 'Found CRLF end-of-line'
