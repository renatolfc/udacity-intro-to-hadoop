#!/usr/bin/env python
# encoding: utf-8

"""Mapper module for solving the `Student Times`_ problem.

.. _Student Times: https://www.udacity.com/course/viewer#!/c-ud617/l-717558831/m-713019075

.. module:: student_times_mapper
.. moduleauthor:: Renato L. F. Cunha <renato@renatocunha.com>
"""

from __future__ import print_function

import sys
import csv
from datetime import datetime

from common import getField, isValidNodeLine

def parseDate(dateRead):
    """Parses the date we just read.

    :dateRead: The date we read.
    :returns: A datetime object representing the date we read.

    """
    if '.' in dateRead:
        # Fractions of a second don't matter to us
        date = dateRead.split('.')[0]

    try:
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def mapper():
    """Mapper function.

    Input is read from sys.stdin and written to sys.stdout. Both streams can be
    overwritten if needed.

    :returns: Nothing. Writes to standard output.
    """

    # The input file is saved as a tab-separated file. The data itself comes from
    # http://content.udacity-data.com/course/hadoop/forum_data.tar.gz -- file
    # "forum_nodes.tsv".
    reader = csv.reader(sys.stdin, delimiter='\t')

    for line in reader:
        # Basic data sanity check
        if not isValidNodeLine(line):
            continue

        author = getField(line, 'author_id')
        date = parseDate(getField(line, 'added_at'))

        if date is None or author is None:
            # Something's gone wrong. Ignore this line.
            continue

        print('{0}\t{1}'.format(author, date.hour))

if __name__ == '__main__':
    mapper()

