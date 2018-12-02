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
from typing import Union, List, Optional


def _normalize_text(text: str) -> str:
    """Removes trailing and leading spaces and quotes."""
    return text.strip().strip('\'"')

# TODO: document classes hieracy in module docstring

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
        self.text = _normalize_text(self.raw_text)


@dataclass
class Comment(Node):
    """
    Represent a single line comment message.

    Is not derived from Statement, since it has no effect by design.
    """


@dataclass
class Name(Node):
    """Represents an inline name which is used as a key for future values."""


@dataclass
class Value(Node):
    """Represents an inline value which is used together with key."""


@dataclass
class Statement(Node):
    """Base class for all affecting statements.""""


@dataclass
class Assign(Statement):
    """Represents key-value pair separated by ``=``."""

    left: Name
    right: Optional[Value] = None


@dataclass
class Module(Node):
    """Wrapper node that represents a single file with or without contents."""

    body: List[Union[Comment, Statement]] = field(default=list)
