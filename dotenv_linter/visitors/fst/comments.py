# -*- coding: utf-8 -*-

from typing_extensions import final

from dotenv_linter.grammar.fst import Comment
from dotenv_linter.violations.comments import SpacedCommentViolation
from dotenv_linter.visitors.base import BaseFSTVisitor


@final
class CommentVisitor(BaseFSTVisitor):
    """Finds wrong comment."""

    def visit_comment(self, node: Comment) -> None:
        """
        Checks how comments are defined.

        Raises:
            SpacedCommentViolation

        """
        self._check_comment_spaces(node)
        self.generic_visit(node)

    def _check_comment_spaces(self, node: Comment) -> None:
        if node.raw_text.startswith(' ') or node.raw_text.endswith(' '):
            self._add_violation(
                SpacedCommentViolation(node, text=node.raw_text),
            )
