from pathlib import Path
from typing import final, Iterable, cast
from lark import Lark, Transformer, Tree, Token

from dotenv_linter.exceptions import ParsingError
from dotenv_linter.grammar.fst import Assign, Comment, Module, Name, Statement

BASE_DIR = Path(__file__).parent


@final
class DotenvTransformer(Transformer[Token, Module]):
    def __init__(self) -> None:
        super().__init__()
        self._body_items: list[Comment | Statement] = []

    def body(self, parsed: list[Comment | Statement | None]) -> list[Comment | Statement]:
        """body: (line _NEWLINE)* line?"""
        self._body_items = [parsed_item for parsed_item in parsed if parsed_item is not None]
        return self._body_items

    def line(self, parsed: list[Comment | Statement]) -> Comment | Statement:
        """
        line: assign
            | name
            | comment
        """
        if not parsed:
            raise ParsingError('No items found')
        return parsed[0]

    def assign(self, parsed: list[Token]) -> Assign:
        """assign: NAME EQUAL VALUE?"""
        name_token = parsed[0]
        equal_token = parsed[1]
        value_token = parsed[2] if len(parsed) == 3 else None
        return Assign.from_token(
            name_token=name_token,
            equal_token=equal_token,
            value_token=value_token,
        )

    def name(self, parsed: list[Token]) -> Name:
        """name: NAME"""
        return Name.from_token(parsed[0])

    def comment(self, parsed: list[Token]) -> Comment:
        """comment: COMMENT"""
        return Comment.from_token(parsed[0])


class DotenvParser:
    """Custom lark parser wrapper."""
    def __init__(self) -> None:
        self._parser = Lark(
            Path(BASE_DIR).joinpath('grammar.lark').open(),
            start="body",
            parser="lalr",
            propagate_positions=True,
        )
        self._transformer = DotenvTransformer()

    def parse(self, to_parse: str) -> Module:
        try:  # noqa: WPS229
            tree = self._parser.parse(to_parse)
            self._transformer.transform(tree)
            return Module(lineno=0, raw_text=to_parse, body=self._transformer._body_items)
        except Exception as exc:
            raise ParsingError(str(exc))
