# -*- coding: utf-8 -*-

from typing_extensions import final

from dotenv_linter.grammar.fst import Node


class BaseViolation(object):
    """Base class for all violations."""

    code: int
    error_template: str

    def __init__(self, node, text: str) -> None:
        """Creates instance of any violation."""
        self._node = node
        self._text = text

    @final
    def as_line(self) -> str:
        """Coverts violation to a single line information."""
        return '{0} {1} {2}'.format(
            self.location(),
            self._formated_code(),
            self.error_template.format(self._text),
        )

    def location(self) -> int:
        """Returns in-file location of a violation."""
        raise NotImplementedError('Should be redefined in a subclass')

    @final
    def _formated_code(self) -> str:
        return str(self.code).zfill(3)


class BaseFSTViolation(BaseViolation):
    """Base class for all ``fst`` violations."""

    _node: Node

    @final
    def location(self) -> int:
        """Returns in-file location of a violation."""
        return self._node.lineno


class BaseFileViolation(BaseViolation):
    """Base class for all violations that operate on whole files."""

    def __init__(self, node=None, text=None) -> None:
        """Creates instance of file-based violation."""
        self._node = node
        self._text = text

    @final
    def location(self) -> int:
        """Returns in-file location of a violation."""
        return 0
