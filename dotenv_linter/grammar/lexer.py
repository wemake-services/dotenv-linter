"""
Lexer definition.

See also:
    https://www.dabeaz.com/ply/ply.html#ply_nn3

"""

from collections.abc import Callable
from typing import Any, ClassVar, TypeAlias, TypeVar, final

from ply import lex

from dotenv_linter.exceptions import ParsingError

_LexerState: TypeAlias = tuple[str, str]

_CallableT = TypeVar('_CallableT', bound=Callable[..., Any])


def _token(re_string: str) -> Callable[[_CallableT], _CallableT]:
    return lex.TOKEN(re_string)  # type: ignore[no-any-return]


@final
class DotenvLexer:  # noqa: WPS214
    """Custom lexer wrapper, grouping methods and attrs together."""

    tokens: ClassVar[tuple[str, ...]] = (
        'WHITESPACE',
        'COMMENT',
        'NAME',
        'EQUAL',
        'VALUE',
    )

    states: ClassVar[tuple[_LexerState, ...]] = (
        ('name', 'exclusive'),  # we have found Name definition
        ('value', 'exclusive'),  # we have found Equal definition
    )

    re_whitespaces: ClassVar[str] = r'[ \t\v\f\u00A0]'

    def __init__(self, **kwargs: Any) -> None:
        """Creates inner lexer."""
        self._lexer = lex.lex(module=self, **kwargs)
        self.reset()

    def reset(self) -> 'DotenvLexer':
        """
        Resets lexers inner state.

        Is done between two separate lexing operations.
        Should not be called directly, since it is a part of ``ply`` API.
        """
        self._lexer.lineno = 1
        self._lexer.begin('INITIAL')
        return self

    def input(self, text: str) -> 'DotenvLexer':
        """
        Passes input to the lexer.

        It is done once per lexing operation.
        Should not be called directly, since it is a part of ``ply`` API.
        """
        self.reset()
        self._lexer.input(text)
        return self

    def token(self) -> lex.LexToken:
        """
        Returns the next token to work with.

        Should not be called directly, since it is a part of ``ply`` API.
        """
        return self._lexer.token()

    @_token(re_whitespaces + r'*[\w-]+')
    def t_NAME(self, token: lex.LexToken) -> lex.LexToken:
        """Parsing NAME tokens."""
        token.lexer.push_state('name')
        return token

    @_token(re_whitespaces + r'*\#.*')
    def t_COMMENT(self, token: lex.LexToken) -> lex.LexToken:
        """Parsing COMMENT tokens."""
        return token

    @_token(re_whitespaces + '*=')
    def t_name_EQUAL(self, token: lex.LexToken) -> lex.LexToken:
        """Parsing EQUAL tokens."""
        token.lexer.push_state('value')
        return token

    @_token('.+')
    def t_value_VALUE(self, token: lex.LexToken) -> lex.LexToken:
        """Parsing VALUE tokens."""
        token.lexer.pop_state()
        return token

    @_token(r'[\n\r\u2028\u2029]')
    def t_ANY_newline(self, token: lex.LexToken) -> None:
        """
        Defines a rule so we can track line numbers.

        These tokens are skipped.
        """
        token.lexer.lineno += len(token.value)
        token.lexer.begin('INITIAL')

    def t_ANY_error(self, token: lex.LexToken) -> None:
        """
        Error handling rule.

        Raises an exception that file can not be parsed.
        """
        raise ParsingError(token.value)
