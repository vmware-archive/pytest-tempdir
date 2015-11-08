# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Pedro Algarvio (pedro@algarvio.me)`
    :copyright: © 2015 by the SaltStack Team, see AUTHORS for more details.
    :license: Apache 2.0, see LICENSE for more details.


    test_tempdir.py
    ~~~~~~~~~~~~~~~
'''

# Import python libs
from __future__ import absolute_import
import os
import textwrap

# Import py libs
import py


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'Temporary Directory Options:',
    ])


def test_tempdir_hook(testdir):
    with open(os.path.join(testdir.tmpdir.strpath, 'conftest.py'), 'w') as wfh:
        wfh.write(textwrap.dedent('''
            import pytest

            def pytest_tempdir_basename():
                return 'bar'
        '''))

    testdir.makepyfile('''
        def test_tempdir_hook(tempdir):
            assert tempdir.strpath.endswith('bar')
    ''')

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_tempdir_hook PASSED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_tempdir_no_clean(testdir):
    tempdir_path = py.path.local.get_temproot().join('bar').realpath().strpath  # pylint: disable=no-member
    # Let' assert it does not yet exist
    with open(os.path.join(testdir.tmpdir.strpath, 'conftest.py'), 'w') as wfh:
        wfh.write(textwrap.dedent('''
            import pytest

            def pytest_tempdir_basename():
                return 'bar'
        '''))

    testdir.makepyfile('''
        import os

        def test_tempdir_no_clean(tempdir):
            assert tempdir.strpath.endswith('bar')
            assert os.path.isdir(tempdir.realpath().strpath)
    ''')

    result = testdir.runpytest('-v', '--tempdir-no-clean', '-vvv')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_tempdir_no_clean PASSED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0
    # Assert that the tempdir was left untouched after the tests suite ended
    assert os.path.isdir(tempdir_path) is True
