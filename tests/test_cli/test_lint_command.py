# -*- coding: utf-8 -*-

import subprocess


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

    for violation_class in all_violations:
        assert str(violation_class.code) in stderr
