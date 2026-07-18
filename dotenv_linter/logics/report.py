import sys
from collections.abc import Iterable
from itertools import chain
from typing import final

from dotenv_linter.grammar.fst import Module
from dotenv_linter.ignore import apply_ignore_filter
from dotenv_linter.types import IgnoreMap
from dotenv_linter.violations.base import BaseViolation


class Report:
    """
    Reports are used to show multiple violations to the user.

    Reports format and sort violations the way it they want it.
    """

    def __init__(self, filename: str) -> None:
        """Creates new report instance."""
        self._filename = filename
        self._collected_from: list[Iterable[BaseViolation]] = []
        self.has_violations = False
        self.fst: Module | None = None
        self.ignore_map: IgnoreMap = {}

    @final
    def collect_from(self, violations: Iterable[BaseViolation]) -> None:
        """Collects violations from different visitors."""
        self._collected_from.append(violations)

    @final
    def collect_one(self, violation: BaseViolation) -> None:
        """Collects a single violation."""
        self._collected_from.append((violation,))

    def report(self) -> None:
        """Reports violations from all visitors."""
        violations = self.get_violations()
        sorted_violations = sorted(
            violations,
            key=lambda violation: violation.location(),
        )

        for ordered_violation in sorted_violations:
            print(  # noqa: WPS421
                f'{self._filename}:{ordered_violation.as_line()}',
                file=sys.stderr,
            )

        self.has_violations = bool(sorted_violations)

    def get_violations(self) -> list[BaseViolation]:
        """Returns all collected violations with ignored violations removed."""
        all_violations: list[BaseViolation] = list(
            chain.from_iterable(self._collected_from)
        )
        if self.fst is not None:
            all_violations = apply_ignore_filter(
                all_violations, self.ignore_map
            )
        return all_violations
