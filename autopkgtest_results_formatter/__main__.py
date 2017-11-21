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

import argparse

from autopkgtest_results_formatter import results_formatter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--destination', help='The path to the destination directory')
    parser.add_argument(
        '--distros', help='The names of the distros, for example: xenial',
        nargs='+')
    parser.add_argument(
        '--day', help='The day of the results, with format yyyymmdd')
    args = parser.parse_args()
    run(args.destination, args.distros, args.day)


def run(destination_path, distros, day):
    formatter = results_formatter.ResultsFormatter(
        destination_path=destination_path, distros=distros,
        ppa_user='snappy-dev', ppa_name='snapcraft-daily', day=day)
    formatter.format()


if __name__ == "__main__":
    main()
