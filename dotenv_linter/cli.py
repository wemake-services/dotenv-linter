
# -*- coding: utf-8 -*-

"""
Here we define all basic CLI command that we provide as a public API.

We use ``click`` as a utility package to help us with CLI definition.
It is a powerfull tool to do this one specific task.

See also:
    https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration
    https://click.palletsprojects.com/en/7.x/arguments/

"""

import sys
from typing import NoReturn, Tuple

import click

from dotenv_linter.checker import DotenvFileChecker


@click.command()
@click.argument('files', nargs=-1, required=True, type=click.Path(exists=True))
def main(files: Tuple[str, ...]) -> NoReturn:
    """Runs linting process for the given files."""
    checker = DotenvFileChecker(files)

    error_message = None
    try:
        checker.run()
    except Exception as ex:
        error_message = str(ex)
    finally:
        checker.finish(message=error_message)
