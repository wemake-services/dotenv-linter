import subprocess


def test_empty_arguments():
    """Checks that `lint` command does not work without arguments."""
    process = subprocess.Popen(
        ['dotenv-linter'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, stderr = process.communicate()

    assert process.returncode == 2
    assert not stdout
    assert stderr


def test_lint_empty_arguments():
    """Checks that `lint` command does not work without arguments."""
    process = subprocess.Popen(
        ['dotenv-linter', 'lint'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, stderr = process.communicate()

    assert process.returncode == 2
    assert not stdout
    assert stderr


def test_lint_missing_files():
    """Checks that `lint` command does not work with non-existing file."""
    process = subprocess.Popen(
        ['dotenv-linter', 'lint', 'sd'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, stderr = process.communicate()

    assert process.returncode == 2
    assert not stdout
    assert stderr


def test_lint_parsing_violation(fixture_path):
    """Checks that `lint` command does not work with parsing errors."""
    process = subprocess.Popen(
        ['dotenv-linter', 'lint', fixture_path('.env.parsing')],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, stderr = process.communicate()

    assert process.returncode == 1
    assert not stdout
    assert '001' in stderr
