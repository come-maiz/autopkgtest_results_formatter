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
import tarfile

from testtools.matchers import (
    FileContains,
    FileExists,
    Not
)

from autopkgtest_results_formatter import (
    markdown_printer,
    result_entry
)
from autopkgtest_results_formatter.tests import unit


class MarkDownPrinterTestCase(unit.TestCase):

    def make_result_entry(self, directory, exitcode, test_package, duration):
        entry_dir_path = os.path.join(self.path, directory)
        os.makedirs(entry_dir_path)
        tar_file_path = os.path.join(entry_dir_path, 'result.tar')
        files = (
            ('exitcode', exitcode),
            ('testpkg-version', test_package),
            ('duration', duration))
        with tarfile.open(tar_file_path, 'w') as tar_file:
            for file_name, value in files:
                file_path = os.path.join(directory, file_name)
                with open(file_path, 'w') as file_:
                    file_.write(value)
                tar_file.add(file_path, arcname=file_name)

    def test_print_without_results(self):
        destination = os.path.join(self.path, 'test.md')
        printer = markdown_printer.MarkdownPrinter(
            destination_path=destination,
            result_entries=[])
        printer.print_results()
        self.assertThat(destination, Not(FileExists()))

    def test_print_one_successful_result(self):
        destination = os.path.join(self.path, 'test.md')
        test_result_dir = (
            'testdistro/testarch/dummy/dummy/testday_dummy_testid@')
        self.make_result_entry(
            test_result_dir, '0', 'package_name package_version', '100')
        printer = markdown_printer.MarkdownPrinter(
            destination_path=destination,
            result_entries=[
                result_entry.ResultEntry(
                    index_url='file://{}'.format(self.path),
                    directory=test_result_dir)])
        printer.print_results()

        expected_url = 'file://{}/{}'.format(
            self.path, test_result_dir)
        self.assertThat(
            destination,
            FileContains(
                '# testday\n'
                '\n'
                '## testdistro\n'
                '\n'
                '### testarch\n'
                '\n'
                'package_name package_version\n\n'
                ':white_check_mark: passed in 100s\n\n'
                '[result]({url}/result.tar) | '
                '[log]({url}/log.gz) | '
                '[artifacts]({url}/artifacts.tar.gz)\n\n'.format(
                    url=expected_url)
            ))

    def test_print_one_failed_result(self):
        destination = os.path.join(self.path, 'test.md')
        test_result_dir = (
            'testdistro/testarch/dummy/dummy/testday_dummy_testid@')
        self.make_result_entry(
            test_result_dir, '1', 'package_name package_version', '100')
        printer = markdown_printer.MarkdownPrinter(
            destination_path=destination,
            result_entries=[
                result_entry.ResultEntry(
                    index_url='file://{}'.format(self.path),
                    directory=test_result_dir)])
        printer.print_results()

        expected_url = 'file://{}/{}'.format(
            self.path, test_result_dir)
        self.assertThat(
            destination,
            FileContains(
                '# testday\n'
                '\n'
                '## testdistro\n'
                '\n'
                '### testarch\n'
                '\n'
                'package_name package_version\n\n'
                ':x: failed in 100s\n\n'
                '[result]({url}/result.tar) | '
                '[log]({url}/log.gz) | '
                '[artifacts]({url}/artifacts.tar.gz)\n\n'.format(
                    url=expected_url)
            ))
