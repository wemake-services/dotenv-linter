# -*- coding: utf-8 -*-

import ast

from dotenv_linter.violations.base import (
    BaseViolation,
    BaseFSTViolation,
    BaseFileViolation,
)

def test_visitor_returns_location():
    """Ensures that `BaseNodeVisitor` return correct violation message."""
    visitor = BaseFSTViolation(node=ast.parse(''), text='violation')
    visitor.error_template = '{0}'
    visitor.code = 1
    assert visitor._node() == (0, 0, 'Z001 violation')

def test_checker_default_locations():
    """Ensures that `BaseViolation` returns correct location. """
    assert BaseViolation(None, None).location() == (0, 0) #noqa: Z441