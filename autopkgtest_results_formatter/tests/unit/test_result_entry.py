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

import json
import os
import tarfile
from unittest import mock

from testtools.matchers import Equals

from autopkgtest_results_formatter import result_entry
from autopkgtest_results_formatter.tests import unit


class TestResultEntryTestCase(unit.TestCase):

    def test_equals(self):
        self.assertThat(
            result_entry.ResultEntry(
                index_url='test_index', directory='test_directory'),
            Equals(result_entry.ResultEntry(
                index_url='test_index', directory='test_directory')))

    def test_download_result_makes_request(self):
        with mock.patch('urllib.request.urlretrieve') as mock_urlretrieve:
            with result_entry.ResultEntry(
                    index_url='http://example.com',
                    directory='test_directory') as entry:
                entry._download_result()

        mock_urlretrieve.assert_called_once_with(
            'http://example.com/test_directory/result.tar', filename=mock.ANY)

    def test_is_pull_request(self):
        test_info_file_path = os.path.join(self.path, 'testinfo.json')
        with open(test_info_file_path, 'w') as test_info_file:
            test_info_file.write(
                json.dumps({
                    'custom_environment': ['UPSTREAM_PULL_REQUEST=dummy']
                }))
        entry_dir = 'test_directory'
        entry_dir_path = os.path.join(self.path, entry_dir)
        os.makedirs(entry_dir_path)
        tar_file_path = os.path.join(entry_dir_path, 'result.tar')
        with tarfile.open(tar_file_path, 'w') as tar_file:
            tar_file.add(test_info_file_path, arcname='testinfo.json')

        with result_entry.ResultEntry(
                index_url='file://{}'.format(self.path),
                directory=entry_dir) as entry:
            self.assertTrue(entry.is_pull_request())

    def test_is_not_pull_request(self):
        test_info_file_path = os.path.join(self.path, 'testinfo.json')
        with open(test_info_file_path, 'w') as test_info_file:
            test_info_file.write('{}')
        entry_dir = 'test_directory'
        entry_dir_path = os.path.join(self.path, entry_dir)
        os.makedirs(entry_dir_path)
        tar_file_path = os.path.join(entry_dir_path, 'result.tar')
        with tarfile.open(tar_file_path, 'w') as tar_file:
            tar_file.add(test_info_file_path, arcname='testinfo.json')

        with result_entry.ResultEntry(
                index_url='file://{}'.format(self.path),
                directory=entry_dir) as entry:
            self.assertFalse(entry.is_pull_request())
