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

from autopkgtest_results_formatter import (
    markdown_printer,
    results_index
)


class ResultsFormatter():
    """Format the test results to a directory of markdown files."""

    def __init__(
            self, *, destination_path, distros, ppa_user, ppa_name, day,
            base_results_url=None):
        """Formatter constructor.

        :parm str destination_path: The path to the destination directory.
        :param distro: The names of the distros, for example: xenial.
        :type distro: list of strings.
        :param str ppa_user: The name of the owner of the PPA. A Launchpad user
            or team, without the `~`.
        :param str ppa_name: The name of the PPA.
        :param str day: The day of the results, with format yyyymmdd.
        :param str base_results_url: The URL where the index is stored. Default
            is the URL to Canonical's prodstack server where Ubuntu autopkgtest
            results are stored. autopkgtest-{distro}-{ppa_user}-{ppa_name} will
            be appended to this string to form the complete URL to the results
            index.
        """
        super().__init__()
        self._destination_path = destination_path
        self._distros = distros
        self._ppa_user = ppa_user
        self._ppa_name = ppa_name
        self._day = day
        self._base_results_url = base_results_url

    def format(self):
        result_entries = []
        for distro in self._distros:
            with results_index.ResultsIndex(
                    distro=distro, ppa_user=self._ppa_user,
                    ppa_name=self._ppa_name,
                    base_results_url=self._base_results_url) as results:
                result_entries += [
                    entry for entry in results.filter_by_day(self._day)
                    if not entry.is_pull_request()]
        for entry in result_entries:
            print(entry.identifier)
        printer = markdown_printer.MarkdownPrinter(
            destination_path=os.path.join(
                self._destination_path, '{}.md'.format(self._day)),
            result_entries=result_entries)
        printer.print_results()
