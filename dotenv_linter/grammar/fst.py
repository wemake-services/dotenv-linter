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

# TODO: doc hieracy

class Node(object):
    col_offset: int


class Statement(Node):
    lineno: int


class Comment(Statement):
    pass


class Assign(Statement):
    pass


class Name(Node):
    pass


class Value(Node):
    pass
