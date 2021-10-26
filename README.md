# PyTest-Locker
<div style="width: 400pt; margin: 0 auto">
    <img src="https://raw.githubusercontent.com/Luttik/pytest-locker/master/docs/assets/images/example.svg" style="max-width: 100%;" alt="Example">
</div>

<p align="center">
    PyTest-Locker: The fasted way to check for unexpected behaviour changes
</p>

<p align="center">
    <a href="https://github.com/Luttik/pytest-locker/actions?query=workflow%3ACI+branch%3Amaster">
        <img src="https://github.com/luttik/pytest-locker/workflows/CI/badge.svg" alt="actions batch">
    </a>
    <a href="https://pypi.org/project/pytest-locker/">
        <img src="https://badge.fury.io/py/pytest-locker.svg" alt="pypi">
    </a>
    <a href="https://pypi.org/project/pytest-locker/">
        <img src="https://shields.io/pypi/pyversions/pytest-locker" alt="python versions">
    </a>
    <a href="https://codecov.io/gh/luttik/pytest-locker">
        <img src="https://codecov.io/gh/Luttik/pytest-locker/branch/master/graph/badge.svg" alt="codecov">
    </a>
    <a href="https://xgithub.com/Luttik/pytest-locker/blob/master/LICENSE">
        <img src="https://shields.io/github/license/luttik/pytest-locker" alt="License: MIT">
    </a>
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
    </a>
</p>

The test-locker can be used to "lock" data during a test. This means that rather than having to manually specify the
expected output you lock the data when it corresponds to expected behaviour, afterwards you only need to check if the
data has not changed.

Data can be a response, but state and previous calls can also be represented as data. This gives you the option to "
lock" just about anything that your software does using this library.

## Why use PyTest-Locker

- Time efficient: No need to hard code expected responses. (Especially usefull for data heavy unittests)
- Easy to verify changes:

    - Seperates the logic of the test from the expected values.
    - The lock files (containing the expected values), and changes to them, are easy to interpret. This makes it really
      simple to evaluate changes during testing, in commits and in pull request.

## Install

run `pip install pytest-locker`

## Usage

### Configuring the project and writing your first test.

1. Add `from pytest_locker import locker` to your
   [conftest.py](https://docs.pytest.org/en/2.7.3/plugins.html?highlight=re)
   file
2. To access the locker by adding it to the method parameters i.e. `def test_example(locker)`

[//]: # (todo Also write instrcutions for non-string types.)
4. Use `locker.lock(your_string, optional_name)` to lock the data (of-course you can also lock other types).
5. Ensure that the [pytest rootdir](https://docs.pytest.org/en/latest/customize.html) is fixed.
   See [the pytest customize documentation](https://docs.pytest.org/en/latest/customize.html) for all the options (one
   is adding a `pytest.ini` to the root folder)
6. Ensure that `.pytest_locker/` is synced via git, to ensure that you, your team, and your CI/CD pipelines are working
   with the same data.

And you're all set!

### Accepting the current behavior and checking fo changes in this behavior

There are two modes based on for locking. The first is

1. When user input is allowed, i.e. when running pytest with
   `--capture  no` or `-s`

   When user input is allowed and the given data does not correspond to the data in the lock the *user is prompted* if
   the new data should be stored or if the tests should fail.

2. When user input is captured which is default behavior for pytest

   If user input is not allowed the tests will *automatically fail* if the expected lock file does not exist or if the
   data does not correspond to the data in the lock file.

## The Locker class

You can also use `pytest_locker.Locker` (i.e. the class of which the
`locker` fixture returns an instance) directly to create fixtures that locks a (non-string) object without needing to
turn the object into a string it.

You can also use `pytest_locker.Locker` as a basis for locking more complex objects than just strings.
One example is `pytest_locker.JsonLocker` (and the corresponding `pytest_locker.json_locker` fixture)

## Examples

For example of use look at the tests in
[repr-utils](https://github.com/Luttik/repr-utils).
