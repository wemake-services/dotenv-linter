import pytest

from dotenv_linter.violations.assigns import SpacedAssignViolation


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [
        ('SOME_KEY =VALUE', 1),
        ('SOME_KEY    =VALUE', 1),
        ('SOME_KEY =', 1),
        ('KEY=VALUE', 0),
    ],
)
def test_spaced_assign_violation(make_violations, code, expected_count):
    """
    Checks if '=' signs have extra spaces.

    raises ``SpacedAssignViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == expected_count

    assert all(
        isinstance(violation, SpacedAssignViolation) for violation in violations
    )
