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

from collections.abc import Sequence
from typing import TypeVar, final

from attr import dataclass, field
from ply import lex

from dotenv_linter.logics.text import normalize_text

TNode = TypeVar('TNode', bound='Node')
TAssign = TypeVar('TAssign', bound='Assign')


@dataclass(frozen=True, slots=True)
class Node:
    """
    Base class for all other nodes.

    Defines base fields that all other nodes have.
    """

    lineno: int
    raw_text: str
    text: str = field(init=False)

    def __attrs_post_init__(self) -> None:
        """Used to tweak instance internals after initialization."""
        object.__setattr__(  # noqa: WPS609
            self,
            'text',
            normalize_text(self.raw_text),
        )

    @classmethod
    def from_token(cls: type[TNode], token: lex.LexToken) -> TNode:
        """Creates instance from parser's token."""
        return cls(
            lineno=token.lineno,
            raw_text=token.value,
        )


@final
@dataclass(frozen=True)
class Comment(Node):
    """
    Represent a single line comment message.

    Is not derived from Statement, since it has no effect by design.
    """


@final
@dataclass(frozen=True)
class Name(Node):
    """Represents an inline name which is used as a key for future values."""


@final  # noqa: WPS110
@dataclass(frozen=True)
class Value(Node):  # noqa: WPS110
    """Represents an inline value which is used together with key."""


@dataclass(frozen=True)
class Statement(Node):
    """Base class for all affecting statements."""


@final
@dataclass(frozen=True, slots=True)
class Assign(Statement):
    """Represents key-value pair separated by ``=``."""

    left: Name
    right: Value | None

    @classmethod
    def from_token(
        cls: type[TAssign],
        name_token: lex.LexToken,
        equal_token: lex.LexToken = None,
        value_token: lex.LexToken = None,
    ) -> TAssign:
        """Creates instance from parser's token."""
        if equal_token is None:
            raise ValueError('Empty EQUAL node is not allowed')

        if value_token is None:
            value_item = None
        else:
            value_item = Value.from_token(value_token)

        return cls(
            left=Name.from_token(name_token),
            right=value_item,
            lineno=name_token.lineno,
            raw_text=equal_token.value,
        )


@dataclass(frozen=True, slots=True)
class Module(Node):
    """Wrapper node that represents a single file with or without contents."""

    body: Sequence[Comment | Statement | Name]
