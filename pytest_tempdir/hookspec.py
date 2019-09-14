# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Pedro Algarvio (pedro@algarvio.me)`
    :copyright: © 2019 by the SaltStack Team, see AUTHORS for more details.
    :license: Apache 2.0, see LICENSE for more details.


    pytest_tempdir.hookspec
    ~~~~~~~~~~~~~~~~~~~~~~~

    Hookspec definition
'''

import pytest


@pytest.hookspec(firstresult=True)
def pytest_tempdir_temproot():
    '''
    An alternate way to define the temporary directory root.
    '''

@pytest.hookspec(firstresult=True)
def pytest_tempdir_basename():
    '''
    An alternate way to define the predictable temporary directory.
    By default returns ``None`` and get's the basename either from the INI file or
    from the CLI passed option
    '''
