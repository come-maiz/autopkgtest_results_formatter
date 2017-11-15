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
from testtools.matchers import Contains

from autopkgtest_results_formatter import results_index


class ResultsIndexTestCase(testtools.TestCase):

    def test_read(self):
        with results_index.ResultsIndex(
                distro='xenial', ppa_user='snappy-dev',
                ppa_name='snapcraft-daily') as index:
            index_contents = index.read()

        self.assertThat(
            index_contents,
            Contains(
                'xenial/amd64/s/snapcraft/20161104_095550_99bb8@/'
                'artifacts.tar.gz'))
