# -*- coding: utf-8 -*-

from typing_extensions import final

from dotenv_linter.grammar.fst import Value
from dotenv_linter.violations.values import (
    QuotedValueViolation,
    SpacedValueViolation,
)
from dotenv_linter.visitors.base import BaseFSTVisitor


@final
class ValueVisitor(BaseFSTVisitor):
    """Finds wrong values."""

    def visit_value(self, node: Value) -> None:
        """
        Visits value nodes to find errors.

        Raises:
            QuotedValueViolation
            SpacedValueViolation

        """
        self._check_value_quotes(node)
        self._check_value_spaces(node)
        self.generic_visit(node)

    def _check_value_spaces(self, node: Value) -> None:
        if node.raw_text.endswith(' ') or node.raw_text.startswith(' '):
            self._add_violation(SpacedValueViolation(node, text=node.raw_text))

    def _check_value_quotes(self, node: Value) -> None:
        text = node.raw_text.strip()
        if text.startswith('"') and text.endswith('"'):
            self._add_violation(QuotedValueViolation(node, text=node.raw_text))
        elif text.startswith("'") and text.endswith("'"):
            self._add_violation(QuotedValueViolation(node, text=node.raw_text))
