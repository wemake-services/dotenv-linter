# -*- coding: utf-8 -*-

from ast import iter_fields
from dataclasses import fields
from typing import List, Tuple, Union

from typing_extensions import final

from dotenv_linter.grammar.fst import Module, Node


def iter_fields(node: Node) -> Tuple[str, Union[List[Node], Node]]:
    """Iterates over all fields inside a ``fst`` node."""
    for field in fields(node):
        yield field, getattr(node, field.name)


class BaseVisitor(object):
    def __init__(self, fst: Module) -> None:
        self._fst = fst
        self.violations = []  # TODO: type

    def add_violation(self, violation) -> None:  # TODO: type
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
