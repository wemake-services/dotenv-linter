# -*- coding: utf-8 -*-

from dataclasses import fields
from typing import Any, Iterable, Iterator, List, Tuple, Union

from typing_extensions import final

from dotenv_linter.grammar.fst import Module, Node
from dotenv_linter.violations.base import BaseViolation

#: Defines field internals of a dataclass, could be `Any`, that's why ignored
FieldInfo = Tuple[str, Union[List[Any], Any]]  # type: ignore


def iter_fields(node: Node) -> Iterator[FieldInfo]:
    """Iterates over all fields inside a ``fst`` node."""
    yield from (
        (field.name, getattr(node, field.name))
        for field in fields(node)
    )


class BaseVisitor(object):
    """Base visitor class for all possible cases."""

    def __init__(self, fst: Module) -> None:
        """Creates default visitor instance."""
        self._fst = fst
        self._violations: List[BaseViolation] = []

    @property
    def violations(self) -> Iterable[BaseViolation]:
        """Utility getter not to expose violations directly."""
        return self._violations

    def _add_violation(self, violation: BaseViolation) -> None:
        """Adds new violations to the visitor."""
        self._violations.append(violation)

    def _post_visit(self) -> None:
        """
        Method to be executed after all nodes have been visited.

        By default does nothing.
        """


class BaseFSTVisitor(BaseVisitor):
    """
    Allows to check ``fst`` trees.

    Attributes:
        contents: ``str`` of the given file.

    """

    def visit(self, node: Node) -> None:
        """
        Visit a ``fst`` node.

        This code is copy-pasted from ``ast`` module, so it should stay
        as it is now. No need to refactor it.
        """
        method = 'visit_{0}'.format(node.__class__.__qualname__.lower())
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: Node) -> None:  # noqa: WPS231
        """
        Called if no explicit visitor function exists for a node.

        This code is copy-pasted from ``ast`` module, so it should stay
        as it is now. No need to refactor it.
        """
        for _field, node_value in iter_fields(node):
            if isinstance(node_value, list):
                for sub_node in node_value:
                    if isinstance(sub_node, Node):
                        self.visit(sub_node)  # noqa: WPS220
            elif isinstance(node_value, Node):
                self.visit(node_value)

    @final
    def run(self) -> None:
        """Visits all token types that have a handler method."""
        self.visit(self._fst)
        self._post_visit()
