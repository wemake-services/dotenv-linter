# -*- coding: utf-8 -*-

"""
Full BNF grammar for this language can be specified as:

.. code:: text

    expression : NAME EQUAL VALUE
            | COMMENT

See also:
    https://www.dabeaz.com/ply/ply.html#ply_nn11

"""

from ply import lex, yacc

from dotenv_linter.exceptions import ParsingError
from dotenv_linter.grammar.fst import Assign, Comment, Name, Value
from dotenv_linter.grammar.lexer import DotenvLexer

tokens = DotenvLexer.tokens


def _get_token(parsed, index: int) -> lex.LexToken:
    return getattr(parsed, 'slice')[index]


def _calc_value_offset(
    name_token: lex.LexToken,
    assign_token: lex.LexToken,
) -> int:
    name_length = name_token.col_offset + len(name_token.value)
    return name_length + len(assign_token.value)


def p_expression_equals(parsed):
    'expression : NAME EQUAL VALUE'
    name_token = _get_token(parsed, 1)
    assign_token = _get_token(parsed, 2)
    value_token = _get_token(parsed, 3)

    left = Name(
        lineno=name_token.lineno,
        col_offset=name_token.col_offset,
        raw_text=name_token.value,
    )
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


def p_expression_comment(parsed):
    'expression : COMMENT'
    token = _get_token(parsed, 1)
    parsed[0] = Comment(
        lineno=token.lineno,
        col_offset=token.col_offset,
        raw_text=token.value,
    )


def p_error(p):
    raise ParsingError(p)


# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)
