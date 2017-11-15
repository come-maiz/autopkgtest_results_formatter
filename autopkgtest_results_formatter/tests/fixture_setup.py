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

import fixtures


class TempCWD(fixtures.TempDir):

    def __init__(self, rootdir=None):
        super().__init__(rootdir)

    def setUp(self):
        """Create a temporary directory and cd into it for the test duration."""
        super().setUp()
        current_dir = os.getcwd()
        self.addCleanup(os.chdir, current_dir)
        os.chdir(self.path)
