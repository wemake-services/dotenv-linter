import pytest

from dotenv_linter.exceptions import ParsingError
from dotenv_linter.grammar.parser import DotenvParser, DotenvTransformer


def _text(*lines: str) -> str:
    """Join lines, so raw strings with backslashes can span several lines."""
    return '\n'.join(lines)


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
@pytest.mark.parametrize(
    ('code', 'expected_values'),
    [
        # Escaped double quotes do not end the value:
        (
            _text(r'KEY="a \" b', 'c"', 'OTHER=1'),
            [_text(r'"a \" b', 'c"'), '1'],
        ),
        (
            _text('KEY="a', r'b \"c\" d', 'e"', 'OTHER=1'),
            [_text('"a', r'b \"c\" d', 'e"'), '1'],
        ),
        # Escapes written as text, without a real line break:
        (
            _text(r'QUOTE="He said:\n\"Ok\""', 'OTHER=1'),
            [r'"He said:\n\"Ok\""', '1'],
        ),
        (r'QUOTE="He said:\n\"Ok\""', [r'"He said:\n\"Ok\""']),
        # The same escapes spread over several real lines:
        (
            _text('QUOTE="He said:', r'\"Ok\"', 'and left"', 'OTHER=1'),
            [_text('"He said:', r'\"Ok\"', 'and left"'), '1'],
        ),
        # An escaped backslash does not escape the closing quote:
        (_text(r'KEY="a\\"', 'OTHER=1'), [r'"a\\"', '1']),
        (
            _text('KEY="a', r'b\\"', 'OTHER=1'),
            [_text('"a', r'b\\"'), '1'],
        ),
        # An escaped backslash followed by an escaped quote:
        (
            _text(r'KEY="a\\\"b', 'c"', 'OTHER=1'),
            [_text(r'"a\\\"b', 'c"'), '1'],
        ),
        # Quotes of the other kind are plain text:
        ('KEY="it\'s\nok"\nOTHER=1', ['"it\'s\nok"', '1']),
        ('KEY=\'say "hi"\nbye\'\nOTHER=1', ['\'say "hi"\nbye\'', '1']),
        ("KEY=\"'a'\n'b'\"\nOTHER=1", ["\"'a'\n'b'\"", '1']),
        ('KEY=\'"a"\n"b"\'\nOTHER=1', ['\'"a"\n"b"\'', '1']),
        # Both kinds of quotes in one file:
        (
            'A="x\ny"\nB=\'x\ny\'\nC="x\ny"',
            ['"x\ny"', "'x\ny'", '"x\ny"'],
        ),
    ],
)
def test_multiline_nested_quotes(code, expected_values):
    """Quotes of both kinds and escapes stay inside quoted values."""
    module = DotenvParser().parse(code)

    assert [assign.right.raw_text for assign in module.body] == expected_values


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
