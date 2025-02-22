"""This module contains list of black-listed ``environment`` variables."""

from typing import Final

#: List of variable we forbid to use.
NAMES_BLACKLIST: Final = frozenset((
    # Code generation:
    'DJANGO_ENV',
))
