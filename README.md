# pytest-cql

[![PyPI version](https://img.shields.io/pypi/v/pytest-cql.svg?style=flat)](https://pypi.org/project/pytest-cql)
[![Python versions](https://img.shields.io/pypi/pyversions/pytest-cql.svg?style=flat)](https://pypi.org/project/pytest-cql)
[![See Build Status on Travis CI](https://travis-ci.org/fruch/pytest-cql.svg?branch=master)](https://travis-ci.org/fruch/pytest-cql)
[![See Build Status on AppVeyor](https://img.shields.io/appveyor/ci/fruch/pytest-cql/master.svg?style=flat)](https://ci.appveyor.com/project/fruch/pytest-cql/branch/master)
[![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/fruch/pytest-cql.svg?style=flat)](https://libraries.io/github/fruch/pytest-cql)
[![Using Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![Codecov Reports](https://codecov.io/gh/fruch/pytest-cql/branch/master/graph/badge.svg)](https://codecov.io/gh/fruch/pytest-cql)

A plugin for pytest to test cql statements

## Features

**TODO**

## Requirements

* having [pytest] tests written

## Installation

You can install "pytest-cql" via [pip] from [PyPI]

``` bash
# not yet in pypi
# pip install pytest-cql
```

## Usage

```bash
python3.6 -m .venv36
source .venv36/bin/activate
pip install -r requirements.txt

# with relocatable
pytest -s --scylla-version unstable/master:324

# with scylla source
SCYLLA_DBUILD_SO_DIR=/home/fruch/Projects/scylla-next/dynamic_libs_for_dtest # this is need if you built scylla with dbuild
pytest -s --scylla-directory /home/`whami`/Projects/scylla-next
```

## Contributing

Contributions are very welcome. Tests can be run with [`tox`][tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [MIT][MIT] license, "pytest-cql" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

## Thanks

This [pytest] plugin was generated with [Cookiecutter] along with [@hackebrot]'s [cookiecutter-pytest-plugin] template.

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@hackebrot]: https://github.com/hackebrot
[MIT]: http://opensource.org/licenses/MIT
[cookiecutter-pytest-plugin]: https://github.com/pytest-dev/cookiecutter-pytest-plugin
[file an issue]: https://github.com/fruch/pytest-cql/issues
[pytest]: https://github.com/pytest-dev/pytest
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/project
