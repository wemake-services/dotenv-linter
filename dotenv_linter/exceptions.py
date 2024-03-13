from typing import final


@final
class ParsingError(Exception):
    """Used when dotenv file has incorrect grammar and cannot be parsed."""
