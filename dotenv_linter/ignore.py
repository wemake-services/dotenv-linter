import re
from typing import Final

from dotenv_linter.grammar.fst import Assign, Comment, Module, Name, Statement
from dotenv_linter.violations.base import BaseViolation
from dotenv_linter.visitors.base import BaseFSTVisitor

_IGNORE_PATTERN: Final = re.compile(
    r'^[ \t]*#\s*dotenv:ignore\[([^\]]+)\]\s*$',
)


def _clean_names(names: list[str]) -> list[str]:
    return [name.strip() for name in names]


def _is_ignore_comment(
    node: Statement | Comment | Name,
) -> re.Match[str] | None:
    if isinstance(node, Comment):
        match = _IGNORE_PATTERN.match(node.raw_text)
        return match or None
    return None


def parse_ignore_comments(module: Module) -> dict[int, set[str]]:
    """
    Accumulate ``# dotenv:ignore[...]`` comments onto the next ``Assign``.

    Multiple consecutive comments are merged into a single set.
    Ignores without a following ``Assign`` are discarded.
    """
    ignore_map: dict[int, set[str]] = {}
    accumulated_ignores: set[str] = set()

    for node in module.body:
        match = _is_ignore_comment(node)
        if match:
            accumulated_ignores.update(_clean_names(match.group(1).split(',')))

        elif isinstance(node, Assign):
            ignore_map[node.lineno] = accumulated_ignores.copy()
            accumulated_ignores.clear()

    return ignore_map


def _should_ignore(
    violation: BaseViolation, ignore_map: dict[int, set[str]]
) -> bool:
    line = violation.location()
    violation_name = type(violation).__name__
    return line in ignore_map and violation_name in ignore_map[line]


def filter_violations(
    visitor: BaseFSTVisitor, ignore_map: dict[int, set[str]]
) -> list[BaseViolation]:
    """Return only violations that are not suppressed by ignore comments."""
    return [
        violation
        for violation in visitor.violations
        if not _should_ignore(violation, ignore_map)
    ]
