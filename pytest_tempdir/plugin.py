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
try:
    from _pytest.monkeypatch import MonkeyPatch
except ImportError:
    from _pytest.monkeypatch import monkeypatch as MonkeyPatch

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


class TempDir(object):
    def __init__(self, config):
        self.config = config
        self._prepare()

    def _prepare(self):
        self.counters = {}
        basename = None
        cli_tempdir_basename = self.config.getvalue('tempdir_basename')
        if cli_tempdir_basename is not None:
            basename = cli_tempdir_basename
        else:
            # Let's see if we have a pytest_tempdir_basename hook implementation
            basename = self.config.hook.pytest_tempdir_basename()
        if basename is None:
            # If by now, basename is still None, use the current directory name
            basename = os.path.basename(py.path.local().strpath)  # pylint: disable=no-member
        mpatch = MonkeyPatch()
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
        mpatch.setattr(self.config, '_tempdir', self, raising=False)
        # Register the cleanup actions
        self.config._cleanup.extend([
            mpatch.undo,
            self._clean_up_tempdir
        ])
        self.tempdir = tempdir

    def _clean_up_tempdir(self):
        '''
        Clean up temporary directory
        '''
        if self.config.getvalue('--tempdir-no-clean') is False:
            log.debug('Cleaning up the tempdir: %s', self.tempdir.strpath)
            try:
                self.tempdir.remove(rec=True, ignore_errors=True)
            except py.error.ENOENT:  # pylint: disable=no-member
                pass
        else:
            log.debug('No cleaning up tempdir: %s', self.tempdir.strpath)

    def mkdir(self, path, use_existing=False):
        abspath = self.tempdir.join(path)
        if abspath not in self.counters:
            self.counters[abspath] = 0
        while True:
            newdir = self.tempdir.join('{0}{1}'.format(path, self.counters[abspath]))
            if newdir.exists() and use_existing is False:
                self.counters[abspath] += 1
                continue
            log.warning('New Dir: %s', newdir)
            return newdir.ensure(dir=True)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return getattr(self.tempdir, name)


def pytest_configure(config):
    '''
    Configure the tempdir
    '''
    # Prep tempdir
    TempDir(config)


@pytest.fixture(scope='session')
def tempdir(request):
    '''
    tmpdir pytest fixture
    '''
    return request.config._tempdir
