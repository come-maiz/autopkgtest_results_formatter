# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2017 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from unittest import mock

import testscenarios
from testtools import ExpectedException
from testtools.matchers import (
    Equals,
    FileExists,
    Not
)

from autopkgtest_results_formatter import (
    errors,
    results_index
)
from autopkgtest_results_formatter.tests import unit


class TestResultsIndexWithoutContextTestCase(
        testscenarios.WithScenarios, unit.TestCase):

    scenarios = (
        ('read', {'method': 'read', 'action': 'read index'}),)

    def test_call_method_without_context_raises_error(self):
        index = results_index.ResultsIndex(
            distro='dummy', ppa_user='dummy', ppa_name='dummy')
        method = getattr(index, self.method)
        error = self.assertRaises(
            errors.ResultsIndexNotDownloadedError, method)
        self.assertThat(error.action, Equals('read index'))


class TestResultsIndexTestCase(unit.TestCase):

    def test_download_makes_request(self):
        with mock.patch('urllib.request.urlretrieve') as mock_urlretrieve:
            with results_index.ResultsIndex(
                    distro='testdistro', ppa_user='testuser',
                    ppa_name='testppa') as index:
                pass

        mock_urlretrieve.assert_called_once_with(
            'https://objectstorage.prodstack4-5.canonical.com/v1/'
            'AUTH_77e2ada1e7a84929a74ba3b87153c0ac/'
            'autopkgtest-testdistro-testuser-testppa')

    def test_context_manager_cleans_retrieve(self):
        test_index_file_path = os.path.join(
            self.path, 'autopkgtest-testdistro-testuser-testppa')
        open(test_index_file_path, 'w').close()
        with results_index.ResultsIndex(
                distro='testdistro', ppa_user='testuser', ppa_name='testppa',
                base_results_url='file://{}'.format(self.path)) as index:
            self.assertThat(index._index_file_path, FileExists())

        self.assertThat(index._index_file_path, Not(FileExists()))

    def test_read(self):
        test_index_file_path = os.path.join(
            self.path, 'autopkgtest-testdistro-testuser-testppa')
        with open(test_index_file_path, 'w') as test_index_file:
            test_index_file.write('testentry1\n')
            test_index_file.write('testentry2\n')

        with results_index.ResultsIndex(
                distro='testdistro', ppa_user='testuser', ppa_name='testppa',
                base_results_url='file://{}'.format(self.path)) as index:
            self.assertThat(
                index.read(),
                Equals('testentry1\ntestentry2\n'))
