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
from typing import List, Optional, Union

from ply import yacc

from dotenv_linter.logics.text import normalize_text
from dotenv_linter.types import ProducedToken


# TODO: document classes hieracy in module docstring
# TODO: use slots, make frozen

@dataclass
class Node(object):
    """
    Base class for all other nodes.

    Defines base fields that all other nodes have.
    """

    lineno: int
    col_offset: int
    raw_text: str

    def __post_init__(self) -> None:
        """Used to tweak instance internals after initialization."""
        self.text = normalize_text(self.raw_text)

    @classmethod
    def from_token(cls, token: ProducedToken):
        """Creates instance from parser's token."""
        raise NotImplementedError()


@dataclass
class Comment(Node):
    """
    Represent a single line comment message.

    Is not derived from Statement, since it has no effect by design.
    """

    @classmethod
    def from_token(cls, token: ProducedToken) -> 'Comment':
        """Creates instance from parser's token."""
        return Comment(
            lineno=token.lineno,
            col_offset=token.col_offset,
            raw_text=token.value,
        )


@dataclass
class Name(Node):
    """Represents an inline name which is used as a key for future values."""

    @classmethod
    def from_token(cls, token: ProducedToken) -> 'Name':
        """Creates instance from parser's token."""
        return cls(
            lineno=token.lineno,
            col_offset=token.col_offset,
            raw_text=token.value,
        )


@dataclass
class Value(Node):
    """Represents an inline value which is used together with key."""

    @classmethod
    def from_token(cls, token: ProducedToken) -> 'Value':
        """Creates instance from parser's token."""
        return cls(
            lineno=token.lineno,
            col_offset=token.col_offset,
            raw_text=token.value,
        )


@dataclass
class Statement(Node):
    """Base class for all affecting statements."""


@dataclass
class Assign(Statement):
    """Represents key-value pair separated by ``=``."""

    left: Name
    right: Optional[Value] = None

    @classmethod
    def from_token(
        cls,
        token: ProducedToken,
        equal: ProducedToken = None,
        value: ProducedToken = None,
    ) -> 'Assign':
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


@dataclass
class Module(Node):
    """Wrapper node that represents a single file with or without contents."""

    body: List[Union[Comment, Statement]] = field(default=list)
