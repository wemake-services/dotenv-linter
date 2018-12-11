# -*- coding: utf-8 -*-

import re
from typing import ClassVar, List
from typing.re import Pattern

from typing_extensions import final

from dotenv_linter.grammar.fst import Assign, Module, Name
from dotenv_linter.violations.names import (
    DuplicateNameViolation,
    IncorrectNameViolation,
    RawNameViolation,
    SpacedNameViolation,
)
from dotenv_linter.visitors.base import BaseFSTVisitor


@final
class NameInModuleVisitor(BaseFSTVisitor):
    """Finds wrong names in dotenv modules."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a list of all names in a file."""
        super().__init__(*args, **kwargs)
        self._names: List[Name] = []

    def visit_module(self, node: Module) -> None:
        """
        Visits module to find raw names.

        Raises:
            RawNameViolation
            DuplicateNameViolation

        """
        self._check_raw_name(node)
        self._save_names(node)
        self.generic_visit(node)

    def _post_visit(self) -> None:
        text_names = [name_node.text for name_node in self._names]
        for name_node in self._names:
            if text_names.count(name_node.text) > 1:
                self._add_violation(
                    DuplicateNameViolation(name_node, text=name_node.text),
                )

    def _check_raw_name(self, node: Module) -> None:
        for sub_node in node.body:
            if isinstance(sub_node, Name):
                self._add_violation(
                    RawNameViolation(sub_node, text=sub_node.text),
                )

    def _save_names(self, node: Module) -> None:
        for sub_node in node.body:
            if isinstance(sub_node, Name):
                self._names.append(sub_node)
            elif isinstance(sub_node, Assign):
                self._names.append(sub_node.left)


@final
class NameVisitor(BaseFSTVisitor):
    """Finds wrong names."""

    _correct_name: ClassVar[Pattern] = re.compile(r'[A-Z_]+[A-Z0-9_]*')

    def visit_name(self, node: Name) -> None:
        """
        Checks how names are defined.

        Raises:
            SpacedNameViolation
            IncorrectNameViolation

        """
        self._check_name_correctness(node)
        self._check_name_spaces(node)
        self.generic_visit(node)

    def _check_name_correctness(self, node: Name) -> None:
        if not self._correct_name.fullmatch(node.text):
            self._add_violation(IncorrectNameViolation(node, text=node.text))

    def _check_name_spaces(self, node: Name) -> None:
        if node.raw_text.startswith(' '):
            self._add_violation(SpacedNameViolation(node, text=node.text))
