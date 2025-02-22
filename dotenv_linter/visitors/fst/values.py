from typing import Final

from typing_extensions import final

from dotenv_linter.grammar.fst import Value
from dotenv_linter.violations.values import (
    InvalidEOLViolation,
    QuotedValueViolation,
    SpacedValueViolation,
)
from dotenv_linter.visitors.base import BaseFSTVisitor

CRLF_EOL: Final = '\r'


@final
class ValueVisitor(BaseFSTVisitor):
    """Finds wrong values."""

    def visit_value(self, node: Value) -> None:
        """
        Visits value nodes to find errors.

        Raises:
            QuotedValueViolation
            SpacedValueViolation
            InvalidEOLViolation

        """
        self._check_value_quotes(node)
        self._check_value_spaces(node)
        self._is_crlf_eol_used(node)

        self.generic_visit(node)

    def _check_value_spaces(self, node: Value) -> None:
        if node.raw_text.endswith(' ') or node.raw_text.startswith(' '):
            self._add_violation(SpacedValueViolation(node, text=node.raw_text))

    def _check_value_quotes(self, node: Value) -> None:
        text = node.raw_text.strip()
        if (text.startswith('"') and text.endswith('"')) or (
            text.startswith("'") and text.endswith("'")
        ):
            self._add_violation(QuotedValueViolation(node, text=node.raw_text))

    def _is_crlf_eol_used(self, node: Value) -> None:
        if node.raw_text.endswith(CRLF_EOL):
            self._add_violation(InvalidEOLViolation(node, text=node.text))
