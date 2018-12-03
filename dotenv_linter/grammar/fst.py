# -*- coding: utf-8 -*-

"""
Here we define nodes for our full syntax tree.

What is full syntax tree?
It is a code representation which always obeys this law:
``to_string(fst(code)) == code``

It is different from abstract syntax tree only in one thing:
it does not loose any relevant details such as:

- comments
- whitespaces
- line breaks

See also:
    https://en.wikipedia.org/wiki/Abstract_syntax_tree

"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, TypeVar, Type

from ply import lex

from dotenv_linter.logics.text import normalize_text

TNode = TypeVar('TNode', bound='Node')
TAssign = TypeVar('TAssign', bound='Assign')


@dataclass(frozen=True)
class Node(object):
    """
    Base class for all other nodes.

    Defines base fields that all other nodes have.
    """

    __slots__ = {'lineno', 'col_offset', 'raw_text', 'text'}

    lineno: int
    col_offset: int
    raw_text: str

    def __post_init__(self) -> None:
        """Used to tweak instance internals after initialization."""
        object.__setattr__(self, 'text', normalize_text(self.raw_text))

    @classmethod
    def from_token(cls: Type[TNode], token: lex.LexToken) -> TNode:
        """Creates instance from parser's token."""
        return cls(
            lineno=token.lineno,
            col_offset=token.col_offset,
            raw_text=token.value,
        )


@dataclass(frozen=True)
class Comment(Node):
    """
    Represent a single line comment message.

    Is not derived from Statement, since it has no effect by design.
    """


@dataclass(frozen=True)
class Name(Node):
    """Represents an inline name which is used as a key for future values."""


@dataclass(frozen=True)
class Value(Node):
    """Represents an inline value which is used together with key."""


@dataclass(frozen=True)
class Statement(Node):
    """Base class for all affecting statements."""


@dataclass(frozen=True)
class Assign(Statement):
    """Represents key-value pair separated by ``=``."""

    __slots__ = {'lineno', 'col_offset', 'raw_text', 'text', 'left', 'right'}

    left: Name
    right: Optional[Value]

    @classmethod
    def from_token(
        cls: Type[TAssign],
        token: lex.LexToken,
        equal: lex.LexToken = None,
        value: lex.LexToken = None,
    ) -> TAssign:
        """Creates instance from parser's token."""
        if equal is None:
            raise ValueError('Empty EQUAL node is not allowed')

        value_item = Value.from_token(value) if value is not None else None
        return cls(
            left=Name.from_token(token),
            right=value_item,
            lineno=token.lineno,
            col_offset=token.col_offset,
            raw_text=equal.value,
        )


@dataclass(frozen=True)
class Module(Node):
    """Wrapper node that represents a single file with or without contents."""

    __slots__ = {'lineno', 'col_offset', 'raw_text', 'text', 'body'}

    body: List[Union[Comment, Statement]]
