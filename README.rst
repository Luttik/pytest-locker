.. image:: https://github.com/luttik/pytest-locker/workflows/CI/badge.svg
    :alt: actions batch
    :target: https://github.com/Luttik/pytest-locker/actions?query=workflow%3ACI+branch%3Amaster
.. image:: https://badge.fury.io/py/pytest-locker.svg
    :alt: pypi
    :target: https://pypi.org/project/pytest-locker/
.. image:: https://codecov.io/gh/Luttik/pytest-locker/branch/master/graph/badge.svg
    :alt: codecov
    :target: https://codecov.io/gh/luttik/pytest-locker


.. image:: https://raw.githubusercontent.com/Luttik/pytest-locker/master/example.svg
    :alt: example image
    :width: 60%
    :align: center 

PyTest-Locker
-------------
The test-locker can be used to "lock" data from during a test.
This means that rather than having to manually specify the expected output
you lock the data when it corresponds to expected bahaviour.

Why use Locker
==============
- Time efficient: No need to hard code expected responses. (Especially usefull for data heavy unittests)
- Easy to verify changes: 

  - Seperates logic of the test and expected values in the test further
  - Lock files, and changes to them, are easy to interpret. 
    Therefore, evaluting them in pull-requests a great method of quality controll. 

Install
=======
run ``pip install pytest-locker``

Use
===
- *Step 1:* Add ``from pytest_locker import locker`` to your
  `conftest.py <https://docs.pytest.org/en/2.7.3/plugins.html?highlight=re>`_ file
- *Step 2:* To access the locker by adding it to the method parameters i.e. ``def test_example(locker)``
- *Step 3:* Use ``locker.lock(your_string, optional_name)`` to lock the data.
- *Additionally:* Don't forget to commit the ``.pytest_locker/`` directory for ci/cd testing

And you're all set!

Tip
===
When using locks to test your file it is even more important than usual that the
`pytest rootdir <https://docs.pytest.org/en/latest/customize.html>`_ is fixed.
Click the `link <https://docs.pytest.org/en/latest/customize.html>`_ for all the options
(one is adding a ``pytest.ini`` to the root folder).

The Locker test Flows
=====================
There are two modes based on for locking.

- When user input is allowed, i.e. when running pytest with ``--capture  no`` or ``-s``

  When user input is allowed and the given data does not correspond to the data in the lock
  the *user is prompted* if the new data should be stored or if the tests should fail.

- When user input is captured which is default behavior for pytest

  If user input is not allowed the tests will *automatically fail* if the expected lock file does not exist
  or if the data does not correspond to the data in the lock file.

The Locker class
================
You can also use ``pytest_locker.Locker`` (i.e. the class of which the ``locker`` fixture returns an instance).
directly to create fixtures that locks a (non-string) object without needing to turn the object into a string it.

Examples
========
For example of use look at the tests in `<https://github.com/Luttik/repr_utils>`_.
