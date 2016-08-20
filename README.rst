pytest-tempdir
==============

.. image:: https://travis-ci.org/saltstack/pytest-tempdir.svg?branch=master
    :target: https://travis-ci.org/saltstack/pytest-tempdir
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/saltstack/pytest-tempdir?branch=master
    :target: https://ci.appveyor.com/project/saltstack-public/pytest-tempdir/branch/master
    :alt: See Build Status on AppVeyor

.. image:: http://img.shields.io/pypi/v/pytest-tempdir.svg
   :target: https://pypi.python.org/pypi/pytest-tempdir

Adds support for a predictable and repeatable temporary directory.

----

This `Pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `Cookiecutter-pytest-plugin`_ template.


Features
--------

* Adds support for a predictable and repeatable temporary directory through the 
  `tempdir` fixture which gets cleaned up in the end of the test run 
  session(this behaviour can be disabled).


Requirements
------------

* None!


Installation
------------

You can install "pytest-tempdir" via `pip`_ from `PyPI`_::

    $ pip install pytest-tempdir


Usage
-----

* Simply define a ``pytest_tempdir_basename`` function on your ``conftest.py`` 
  which returns a string to define the basename or pass ``--tempdir-basename``.
* If you wish to leave the temporary directory intact for further inspection 
  after the tests suite ends, pass ``--tempdir-no-clean``.


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `Apache 2.0`_ license, "pytest-tempdir" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

Changelog
---------

v2016.8.20
~~~~~~~~~~

* Support pytest 2.x and 3.x

v2015.12.6
~~~~~~~~~~

* Each absolute path gets it's own counter

v2015.11.29
~~~~~~~~~~~

* Append a counter value to existing directory names

v2015.11.17
~~~~~~~~~~~

* Fix more encoding issues when running setup and the system locale is not set

v2015.11.16
~~~~~~~~~~~

* Fix encoding issue when running setup and the system locale is not set

v2015.11.8
~~~~~~~~~~

* Fix stale tempdir cleanup logic

v2015.11.6
~~~~~~~~~~

* Wipe the tempdir directory on test session start if it exists

v2015.11.4
~~~~~~~~~~

* First working release

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/saltstack/pytest-tempdir/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.org/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`Apache 2.0`: http://www.apache.org/licenses/LICENSE-2.0
