# -*- coding: utf-8 -*-

"""
Full BNF grammar for this language can be specified as:

.. code:: text

    expression : NAME EQUAL VALUE
            | COMMENT

This module generates ``parser.out`` and ``parsetab.py`` when first invoked.
Do not touch these files, unless you know what you are doing.

See also:
    https://www.dabeaz.com/ply/ply.html#ply_nn11

"""

from typing import NoReturn

from ply import lex, yacc

from dotenv_linter.exceptions import ParsingError
from dotenv_linter.grammar.fst import Assign, Comment, Name, Value
from dotenv_linter.grammar.lexer import DotenvLexer


def _get_token(parsed: yacc.YaccProduction, index: int) -> lex.LexToken:
    """YaccProduction has a broken __getitem__ method definition."""
    return getattr(parsed, 'slice')[index]


def _calc_value_offset(
    name_token: lex.LexToken,
    assign_token: lex.LexToken,
) -> int:
    name_length = name_token.col_offset + len(name_token.value)
    return name_length + len(assign_token.value)


class DotenvParser(object):
    """
    Custom parser wrapper, grouping methods and attrs together.

    Methods starting with ``p_`` uses BNF grammar to be correctly
    collected by ``ply.yacc`` module. Do not change them.
    """

    def __init__(self, **kwarg) -> None:
        """Creates inner parser instance."""
        self.lexer = DotenvLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, **kwarg)

    def parse(self, to_parse: str, **kwargs) -> yacc.YaccProduction:
        """Parses input string to FST."""
        # TODO: use `Module` to wrap this result
        return self.parser.parse(to_parse, lexer=self.lexer.lexer, **kwargs)

    def p_expression_equals(self, parsed: yacc.YaccProduction) -> None:
        """expression : NAME EQUAL VALUE"""
        name_token = _get_token(parsed, 1)
        assign_token = _get_token(parsed, 2)
        value_token = _get_token(parsed, 3)

        left = Name(
            lineno=name_token.lineno,
            col_offset=name_token.col_offset,
            raw_text=name_token.value,
        )
        # TODO: handle when value is not provided: KEY=
        # TODO: handle when `EQUALS` is not provided: KEY
        right = Value(
            lineno=value_token.lineno,
            col_offset=_calc_value_offset(name_token, assign_token),
            raw_text=value_token.value,
        )
        parsed[0] = Assign(
            left=left,
            right=right,
            lineno=name_token.lineno,
            col_offset=name_token.col_offset,
            raw_text=assign_token.value,
        )

    def p_expression_comment(self, parsed: yacc.YaccProduction) -> None:
        """expression : COMMENT"""
        token = _get_token(parsed, 1)
        parsed[0] = Comment(
            lineno=token.lineno,
            col_offset=token.col_offset,
            raw_text=token.value,
        )

    def p_error(self, parsed: yacc.YaccProduction) -> NoReturn:
        """Raising errors on syntax errors."""
        raise ParsingError(parsed)


if __name__ == '__main__':
    # TODO: remove
    parser = DotenvParser()

    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)
