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
    ('code', 'expected_count'),
    [
        ('key=VALUE', 1),
        ('Key=VALUE', 1),
        ('123START_WITH_NUMBER=VALUE', 1),
        ('SOME-KEY=VALUE', 1),
        ('CORRECT=NAME', 0),
    ],
)
def test_incorrect_name_violations(make_violations, code, expected_count):
    """
    Check that variable names with invalid characters.

    raises ``IncorrectNameViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == expected_count

    assert all(
        isinstance(violation, IncorrectNameViolation)
        for violation in violations
    )


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [('DJANGO_ENV=VALUE', 1), ('SOME_KEY=VALUE', 0)],
)
def test_reserved_name_violations(make_violations, code, expected_count):
    """
    Check that using a reserved name.

    raises ``ReservedNameViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == expected_count

    assert all(
        isinstance(violation, ReservedNameViolation) for violation in violations
    )


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [
        ('SOME_KEY_0O=1', 1),
        ('SOME_KEY_O0=1', 1),
        ('KEY_1I=VALUE', 1),
        ('WEMAKE=SERVICE', 0),
    ],
)
def test_unreadable_name_violations(make_violations, code, expected_count):
    """
    Check that names containing visually ambiguous characters.

    raises ``UnreadableNameViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == expected_count

    assert all(
        isinstance(violation, UnreadableNameViolation)
        for violation in violations
    )


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [
        ('KEY=VALUE1\nKEY=VALUE2', 2),
        ('KEY=VALUE\nSOME_KEY=VALUE\nKEY=VALUE', 2),
        ('KEY=VALUE\nSOME_KEY=VALUE', 0),
    ],
)
def test_duplicate_name_violation(make_violations, code, expected_count):
    """
    Checks if a duplicate variable exists.

    raises ``DuplicateNameViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == expected_count

    assert all(
        isinstance(violation, DuplicateNameViolation)
        for violation in violations
    )


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [('  SOME_KEY=VALUE', 1), ('DEBUG=TRUE', 0)],
)
def test_spaced_name_violation(make_violations, code, expected_count):
    """
    Checks leading spaces in name.

    raises ``SpacedNameViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == expected_count

    assert all(
        isinstance(violation, SpacedNameViolation) for violation in violations
    )
