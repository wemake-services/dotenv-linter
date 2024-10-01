import pytest

from dotenv_linter.grammar.parser import DotenvParser
from dotenv_linter.violations.base import BaseFSTViolation, BaseViolation


def test_visitor_returns_location() -> None:
    """Ensures that `BaseVisitor` return correct violation message."""
    node = DotenvParser().parse(to_parse='')
    visitor = BaseFSTViolation(node, text='violation')
    visitor.error_template = '{0}'
    visitor.code = 1
    assert visitor.location() == 0


def test_checker_default_locations() -> None:
    """Ensures that `BaseViolation.location` is not implemented."""
    with pytest.raises(NotImplementedError):
        BaseViolation(node=None, text=None).location()
