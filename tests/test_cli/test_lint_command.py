import os
import subprocess
from collections.abc import Callable

from dotenv_linter.violations.values import InvalidEOLViolation


def test_lint_correct_fixture(fixture_path):
    """Checks that `lint` command works for correct input."""
    process = subprocess.Popen(
        ['dotenv-linter', 'lint', fixture_path('.env.correct')],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    _, stderr = process.communicate()

    assert process.returncode == 0
    assert stderr == ''


def test_lint_multiple_fixture(fixture_path):
    """Checks that `lint` command works for multiple input."""
    process = subprocess.Popen(
        [
            'dotenv-linter',
            fixture_path('.env.correct'),
            fixture_path('.env.empty'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    _, stderr = process.communicate()

    assert process.returncode == 0
    assert stderr == ''


def test_lint_multiple_fixture_with_duplicates(fixture_path):
    """
    Checks that `lint` command works for multiple input.

    See: https://github.com/wemake-services/dotenv-linter/issues/20
    """
    process = subprocess.Popen(
        [
            'dotenv-linter',
            fixture_path('.env.correct'),
            fixture_path('.env.duplicate'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    _, stderr = process.communicate()

    assert process.returncode == 0
    assert stderr == ''


def test_lint_wrong_fixture(fixture_path, all_violations):
    """Checks that `lint` command works for wrong files."""
    process = subprocess.Popen(
        [
            'dotenv-linter',
            fixture_path('.env.incorrect'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    _, stderr = process.communicate()

    assert process.returncode == 1

    violations_without_eol = set(all_violations) - {InvalidEOLViolation}
    for violation_class in violations_without_eol:
        assert str(violation_class.code) in stderr


def test_lint_wrong_eol(fixture_path: Callable[[str], str]) -> None:
    """Checks that `lint` command works for with with CRLF end-of-line."""
    temp_file_path = fixture_path('.env.temp')
    with open(temp_file_path, mode='w') as temp_file:
        temp_file.write('VARIABLE_WITH_CRLF_EOL=123\r\n')

    process = subprocess.Popen(
        [
            'dotenv-linter',
            fixture_path(temp_file_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        # It is important to set this to `False`, otherwise eol are normalized
        universal_newlines=False,
        encoding='utf8',
    )
    _, stderr = process.communicate()

    assert process.returncode == 1

    assert str(InvalidEOLViolation.code) in stderr

    os.remove(temp_file_path)
