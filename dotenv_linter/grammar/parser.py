# -*- coding: utf-8 -*-

"""
Full BNF grammar for this language can be specified as:

.. code:: text

    expression : NAME EQUAL VALUE
               | NAME EQUAL
               | NAME
               | COMMENT
               | expression

This module generates ``parser.out`` and ``parsetab.py`` when first invoked.
Do not touch these files, unless you know what you are doing.

See also:
    https://www.dabeaz.com/ply/ply.html#ply_nn11

"""

from typing import NoReturn, Optional

from ply import lex, yacc

from dotenv_linter.exceptions import ParsingError
from dotenv_linter.grammar.fst import Assign, Comment, Name, Module, Value
from dotenv_linter.grammar.lexer import DotenvLexer


def _get_token(
    parsed: yacc.YaccProduction,
    index: int,
) -> Optional[lex.LexToken]:
    """YaccProduction has a broken __getitem__ method definition."""
    try:
        return getattr(parsed, 'slice')[index]
    except IndexError:
        return None


def _calc_value_offset(
    name_token: lex.LexToken,
    assign_token: lex.LexToken,
) -> int:
    name_length = name_token.col_offset + len(name_token.value)
    return name_length + len(assign_token.value)


class _AssignParse(object):
    def __init__(self, parsed: yacc.YaccProduction) -> None:
        self._parsed = parsed

    def parse_assign(self) -> None:
        name_token = _get_token(self._parsed, 1)
        assign_token = _get_token(self._parsed, 2)
        value_token = _get_token(self._parsed, 3)

        if value_token is not None and assign_token is not None:
            parsed = self._parse_assign(name_token, assign_token, value_token)
        elif assign_token is not None:
            parsed = self._parse_empty_assign(name_token, assign_token)
        else:
            parsed = self._parse_only_name(name_token)
        print(vars(self._parsed))
        self._parsed[0] = parsed

    def _parse_only_name(self, name_token: lex.LexToken) -> Name:
        return Name(
            lineno=name_token.lineno,
            col_offset=name_token.col_offset,
            raw_text=name_token.value,
        )

    def _parse_empty_assign(
        self,
        name_token: lex.LexToken,
        assign_token: lex.LexToken,
    ) -> Assign:
        left = Name(
            lineno=name_token.lineno,
            col_offset=name_token.col_offset,
            raw_text=name_token.value,
        )
        return Assign(
            left=left,
            right=None,
            lineno=name_token.lineno,
            col_offset=name_token.col_offset,
            raw_text=assign_token.value,
        )

    def _parse_assign(
        self,
        name_token: lex.LexToken,
        assign_token: lex.LexToken,
        value_token: lex.LexToken,
    ) -> Assign:
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
        return Assign(
            left=left,
            right=right,
            lineno=name_token.lineno,
            col_offset=name_token.col_offset,
            raw_text=assign_token.value,
        )


class DotenvParser(object):
    """
    Custom parser wrapper, grouping methods and attrs together.

    Methods starting with ``p_`` uses BNF grammar to be correctly
    collected by ``ply.yacc`` module. Do not change them.
    """

    start = 'expression'

    def __init__(self, **kwarg) -> None:
        """Creates inner parser instance."""
        self.lexer = DotenvLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, debug=True, **kwarg)

    def parse(self, to_parse: str, **kwargs) -> Module:
        """Parses input string to FST."""
        # TODO: use `Module` to wrap this result
        return self.parser.parse(input=to_parse, debug=True, lexer=self.lexer, **kwargs)

    def p_expression_full(self, parsed: yacc.YaccProduction) -> None:
        """
        expression : NAME
                   | NAME EQUAL
                   | NAME EQUAL VALUE
        """
        _AssignParse(parsed).parse_assign()

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
        raise ParsingError(parsed.value)


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
