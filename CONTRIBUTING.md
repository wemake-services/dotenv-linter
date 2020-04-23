# How to contribute

## Step 1

### Fork this repository

[Fork it!](https://help.github.com/en/github/getting-started-with-github/fork-a-repo)

Making changes to a fork and submitting from there usually ends up being easier for both you and us.

## Step 2

### Install Dependencies

We use [poetry](https://github.com/python-poetry/poetry) to manage our dependencies.

To install them you would need to run the following command:

```bash
poetry install
```

## Step 3

### Run the Tests

Run all tests beforehand and make a note of the coverage percentage

We use pytest and flake8 for quality control. To run all tests:

```bash
pytest
```

### Run linting

We use `wemake-python-styleguide` to lint our code. To run it use:

```bash
flake8 .
```

### Run type checks

We `mypy` to check our code. To run it use:

```bash
mypy dotenv_linter
```

## Step 4

### Make Your Changes

Write your code. Make your changes.

## Step 5

### Edit the docs

Any changes you have made that require documentation, make sure to document them!
Add your docstrings (if applicable), and let future users and contributors know what
your changes do and how they should be used


## Step 6

### Add New Tests and Run

Make sure that everything you've done hasn't broken anything that we've done!
If you have added new functionality or features, make sure you have added a test
for that functionality or feature


## Step 7

### Pull Request

Submit a PR for your changes. Make sure to include in the commit/PR message what issue you are
addressing (if fixing a bug or feature request).

# Other Help

You can contribute by spreading a word about this library. It would also be a huge contribution to write a short article on how you are using this project. What are your best-practices?
