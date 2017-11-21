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


class ResultEntryTestCase(unit.TestCase):

    def make_result_tar(self, files):
        entry_dir = 'test_directory'
        entry_dir_path = os.path.join(self.path, entry_dir)
        os.makedirs(entry_dir_path)
        tar_file_path = os.path.join(entry_dir_path, 'result.tar')
        with tarfile.open(tar_file_path, 'w') as tar_file:
            for path, name in files:
                tar_file.add(path, arcname=name)
        return entry_dir

    def test_equals(self):
        self.assertThat(
            result_entry.ResultEntry(
                index_url='test_index', directory='test_directory'),
            Equals(result_entry.ResultEntry(
                index_url='test_index', directory='test_directory')))

    def test_get_distro(self):
        self.assertThat(
            result_entry.ResultEntry(
                index_url='dummy',
                directory=('test_distro/dummy/dummy/dummy/'
                           'dummy_dummy_dummy')).distro,
            Equals('test_distro'))

    def test_get_architecture(self):
        self.assertThat(
            result_entry.ResultEntry(
                index_url='dummy',
                directory=('dummy/test_arch/dummy/dummy/'
                           'dummy_dummy_dummy')).architecture,
            Equals('test_arch'))

    def test_get_day(self):
        self.assertThat(
            result_entry.ResultEntry(
                index_url='dummy',
                directory=('dummy/dummy/dummy/dummy/'
                           'testday_dummy_testday@')).day,
            Equals('testday'))

    def test_get_identifier(self):
        self.assertThat(
            result_entry.ResultEntry(
                index_url='dummy',
                directory=('test_distro/test_arch/dummy/dummy/'
                           'testday_testtime_testid@')).identifier,
            Equals('test_distrotest_archtestdaytesttimetestid'))

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
        entry_dir = self.make_result_tar(
            [(test_info_file_path, 'testinfo.json')])

        with result_entry.ResultEntry(
                index_url='file://{}'.format(self.path),
                directory=entry_dir) as entry:
            self.assertTrue(entry.is_pull_request())

    def test_is_not_pull_request(self):
        test_info_file_path = os.path.join(self.path, 'testinfo.json')
        with open(test_info_file_path, 'w') as test_info_file:
            test_info_file.write('{}')
        entry_dir = self.make_result_tar(
            [(test_info_file_path, 'testinfo.json')])

        with result_entry.ResultEntry(
                index_url='file://{}'.format(self.path),
                directory=entry_dir) as entry:
            self.assertFalse(entry.is_pull_request())

    def test_is_success(self):
        test_exitcode_file_path = os.path.join(self.path, 'exitcode')
        with open(test_exitcode_file_path, 'w') as test_info_file:
            test_info_file.write('0')
        entry_dir = self.make_result_tar(
            [(test_exitcode_file_path, 'exitcode')])

        with result_entry.ResultEntry(
                index_url='file://{}'.format(self.path),
                directory=entry_dir) as entry:
            self.assertTrue(entry.is_success())

    def test_is_not_success(self):
        test_exitcode_file_path = os.path.join(self.path, 'exitcode')
        with open(test_exitcode_file_path, 'w') as test_info_file:
            test_info_file.write('1')
        entry_dir = self.make_result_tar(
            [(test_exitcode_file_path, 'exitcode')])

        with result_entry.ResultEntry(
                index_url='file://{}'.format(self.path),
                directory=entry_dir) as entry:
            self.assertFalse(entry.is_success())

    def test_get_test_package(self):
        testpkg_version_path = os.path.join(self.path, 'testpkg-version')
        with open(testpkg_version_path, 'w') as testpkg_version_file:
            testpkg_version_file.write('package_name test_version')
        entry_dir = self.make_result_tar(
            [(testpkg_version_path, 'testpkg-version')])

        with result_entry.ResultEntry(
                index_url='file://{}'.format(self.path),
                directory=entry_dir) as entry:
            self.assertThat(
                entry.get_test_package(),
                Equals('package_name test_version'))

    def test_get_duration(self):
        duration_path = os.path.join(self.path, 'duration')
        with open(duration_path, 'w') as duration_file:
            duration_file.write('test_duration')
        entry_dir = self.make_result_tar(
            [(duration_path, 'duration')])

        with result_entry.ResultEntry(
                index_url='file://{}'.format(self.path),
                directory=entry_dir) as entry:
            self.assertThat(
                entry.get_duration(),
                Equals('test_duration'))

    def test_get_links(self):
        entry = result_entry.ResultEntry(
            index_url='http://example.com', directory='test_directory')
        self.assertThat(
            entry.get_links(),
            Equals([
                ('result', 'http://example.com/test_directory/result.tar'),
                ('log', 'http://example.com/test_directory/log.gz'),
                ('artifacts',
                 'http://example.com/test_directory/artifacts.tar.gz')]))
