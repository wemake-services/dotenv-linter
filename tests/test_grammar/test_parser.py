import pytest

from dotenv_linter.exceptions import ParsingError
from dotenv_linter.grammar.parser import DotenvParser, DotenvTransformer


def _text(*lines: str) -> str:
    """Join lines, so raw strings with backslashes can span several lines."""
    return '\n'.join(lines)


def _pairs(code: str) -> dict[str, str]:
    """Parses code into ``{name: value}``, so names are checked as well."""
    module = DotenvParser().parse(code)
    return {
        assign.left.raw_text: assign.right.raw_text for assign in module.body
    }


def test_parsing_error():
    """Calling ``line`` with an empty list raises ``ParsingError``."""
    transformer = DotenvTransformer()

    with pytest.raises(ParsingError):
        transformer.line([])


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected'),
    [
        ('KEY="line1\nline2"', {'KEY': '"line1\nline2"'}),
        ("KEY='line1\nline2'", {'KEY': "'line1\nline2'"}),
        ('KEY="a\nb\nc"', {'KEY': '"a\nb\nc"'}),
        ('KEY="line1\nline2" # note', {'KEY': '"line1\nline2" # note'}),
        ('KEY= "line1\nline2"', {'KEY': ' "line1\nline2"'}),
        (
            'KEY="line1\nline2"\nOTHER=1',
            {'KEY': '"line1\nline2"', 'OTHER': '1'},
        ),
    ],
)
def test_multiline_quoted_value(code, expected):
    """A quoted value can span several lines."""
    assert _pairs(code) == expected


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected'),
    [
        # Escaped double quotes do not end the value:
        (
            _text(r'KEY="a \" b', 'c"', 'OTHER=1'),
            {'KEY': _text(r'"a \" b', 'c"'), 'OTHER': '1'},
        ),
        (
            _text('KEY="a', r'b \"c\" d', 'e"', 'OTHER=1'),
            {'KEY': _text('"a', r'b \"c\" d', 'e"'), 'OTHER': '1'},
        ),
        # Escapes written as text, without a real line break:
        (
            _text(r'QUOTE="He said:\n\"Ok\""', 'OTHER=1'),
            {'QUOTE': r'"He said:\n\"Ok\""', 'OTHER': '1'},
        ),
        (
            r'QUOTE="He said:\n\"Ok\""',
            {'QUOTE': r'"He said:\n\"Ok\""'},
        ),
        # The same escapes spread over several real lines:
        (
            _text('QUOTE="He said:', r'\"Ok\"', 'and left"', 'OTHER=1'),
            {
                'QUOTE': _text('"He said:', r'\"Ok\"', 'and left"'),
                'OTHER': '1',
            },
        ),
        # An escaped backslash does not escape the closing quote:
        (
            _text(r'KEY="a\\"', 'OTHER=1'),
            {'KEY': r'"a\\"', 'OTHER': '1'},
        ),
        (
            _text('KEY="a', r'b\\"', 'OTHER=1'),
            {'KEY': _text('"a', r'b\\"'), 'OTHER': '1'},
        ),
        # An escaped backslash followed by an escaped quote:
        (
            _text(r'KEY="a\\\"b', 'c"', 'OTHER=1'),
            {'KEY': _text(r'"a\\\"b', 'c"'), 'OTHER': '1'},
        ),
        # Quotes of the other kind are plain text:
        (
            'KEY="it\'s\nok"\nOTHER=1',
            {'KEY': '"it\'s\nok"', 'OTHER': '1'},
        ),
        (
            'KEY=\'say "hi"\nbye\'\nOTHER=1',
            {'KEY': '\'say "hi"\nbye\'', 'OTHER': '1'},
        ),
        (
            "KEY=\"'a'\n'b'\"\nOTHER=1",
            {'KEY': "\"'a'\n'b'\"", 'OTHER': '1'},
        ),
        (
            'KEY=\'"a"\n"b"\'\nOTHER=1',
            {'KEY': '\'"a"\n"b"\'', 'OTHER': '1'},
        ),
        # Both kinds of quotes in one file:
        (
            'A="x\ny"\nB=\'x\ny\'\nC="x\ny"',
            {'A': '"x\ny"', 'B': "'x\ny'", 'C': '"x\ny"'},
        ),
        # Single quotes are literal, so a trailing backslash is just text:
        (
            _text(r"KEY='a\'", 'OTHER=1'),
            {'KEY': r"'a\'", 'OTHER': '1'},
        ),
        # A statement after a multiline value is a separate key:
        (
            'KEY="line1\nline2\nline3"\nOTHER=1',
            {'KEY': '"line1\nline2\nline3"', 'OTHER': '1'},
        ),
    ],
)
def test_multiline_nested_quotes(code, expected):
    """Quotes of both kinds and escapes stay inside quoted values."""
    assert _pairs(code) == expected


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_escaped_line_break_and_tab_stay_in_value():
    r"""``\n`` and ``\t`` written as text are not a line break or a tab."""
    code = _text(
        r'DOUBLE="a\nb\tc"',
        r"SINGLE='a\nb\tc'",
        r'PLAIN=a\nb\tc',
        r'MIXED="x\ny',
        r'z\tw"',
        'OTHER=1',
    )

    module = DotenvParser().parse(code)

    assert _pairs(code) == {
        'DOUBLE': r'"a\nb\tc"',
        'SINGLE': r"'a\nb\tc'",
        'PLAIN': r'a\nb\tc',
        'MIXED': _text(r'"x\ny', r'z\tw"'),
        'OTHER': '1',
    }
    # Only the real line break inside ``MIXED`` moves the line counter:
    assert [assign.lineno for assign in module.body] == [1, 2, 3, 4, 6]


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
@pytest.mark.parametrize(
    ('code', 'expected'),
    [
        ('KEY="unclosed\nOTHER=1', {'KEY': '"unclosed', 'OTHER': '1'}),
        ("KEY='unclosed\nOTHER=1", {'KEY': "'unclosed", 'OTHER': '1'}),
        ('KEY=ab"c\nOTHER=1', {'KEY': 'ab"c', 'OTHER': '1'}),
        ('KEY=value\nOTHER=1', {'KEY': 'value', 'OTHER': '1'}),
        ('KEY="1"\nOTHER="2"', {'KEY': '"1"', 'OTHER': '"2"'}),
    ],
)
def test_unclosed_quote_ends_at_line_break(code, expected):
    """Values that do not close their quote keep ending at the line break."""
    assert _pairs(code) == expected
