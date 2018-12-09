# -*- coding: utf-8 -*-

import sys
from itertools import chain
from typing import Iterable, List

from typing_extensions import final

from dotenv_linter.visitors.base import BaseVisitor


class Report(object):
    """
    Reports are used to show multiple violations to the user.

    Reports format and sort violations the way it they want it.
    """

    def __init__(self, filename: str) -> None:
        """Creates new report instance."""
        self._filename = filename
        self._collected_from: List[BaseVisitor] = []
        self.has_violations = False

    @final
    def collect_from(self, visitor: BaseVisitor) -> None:
        """Collects violations from different visitors."""
        self._collected_from.append(visitor)

    def report(self) -> None:
        """Reports violations from all visitors."""
        sorted_violations = sorted(
            chain.from_iterable(
                visitor.violations for visitor in self._collected_from
            ),
            key=lambda violation: violation.location()
        )

        for violation in sorted_violations:
            print(
                '{0}:{1}'.format(self._filename, violation.as_line()),
                file=sys.stderr,
            )

        self.has_violations = bool(sorted_violations)
