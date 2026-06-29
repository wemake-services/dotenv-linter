import pytest

from dotenv_linter.violations.comments import SpacedCommentViolation


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [
        (' # COMMENT', 1),
        ('      #COMMENT', 1),
        ('# CORRECT COMMENT#CORRECT COMMENT', 0),
    ],
)
def test_spaced_comments_violation(make_violations, code, expected_count):
    """
    Checks leading spaces in comments.

    raises ``SpacedCommentViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == expected_count

    assert all(
        isinstance(violation, SpacedCommentViolation)
        for violation in violations
    )
