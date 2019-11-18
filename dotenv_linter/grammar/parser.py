# -*- coding: utf-8 -*-

"""
Full BNF grammar for this language can be specified as:

.. code:: text

    body :
         | body line

    line : assign
         | name
         | comment

    assign : NAME EQUAL
           | NAME EQUAL VALUE

    name : NAME
    comment : COMMENT

This module generates ``parser.out`` and ``parsetab.py`` when first invoked.
Do not touch these files, unless you know what you are doing.

See also:
    https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form
    https://www.dabeaz.com/ply/ply.html#ply_nn11

"""

from typing import List, NoReturn, Optional, Union

from ply import lex, yacc
from typing_extensions import final

from dotenv_linter.exceptions import ParsingError
from dotenv_linter.grammar.fst import Assign, Comment, Module, Name, Statement
from dotenv_linter.grammar.lexer import DotenvLexer


def _get_token(
    parsed: yacc.YaccProduction,
    index: int,
) -> Optional[lex.LexToken]:  # TODO: lex.LexToken is in fact just `Any`
    """YaccProduction has a broken __getitem__ method definition."""
    return parsed.slice[index]


@final
class DotenvParser(object):
    """
    Custom parser wrapper, grouping methods and attrs together.

    Methods starting with ``p_`` uses BNF grammar to be correctly
    collected by ``ply.yacc`` module. Do not change them.
    """

    tokens = DotenvLexer.tokens

    def __init__(self, **kwarg) -> None:
        """Creates inner parser instance."""
        self._lexer = DotenvLexer()
        self._parser = yacc.yacc(module=self, **kwarg)  # should be last

    def parse(self, to_parse: str, **kwargs) -> Module:
        """Parses input string to FST."""
        self._body_items: List[Union[Comment, Statement]] = []
        self._parser.parse(input=to_parse, lexer=self._lexer, **kwargs)
        return Module(lineno=0, raw_text=to_parse, body=self._body_items)

    def p_body(self, parsed: yacc.YaccProduction) -> None:
        """
        body :
             | body line
        """
        if len(parsed) == 3 and parsed[2] is not None:
            self._body_items.append(parsed[2])
            parsed[0] = parsed[2]

    def p_line(self, parsed: yacc.YaccProduction) -> None:
        """
        line : assign
             | name
             | comment
        """
        parsed[0] = parsed[1]

    def p_assign(self, parsed: yacc.YaccProduction) -> None:
        """
        assign : NAME EQUAL
               | NAME EQUAL VALUE
        """
        value_token = _get_token(parsed, 3) if len(parsed) == 4 else None
        parsed[0] = Assign.from_token(
            name_token=_get_token(parsed, 1),
            equal_token=_get_token(parsed, 2),
            value_token=value_token,
        )

    def p_name(self, parsed: yacc.YaccProduction) -> None:
        """name : NAME"""
        parsed[0] = Name.from_token(_get_token(parsed, 1))

    def p_comment(self, parsed: yacc.YaccProduction) -> None:
        """comment : COMMENT"""
        parsed[0] = Comment.from_token(_get_token(parsed, 1))

    def p_error(self, parsed: yacc.YaccProduction) -> NoReturn:
        """Raising exceptions on syntax errors."""
        raise ParsingError(parsed)
