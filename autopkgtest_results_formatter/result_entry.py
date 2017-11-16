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
