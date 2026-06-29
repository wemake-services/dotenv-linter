import pytest

from dotenv_linter.violations.parsing import ParsingViolation


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_count'),
    [('=VALUE', 1), ('=', 1), ('SOME_KEY=VALUE', 0)],
)
def test_parsing_violation(make_violations, code, expected_count):
    """
    Checks that this unparsable file.

    raises ``ParsingViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == expected_count

    assert all(
        isinstance(violation, ParsingViolation) for violation in violations
    )
