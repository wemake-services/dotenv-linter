# -*- coding: utf-8 -*-

"""
Lexer definition.

See also:
    https://www.dabeaz.com/ply/ply.html#ply_nn3

"""

from ply import lex
from typing_extensions import final

from dotenv_linter.exceptions import ParsingError


def _get_offset(token: lex.LexToken) -> int:
    """Returns and resets offset for the current lexer."""
    offset = getattr(token.lexer, 'col_offset', 1)  # TODO: fix offsets
    token.lexer.col_offset = 1
    return offset



@final
class DotenvLexer(object):
    """Custom lexer wrapper, grouping methods and attrs together."""

    tokens = (
        'WHITESPACE',
        'COMMENT',
        'NAME',
        'EQUAL',
        'VALUE',
    )

    states = (
        ('value', 'exclusive'),
    )

    re_whitespaces = r'[ \t\v\f\u00A0]'

    def __init__(self, **kwargs) -> None:
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

    @lex.TOKEN(re_whitespaces + r'*[\w-]+')
    def t_NAME(self, token: lex.LexToken) -> lex.LexToken:
        """Parsing NAME tokens."""
        token.col_offset = _get_offset(token) # TODO: decorator
        return token

    @lex.TOKEN(re_whitespaces + r'*\#.+')
    def t_COMMENT(self, token: lex.LexToken) -> lex.LexToken:
        """Parsing COMMENT tokens."""
        token.col_offset = _get_offset(token)  # TODO: decorator
        return token

    @lex.TOKEN(re_whitespaces + r'*=')
    def t_EQUAL(self, token: lex.LexToken) -> lex.LexToken:
        """Parsing EQUAL tokens."""
        token.col_offset = _get_offset(token)  # TODO: decorator
        token.lexer.push_state('value')
        return token

    @lex.TOKEN(r'.+')
    def t_value_VALUE(self, token: lex.LexToken) -> lex.LexToken:
        """Parsing VALUE tokens."""
        token.col_offset = _get_offset(token)  # TODO: decorator
        token.lexer.pop_state()
        return token

    @lex.TOKEN(r'[\n\r\u2028\u2029]')
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
