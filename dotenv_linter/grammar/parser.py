from pathlib import Path
from typing import List
from lark import Lark, Transformer, Token

from dotenv_linter.exceptions import ParsingError
from dotenv_linter.grammar.fst import Assign, Comment, Module, Name, Statement

BASE_DIR = Path(__file__).parent


class DotenvTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self._body_items: List[Comment | Statement] = []

    def body(self, items):
        self._body_items = [item for item in items if item is not None]
        return self._body_items

    def line(self, items):
        if not items:
            raise ParsingError('No items found')
        return items[0]

    def assign(self, items):
        name_token = items[0]
        equal_token = items[1]
        value_token = items[2] if len(items) == 3 else None
        return Assign.from_token(
            name_token=name_token,
            equal_token=equal_token,
            value_token=value_token,
        )

    def name(self, items):
        return Name.from_token(items[0])

    def comment(self, items):
        return Comment.from_token(items[0])


class DotenvParser:
    def __init__(self):
        self._parser = Lark(
            Path(BASE_DIR).joinpath('grammar.lark').open(),
            start="body",
            parser="lalr",
            propagate_positions=True,
        )
        self._transformer = DotenvTransformer()

    def parse(self, to_parse: str) -> Module:
        try:
            tree = self._parser.parse(to_parse)
            self._transformer.transform(tree)
            return Module(lineno=0, raw_text=to_parse, body=self._transformer._body_items)
        except Exception as e:
            raise ParsingError(str(e))
