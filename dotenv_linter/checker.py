from __future__ import annotations

import sys
from collections.abc import Iterable, Iterator
from enum import IntEnum
from pathlib import Path
from typing import Any, NoReturn, final

from dotenv_linter.exceptions import ParsingError
from dotenv_linter.grammar.fst import Module
from dotenv_linter.grammar.parser import DotenvParser
from dotenv_linter.logics.report import Report
from dotenv_linter.violations.parsing import ParsingViolation
from dotenv_linter.visitors.fst import assigns, comments, names, values


@final
class _ExitCodes(IntEnum):
    initial = -1
    success = 0
    linting_error = 1
    system_error = 137


@final
class _FSTChecker:
    """Internal checker instance to actually run all the checks."""

    _visitors_pipeline = (
        assigns.AssignVisitor,
        comments.CommentVisitor,
        names.NameVisitor,
        names.NameInModuleVisitor,
        values.ValueVisitor,
    )

    def __init__(self, filenames: Iterable[str]) -> None:
        """Creates new instance."""
        self._filenames = filenames
        self._parser = DotenvParser()
        self.status = _ExitCodes.initial

    def run(self) -> None:
        """Executes all checks for each given filename."""
        for filename, file_contents in self._prepare_file_contents():
            fst = self._prepare_fst(filename, file_contents)
            self._lint_file(filename, fst)
        self._check_global_status()

    def _prepare_file_contents(self) -> Iterator[tuple[str, str]]:
        """Returns iterator with each file contents."""
        for filename in self._filenames:  # TODO: move this logic from here
            # From `open` docs on `newline` - If it is '', universal
            # newline mode is enabled but line endings are returned
            # to the caller untranslated
            with Path(filename).open(
                encoding='utf8',
                newline='',
            ) as file_object:
                yield filename, file_object.read()

    def _prepare_fst(
        self,
        filename: str,
        file_contents: str,
    ) -> Module | None:
        try:
            return self._parser.parse(file_contents)
        except ParsingError:
            return None

    def _lint_file(self, filename: str, fst: Module | None) -> None:
        report = Report(filename)

        # TODO: this looks not that pretty. A refactor maybe?
        if fst is None:
            report.collect_one(ParsingViolation())
        else:
            for visitor_class in self._visitors_pipeline:
                visitor = visitor_class(fst)
                visitor.run()
                report.collect_from(visitor)

        report.report()
        self._check_report_status(report)

    def _check_report_status(self, report: Report) -> None:
        """Checks report status and sets the global status."""
        if report.has_violations:
            self.status = _ExitCodes.linting_error

    def _check_global_status(self) -> None:
        """Checks the final status when all checks has been executed."""
        if self.status == _ExitCodes.initial:
            self.status = _ExitCodes.success


@final
class DotenvFileChecker:
    """
    Main class of the application.

    It does all the communication.
    """

    # TODO: create options
    def __init__(
        self,
        filenames: Iterable[str],
        options: Any | None = None,
    ) -> None:
        """Creates new instance."""
        self._fst_checker = _FSTChecker(filenames)

    def run(self) -> NoReturn:
        """Executes the linting process."""
        self._fst_checker.run()
        if self._fst_checker.status == _ExitCodes.initial:
            # This means, that linting process did not change status:
            self._fst_checker.status = _ExitCodes.system_error
        self._exit()

    def fail(self) -> NoReturn:
        """Exits the program with fail status code."""
        self._fst_checker.status = _ExitCodes.system_error
        self._exit()

    def _exit(self) -> NoReturn:
        sys.exit(int(self._fst_checker.status.value))
