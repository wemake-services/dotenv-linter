import pytest

from dotenv_linter.violations.names import (
    DuplicateNameViolation,
    IncorrectNameViolation,
    ReservedNameViolation,
    SpacedNameViolation,
    UnreadableNameViolation,
)


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    'code',
    [
        'key=VALUE',
        'Key=VALUE',
        '123START_WITH_NUMBER=VALUE',
        'SOME-KEY=VALUE',
    ],
)
def test_incorrect_name_violations(make_violations, code):
    """
    Check that variable names with invalid characters.

    raises ``IncorrectNameViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == 1
    assert isinstance(violations[0], IncorrectNameViolation)


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    'code',
    [
        'DJANGO_ENV=VALUE',
    ],
)
def test_reserved_name_violations(make_violations, code):
    """
    Check that using a reserved name.

    raises ``ReservedNameViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == 1
    assert isinstance(violations[0], ReservedNameViolation)


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    'code',
    [
        'SOME_KEY_0O=1',
        'SOME_KEY_O0=1',
        'KEY_1I=VALUE',
    ],
)
def test_unreadable_name_violations(make_violations, code):
    """
    Check that names containing visually ambiguous characters.

    raises ``UnreadableNameViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == 1
    assert isinstance(violations[0], UnreadableNameViolation)


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    'code',
    [
        ('KEY=VALUE1\nKEY=VALUE2'),
        ('KEY=VALUE\nSOME_KEY=VALUE\nKEY=VALUE'),
    ],
)
def test_dublicate_name_violation(make_violations, code):
    """
    Checks if a duplicate variable exists.

    raises ``DuplicateNameViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == 2
    for violation in violations:
        assert isinstance(violation, DuplicateNameViolation)


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    'code',
    [
        ('  SOME_KEY=VALUE'),
    ],
)
def test_spaced_name_violation(make_violations, code):
    """
    Checks leading spaces in name.

    raises ``SpacedNameViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == 1
    assert isinstance(violations[0], SpacedNameViolation)
