
# -*- coding: utf-8 -*-

# See also:
# https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration
# https://click.palletsprojects.com/en/7.x/arguments/

import sys
from typing import Tuple

import click
from click_default_group import DefaultGroup

from dotenv_linter.checker import DotenvFileChecker
from dotenv_linter.version import pkg_version


@click.group(
    cls=DefaultGroup,
    default='lint',
    default_if_no_args=True,
    invoke_without_command=True,
)
@click.option('--version', is_flag=True, default=False)
def cli(version):
    """
    Main entrypoint to the app.

    Runs ``lint`` command by default if nothing else is not specified.
    Runs ``--version`` subcommand if this option is provided.
    """
    if version:
        print(pkg_version)  # noqa: WPS421


@cli.command()
@click.argument(
    'files',
    nargs=-1,
    required=True,
    type=click.Path(exists=True, dir_okay=False),
)
def lint(files: Tuple[str, ...]):
    """Runs linting process for the given files."""
    checker = DotenvFileChecker(files)

    try:
        checker.run()
    except Exception as ex:
        print(ex, file=sys.stderr)  # noqa: WPS421
        checker.fail()
