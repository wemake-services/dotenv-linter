import pytest

_disable_violations = """\
# dotenv:disable
wemake=DOTENV
WEMAKE = DOTENV
WEMAKE = "WPS"
"""

_enable_violations = """\
# dotenv:enable
WEMAKE=DOTENV
WEMAKE="DOTENV"
"""

_enable_disable_mixed_violations = """\
# dotenv:enable
SOME_KEY=VALUE
# dotenv:disable[QuotedValueViolation, ReservedNameViolation]
# dotenv:disable[DuplicateNameViolation]
WEMAKE="DMR"
DJANGO_ENV=1
KEY="VALUE"
# dotenv:ignore[CommentInValueViolation]
WEMAKE_=VALUE # This is a comment
# dotenv:disable[QuotedValueViolation, ReservedNameViolation]
GOOD=VALUE
# dotenv:enable[QuotedValueViolation]
NEW_GOOD=VALUE
"""

_edge_case_ignore = """\
# dotenv:disable[QuotedValueViolation, ReservedNameViolation]
GOOD="VALUE"
# dotenv:enable[QuotedValueViolation]
NEW_GOOD="VALUE"
"""

_enable_with_ignores = """\
# dotenv:enable
WEMAKE=DOTENV
# dotenv:ignore[QuotedValueViolation, UnreadableNameViolation]
WEMAKE_SERVICE_0O="DOTENV"
"""

_disable_mixed = """\
# dotenv:disable[QuotedValueViolation]
WEMAKE="DOTENV"
# dotenv:disable[UnreadableNameViolation]
WEMAKE_SERVICE_0O="DOTENV"
"""

_duplicate_keys = """\
# dotenv:disable
# This and the following lines are not checked all violations
KEY=VALUE
SOME_KEY=VALUE
# dotenv:enable
# This and the following lines are checked all violations
KEY=VALUE
SOME_KEY=VALUE
"""


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_disable(make_violations):
    """Checks that disable lines will be ignore."""
    violations = make_violations(_disable_violations)

    assert len(violations) == 0


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_enable(make_violations):
    """Checks that enable lines will be ignore."""
    violations = make_violations(_enable_violations)

    assert len(violations) == 3


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_enable_disable_mixed(make_violations):
    """Checks that enable and disable lines will be ignore."""
    violations = make_violations(_enable_disable_mixed_violations)

    assert len(violations) == 0


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_enable_with_ignores(make_violations):
    """Checks that enable lines with ignores will be ignore."""
    violations = make_violations(_enable_with_ignores)

    assert len(violations) == 0


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_edge_case_ignore(make_violations):
    """Checks that enable lines with ignores will be ignore."""
    violations = make_violations(_edge_case_ignore)

    assert len(violations) == 1


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_disable_mixed(make_violations):
    """Checks that disable lines will be ignore."""
    violations = make_violations(_disable_mixed)

    assert len(violations) == 0


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_duplicate_keys(make_violations):
    """Checks that duplicate keys will be ignore."""
    violations = make_violations(_duplicate_keys)

    assert len(violations) == 2
