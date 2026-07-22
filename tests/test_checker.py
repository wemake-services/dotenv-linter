from unittest.mock import MagicMock

import pytest

from dotenv_linter.checker import DotenvFileChecker
from dotenv_linter.constants import ExitCodes


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_fail_sets_status_and_exits():
    """Test that ``fail()`` sets the internal status to ``system_error``."""
    checker = DotenvFileChecker(filenames=())

    with pytest.raises(SystemExit) as exc_info:
        checker.fail()

    assert exc_info.value.code == ExitCodes.system_error


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_run_with_initial_status():
    """Test that ``run()`` forces ``system_error``."""
    checker = DotenvFileChecker(filenames=())
    mock_fst = MagicMock()
    mock_fst.status = ExitCodes.initial
    checker._fst_checker = mock_fst  # ruff:ignore[private-member-access]

    with pytest.raises(SystemExit) as exc_info:
        checker.run()

    assert mock_fst.status == ExitCodes.system_error
    assert exc_info.value.code == ExitCodes.system_error
