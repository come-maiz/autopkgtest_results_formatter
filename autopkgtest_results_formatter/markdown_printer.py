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


class MarkdownPrinter():

    def __init__(self, *, destination_path, result_entries):
        self._markdown_file_path = destination_path
        self._result_entries = result_entries

    def print_results(self):
        parsed_dictionary = self._parse()
        with open(self._markdown_file_path, 'w') as markdown_file:
            for day in parsed_dictionary:
                markdown_file.write('# {}\n\n'.format(day))
                for distro in parsed_dictionary[day]:
                    markdown_file.write('## {}\n\n'.format(distro))
                    for arch in parsed_dictionary[day][distro]:
                        markdown_file.write('### {}\n\n'.format(arch))
                        for entry_id in parsed_dictionary[day][distro][arch]:
                            self._print_result(
                                parsed_dictionary[day][distro][arch][entry_id],
                                markdown_file
                            )

    def _parse(self):
        parsed_dictionary = {}
        for entry in self._result_entries:
            day = entry.day
            if day not in parsed_dictionary:
                parsed_dictionary[day] = {}
            distro = entry.distro
            if distro not in parsed_dictionary[day]:
                parsed_dictionary[day][distro] = {}
            architecture = entry.architecture
            if architecture not in parsed_dictionary[day][distro]:
                parsed_dictionary[day][distro][architecture] = {}
            parsed_dictionary[day][distro][architecture].update({
                entry.identifier: {
                    'version': entry.get_test_package(),
                    'result': entry.is_success(),
                    'duration': entry.get_duration(),
                    'links': entry.get_links()
                }
            })
        return parsed_dictionary

    def _print_result(self, entry, markdown_file):
        markdown_file.write(
            '{}\n'.format(entry['version']))
        if entry['result']:
            markdown_file.write(':white_check_mark: passed ')
        else:
            markdown_file.write(':x: failed ')
        markdown_file.write('in {}s\n'.format(entry['duration']))
        for name, url in entry['links']:
            markdown_file.write('({})[{}]\n'.format(name, url))
