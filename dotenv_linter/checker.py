# -*- coding: utf-8 -*-

import sys
from enum import Enum
from typing import Iterator, NoReturn, Optional, Tuple

from dotenv_linter.grammar.fst import Module
from dotenv_linter.grammar.parser import DotenvParser, ParsingError
from dotenv_linter.visitors.base import BaseFSTVisitor


class _ExitCodes(Enum):
    initial = -1
    success = 0
    linting_error = 1
    system_error = 137


class _FSTChecker(object):
    """"""

    _visitors_pipeline = (
        BaseFSTVisitor,
    )

    def __init__(self, filenames: Tuple[str, ...]) -> None:
        self._filenames = filenames
        self._status = _ExitCodes.initial
        self._parser = DotenvParser()

    def run(self) -> None:
        for filename, file_contents in self._prepare_file_contents():
            fst = self._prepare_fst(filename, file_contents)
            print(fst)
            if fst is None:
                continue

            for visitor_class in self._visitors_pipeline:
                visitor = visitor_class(fst)
                visitor.run()
                self._report_violations(filename, visitor.violations)

        if self._status == _ExitCodes.initial:
            self._status = _ExitCodes.success

    def _prepare_file_contents(self) -> Iterator[str]:
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
            # TODO: insert correct violation class
            self._report_violations([])

    def _report_violations(self, filename: str, violations) -> None:
        """Reports all violations that happened inside a visitor."""
        if self._status == _ExitCodes.initial:
            self._status = _ExitCodes.linting_error

        for violation in violations:  # TODO: we can create `Report` class
            sys.stderr.write('{0}: {1}'.format(filename, violation.as_line()))
        sys.stderr.flush()


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
            output.write(message)
            output.flush()
        sys.exit(int(self._fst_checker._status.value))
