from __future__ import annotations

import sys
from collections.abc import Iterable
from typing import Any, NoReturn, final

from dotenv_linter.constants import ExitCodes
from dotenv_linter.fst_checker import FSTChecker


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
        self._fst_checker = FSTChecker(filenames)

    def run(self) -> NoReturn:
        """Executes the linting process."""
        self._fst_checker.run()
        if self._fst_checker.status == ExitCodes.initial:
            # This means, that linting process did not change status:
            self._fst_checker.status = ExitCodes.system_error
        self._exit()

    def fail(self) -> NoReturn:
        """Exits the program with fail status code."""
        self._fst_checker.status = ExitCodes.system_error
        self._exit()

    def _exit(self) -> NoReturn:
        sys.exit(int(self._fst_checker.status.value))
