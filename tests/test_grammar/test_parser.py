import pytest

from dotenv_linter.exceptions import ParsingError
from dotenv_linter.grammar.parser import DotenvTransformer


def test_parsing_error():
    """Calling ``line`` with an empty list raises ``ParsingError``."""
    transformer = DotenvTransformer()

    with pytest.raises(ParsingError):
        transformer.line([])
