# -*- coding: utf-8 -*-

"""
Full BNF grammar for this language can be specified as:

.. code:: text

    expression : NAME
               | NAME EQUAL
               | NAME EQUAL VALUE
               | COMMENT
               | expression

This module generates ``parser.out`` and ``parsetab.py`` when first invoked.
Do not touch these files, unless you know what you are doing.

See also:
    https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form
    https://www.dabeaz.com/ply/ply.html#ply_nn11

"""

from typing import NoReturn, Union

from ply import lex, yacc

from dotenv_linter.exceptions import ParsingError
from dotenv_linter.grammar.fst import Assign, Comment, Name, Module, Value
from dotenv_linter.grammar.lexer import DotenvLexer


def _get_token(
    parsed: yacc.YaccProduction,
    index: int,
):  # TODO: Optional Union[lex.LexToken, yacc.YaccSymbol]
    """YaccProduction has a broken __getitem__ method definition."""
    return getattr(parsed, 'slice')[index]


class DotenvParser(object):
    """
    Custom parser wrapper, grouping methods and attrs together.

    Methods starting with ``p_`` uses BNF grammar to be correctly
    collected by ``ply.yacc`` module. Do not change them.
    """

    # start = 'expression'

    def __init__(self, **kwarg) -> None:
        """Creates inner parser instance."""
        self.lexer = DotenvLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, **kwarg)

    def parse(self, to_parse: str, **kwargs) -> Module:
        """Parses input string to FST."""
        return self.parser.parse(
            input=to_parse, lexer=self.lexer, **kwargs,
        )

    def p_body(self, p):
        """
        body :
             | body line
        """
        print('body', getattr(p, 'slice'))

    def p_line(self, parsed):
        """
        line : assign
             | name
             | comment
        """
        print('line', getattr(parsed, 'slice'))

    def p_assign(self, parsed):
        """
        assign : NAME EQUAL
               | NAME EQUAL VALUE
        """
        print('assign', getattr(parsed, 'slice'))

    def p_name(self, parsed):
        """name : NAME"""
        print('name', getattr(parsed, 'slice'))

    def p_comment(self, parsed):
        """comment : COMMENT"""
        print('com', getattr(parsed, 'slice'))

    def p_error(self, parsed: yacc.YaccProduction) -> NoReturn:
        """Raising errors on syntax errors."""
        print('error', parsed)
        raise ParsingError(parsed)


if __name__ == '__main__':
    # TODO: remove
    parser = DotenvParser()

    data = '''
# test
first
val =
# end
sec = 3
'''
    result = parser.parse(data)
    print(result)
