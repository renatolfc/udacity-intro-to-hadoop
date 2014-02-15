#!/usr/bin/env python
# encoding: utf-8

"""Reducer module for solving the `Student Times`_ problem.

.. _Student Times: https://www.udacity.com/course/viewer#!/c-ud617/l-717558831/m-713019075

.. module:: student_times_reducer
.. moduleauthor:: Renato L. F. Cunha <renato@renatocunha.com>
"""

from __future__ import print_function

import sys

def increment(postHours, hour):
    postHours[hour % 24] += 1


def emptyHours():
    return [0] * 24


def getMathingIndices(iterable, value):
    return [i for i, e in enumerate(iterable) if e == value]


def output(author, postHours):
    maximum = max(postHours)
    for hour in getMathingIndices(postHours, maximum):
        print('{0}\t{1}'.format(author, hour))


def getData(line):
    data = line.strip().split('\t')

    # Our mapper outputs two columns. Anything different is can be
    # considered corrupt
    if len(data) != 2:
        return None

    # In the format we expect
    author, hour = data

    try:
        hour = int(hour)
    except ValueError:
        # This is not an hour. :-(
        return None

    return author, hour

def reducer():
    """Reducer function.

    :returns: Nothing. Writes to standard output.
    """

    lastAuthor = '-1'
    postHours = emptyHours()
    for line in sys.stdin:
        data = getData(line)
        if data is None:
            continue
        author, hour = data

        if author != lastAuthor:
            if lastAuthor != '-1':
                output(lastAuthor, postHours)
                postHours = emptyHours()
                increment(postHours, hour)
            else:
                increment(postHours, hour)

        lastAuthor = author

    output(author, postHours)


if __name__ == '__main__':
    reducer()
