# -*- coding: utf-8 -*-

from typing import Tuple
from typing_extensions import final

from dotenv_linter.grammar.fst import Node


class BaseViolation(object):
    """Base class for all violations."""

    code: int
    error_template: str

    def __init__(self, node) -> None:
        """Creates instance of any violation."""
        self._node = node

    def as_line(self) -> str:
        """Coverts violation to a single line information."""
        location = '{0}:{1}'.format(*self._location())
        return '{0} {1}: {2}'.format(
            location, self._formated_code(), self.error_template,
        )

    def _formated_code(self) -> str:
        return str(self.code).zfill(3)

    def _location(self) -> Tuple[int, int]:
        """"Returns in-file location of a violation."""
        raise NotImplementedError('Should be redefined in a subclass')


class BaseFSTViolation(BaseViolation):
    """Base class for all ``fst`` violations."""

    _node: Node

    def _location(self) -> Tuple[int, int]:
        return self._node.lineno, self._node.col_offset
