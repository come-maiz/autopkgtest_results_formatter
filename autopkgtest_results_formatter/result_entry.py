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
import shutil
import tarfile
import tempfile
from urllib import request


class ResultEntry():
    """A result entry in the autopkgtest results index.

    It should be used as a context manager, otherwise the caller has to call
    the `cleanup` method.
    """

    def __init__(self, *, index_url, directory):
        """ResultEntry constructor.

        :param str index_url: The URL to the results index.
        :param str directory: The directory of this result entry.
        """
        self._index_url = index_url
        self._directory = directory
        self._temp_dir = tempfile.mkdtemp()
        self._result_dir_path = None
        self._distro = None
        self._architecture = None
        self._day = None
        self._identifier = None

    def __eq__(self, other):
        return (
            self._index_url == other._index_url and
            self._directory == other._directory)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()

    def cleanup(self):
        request.urlcleanup()
        if self._temp_dir:
            shutil.rmtree(self._temp_dir)
            self._temp_dir = None

    @property
    def distro(self):
        if not self._distro:
            return self._get_info_from_directory()[0]
        return self._distro

    @property
    def architecture(self):
        if not self._architecture:
            return self._get_info_from_directory()[1]
        return self._architecture

    @property
    def day(self):
        if not self._day:
            return self._get_info_from_directory()[2]
        return self._day

    @property
    def identifier(self):
        if not self._identifier:
            return self._get_info_from_directory()[3]
        return self._identifier

    def _get_info_from_directory(self):
        dir_parts = self._directory.split('/')[-5:]
        self._distro, self._architecture, _, _, day_time_id = dir_parts
        self._day, time, identifier = day_time_id.split('_')
        self._identifier = (
            self._distro + self._architecture + self._day + time +
            identifier.rstrip('@'))
        return (self._distro, self._architecture, self._day, self._identifier)

    def is_pull_request(self):
        """Return True if this entry is a pull request, otherwise, False."""
        test_info = self._get_test_info()
        return (
            'custom_environment' in test_info and
            [x for x in test_info['custom_environment'] if
             x.startswith('UPSTREAM_PULL_REQUEST=')] != [])

    def _get_test_info(self):
        result_dir_path = self._get_result()
        with open(os.path.join(result_dir_path, 'testinfo.json')) as test_info:
            return json.load(test_info)

    def _get_result(self):
        if not self._result_dir_path:
            result_tar_path = self._download_result()
            self._result_dir_path = tempfile.mkdtemp(dir=self._temp_dir)
            result_tar = tarfile.TarFile(result_tar_path)
            result_tar.extractall(self._result_dir_path)
        return self._result_dir_path

    def _download_result(self):
        result_file_path = os.path.join(self._temp_dir, 'result.tar')
        request.urlretrieve(
            '{index}/{directory}/result.tar'.format(
                index=self._index_url, directory=self._directory),
            filename=result_file_path)
        return result_file_path

    def get_test_package(self):
        """Return the package name and version used for this test."""
        result_dir_path = self._get_result()
        with open(os.path.join(
                result_dir_path, 'testpkg-version')) as testpkg_version:
            return testpkg_version.read().strip()

    def is_success(self):
        """Return True if this entry is exited with 0, otherwise, False."""
        return self._get_exitcode().strip() == '0'

    def _get_exitcode(self):
        result_dir_path = self._get_result()
        with open(os.path.join(result_dir_path, 'exitcode')) as exitcode:
            return exitcode.read()

    def get_duration(self):
        """Return the duration of the test execution."""
        result_dir_path = self._get_result()
        with open(os.path.join(
                result_dir_path, 'duration')) as duration:
            return duration.read().strip()

    def get_links(self):
        """Return the execution output as a list of tuples (name, url)."""
        return [
            (file_name.split(os.extsep)[0],
             '{index}/{directory}/{file_name}'.format(
                 index=self._index_url, directory=self._directory,
                 file_name=file_name)) for
            file_name in ('result.tar', 'log.gz', 'artifacts.tar.gz')
        ]
