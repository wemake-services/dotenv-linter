# -*- coding: utf-8 -*-

"""
This module contains custom ``mypy`` types that we commonly use.

Policy
------

If any of the following statements is true, move the type to this file:

- if type is used in multiple files
- if type is complex enough it has to be documented
- if type is very important for the public API

"""

from typing import Union, Optional

from ply import lex

#: Token produced lexing incoming text:
ProducedToken = Optional[lex.LexToken]
