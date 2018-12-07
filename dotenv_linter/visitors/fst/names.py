# -*- coding: utf-8 -*-

from dotenv_linter.grammar.fst import Module, Name
from dotenv_linter.visitors.base import BaseFSTVisitor


class NameVisitor(BaseFSTVisitor):
    def visit_module(self, node: Module) -> None:
        """Visits module to find raw names."""

    def _check_raw_name(self, node: Module) -> None:
        for sub_node in node.body:
            if isinstance(sub_node, Name):
                self.add_violation()
