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


class AutopkgtestResultsFormatterError(Exception):
    """Base class for autopkgtest_results_formatter exceptions.

    :cvar fmt: A format string that daughter classes must override.
    """

    # Daughter classes must redefine this.
    fmt = None

    def __init__(self, **kwargs):
        """Constructor of the autopkgtest_results_formatter base exception."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        """String representation of the error.

        It is formed applying the keyword arguments passed in the constructor
        to the `fmt` class variable defined by the error class.

        :raises NotImplementedError: If the error class doesn't define the fmt.
        """
        if not self.fmt:
            raise NotImplementedError()
        return self.fmt.format([], **self.__dict__)


class ResultsIndexNotDownloadedError(AutopkgtestResultsFormatterError):
    """Exception raised when"""

    fmt = ('Failed to {action}: The results index has not been downloaded. '
           'Use the ResultsIndex class as a context manager.')
