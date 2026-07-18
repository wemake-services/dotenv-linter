from typing_extensions import final

from dotenv_linter.grammar.fst import Assign, Comment, Module
from dotenv_linter.ignore import ViolationToggle
from dotenv_linter.types import IgnoreMap
from dotenv_linter.visitors.base import BaseFSTVisitor


@final
class MetadataVisitor(BaseFSTVisitor):
    """Collects metadata from the FST for use by other components."""

    def __init__(self, fst: Module) -> None:
        """Create a new MetadataVisitor instance."""
        super().__init__(fst)
        self.ignore_map: IgnoreMap = {}
        self._violation_toggle: ViolationToggle = ViolationToggle()

    def visit_comment(self, node: Comment) -> None:
        """Visits comment nodes to find ignores comment."""
        self._violation_toggle.process_comment(node)

    def visit_assign(self, node: Assign) -> None:
        """Visits assign nodes to add violations."""
        violations = self._violation_toggle.get_violations()
        self.ignore_map[node.lineno] = violations
