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

import testtools
from testtools.matchers import (
    DirExists,
    Not
)

from autopkgtest_results_formatter import result_entry


TEST_RESULT_INDEX_URL = (
    'https://objectstorage.prodstack4-5.canonical.com/v1/'
    'AUTH_77e2ada1e7a84929a74ba3b87153c0ac/'
    'autopkgtest-xenial-snappy-dev-snapcraft-daily')
TEST_RESULT_DIRECTORY_PULL_REQUEST = (
    'xenial/i386/s/snapcraft/20171115_174112_f7052@')
TEST_RESULT_DIRECTORY_PPA = (
    'xenial/amd64/s/snapcraft/20171114_134152_41f31@')
TEST_RESULT_DIRECTORY_SUCCESS = (
    'xenial/amd64/s/snapcraft/20161104_095550_99bb8@')
TEST_RESULT_DIRECTORY_FAILURE = TEST_RESULT_DIRECTORY_PPA


class ResultEntryTestCase(testtools.TestCase):

    def test_context_manager_cleans_up(self):
        with result_entry.ResultEntry(
                index_url=TEST_RESULT_INDEX_URL,
                directory=TEST_RESULT_DIRECTORY_PULL_REQUEST) as entry:
            entry.is_pull_request()
            temp_dir = entry._temp_dir
            self.assertThat(temp_dir, DirExists())

        self.assertThat(temp_dir, Not(DirExists()))

    def test_is_pull_request(self):
        with result_entry.ResultEntry(
                index_url=TEST_RESULT_INDEX_URL,
                directory=TEST_RESULT_DIRECTORY_PULL_REQUEST) as entry:
            self.assertTrue(entry.is_pull_request())

    def test_is_not_pull_request(self):
        with result_entry.ResultEntry(
                index_url=TEST_RESULT_INDEX_URL,
                directory=TEST_RESULT_DIRECTORY_PPA) as entry:
            self.assertFalse(entry.is_pull_request())

    def test_is_success(self):
        with result_entry.ResultEntry(
                index_url=TEST_RESULT_INDEX_URL,
                directory=TEST_RESULT_DIRECTORY_SUCCESS) as entry:
            self.assertTrue(entry.is_success())

    def test_is_not_success(self):
        with result_entry.ResultEntry(
                index_url=TEST_RESULT_INDEX_URL,
                directory=TEST_RESULT_DIRECTORY_FAILURE) as entry:
            self.assertFalse(entry.is_success())
