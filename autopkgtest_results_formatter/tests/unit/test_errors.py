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

import testscenarios
from testtools.matchers import Equals

from autopkgtest_results_formatter import errors
from autopkgtest_results_formatter.tests import unit


class AutopkgtestResultsFormatterErrorTestCase(unit.TestCase):

    def test_daughter_class_str_without_fmt_raises_error(self):
        class TestError(errors.AutopkgtestResultsFormatterError):
            pass

        test_error = TestError()
        self.assertRaises(NotImplementedError, str, test_error)

    def test_daughter_class_str_with_fmt(self):
        class TestError(errors.AutopkgtestResultsFormatterError):

            fmt = 'test format with {arg1} and {arg2}'

        test_error = TestError(arg1='test arg1', arg2='test arg2')
        self.assertThat(
            str(test_error),
            Equals('test format with test arg1 and test arg2'))


class ErrorFormattingTestCase(testscenarios.WithScenarios, unit.TestCase):

    scenarios = (
        ('ResultsIndexNotDownloadedError', {
            'exception': errors.ResultsIndexNotDownloadedError,
            'kwargs': {'action': 'do test action'},
            'expected_message': (
                'Failed to do test action: The results index has not been downloaded. '
                'Use the ResultsIndex class as a context manager.')}),
    )

    def test_error_formatting(self):
        self.assertThat(
            str(self.exception(**self.kwargs)),
            Equals(self.expected_message))
