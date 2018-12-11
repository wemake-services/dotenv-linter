# -*- coding: utf-8 -*-

from typing_extensions import final

from dotenv_linter.grammar.fst import Assign
from dotenv_linter.violations.assigns import SpacedAssignViolation
from dotenv_linter.visitors.base import BaseFSTVisitor


@final
class AssignVisitor(BaseFSTVisitor):
    """Finds wrong assigns."""

    def visit_assign(self, node: Assign) -> None:
        """
        Visits assign nodes to find errors.

        Raises:
            SpacedAssignViolation

        """
        self._check_assign_char(node)
        self.generic_visit(node)

    def _check_assign_char(self, node: Assign) -> None:
        if node.raw_text.startswith(' '):
            self._add_violation(
                SpacedAssignViolation(node, text=node.text),
            )
