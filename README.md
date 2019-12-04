# dotenv-linter

[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)
[![Build Status](https://travis-ci.org/wemake-services/dotenv-linter.svg?branch=master)](https://travis-ci.org/wemake-services/dotenv-linter)
[![Coverage](https://coveralls.io/repos/github/wemake-services/dotenv-linter/badge.svg?branch=master)](https://coveralls.io/github/wemake-services/dotenv-linter?branch=master)
[![Github Action](https://github.com/wemake-services/dotenv-linter/workflows/dotenv/badge.svg)](https://github.com/wemake-services/dotenv-linter/actions)
[![Python Version](https://img.shields.io/pypi/pyversions/dotenv-linter.svg)](https://pypi.org/project/dotenv-linter/)
[![Documentation Status](https://readthedocs.org/projects/dotenv-linter/badge/?version=latest)](https://dotenv-linter.readthedocs.io/en/latest/?badge=latest)

---

Simple linter for `.env` files.

![dotenv-logo](https://raw.githubusercontent.com/wemake-services/dotenv-linter/master/docs/_static/dotenv-logo@2.png)

While `.env` files are very simple it is required to keep them consistent.
This tool offers a wide range of consistency rules and best practices.

And it integrates perfectly to any existing workflow.


## Installation and usage

```bash
pip install dotenv-linter
```

And then run it:

```bash
dotenv-linter .env .env.template
```

See [Usage](https://dotenv-linter.readthedocs.io/en/latest/#usage)
section for more information.


## Examples

There are many things that can go wrong in your `.env` files:

```ini
# Next line has leading space which will be removed:
 SPACED=

# Equal signs should not be spaced:
KEY = VALUE

# Quotes won't be preserved after parsing, do not use them:
SECRET="my value"

# Beware of duplicate keys!
SECRET=Already defined ;(

# Respect the convention, use `UPPER_CASE`:
kebab-case-name=1
snake_case_name=2
```

And much more! You can find the [full list of violations in our docs](https://dotenv-linter.readthedocs.io/en/latest/pages/violations/).


## Gratis

Special thanks goes to [Ignacio Toledo](https://ign.uy)
for creating an awesome logo for the project.
