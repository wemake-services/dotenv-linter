import re
from typing import Final, final

from dotenv_linter.grammar.fst import Comment
from dotenv_linter.logics.text import clean_names
from dotenv_linter.types import IgnoreMap
from dotenv_linter.violations.base import BaseViolation

_IGNORE_PATTERN: Final = re.compile(
    r'^[ \t]*#\s*dotenv:ignore\[([^\]]+)\]\s*$',
)

_DISABLE_PATTERN: Final = re.compile(
    r'^[ \t]*#\s*dotenv:disable(?:\[([^\]]*)\])?\s*$',
)

_ENABLE_PATTERN: Final = re.compile(
    r'^[ \t]*#\s*dotenv:enable(?:\[([^\]]*)\])?\s*$',
)

_ALL_VIOLATIONS_DISABLED: Final = 'ALL disabled'


@final
class ViolationToggle:
    """
    Toggle violations based on disable, enable, and ignore comments.

    Stores current violations on ``current_violations``.
    Accumulates ignores on ``accumulated_ignores``.
    """

    def __init__(self) -> None:
        """Create a new ViolationToggle instance."""
        self.current_violations: set[str] = set()
        self.accumulated_ignores: set[str] = set()
        self.ignore_map: IgnoreMap = {}

    def process_comment(self, node: Comment) -> None:
        """Process a comment node: apply disable, enable, or ignore logic."""
        comments_handlers = (
            (_DISABLE_PATTERN, self._apply_disable),
            (_ENABLE_PATTERN, self._apply_enable),
            (_IGNORE_PATTERN, self._apply_ignore_line),
        )

        for comment_pattern, comment_handler in comments_handlers:
            match = comment_pattern.match(node.raw_text)
            if match:
                comment_handler(match)
                return

    def get_violations(self) -> set[str]:
        """Return currently active violations and reset accumulated ignores."""
        violations = self.current_violations.union(self.accumulated_ignores)
        self._clear_accumulated_ignores()
        return violations

    def _apply_disable(self, match: re.Match[str]) -> None:
        violations = match.group(1)
        if violations:
            violations_list = clean_names(violations.split(','))
            self.current_violations.update(set(violations_list))
        else:
            self.current_violations = {_ALL_VIOLATIONS_DISABLED}

    def _apply_enable(self, match: re.Match[str]) -> None:
        violations = match.group(1)
        if violations:
            violations_list = clean_names(violations.split(','))
            self.current_violations -= set(violations_list)
            self.current_violations.discard(_ALL_VIOLATIONS_DISABLED)
        else:
            self.current_violations.clear()

    def _apply_ignore_line(self, match: re.Match[str]) -> None:
        violations_list = clean_names(match.group(1).split(','))
        self.accumulated_ignores.update(set(violations_list))

    def _clear_accumulated_ignores(self) -> None:
        """Clear accumulated ignores."""
        self.accumulated_ignores.clear()


def should_ignore(violation: BaseViolation, ignore_map: IgnoreMap) -> bool:
    """Return ``True`` if violation should be ignored, ``False`` otherwise."""
    line = violation.location()
    violation_name = type(violation).__name__
    return line in ignore_map and (
        violation_name in ignore_map[line]
        or _ALL_VIOLATIONS_DISABLED in ignore_map[line]
    )


def apply_ignore_filter(
    violations: list[BaseViolation], ignore_map: IgnoreMap
) -> list[BaseViolation]:
    """Return only violations that are not suppressed by ignore comments."""
    return [
        violation
        for violation in violations
        if not should_ignore(violation, ignore_map)
    ]
