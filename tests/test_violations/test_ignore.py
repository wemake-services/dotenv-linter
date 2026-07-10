import pytest

_group_of_mixed_violations = """\
# dotenv:ignore[CommentInValueViolation, SpacedValueViolation]
# dotenv:ignore[UnreadableNameViolation, IncorrectNameViolation]
kEYO0= VALUE # comment
"""

_ignore_duplicate_name = """\
# dotenv:ignore[DuplicateNameViolation]
KEY=VALUE
# dotenv:ignore[DuplicateNameViolation]
KEY=VALUE
"""


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [
        ('# dotenv:ignore[IncorrectNameViolation]\nwemake=DOTENV', 0),
        ('wemake=DOTENV', 1),
    ],
)
def test_ignore_incorrect_name(make_violations, code, expected_count):
    """Checks that ``IncorrectNameViolation`` will be ignore."""
    violations = make_violations(code)

    assert len(violations) == expected_count


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [
        (_ignore_duplicate_name, 0),
        ('KEY=VALUE\nKEY=VALUE', 2),
    ],
)
def test_ignore_duplicate_name(make_violations, code, expected_count):
    """Checks that ``DuplicateNameViolation`` will be ignore."""
    violations = make_violations(code)

    assert len(violations) == expected_count


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_ignore_group_of_mixed_violations(make_violations):
    """Checks that group of mixed violations will be ignore."""
    violations = make_violations(_group_of_mixed_violations)

    assert len(violations) == 0


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [
        ('# dotenv:ignore[ReservedNameViolation]\nDJANGO_ENV=1', 0),
        ('DJANGO_ENV=VALUE', 1),
    ],
)
def test_ignore_reserved_name(make_violations, code, expected_count):
    """Checks that ``ReservedNameViolation`` will be ignore."""
    violations = make_violations(code)

    assert len(violations) == expected_count


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [
        ('# dotenv:ignore[UnreadableNameViolation]\nMY_1I_VAR=VALUE', 0),
        ('MY_1I_VAR=VALUE', 1),
    ],
)
def test_ignore_unreadable_name(make_violations, code, expected_count):
    """Checks that ``UnreadableNameViolation`` will be ignore."""
    violations = make_violations(code)

    assert len(violations) == expected_count


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [
        ('# dotenv:ignore[SpacedAssignViolation]\nKEY =', 0),
        ('KEY= 1', 1),
    ],
)
def test_ignore_spaced_name(make_violations, code, expected_count):
    """Checks that ``SpacedAssignViolation`` will be ignore."""
    violations = make_violations(code)

    assert len(violations) == expected_count


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [
        ('# dotenv:ignore[SpacedValueViolation]\nKEY=VALUE ', 0),
        ('KEY=VALUE ', 1),
    ],
)
def test_ignore_spaced_value(make_violations, code, expected_count):
    """Checks that ``SpacedValueViolation`` will be ignore."""
    violations = make_violations(code)

    assert len(violations) == expected_count
