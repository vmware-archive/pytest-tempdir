# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Pedro Algarvio (pedro@algarvio.me)`
    :copyright: © 2015 by the SaltStack Team, see AUTHORS for more details.
    :license: Apache 2.0, see LICENSE for more details.


    pytest_logging.plugin
    ~~~~~~~~~~~~~~~~~~~~~
'''
# pylint: disable=protected-access,redefined-outer-name

# Import python libs
from __future__ import absolute_import
import os
import logging
from functools import partial

# Import py libs
import py

# Import pytest libs
import pytest
from _pytest.monkeypatch import monkeypatch

log = logging.getLogger('pytest.tempdir')


class Hooks(object):  # pylint: disable=too-few-public-methods
    '''
    Class to add new hooks to pytest
    '''

    @pytest.hookspec(firstresult=True)
    def pytest_tempdir_basename(self):
        '''
        An alternate way to define the predictable temporary directory.
        By default returns ``None`` and get's the basename either from the INI file or
        from the CLI passed option
        '''


def pytest_addhooks(pluginmanager):
    '''
    Register our new hooks
    '''
    pluginmanager.add_hookspecs(Hooks)


def pytest_addoption(parser):
    '''
    Add CLI options to py.test
    '''
    group = parser.getgroup('tempdir', 'Temporary Directory Options')
#        'Tempdir -\n'
#        '  Predictable and repeatable temporary directory from where additional\n'
#        '  temporary directories can be based off. At the start of each test\n'
#        '  session, if the path exists, IT WILL BE WIPED!'
#    )
    group.addoption('--tempdir-basename',
                    default=None,
                    help='The predictable temporary directory base name. '
                         'Defaults to the current directory name if not '
                         'passed as a CLI parameter and if not defined '
                         'using the tempdir_basename session scoped fixture. '
                         'If the temporary directory exists when the test '
                         'session starts, IT WILL BE WIPED!')
    group.addoption('--tempdir-no-clean',
                    default=False,
                    action='store_true',
                    help='Disable the removal of the created temporary directory')


def pytest_report_header(config):
    '''
    return a string to be displayed as header info for terminal reporting.
    '''
    return 'tempdir: {0}'.format(config._tempdir.strpath)


def pytest_configure(config):
    '''
    Configure the tempdir
    '''
    basename = None
    cli_tempdir_basename = config.getvalue('tempdir_basename')
    if cli_tempdir_basename is not None:
        basename = cli_tempdir_basename
    else:
        # Let's see if we have a pytest_tempdir_basename hook implementation
        basename = config.hook.pytest_tempdir_basename()
    if basename is None:
        # If by now, basename is still None, use the current directory name
        basename = os.path.basename(py.path.local().strpath)  # pylint: disable=no-member

    def clean_up_tempdir(config):
        '''
        Clean up temporary directory
        '''
        if config.getvalue('--tempdir-no-clean') is False:
            log.debug('Cleaning up the tempdir: %s', config._tempdir.strpath)
            try:
                config._tempdir.remove(rec=True, ignore_errors=True)
            except py.error.ENOENT:  # pylint: disable=no-member
                pass
        else:
            log.debug('No cleaning up tempdir: %s', config._tempdir.strpath)

    mpatch = monkeypatch()
    temproot = py.path.local.get_temproot()  # pylint: disable=no-member
    # Let's get the full real path to the tempdir
    tempdir = temproot.join(basename).realpath()
    if tempdir.exists():
        # If it exists, it's a stale tempdir. Remove it
        log.warning('Removing stale tempdir: %s', tempdir.strpath)
        tempdir.remove(rec=True, ignore_errors=True)
    # Make sure the tempdir is created
    tempdir.ensure(dir=True)
    # Store a reference the tempdir for cleanup purposes when ending the test
    # session
    mpatch.setattr(config, '_tempdir', tempdir, raising=False)
    # Register the cleanup actions
    config._cleanup.extend([
        mpatch.undo,
        partial(clean_up_tempdir, config)
    ])


@pytest.fixture(scope='session')
def tempdir(request):
    '''
    tmpdir pytest fixture
    '''
    return request.config._tempdir
