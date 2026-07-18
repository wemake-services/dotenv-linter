from __future__ import annotations

from typing import ClassVar, TypeAlias, final

from dotenv_linter.grammar.fst import Module
from dotenv_linter.logics.report import Report
from dotenv_linter.violations.parsing import ParsingViolation
from dotenv_linter.visitors.base import BaseFSTVisitor
from dotenv_linter.visitors.fst import (
    assigns,
    comments,
    metadata,
    names,
    values,
)

_VisitorTypes: TypeAlias = tuple[type[BaseFSTVisitor], ...]


@final
class ReportCollector:
    """
    Run all FST visitors.

    Run all visitors against a module,
    filter out ignored violations, and produce a ``Report``.
    """

    _visitors_pipeline: ClassVar[_VisitorTypes] = (
        assigns.AssignVisitor,
        comments.CommentVisitor,
        names.NameVisitor,
        names.NameInModuleVisitor,
        values.ValueVisitor,
    )

    def collect(self, filename: str, fst: Module | None) -> Report:
        """Run the visitors and return collected violations as a ``Report``."""
        report = Report(filename)
        if fst is None:
            report.collect_one(ParsingViolation())
        else:
            report.fst = fst
            self._collect_metadata(fst, report)
            for visitor_class in self._visitors_pipeline:
                visitor = visitor_class(fst)
                visitor.run()
                report.collect_from(visitor.violations)

        return report

    def _collect_metadata(self, fst: Module, report: Report) -> None:
        """Collect metadata from the FST."""
        metadata_visitor = metadata.MetadataVisitor(fst)
        metadata_visitor.run()
        report.ignore_map = metadata_visitor.ignore_map
