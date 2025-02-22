from __future__ import annotations

from typing_extensions import final

from dotenv_linter.grammar.fst import Node


class BaseViolation:
    """Base class for all violations."""

    code: int
    error_template: str

    def __init__(self, node: Node | None, text: str | None) -> None:
        """Creates instance of any violation."""
        self._node = node
        self._text = text

    @final
    def as_line(self) -> str:
        """Converts violation to a single line information."""
        violation = self.error_template.format(self._text)
        return f'{self.location()} {self._formated_code()} {violation}'

    def location(self) -> int:
        """Returns in-file location of a violation."""
        raise NotImplementedError('Should be redefined in a subclass')

    @final
    def _formated_code(self) -> str:
        return str(self.code).zfill(3)


class BaseFSTViolation(BaseViolation):
    """Base class for all ``fst`` violations."""

    _node: Node
    _text: str

    def __init__(self, node: Node, text: str) -> None:  # noqa: WPS612
        """Creates instance of fst-based violation."""
        super().__init__(node, text)

    @final
    def location(self) -> int:
        """Returns in-file location of a violation."""
        return self._node.lineno


class BaseFileViolation(BaseViolation):
    """Base class for all violations that operate on whole files."""

    def __init__(  # noqa: WPS612
        self,
        node: None = None,
        text: None = None,
    ) -> None:
        """Creates instance of file-based violation."""
        super().__init__(node, text)

    @final
    def location(self) -> int:
        """Returns in-file location of a violation."""
        return 0
