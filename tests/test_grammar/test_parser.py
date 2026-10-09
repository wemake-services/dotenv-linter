import pytest

from dotenv_linter.exceptions import ParsingError
from dotenv_linter.grammar.parser import DotenvParser, DotenvTransformer


def test_parsing_error():
    """Calling ``line`` with an empty list raises ``ParsingError``."""
    transformer = DotenvTransformer()

    with pytest.raises(ParsingError):
        transformer.line([])


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_values'),
    [
        ('KEY="line1\nline2"', ['"line1\nline2"']),
        ("KEY='line1\nline2'", ["'line1\nline2'"]),
        ('KEY="a\nb\nc"', ['"a\nb\nc"']),
        ('KEY="line1\nline2" # note', ['"line1\nline2" # note']),
        ('KEY= "line1\nline2"', [' "line1\nline2"']),
        ('KEY="line1\nline2"\nOTHER=1', ['"line1\nline2"', '1']),
    ],
)
def test_multiline_quoted_value(code, expected_values):
    """A quoted value can span several lines."""
    module = DotenvParser().parse(code)

    assert [assign.right.raw_text for assign in module.body] == expected_values


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_multiline_value_with_escaped_quote():
    """An escaped double quote does not end a multiline value."""
    code = r"""KEY="a \" b
c"
OTHER=1"""

    first, second = DotenvParser().parse(code).body

    assert first.right.raw_text == code.removeprefix('KEY=').removesuffix(
        '\nOTHER=1',
    )
    assert second.right.raw_text == '1'


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_backslash_does_not_escape_single_quote():
    """Single quotes are literal, so a trailing backslash is just text."""
    code = r"""KEY='a\'
OTHER=1"""

    module = DotenvParser().parse(code)

    assert [assign.right.raw_text for assign in module.body] == [
        r"'a\'",
        '1',
    ]


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_multiline_value_keeps_next_line_number():
    """Statements after a multiline value report their real line."""
    module = DotenvParser().parse('KEY="line1\nline2\nline3"\nOTHER=1')

    assert [assign.lineno for assign in module.body] == [1, 4]


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected_values'),
    [
        ('KEY="unclosed\nOTHER=1', ['"unclosed', '1']),
        ("KEY='unclosed\nOTHER=1", ["'unclosed", '1']),
        ('KEY=ab"c\nOTHER=1', ['ab"c', '1']),
        ('KEY=value\nOTHER=1', ['value', '1']),
        ('KEY="1"\nOTHER="2"', ['"1"', '"2"']),
    ],
)
def test_unclosed_quote_ends_at_line_break(code, expected_values):
    """Values that do not close their quote keep ending at the line break."""
    module = DotenvParser().parse(code)

    assert [assign.right.raw_text for assign in module.body] == expected_values
