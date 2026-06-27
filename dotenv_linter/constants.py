"""This module contains list of black-listed ``environment`` variables."""

from enum import IntEnum, unique
from typing import Final, final

#: List of variable we forbid to use.
NAMES_BLACKLIST: Final = frozenset((
    # Code generation:
    'DJANGO_ENV',
))

UNREADABLE_CHARACTER_COMBINATIONS: Final = frozenset(
    ('1I', '0O', 'O0', 'Il', 'lI', '1l', 'l1'),
)


@final
@unique
class ExitCodes(IntEnum):
    """CLI exit status codes."""

    initial = -1
    success = 0
    linting_error = 1
    system_error = 137
