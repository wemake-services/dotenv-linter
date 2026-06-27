import pytest

from dotenv_linter.violations.assigns import SpacedAssignViolation


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    'code',
    ['SOME_KEY =VALUE', 'SOME_KEY    =VALUE', 'SOME_KEY ='],
)
def test_spaced_assign_violation(make_violations, code):
    """
    Checks if '=' signs have extra spaces.

    raises ``SpacedAssignViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == 1
    assert isinstance(violations[0], SpacedAssignViolation)
