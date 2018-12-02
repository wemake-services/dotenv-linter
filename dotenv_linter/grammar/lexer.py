# -*- coding: utf-8 -*-

"""
Lexer definition.

See also:
    https://www.dabeaz.com/ply/ply.html#ply_nn3

"""

from ply import lex

from dotenv_linter.exceptions import ParsingError


def _get_offset(token: lex.LexToken) -> int:
    offset = getattr(token.lexer, 'col_offset', 0)
    token.lexer.col_offset = 0
    return offset


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

    def __init__(self, **kwargs) -> None:
        """Creates inner lexer."""
        self._lexer = lex.lex(module=self, **kwargs)
        self._text = ''
        self.reset()

    def reset(self) -> 'DotenvLexer':
        self._text = ''
        self._lexer.lineno = 1
        self._lexer.begin('INITIAL')
        return self

    def input(self, text: str) -> 'DotenvLexer':
        self.reset()
        self._text = text
        self._lexer.input(text)
        return self

    def token(self) -> lex.LexToken:
        return self._lexer.token()

    @lex.TOKEN(r'[ \t\v\f\u00A0]')
    def t_WHITESPACE(self, token: lex.LexToken) -> None:
        try:
            token.lexer.col_offset += 1
        except AttributeError:
            token.lexer.col_offset = 1

    @lex.TOKEN(r'\w+')
    def t_NAME(self, token: lex.LexToken) -> lex.LexToken:
        token.col_offset = _get_offset(token)
        return token

    @lex.TOKEN(r'\#.+')
    def t_COMMENT(self, token: lex.LexToken) -> lex.LexToken:
        token.col_offset = _get_offset(token)
        return token

    @lex.TOKEN(r'=')
    def t_EQUAL(self, token: lex.LexToken) -> lex.LexToken:
        token.col_offset = _get_offset(token)
        token.lexer.push_state('value')
        return token

    @lex.TOKEN(r'.+')
    def t_value_VALUE(self, token: lex.LexToken) -> lex.LexToken:
        token.col_offset = _get_offset(token)
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
        raise ParsingError(token.value[0])


if __name__ == '__main__':
    # TODO: remove
    data = '''
    # Comment line
    KEY=1#=a
    NAME = 1 2 3
    D=
    D=
    '''

    lexer = DotenvLexer()
    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok, tok.col_offset)
