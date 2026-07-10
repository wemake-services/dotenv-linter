from __future__ import annotations

from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import final

from dotenv_linter.constants import ExitCodes
from dotenv_linter.exceptions import ParsingError
from dotenv_linter.grammar.fst import Module
from dotenv_linter.grammar.parser import DotenvParser
from dotenv_linter.logics.collector import ReportCollector
from dotenv_linter.logics.report import Report


def _read_file_content(filename: str) -> str:
    # From `open` docs on `newline` - If it is '', universal
    # newline mode is enabled but line endings are returned
    # to the caller untranslated
    with Path(filename).open(encoding='utf8', newline='') as file_object:
        return file_object.read()


@final
class FSTChecker:
    """Internal checker instance to actually run all the checks."""

    def __init__(self, filenames: Iterable[str]) -> None:
        """Creates new instance."""
        self._filenames = filenames
        self._parser = DotenvParser()
        self._report_collector = ReportCollector()
        self.status = ExitCodes.initial
        self.reports: list[Report] = []

    def run(self) -> None:
        """Executes all checks for each given filename."""
        for filename, file_contents in self._prepare_file_contents():
            fst = self._prepare_fst(file_contents)
            self._lint_file(filename, fst)
        self._check_global_status()

    def _prepare_file_contents(self) -> Iterator[tuple[str, str]]:
        """Returns iterator with each file contents."""
        for filename in self._filenames:
            yield filename, _read_file_content(filename)

    def _prepare_fst(
        self,
        file_contents: str,
    ) -> Module | None:
        try:
            return self._parser.parse(file_contents)
        except ParsingError:
            return None

    def _lint_file(self, filename: str, fst: Module | None) -> None:
        report = self._report_collector.collect(filename, fst)
        self.reports.append(report)
        report.report()
        self._check_report_status(report)

    def _check_report_status(self, report: Report) -> None:
        """Checks report status and sets the global status."""
        if report.has_violations:
            self.status = ExitCodes.linting_error

    def _check_global_status(self) -> None:
        """Checks the final status when all checks has been executed."""
        if self.status == ExitCodes.initial:
            self.status = ExitCodes.success
