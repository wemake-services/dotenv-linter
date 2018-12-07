# -*- coding: utf-8 -*-

from dataclasses import fields
from typing import Any, List, Tuple, Union, Iterator

from typing_extensions import final

from dotenv_linter.grammar.fst import Module, Node
from dotenv_linter.violations.base import BaseViolation

FieldInfo = Tuple[str, Union[List[Any], Any]]


def iter_fields(node: Node) -> Iterator[FieldInfo]:
    """Iterates over all fields inside a ``fst`` node."""
    for field in fields(node):
        yield field.name, getattr(node, field.name)


class BaseVisitor(object):
    def __init__(self, fst: Module) -> None:
        self._fst = fst
        self.violations: List[BaseViolation] = []

    def add_violation(self, violation: BaseViolation) -> None:
        """Adds new violations to the visitor."""
        self.violations.append(violation)

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
        """Visit a ``fst`` node."""
        method = 'visit_' + node.__class__.__qualname__.lower()
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: Node) -> None:
        """Called if no explicit visitor function exists for a node."""
        for _field, node_value in iter_fields(node):
            if isinstance(node_value, list):
                for sub_node in node_value:
                    if isinstance(sub_node, Node):
                        self.visit(sub_node)
            elif isinstance(node_value, Node):
                self.visit(node_value)

    @final
    def run(self) -> None:
        """Visits all token types that have a handler method."""
        self.visit(self._fst)
        self._post_visit()
