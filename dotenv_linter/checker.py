# -*- coding: utf-8 -*-

import sys
from enum import Enum
from typing import Iterator, NoReturn, Optional, Tuple

from typing_extensions import final

from dotenv_linter.grammar.fst import Module
from dotenv_linter.grammar.parser import DotenvParser, ParsingError
from dotenv_linter.logics.report import Report
from dotenv_linter.visitors.fst import assigns, names


@final
class _ExitCodes(Enum):
    initial = -1
    success = 0
    linting_error = 1
    system_error = 137


@final
class _FSTChecker(object):
    """"""

    _visitors_pipeline = (
        assigns.AssignVisitor,
        names.NameVisitor,
        names.NameInModuleVisitor,
    )

    def __init__(self, filenames: Tuple[str, ...]) -> None:
        self._filenames = filenames
        self._status = _ExitCodes.initial
        self._parser = DotenvParser()

    def run(self) -> None:
        for filename, file_contents in self._prepare_file_contents():
            fst = self._prepare_fst(filename, file_contents)
            if fst is None:
                continue

            self._lint_file(filename, fst)
        self._check_global_status()

    def _prepare_file_contents(self) -> Iterator[Tuple[str, str]]:
        """Returns iterator with each file contents."""
        for filename in self._filenames:
            with open(filename, encoding='utf8') as file_object:
                yield filename, file_object.read()

    def _prepare_fst(
        self,
        filename: str,
        file_contents: str,
    ) -> Optional[Module]:
        """Builds ``fst`` tree for a given """
        try:
            return self._parser.parse(file_contents)
        except ParsingError:
            pass
            # TODO: insert correct violation class
            # self._report_violations([])
        return None

    def _lint_file(self, filename: str, fst: Module) -> None:
        report = Report(filename)
        for visitor_class in self._visitors_pipeline:
            visitor = visitor_class(fst)
            visitor.run()
            report.collect_from(visitor)
        report.report()
        self._check_report_status(report)

    def _check_report_status(self, report: Report) -> None:
        """Checks report status and sets the global status."""
        if report.has_violations:
            self._status = _ExitCodes.linting_error

    def _check_global_status(self) -> None:
        """Checks the final status when all checks has been executed."""
        if self._status == _ExitCodes.initial:
            self._status = _ExitCodes.success


@final
class DotenvFileChecker(object):
    """
    Main class of the application.

    It does all the communication.
    """

    def __init__(self, filenames: Tuple[str, ...], options = None):
        """Creates new instance."""
        self._fst_checker = _FSTChecker(filenames)

    def run(self) -> None:
        """Executes the linting process."""
        self._fst_checker.run()

    def finish(self, message: Optional[str]) -> NoReturn:
        """Returns the status code and text messages."""
        if self._fst_checker._status == _ExitCodes.initial:
            # This means, that linting process did not change status:
            self._fst_checker._status = _ExitCodes.system_error

        if message:
            if self._fst_checker._status == _ExitCodes.success:
                output = sys.stdout
            else:
                output = sys.stderr
            print(message, file=output)
        sys.exit(int(self._fst_checker._status.value))
