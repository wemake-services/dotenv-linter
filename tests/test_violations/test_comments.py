import pytest

from dotenv_linter.violations.comments import SpacedCommentViolation


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    'code',
    [
        ' # COMMENT',
        '      #COMMENT',
    ],
)
def test_spaced_comments_violation(make_violations, code):
    """
    Checks leading spaces in comments.

    raises ``SpacedCommentViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == 1
    assert isinstance(violations[0], SpacedCommentViolation)
