.. image:: https://github.com/luttik/test-locker/workflows/CI/badge.svg
    :alt: actions batch
    :target: https://github.com/Luttik/test-locker/actions?query=workflow%3ACI+branch%3Amaster
.. image:: https://badge.fury.io/py/test-locker.svg
    :alt: pypi
    :target: https://pypi.org/project/test-locker/

.. image:: https://codecov.io/gh/test-locker/branch/master/graph/badge.svg
    :alt: codecov
    :target: https://codecov.io/gh/luttik/test-locker

Test-Locker
-----------
The test-locker can be used to "lock" data from during a test.
This means that rather than having to manually specify the expected output
you lock the data when it corresponds to expected bahaviour.

There are two modes based on for locking.

- When user input is allowed, i.e. when running pytest with ``--capture  no``

  When user input is allowed and the given data does not correspond to the data in the lock
  the *user is prompted* if the new data should be stored or if the tests should fail.

- When user input is captured which is default behavior for pytest

  If user input is not allowed the tests will *automatically fail* if the expected lock file does not exist
  or if the data does not correspond to the data in the lock file.


install
=======
run ``pip install test-locker``

Use
===
- Step 1: Add ``from test_locker import locker`` to your
  `conftest.py <https://docs.pytest.org/en/2.7.3/plugins.html?highlight=re>`_ file
- Step 2: To access the locker by adding it to the method parameters i.e. ``def test_example(locker)``

And you're all set!

The Locker class
================
You can also use ``test_locker.Locker`` (i.e. the class of which the ``locker`` fixture returns an instance).
directly to create fixtures that locks a (non-string) object without needing to turn the object into a string it.

Examples
========
For example of use look at the tests in `<https://github.com/Luttik/repr_utils>`_.