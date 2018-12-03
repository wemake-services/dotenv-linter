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

from typing import NoReturn, Union, Optional

from ply import lex, yacc

from dotenv_linter.exceptions import ParsingError
from dotenv_linter.grammar.fst import Assign, Comment, Name, Module, Value
from dotenv_linter.grammar.lexer import DotenvLexer
from dotenv_linter.types import ProducedToken


def _get_token(
    parsed: yacc.YaccProduction,
    index: int,
) -> ProducedToken:
    """YaccProduction has a broken __getitem__ method definition."""
    return getattr(parsed, 'slice')[index]


class DotenvParser(object):
    """
    Custom parser wrapper, grouping methods and attrs together.

    Methods starting with ``p_`` uses BNF grammar to be correctly
    collected by ``ply.yacc`` module. Do not change them.
    """

    def __init__(self, **kwarg) -> None:
        """Creates inner parser instance."""
        self._lexer = DotenvLexer()
        self.tokens = self._lexer.tokens  # API requirement
        self._parser = yacc.yacc(module=self, **kwarg)
        self._body_items = []

    def parse(self, to_parse: str, **kwargs) -> Module:
        """Parses input string to FST."""
        self._parser.parse(
            input=to_parse, lexer=self._lexer, **kwargs,
        )

        return Module(
            lineno=0, col_offset=0, raw_text=to_parse, body=self._body_items,
        )

    def p_body(self, parsed):
        """
        body :
             | body line
        """
        if len(parsed) == 3:
            parsed[0] = parsed[2]
            self._body_items.append(parsed[0])

    def p_line(self, parsed):
        """
        line : assign
             | name
             | comment
        """
        parsed[0] = parsed[1]

    def p_assign(self, parsed):
        """
        assign : NAME EQUAL
               | NAME EQUAL VALUE
        """
        value_token = _get_token(parsed, 3) if len(parsed) == 4 else None
        parsed[0] = Assign.from_token(
            token=_get_token(parsed, 1),
            equal=_get_token(parsed, 2),
            value=value_token,
        )

    def p_name(self, parsed):
        """name : NAME"""
        parsed[0] = Name.from_token(_get_token(parsed, 1))

    def p_comment(self, parsed):
        """comment : COMMENT"""
        parsed[0] = Comment.from_token(_get_token(parsed, 1))

    def p_error(self, parsed: yacc.YaccProduction) -> NoReturn:
        """Raising errors on syntax errors."""
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
