#!/bin/bash

# Diagnostic output:
echo "Using reporter: $INPUT_REPORTER"
echo "Linting options: $INPUT_OPTIONS"
echo 'dotenv-linter --version:'
dotenv-linter --version
echo '================================='
echo

# Runs dotenv-linter, possibly with reviewdog:
if [ "$INPUT_REPORTER" == 'terminal' ]; then
  output=$(dotenv-linter "$INPUT_OPTIONS")
  status="$?"
elif [ "$INPUT_REPORTER" == 'github-pr-review' ] ||
     [ "$INPUT_REPORTER" == 'github-pr-check' ]; then
  # We will need this token for `reviewdog` to work:
  export REVIEWDOG_GITHUB_API_TOKEN="$GITHUB_TOKEN"

  output=$(dotenv-linter "$INPUT_OPTIONS" 2>&1)
  echo "$output" | reviewdog -efm='%f:%l %m' -reporter="$INPUT_REPORTER" -level=error
  # `reviewdog` does not fail with any status code, so we have to get dirty:
  status=$(test "$output" = ''; echo $?)
else
  output="Invalid action reporter specified: $INPUT_REPORTER"
  status=1
fi

# Sets the output variable for Github Action API:
# See: https://help.github.com/en/articles/development-tools-for-github-action
echo "::set-output name=output::$output"
echo '================================='
echo

# Fail the build in case status code is not 0:
if [ "$status" != 0 ]; then
  echo 'Failing with output:'
  echo "$output"
  echo "Process failed with the status code: $status"
  exit "$status"
fi
