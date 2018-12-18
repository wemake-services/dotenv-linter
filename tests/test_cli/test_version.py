# -*- coding: utf-8 -*-

import subprocess

from dotenv_linter.version import pkg_version


def test_call_version_option():
    """Checks that version command works."""
    output_text = subprocess.check_output(
        ['dotenv-linter', '--version'],
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding='utf8',
    )

    assert pkg_version in output_text
