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


def clean_names(names: list[str]) -> list[str]:
    """
    Cleans names from trailing and leading spaces.

    >>> clean_names(['abc', ' def '])
    ['abc', 'def']
    """
    return [name.strip() for name in names]
