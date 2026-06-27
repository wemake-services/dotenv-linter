import pytest

from dotenv_linter.violations.parsing import ParsingViolation


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    'code',
    ['=VALUE', '='],
)
def test_parsing_violation(make_violations, code):
    """
    Checks that this unparsable file.

    raises ``ParsingViolation``.
    """
    violations = make_violations(code)

    assert len(violations) == 1
    assert isinstance(violations[0], ParsingViolation)
