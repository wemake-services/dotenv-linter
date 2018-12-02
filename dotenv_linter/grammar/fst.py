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

"""

from dataclasses import dataclass, field
from typing import Union, List


def normalize_text(text: str) -> str:
    """Removes trailing and leading spaces and quotes."""
    return text.strip().strip('\'"')

# TODO: doc class hieracy

@dataclass
class Node(object):
    lineno: int
    col_offset: int
    raw_text: str

    def __post_init__(self) -> None:
        self.text = normalize_text(self.raw_text)


@dataclass
class Comment(Node):
    pass


@dataclass
class Name(Node):
    pass


@dataclass
class Value(Node):
    pass


@dataclass
class Statement(Node):
    pass

@dataclass
class Assign(Statement):
    left: Name
    right: Value


@dataclass
class Module(Node):
    body: List[Union[Comment, Statement]] = field(default=list)
