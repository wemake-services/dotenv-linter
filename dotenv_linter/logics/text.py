# -*- coding: utf-8 -*-


def normalize_text(text: str) -> str:
    """
    Removes trailing and leading spaces and quotes.

    >>> normalize_text('abc')
    'abc'

    >>> normalize_text('  abc  ')
    'abc'

    >>> normalize_text(' "abc" ')
    'abc'

    """
    return text.strip().strip('\'"')
