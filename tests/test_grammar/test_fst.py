import pytest
from lark import Token

from dotenv_linter.grammar.fst import Assign


def test_from_token_raises_value_error():
    """Check that ``Assign.from_token`` raises ``ValueError``."""
    name_token = Token('NAME', 'KEY')
    value_token = Token('VALUE', 'VALUE')

    with pytest.raises(ValueError, match='Empty EQUAL node is not allowed'):
        Assign.from_token(name_token, None, value_token)
