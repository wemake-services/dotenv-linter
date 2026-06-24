"""This module contains list of black-listed ``environment`` variables."""

from typing import Final

#: List of variable we forbid to use.
NAMES_BLACKLIST: Final = frozenset((
    # Code generation:
    'DJANGO_ENV',
))

UNREADABLE_CHARACTER_COMBINATIONS: Final = frozenset(
    ('1I', '0O', 'O0', 'Il', 'lI', '1l', 'l1'),
)
