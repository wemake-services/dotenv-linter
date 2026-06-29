import pytest

from dotenv_linter.violations.values import (
    CommentInValueViolation,
    QuotedValueViolation,
    SpacedValueViolation,
)


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [
        ('SOME_KEY="1"', 1),
        ("SOME_KEY='1'", 1),
        ('SOME_KEY="VALUE"', 1),
        ('KEY=VALUE', 0),
    ],
)
def test_quoted_value_violation(make_violations, code, expected_count):
    """
    Checks if value in quoted.

    raises ``QuotedValueViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == expected_count

    assert all(
        isinstance(violation, QuotedValueViolation) for violation in violations
    )


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [('SOME_KEY=1  ', 1), ('SOME_KEY=VALUE     ', 1), ('KEY=VALUE', 0)],
)
def test_spaced_value_violation(make_violations, code, expected_count):
    """
    Checks if value trailing spaces.

    raises ``SpacedValueViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == expected_count

    assert all(
        isinstance(violation, SpacedValueViolation) for violation in violations
    )


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [
        ('KEY=VALUE # COMMENT', 1),
        ('KEY=VALUE# COMMENT', 1),
        ('KEY=# VALUE', 1),
        ('KEY=VAL#123', 0),
    ],
)
def test_comment_in_value_violation(make_violations, code, expected_count):
    """
    Checks if value has comment.

    raises ``CommentInValueViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == expected_count

    assert all(
        isinstance(violation, CommentInValueViolation)
        for violation in violations
    )
