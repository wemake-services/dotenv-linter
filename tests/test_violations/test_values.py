import pytest

from dotenv_linter.violations.values import (
    QuotedValueViolation,
    SpacedValueViolation,
)


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    'code',
    [
        'SOME_KEY="1"',
        "SOME_KEY='1'",
        'SOME_KEY="VALUE"',
    ],
)
def test_quated_value_violation(make_violations, code):
    """
    Checks if value in quoted.

    raises ``QuotedValueViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == 1
    assert isinstance(violations[0], QuotedValueViolation)


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    'code',
    [
        'SOME_KEY=1  ',
        'SOME_KEY=VALUE     ',
    ],
)
def test_spaced_value_violation(make_violations, code):
    """
    Checks if value trailing spaces.

    raises ``SpacedValueViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == 1
    assert isinstance(violations[0], SpacedValueViolation)
