from collections.abc import Callable
from pathlib import Path

import pytest

from dotenv_linter.checker import DotenvFileChecker
from dotenv_linter.violations.base import BaseViolation


@pytest.fixture
def make_violations(tmp_path: Path) -> Callable[[str], list[BaseViolation]]:
    """Create all violations for files."""

    def factory(code: str) -> list[BaseViolation]:
        env_file = tmp_path / '.env'
        env_file.write_text(code)

        checker = DotenvFileChecker(filenames=[str(env_file)])
        with pytest.raises(SystemExit):
            checker.run()

        violations = []
        for report in checker._fst_checker.reports:  # noqa: SLF001
            violations.extend(report.get_violations())
        return violations

    return factory
